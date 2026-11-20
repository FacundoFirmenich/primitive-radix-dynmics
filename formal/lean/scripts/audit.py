#!/usr/bin/env python3
"""Rebuild and audit every project theorem. Author: Facundo Firmenich.

No native evaluator supplies a proof. This runner invokes Lean's kernel,
checks proof dependencies, and tests deliberately false mutations separately.
"""
from pathlib import Path
import argparse, datetime, hashlib, json, os, re, shutil, subprocess, sys
ROOT = Path(__file__).resolve().parents[1]
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def stripped(s):
    # Lean supports nested block comments.
    out=[]; i=0; depth=0
    while i<len(s):
        if s[i:i+2]=='/-': depth+=1; i+=2
        elif depth and s[i:i+2]=='-/': depth-=1; i+=2
        elif depth: i+=1
        elif s[i:i+2]=='--':
            j=s.find('\n',i); i=len(s) if j<0 else j
        else: out.append(s[i]); i+=1
    if depth: raise ValueError('unclosed comment')
    return ''.join(out)
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--lake',default=os.environ.get('LAKE','lake'))
    ap.add_argument('--records',default='records/current'); args=ap.parse_args()
    lake=shutil.which(args.lake)
    if not lake: raise SystemExit('lake not found: install the pinned lean-toolchain or pass --lake')
    dest=ROOT/args.records; dest.mkdir(parents=True,exist_ok=True)
    print((ROOT/'records/INPUTS.json').read_text(),flush=True)
    env=dict(os.environ); env.setdefault('LEAN_NUM_THREADS','4')
    cmds=[]
    def run(label,cmd,expect=0):
        start=datetime.datetime.now(datetime.timezone.utc).isoformat()
        p=subprocess.run(cmd,cwd=ROOT,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        (dest/(label+'.log')).write_text(p.stdout)
        cmds.append({'label':label,'argv':cmd,'exit_code':p.returncode,'expected':expect,'started_utc':start})
        if (expect==0 and p.returncode!=0) or (expect!=0 and p.returncode==0):
            raise RuntimeError(f'{label}: unexpected exit {p.returncode}; see log')
        return p.stdout
    version=run('lean-version',[lake,'env','lean','--version']).strip()
    if 'version 4.19.0' not in version: raise RuntimeError('unexpected Lean version')
    manifest=json.loads((ROOT/'lake-manifest.json').read_text())
    pkg=next(p for p in manifest['packages'] if p['name']=='mathlib')
    if pkg['rev']!='c44e0c8ee63ca166450922a373c7409c5d26b00b': raise RuntimeError('wrong mathlib pin')
    sources=[ROOT/'RadixMobius.lean',*sorted((ROOT/'RadixMobius').glob('*.lean'))]
    declarations=[]
    for p in sources:
        raw=p.read_text(); s=stripped(raw)
        if re.search(r'\b(sorry|admit|native_decide|ofReduceBool|axiom|unsafe)\b',s):
            raise RuntimeError('forbidden proof construct in '+str(p))
        if re.search(r'^\s*(opaque|constant)\b',s,re.M): raise RuntimeError('unreviewed constant')
        for m in re.finditer(r'^(?:theorem|lemma)\s+(\w+)\b',s,re.M):
            declarations.append({'name':'RadixMobius.'+m.group(1),'file':str(p.relative_to(ROOT)),
                                 'line':raw[:raw.index(m.group(1))].count('\n')+1})
    if len({d['name'] for d in declarations})!=len(declarations): raise RuntimeError('duplicate theorem')
    dependency_revisions={}
    for package in manifest['packages']:
        path=ROOT/manifest['packagesDir']/package['name']
        rev=run('dependency-'+package['name'],['git','-C',str(path),'rev-parse','HEAD']).strip()
        if rev!=package['rev']: raise RuntimeError('dependency revision mismatch: '+package['name'])
        run('dependency-clean-'+package['name'],['git','-C',str(path),'diff','--exit-code','HEAD'])
        dependency_revisions[package['name']]=rev
    coverage=json.loads((ROOT/'COVERAGE.json').read_text())
    names={d['name'] for d in declarations}
    if coverage['theorems_expected']!=len(declarations) or coverage['modules_expected']!=len(sources)-1:
        raise RuntimeError('coverage inventory mismatch')
    for card in coverage['claims']:
        if not set(card['theorems'])<=names: raise RuntimeError('missing coverage declaration')
    run('build',[lake,'build'])
    audit=dest/'Audit.lean'; statements=dest/'Statements.lean'
    audit.write_text('import RadixMobius\n'+''.join('#print axioms '+d['name']+'\n' for d in declarations))
    statements.write_text('import RadixMobius\n'+''.join('#check '+d['name']+'\n' for d in declarations))
    axioms=run('axioms',[lake,'env','lean','--trust=0',str(audit.relative_to(ROOT))])
    allowed={'propext','Classical.choice','Quot.sound'}; seen=set()
    for d in declarations:
        pat=re.escape("'"+d['name']+"'")+r' (?:depends on axioms: \[([^\]]*)\]|does not depend on any axioms)'
        m=re.search(pat,axioms,re.S)
        if not m: raise RuntimeError('missing axiom report '+d['name'])
        deps=[a.strip() for a in (m.group(1) or '').split(',') if a.strip()]
        if set(deps)-allowed: raise RuntimeError('unexpected axioms '+str(deps))
        d['axioms']=deps; seen.update(deps)
    run('statements',[lake,'env','lean','--trust=0',str(statements.relative_to(ROOT))])
    # Wrong assertions must be rejected; their negations must be proved. Each
    # positive file imports exactly the same library as its negative partner.
    mutations=[
      ('wrong-base','pairT (oldBase+1) (oldCarrier 0) = oldCarrier (graphT 0)', 'decide'),
      ('missing-primitivity','Nat.gcd ((3*2)%2) 2 = Nat.gcd 3 2','decide'),
      ('saturation-subtraction','Nat.gcd 2 (2+(3*(1-2))%2) = Nat.gcd 3 2','decide'),
      ('missing-square-guard','IsSquare ((2 : ℤ))','norm_num [IsSquare]'),
      ('closed-half-endpoint','High ((1 : ℚ)/2)','norm_num [High]'),
      ('closed-one-endpoint','High (1 : ℚ)','norm_num [High]'),
      ('truncated-monoid','codeOf [] ∈ actionCodes.tail','decide')]
    for label,prop,tactic in mutations:
        bad=dest/(label+'-reject.lean'); good=dest/(label+'-control.lean')
        header='import RadixMobius\nnamespace RadixMobius\n'
        # For the square test the positive proof uses the standard square bound.
        good_tactic=tactic if label!='missing-square-guard' else '\n  rintro ⟨r, hr⟩\n  have h1 : r < 2 := by nlinarith\n  have h2 : -2 < r := by nlinarith\n  have h : r = -1 ∨ r = 0 ∨ r = 1 := by omega\n  rcases h with h | h | h <;> subst r <;> norm_num at hr'
        bad.write_text(header+f'example : {prop} := by {tactic}\nend RadixMobius\n')
        good.write_text(header+f'example : ¬ ({prop}) := by {good_tactic}\nend RadixMobius\n')
        run(label+'-control',[lake,'env','lean','--trust=0',str(good.relative_to(ROOT))])
        out=run(label+'-reject',[lake,'env','lean','--trust=0',str(bad.relative_to(ROOT))],expect=1)
        if 'error:' not in out or any(e in out for e in ['unknown module','unknown identifier','file not found']):
            raise RuntimeError('mutation rejected for the wrong reason: '+label)
    source_hashes={str(p.relative_to(ROOT)):sha(p) for p in sources}
    for f in ['lean-toolchain','lakefile.lean','lake-manifest.json','scripts/audit.py','COVERAGE.json']:
        source_hashes[f]=sha(ROOT/f)
    result={'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
      'author':'Facundo Firmenich','Lean':version,'mathlib_revision':pkg['rev'],
      'named_theorems':len(declarations),'modules':len(sources)-1,
      'dependency_revisions':dependency_revisions,
      'standard_axioms_used':sorted(seen),'custom_axioms':[],
      'sorry_admit_native_decide':False,'kernel_trust_argument':0,
      'mutation_pairs':len(mutations),'commands':cmds,'source_hashes':source_hashes,
      'declarations':declarations,
      'project_olean_hashes':{str(p.relative_to(ROOT)):sha(p) for p in sorted((ROOT/'.lake/build/lib/lean/RadixMobius').glob('*.olean'))},
      'coverage':'See COVERAGE.json; this is partial formalization, not a certificate of the full paper.',
      'audit_provenance':'Self-review of semantics; Lean kernel verification of proof terms.'}
    (dest/'AUDIT.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({k:result[k] for k in ['status','named_theorems','modules','standard_axioms_used','mutation_pairs']},indent=2))
if __name__=='__main__': main()
