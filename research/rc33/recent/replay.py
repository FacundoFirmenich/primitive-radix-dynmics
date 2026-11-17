"""Replay the public exact-code subset without modifying archived checkpoints."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, platform, shutil, subprocess, sys, tempfile, time

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
OUT=ROOT/'outputs/reports/recent'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    manifest=json.loads((HERE/'SOURCE_MANIFEST.json').read_text())
    for row in manifest['files']:
        assert sha(ROOT/row['public_path'])==row['sha256'],row['public_path']
    config={'units':'dimensionless; exact integers and rationals; labelled Decimal entropy approximation',
            'whole_inputs':[4777,6444,7444], 'witness_core':[406,712,1265,731,557],
            'base':88011536665779,'CRT_modulus':223336848698040,
            'boundary_equations':['2*u+v+z=3*t','A>6*t','A divides t**2-u**2'],
            'cover_equations':['K=<u,2v>','N=<2(v-u)>','components=|G|/|K|','period=|K|/|N|'],
            'FST_equations':['K_s=8*10**ell-9*s','H_s=K_s/7**v7(K_s)'],
            'saved_boundary_T':5000,'current_direct_T':180,'root_moduli':[2,2500],
            'FST_full_suffix_lengths':[1,2,3,4,5,6],'python':platform.python_version()}
    print('CONFIGURATION BEFORE COMPUTATION\n'+json.dumps(config,indent=2),flush=True)
    commands=[('sine/input','verificar_puente.py',[]),('sine','independent_checks.py',[]),
              ('synergies','independent_checks.py',[]),('synergies/input','verificacion_exacta.py',[]),
              ('chamber','independent_validation.py',[]),('chamber','terminal_replay.py',[]),
              ('weighted','verify_covers.py',[]),('triadic','verify_triadic_extension.py',[]),
              ('triadic/source-replay','auditar_triada.py',[]),
              ('triadic/source-replay','auditar_irreducibles_ORIGINAL.py',['--out-dir','baseline_dos_fuentes'])]
    runs=[]
    with tempfile.TemporaryDirectory(prefix='rgphi-public-replay-') as temp:
        work=Path(temp)
        for row in manifest['files']:
            rel=Path(row['public_path']).relative_to(HERE.relative_to(ROOT))
            dest=work/rel;dest.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(ROOT/row['public_path'],dest)
        for module,script,args in commands:
            start=time.monotonic();cwd=work/module
            result=subprocess.run([sys.executable,script,*args],cwd=cwd,capture_output=True,text=True)
            log=OUT/(module.replace('/','-')+'-'+script.replace('.py','.log'))
            log.write_text(result.stdout+result.stderr)
            assert result.returncode==0,(module,script,result.stderr[-1800:])
            runs.append({'module':module,'script':script,'returncode':0,'seconds':time.monotonic()-start,
                         'code_sha256':sha(cwd/script),'log':str(log.relative_to(ROOT)),'log_sha256':sha(log)})
            print('PASS',module,script,flush=True)
        # Check the saved complete run, its code version and its terminal list.
        chamber=work/'chamber'
        saved=json.loads((chamber/'BOUNDARY_CENSUS_T5000.json').read_text())
        assert saved['config']['source_sha256']==sha(chamber/'boundary_census.py')
        counts=saved['census']['counts']
        assert counts['primitive_core_candidates']==24470981 and counts['three_square_candidates']==157
        assert counts.get('four_square_candidates',0)==0 and not saved['census']['realizations']
        small=json.loads((chamber/'BOUNDARY_CENSUS_T600.json').read_text())['census']
        assert small['three_square_samples']==[x for x in saved['census']['three_square_samples'] if x['t_u_v_z'][0]<=600]
        terminal=json.loads((chamber/'TERMINAL_CHECK.json').read_text())
        assert terminal['terminal_three_square_cores_checked']==157 and terminal['survivors']==0
        # Exact same-source replay of the supplied nine pi-phase decisions.
        assert json.loads((work/'sine/input/RESULTADOS_EXACTOS.json').read_text())==json.loads((HERE/'sine/input/RESULTADOS_EXACTOS.json').read_text())
        import sympy as s
        A,Q,C,D,ka,kc,kd,kq,ha,hc,hd,hq,al,be,ga,de=s.symbols('A Q C D ka kc kd kq ha hc hd hq al be ga de',nonzero=True)
        sub={A:ha*(D-al*Q)/ka,C:hc*(D-be*Q)/kc}
        ND=(be*ka*hc)**2-(ga*al*kc*ha)**2;NQ=(ka*hc)**2-(de*kc*ha)**2
        assert s.simplify(((ka*kc)**2*(C*C-ga*ga*A*A)).subs(sub).subs(D,0)-Q*Q*ND)==0
        assert s.simplify(((ka*kc)**2*(C*C-de*de*A*A)).subs(sub).subs(Q,0)-D*D*NQ)==0
        sub={D:hd*(C-ga*A)/kd,Q:hq*(C-de*A)/kq}
        NA=(kq*hd)**2-(al*kd*hq)**2;NC=(ga*kq*hd)**2-(be*de*kd*hq)**2
        assert s.simplify(((kd*kq)**2*(D*D-al*al*Q*Q)).subs(sub).subs(A,0)-C*C*NA)==0
        assert s.simplify(((kd*kq)**2*(D*D-be*be*Q*Q)).subs(sub).subs(C,0)-A*A*NC)==0
        r=s.symbols('r');matrix=s.Matrix([[1,-1,0,0],[0,1,1,0],[0,0,1,-r*r],[r*r,0,0,1]])
        assert s.expand(matrix.det()-(1-r**4))==0
        for module,name in [('sine','INDEPENDENT_RESULTS.json'),('synergies','INDEPENDENT_RESULTS.json'),
                            ('chamber','INDEPENDENT_VALIDATION.json'),('chamber','TERMINAL_CHECK.json'),
                            ('weighted','EXACT_RESULTS.json'),('triadic','EXACT_RESULTS.json')]:
            shutil.copy2(work/module/name,OUT/(module+'-'+name))
    for row in manifest['files']:assert sha(ROOT/row['public_path'])==row['sha256']
    receipt={'status':'PASS','edition':'RC3.3','recorded_utc':datetime.now(timezone.utc).isoformat(),
             'configuration':config,'runs':runs,'checkpoint_files_unchanged':len(manifest['files']),
             'opposite_cofactor_symbolic_cancellations':4,'quartic_determinant':'1-r**4',
             'new_full_T5000_run':False,'new_global_existence_rows_closed':0,
             'scope':'Current replay of public exact code/data; saved T5000 run preserved; no external independent peer-review claim.'}
    (OUT/'RUN_MANIFEST.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print('RECENT PUBLIC REPLAY PASS')

if __name__=='__main__':main()
