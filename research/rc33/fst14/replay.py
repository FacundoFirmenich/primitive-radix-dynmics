"""Bounded disposable replay; preserves all received inputs and adapter source."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,hashlib,json,platform,resource,shutil,subprocess,sys,tempfile,time
S=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();O=Path(a.output).resolve()
if O==S or S in O.parents:raise ValueError('output must be outside the source module')
O.mkdir(parents=True,exist_ok=True)
for n in ['FST14_RESULTS.json','terminal.log','RUN_MANIFEST.json']:
 if (O/n).exists():(O/n).unlink()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def sources():return {p.relative_to(S).as_posix():sha(p) for p in sorted(S.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc'}
before=sources()
if (S/'INPUTS.json').exists():
 for row in json.loads((S/'INPUTS.json').read_text()):assert sha(S/row['path'])==row['sha256']
print('CONFIG: exact K=8*10^ell-9*val(w),q=343; all suffixes d=1..3 over8 labels; lengths0..100; CRT m,n=1..14; deep d=10,31,110 and index10000000000123456789; declared adapters, no historical tests claimed.',flush=True)
def cap():
 resource.setrlimit(resource.RLIMIT_CPU,(60,60));resource.setrlimit(resource.RLIMIT_AS,(2*1024**3,2*1024**3))
t=time.monotonic();started=datetime.now(timezone.utc).isoformat();status='completed'
with tempfile.TemporaryDirectory(prefix='rgphi-fst14-') as temp:
 W=Path(temp)/'source';shutil.copytree(S,W,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
 try:
  p=subprocess.run([sys.executable,'audit_terminal.py','FST14_RESULTS.json'],cwd=W,text=True,capture_output=True,timeout=90,preexec_fn=cap)
  (O/'terminal.log').write_text(p.stdout+p.stderr);code=p.returncode
  if code:status='failed'
 except subprocess.TimeoutExpired as e:status='timeout';code=None;(O/'terminal.log').write_text(str(e))
 if (W/'FST14_RESULTS.json').exists():shutil.copy2(W/'FST14_RESULTS.json',O/'FST14_RESULTS.json')
after=sources()
if before!=after:status='inputs-changed'
if status=='completed' and (not (O/'FST14_RESULTS.json').exists() or json.loads((O/'FST14_RESULTS.json').read_text()).get('status')!='PASS'):status='result-invalid'
manifest={'schema_version':2,'claim_id':'F14V','command':[sys.executable,'replay.py','--output',str(O)],'cwd':'disposable copy of frozen source',
 'environment':{'python':platform.python_version(),'platform':platform.platform()},
 'mathematics':{'coefficient_domain':'exact integers','assertion_tested':'Finite suffix-orbit and inverse comparisons under declared adapters','bounds':{'suffix_digits':[1,3],'CRT_moduli':[1,14],'count_lengths':[0,100],'deep_digits':[10,31,110],'deep_index':'10000000000123456789'},'non_claims':['Missing original baselines and50-test suite not replayed','No browser atlas received','No global RGphi existence or uniqueness closure']},
 'run':{'started_at':started,'runtime_seconds':time.monotonic()-t,'status':status,'exit_status':code,'CPU_seconds_limit':60,'wall_seconds_limit':90,'address_space_bytes':2*1024**3},
 'input_artifacts':[{'path':n,'sha256':h,'sha256_after':after.get(n)} for n,h in before.items()],
 'outputs':[{'path':n,'sha256':sha(O/n)} for n in ['FST14_RESULTS.json','terminal.log'] if (O/n).exists()],
 'status':'PASS' if status=='completed' else 'FAIL'}
(O/'RUN_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
assert status=='completed',(status,code)
print('PASS: terminal inversion, source hashes unchanged, adapter boundary explicit.')
