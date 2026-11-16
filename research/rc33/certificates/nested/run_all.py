#!/usr/bin/env python3
"""Replay all scoped attacks locally and pin the actual executed inputs."""
from pathlib import Path
import subprocess,sys,json,hashlib,datetime,time
R=Path(__file__).resolve().parent
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def hashes():
    files=list(R.glob('*.py'))+list((R/'source-checker').rglob('*.py'))+list((R/'source-checker').rglob('*.md'))
    return {str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(files)}
manifest={'checkpoint':'NEST-ATTACK-001','started_utc':now(),'input_hashes_before':hashes(),'jobs':[],'python':sys.version}
mp=R/'RUN_MANIFEST.json';mp.write_text(json.dumps(manifest,indent=2))
for args,name in [(['nested_strata.py','--max-h','14'],'nested_strata_h14'),(['nested_planes.py'],'nested_planes_controls'),(['verify_c4_plane.py'],'c4_plane_separate'),(['nested_identity_attacks.py'],'nested_identities'),(['helical_lift_attack.py'],'helical_memory')]:
    st=time.monotonic();run=subprocess.run([sys.executable,'-B',*args],cwd=R,capture_output=True,text=True)
    log=R/(name+'.log');log.write_text(run.stdout+run.stderr)
    manifest['jobs'].append({'argv':[sys.executable,'-B',*args],'returncode':run.returncode,'seconds':time.monotonic()-st,'log':log.name,'sha256':hashlib.sha256(log.read_bytes()).hexdigest()});mp.write_text(json.dumps(manifest,indent=2))
    assert run.returncode==0,run.stderr
    print(name,'PASS',flush=True)
rows=json.loads((R/'NESTED_STRATA_RESULTS.json').read_text())
assert len(rows)==24 and sum(len(x['planes']) for x in rows)==693
assert sum(p['level_pairs'] for x in rows for p in x['planes'])==156195248
assert all(not p['degenerate'] for x in rows for p in x['planes'])
cores={(x['code'],x['r'],tuple(c)) for x in rows for p in x['planes'] for c in p['primitive_square_cores']}
assert cores=={(119772,3,(406,712,1265,731))}
real={(x['code'],x['r'],tuple(v['coordinates']),tuple(v['base_and_period'])) for x in rows for p in x['planes'] for v in p['realizations']}
assert real=={(119772,3,(406,712,1265,731,557),(88011536665779,223336848698040))}
manifest['input_hashes_after']=hashes();assert manifest['input_hashes_before']==manifest['input_hashes_after']
manifest['finished_utc']=now();manifest['status']='PASS_SCOPED_ALL_HEIGHT_STRATA_NOT_GLOBAL_CLASSIFICATION';mp.write_text(json.dumps(manifest,indent=2))
print(manifest['status'])
