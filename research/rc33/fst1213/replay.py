"""Portable bounded replay. Received files and code are copied before execution."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,hashlib,json,platform,os,resource,shutil,subprocess,sys,tempfile,time
S=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args()
O=Path(args.output).resolve();O.mkdir(parents=True,exist_ok=True)
if O==S or S in O.parents:raise ValueError('output must be outside the frozen source module')
for name in ['EXACT_RESULTS.json','ATLAS_AUDIT.json','exact.log','atlases.log','RUN_MANIFEST.json']:
 if (O/name).is_file():(O/name).unlink()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def sourcefiles():return [p for p in sorted(S.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc']
before={p.relative_to(S).as_posix():sha(p) for p in sourcefiles()}
if (S/'INPUTS.json').is_file():
 for row in json.loads((S/'INPUTS.json').read_text()):assert sha(S/row['path'])==row['sha256'],row['path']
for row in json.loads((S/'extracted/SOURCE_PROVENANCE.json').read_text()):
 assert sha(S/'extracted'/row['exact_extracted_script'])==row['script_sha256']
 if (S/'inputs'/row['HTML']).exists():assert sha(S/'inputs'/row['HTML'])==row['HTML_sha256']
started=datetime.now(timezone.utc).isoformat();runs=[];status='completed';t=time.monotonic()
print('CONFIG BEFORE REPLAY: exact decimal-word arithmetic, primes2/5/7/11/17/19/31/73/101; distributions n=0..6, ranks n=0..4, modular tests M=1..80,n=0..3, five DFAs, L<=30, entropy f<=25 with80-decimal interval arithmetic; Python and Node; no historical suites or15-family census claimed.',flush=True)
def limits(python):
 def cap():
  resource.setrlimit(resource.RLIMIT_CPU,(60,60))
  if python:resource.setrlimit(resource.RLIMIT_AS,(2*1024**3,2*1024**3))
 return cap
with tempfile.TemporaryDirectory(prefix='rgphi-fst1213-') as temp:
 W=Path(temp)/'work';shutil.copytree(S,W,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
 for tag,argv,py in [('exact',[sys.executable,'audit_inverse.py'],True),('atlases',['node','audit_atlases.js'],False)]:
  rt=time.monotonic();record={'name':tag,'argv':argv,'cpu_seconds':60,'wall_timeout_seconds':90,'address_space_limit_bytes':2*1024**3 if py else None}
  try:
   p=subprocess.run(argv,cwd=W,text=True,capture_output=True,timeout=90,preexec_fn=limits(py))
   (O/(tag+'.log')).write_text(p.stdout+p.stderr);record.update(returncode=p.returncode,seconds=time.monotonic()-rt,status='completed' if p.returncode==0 else 'failed')
  except subprocess.TimeoutExpired as e:
   (O/(tag+'.log')).write_text(str(e));record.update(returncode=None,seconds=time.monotonic()-rt,status='timeout')
  if record['status']!='completed':status=record['status']
  runs.append(record)
  print(tag,record['status'],flush=True)
  if status!='completed':break
 for name in ['EXACT_RESULTS.json','ATLAS_AUDIT.json']:
  if (W/name).is_file():shutil.copy2(W/name,O/name)
after={p.relative_to(S).as_posix():sha(p) for p in sourcefiles()}
if before!=after:status='inputs-changed'
if status=='completed':
 for name in ['EXACT_RESULTS.json','ATLAS_AUDIT.json']:
  if not (O/name).is_file() or json.loads((O/name).read_text()).get('status')!='PASS':status='result-invalid'
manifest={'schema_version':2,'claim_id':'F13V','repository':{'commit':'','dirty':True},
 'command':[sys.executable,'replay.py','--output',str(O)],'cwd':'temporary copy of the frozen module',
 'environment':{'software':[{'name':'Python','version':platform.python_version()},{'name':'Node','version':subprocess.check_output(['node','--version'],text=True).strip()}],'hardware':platform.machine()+'; '+platform.platform()},
 'mathematics':{'assertion_tested':'Exact finite distributions, literal inverse ranks, bounded regular rank/unrank, erasure fusions, modular/DFA counts, received atlas selftests and interval arithmetic.',
 'coefficient_domain':'exact integers, rationals and arbitrary-precision real intervals','conventions':'Empty word and leading zeros retained; side information excludes transmitting h and length.',
 'inputs':['K=8*10**len(w)-9*val(w)','q=343','effective modulus=M/gcd(M,9)'],
 'bounds':{'distribution_lengths':[0,6],'roundtrip_lengths':[0,4],'modular_lengths':[0,3],'moduli':[1,80],'bounded_DFA_Lmax':30,'interval_decimal_digits':80},
 'non_claims':['Historical Python suites were not supplied','Natural boundaries and non-CFL require the written proof and classical source records','No15-family/1922-endpoint replay','No computational optimality or global RGphi arithmetic closure']},
 'randomness':{'used':False,'generator':'','seed':None},
 'run':{'started_at':started,'runtime_seconds':time.monotonic()-t,'exit_status':0 if status=='completed' else 1,'status':status,'resource_limits':{'per_process_CPU_seconds':60,'Python_address_space_bytes':2*1024**3,'Node_address_space_limit':None},'wall_timeout_seconds':90},
 'runs':runs,'input_artifacts':[{'path':name,'sha256':h,'sha256_after':after.get(name)} for name,h in before.items()],
 'outputs':[{'path':p.name,'sha256':sha(p),'kind':'result' if p.suffix=='.json' else 'log'} for p in sorted(O.iterdir()) if p.is_file() and p.name!='RUN_MANIFEST.json'],
 'checks':['literal finite coverage','independent BigInt atlas source','two local patch regressions','unchanged received payloads'],
 'result':'implementation and finite assertion verified in the stated ranges' if status=='completed' else'see run status',
 'residual_risks':['Same-session assisted self-review','Partial source availability for historical campaigns and the sine patch'],
 'status':'PASS' if status=='completed' else'FAIL'}
(O/'RUN_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
assert status=='completed',(status,runs)
print('PASS: frozen FST12/13 computation contracts; source hashes unchanged.')
