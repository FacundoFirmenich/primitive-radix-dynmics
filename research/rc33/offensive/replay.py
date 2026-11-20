"""Replay the fixed opposite-fibre/parity certificates in an isolated directory."""
from pathlib import Path
import hashlib,json,platform,shutil,subprocess,sys,time
import sympy

ROOT=Path(__file__).resolve().parents[3]
SRC=ROOT/'research/rc33/offensive/certificate'
WORK=ROOT/'build/offensive-replay'
manifest=json.loads((SRC/'MANIFEST_SHA256.json').read_text())
for name,digest in manifest.items():
    assert hashlib.sha256((SRC/name).read_bytes()).hexdigest()==digest,name
print(json.dumps(dict(
    stage='BEFORE',arithmetic='exact Z and Q; dimensionless',
    equations=['A | D^2-r^2 Q^2','C | D^2-Q^2',
               'D | C^2-r^2 A^2','Q | C^2-A^2',
               'Psi(x)=1/(2x)','epsilon_B(x)=floor(B/x) mod 2'],
    small_fixed_coordinates=[1,16],small_free_coordinates=[1,32],
    classes=[[2,'normal'],[3,'normal'],[3,'reflected']],
    fixed_snapshot_contexts=128058,
    snapshot_sha256=manifest['PAIR_CONTEXTS_SNAPSHOT.jsonl'],
    units='none',unknown_global_height_bound=None,
    python=platform.python_version(),sympy=sympy.__version__,
    exact_inputs='All coordinate values are preserved in the hashed input files.'
),indent=2),flush=True)
WORK.mkdir(parents=True,exist_ok=True)
(ROOT/'outputs/reports/offensive').mkdir(parents=True,exist_ok=True)
for name in manifest:shutil.copy2(SRC/name,WORK/name)
inputs={n:d for n,d in manifest.items() if n.endswith('.py') or n in
        ['CANDIDATE_DIAGNOSTIC.json','CORE_GATE_RESULTS.json','PAIR_CONTEXTS_SNAPSHOT.jsonl']}
tic=time.monotonic()
for script in ['test_paired.py','test_duality.py','test_opposite_resume.py','scan_pairs.py']:
    with (WORK/(script+'.log')).open('w') as log:
        p=subprocess.run([sys.executable,'-B',str(WORK/script)],stdout=log,stderr=subprocess.STDOUT)
    assert p.returncode==0,(script,str(WORK/(script+'.log')))
    print('PASS',script,flush=True)
for name,digest in inputs.items():
    assert hashlib.sha256((WORK/name).read_bytes()).hexdigest()==digest,name
for name,digest in manifest.items():
    assert hashlib.sha256((SRC/name).read_bytes()).hexdigest()==digest,('archive changed',name)
results={n:json.loads((WORK/n).read_text()) for n in
         ['PAIRED_TEST_RESULTS.json','DUALITY_TEST_RESULTS.json',
          'OPPOSITE_RESUME_RESULTS.json','PAIR_SCAN_RESULTS.json']}
assert all(x['status']=='PASS' for x in results.values())
scan=results['PAIR_SCAN_RESULTS.json']
assert scan['declared_contexts']==scan['counts']['contexts']==128058
assert scan['counts']['cartesian_pairs']==138985
assert scan['counts']['joint_pairs']==0 and not scan['square_cores'] and not scan['deferred']
resume=results['OPPOSITE_RESUME_RESULTS.json']
assert resume['processed']==112 and resume['closed_for_static_inputs']
out=dict(status='PASS',seconds=time.monotonic()-tic,inputs_unchanged=True,
         results=results,scope='Fixed declared domains; no global nonexistence assertion.')
(ROOT/'outputs/reports/offensive/OFFENSIVE_REPLAY.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS: fixed opposite fibres, parity identities and checkpoint replay',flush=True)
