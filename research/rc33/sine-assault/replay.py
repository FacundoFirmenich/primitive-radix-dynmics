"""Bounded exact replay of the integrated phase, atom and arithmetic-index gates."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,hashlib,json,platform,resource,shutil,subprocess,sys,tempfile,time
S=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();O=Path(a.output).resolve();O.mkdir(parents=True,exist_ok=True)
if O==S or S in O.parents:raise ValueError('results must be outside the frozen source tree')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
# Only received inputs, declared source engines and code are execution inputs.
def files():return {p.relative_to(S).as_posix():sha(p) for p in sorted(S.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc' and (p.suffix in ['.py','.js','.md','.patch'] or 'inputs' in p.relative_to(S).parts or p.name in ['INPUTS.json','ATOMIC_ORIGINAL_RESULTS.json'])}
before=files()
if (S/'INPUTS.json').exists():
 for row in json.loads((S/'INPUTS.json').read_text()):
  if (S/row['path']).exists():assert sha(S/row['path'])==row['sha256']
expected=['EXACT_CERTIFICATE.json','PHASE_DATASET.json','CELL_PATTERNS.csv','EXTENDED_PARTITIONS.json','ATOMIC_AUDIT.json','ATOMIC_ATLAS_AUDIT.json','AUDITORIA_CUATRO_LINEAS.json','closure/STRUCTURE_AUDIT.json','closure/LAMBDA2_RESULTS.json','closure/LAMBDA_3_STRATA.json','closure/LAMBDA_4_STRATA.json','closure/LAMBDA_5_STRATA.json','results/fifth_coordinate_checks.json']
for name in expected+['RUN_MANIFEST.json']:
 if (O/Path(name).name).exists():(O/Path(name).name).unlink()
started=datetime.now(timezone.utc).isoformat();ts=time.monotonic();runs=[];status='completed'
print('CONFIG: exact integer/rational phase partitions and inverse gates; frozen originals and declared path redirect; completion indices2..5 over all heights, full command-specific parameters printed by each child;CPU90s and wall120s per child; Python3 and Node.',flush=True)
def limit(node=False):
 resource.setrlimit(resource.RLIMIT_CPU,(90,90))
 if not node:resource.setrlimit(resource.RLIMIT_AS,(3*1024**3,3*1024**3))
commands=[('phase',[sys.executable,'verify_patch.py']),('partitions',[sys.executable,'extended_partitions.py']),('atoms',[sys.executable,'audit_atomic.py']),('atlas',['node','audit_atomic_atlas.js']),('structure',[sys.executable,'closure/audit_structure.py']),('lambda2',[sys.executable,'closure/lambda2_planes.py']),('legacy_nonabsorption',[sys.executable,'closure/legacy_fifth_coordinate.py'])]+[(f'lambda{L}',[sys.executable,'closure/index_strata.py','--lambda',str(L)]) for L in [3,4,5]]
with tempfile.TemporaryDirectory(prefix='rgphi-sine-assault-') as temp:
 W=Path(temp)/'source';shutil.copytree(S,W,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
 for name in expected:
  if (W/name).exists():(W/name).unlink()
 for tag,argv in commands:
  t=time.monotonic();log=O/(tag+'.log');rec=dict(name=tag,argv=argv,CPU_seconds=90,wall_seconds=120)
  try:
   q=subprocess.run(argv,cwd=W,text=True,capture_output=True,timeout=120,preexec_fn=lambda:limit(tag=='atlas'));log.write_text(q.stdout+q.stderr);rec.update(status='completed' if q.returncode==0 else'failed',returncode=q.returncode,seconds=time.monotonic()-t)
  except subprocess.TimeoutExpired as e:log.write_text(str(e));rec.update(status='timeout',returncode=None,seconds=time.monotonic()-t)
  runs.append(rec);print(tag,rec['status'],flush=True)
  if rec['status']!='completed':status=rec['status'];break
 for name in expected:
  if (W/name).is_file():shutil.copy2(W/name,O/Path(name).name)
after=files()
if before!=after:status='inputs-changed'
if status=='completed':
 for name in expected:
  if not (O/Path(name).name).exists():status='missing-output'
 if status=='completed':
  for L in [3,4,5]:assert not any(r['necessary_candidates'] for r in json.loads((O/f'LAMBDA_{L}_STRATA.json').read_text())['results'])
manifest=dict(schema_version=2,status='PASS' if status=='completed' else'FAIL',claims=['SPW','SPP','SPF','ATM','LCF','LCG','LCE'],command=[sys.executable,'replay.py','--output',str(O)],environment=dict(python=platform.python_version(),node=subprocess.check_output(['node','--version'],text=True).strip(),platform=platform.platform()),
 mathematics=dict(domain='exact integer/rational and symbolic identities; six separately identified illustrative floating assertions not used in proofs',coverage='All potential phase cells, fifteen literal words,9841 whole-token words, carry states, all-height index strata2..5; no empirical pi trajectories or unbounded index census',non_claims=['No global existence/uniqueness/minimum-base closure','No replay of missing historical pi ormantissa campaigns','No browser visual audit of supplied interactive atlas']),
 run=dict(started_at=started,seconds=time.monotonic()-ts,status=status),runs=runs,input_artifacts=[dict(path=n,sha256=h,sha256_after=after.get(n)) for n,h in before.items()],outputs=[dict(path=p.name,sha256=sha(p)) for p in sorted(O.iterdir()) if p.is_file() and p.name!='RUN_MANIFEST.json'])
(O/'RUN_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n');assert status=='completed',(status,runs)
print('PASS: integrated exact gates; source hashes unchanged; no coordinate cutoff in fixed-index strata.')
