from __future__ import annotations
import argparse, csv, json, subprocess, shutil, sys
from fractions import Fraction
from pathlib import Path
from math import isqrt
from .core import T,S,defects

ROOT=Path(__file__).resolve().parents[2]
CERT=ROOT/'certificates'

def verify_nonsquares():
    rows=list(csv.DictReader((CERT/'NONSQUARE_CERTIFICATE_J1_37.csv').open(encoding='utf-8', newline='')))
    assert len(rows)==37
    for row in rows:
        j=int(row['j']); v=int(row['value'])
        assert v==403*j*j+15314*j+190969
        assert isqrt(v)**2!=v
        assert row['is_square']=='0'
    return {'rows':37,'status':'PASS'}

def verify_counterfamily(n=1001):
    state_rows=list(csv.DictReader((CERT/'STATES_AND_ACTIONS.csv').open(encoding='utf-8', newline='')))
    states=[Fraction(int(r['numerator']),int(r['denominator'])) for r in state_rows]
    spec=json.loads((CERT/'ARITHMETIC_PROGRESSION.json').read_text(encoding='utf-8'))
    tmap=spec['T']; smap=spec['S']; B0=spec['B0']; M=spec['modulus']
    for k in range(n):
        B=B0+k*M
        for i,x in enumerate(states):
            assert T(x,B)==states[tmap[i]]
            assert S(x,B)==states[smap[i]]
        strict=[]
        for i,x in enumerate(states):
            gt,gs=defects(x,B)
            if gt>1: strict.append(('T',i,tmap[i],gt))
            if gs>1: strict.append(('S',i,smap[i],gs))
        assert strict==[('S',3,0,3)]
    seen={0}; stack=[0]
    while stack:
        i=stack.pop()
        for j in (tmap[i],smap[i]):
            if j not in seen: seen.add(j); stack.append(j)
    assert len(seen)==5
    return {'bases_checked':n,'unique_strict_edge':'S3:x3->x0','status':'PASS'}

def verify_spectral():
    c=json.loads((CERT/'COUNTERFAMILY_CYCLE_CERTIFICATE.json').read_text(encoding='utf-8'))
    M=c['matrix_product']; v=c['eigenvector']; d=c['defect_product']; B=c['base']
    lhs=[M[0][0]*v[0]+M[0][1]*v[1],M[1][0]*v[0]+M[1][1]*v[1]]
    assert lhs==[d*v[0],d*v[1]]
    det=M[0][0]*M[1][1]-M[0][1]*M[1][0]
    tr=M[0][0]+M[1][1]
    assert det==B**4
    assert tr==d+B**4//d
    disc=tr*tr-4*det
    assert isqrt(disc)**2==disc
    return {'cycle_length':4,'defect_product':d,'status':'PASS'}

def verify_claim_graph():
    claims={r['claim_id']:r for r in csv.DictReader((ROOT/'data/claims.csv').open(encoding='utf-8', newline=''))}
    deps=list(csv.DictReader((ROOT/'data/dependencies.csv').open(encoding='utf-8', newline='')))
    for e in deps: assert e['source'] in claims and e['target'] in claims
    promoted={k for k,v in claims.items() if not v['status'].startswith('NOT_') and v['status']!='DEFINITION'}
    assert {'C009','C011','C012'}<=promoted
    return {'claims':len(claims),'dependency_edges':len(deps),'status':'PASS'}

def verify_embargo():
    bad=[]
    for p in ROOT.rglob('*'):
        if not p.is_file(): continue
        rel=p.relative_to(ROOT)
        if any(part in {'paper','papers','manuscript','manuscripts','supplement','supplements','private-paper','private-manuscript'} for part in rel.parts): bad.append(str(rel))
        if p.suffix.lower()=='.tex': bad.append(str(rel))
    assert not bad, f'Embargo violation: {bad}'
    return {'manuscript_files':0,'status':'PASS'}

def run_cpp():
    compiler=shutil.which('g++') or shutil.which('clang++')
    if not compiler: return {'status':'SKIP','reason':'no C++17 compiler'}
    out=ROOT/'outputs/reports/trusted_checker_017.bin'
    out.parent.mkdir(parents=True,exist_ok=True)
    subprocess.run([compiler,'-std=c++17','-O2',str(ROOT/'src/rmr/trusted_checker.cpp'),'-o',str(out)],check=True,capture_output=True,text=True)
    r=subprocess.run([str(out)],check=True,capture_output=True,text=True)
    return {'status':'PASS','compiler':Path(compiler).name,'stdout':r.stdout.strip().splitlines()[-5:]}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--report',type=Path,default=ROOT/'outputs/reports/verification_report.json'); args=ap.parse_args()
    result={'nonsquare_certificate':verify_nonsquares(),'counterfamily':verify_counterfamily(),'spectral_cycle':verify_spectral(),'claim_graph':verify_claim_graph(),'embargo':verify_embargo(),'cpp_replay':run_cpp()}
    result['overall']='PASS' if all(v['status'] in {'PASS','SKIP'} for v in result.values() if isinstance(v,dict)) else 'FAIL'
    args.report.parent.mkdir(parents=True,exist_ok=True); args.report.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2)); return 0 if result['overall']=='PASS' else 1
if __name__=='__main__': raise SystemExit(main())
