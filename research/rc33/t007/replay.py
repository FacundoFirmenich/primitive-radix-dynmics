"""Reproduce scoped T007 certificates without publishing manuscript source."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,platform,shutil,subprocess,sys,tempfile,time
H=Path(__file__).resolve().parent;R=H.parents[2];full='--full-hexagon' in sys.argv
O=R/('outputs/reports/t007-full-hexagon' if full else 'outputs/reports/t007');O.mkdir(parents=True,exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
files=[p for p in H.rglob('*') if p.is_file() and '__pycache__' not in p.parts]
before={str(p.relative_to(R)):sha(p) for p in files};started=datetime.now(timezone.utc).isoformat();runs=[]
config={'units':'dimensionless exact word counts, integer congruences and projective finite-field points','observer_n':[16,20],'hexagon_d':[4,5,6,7],'hexagon_Q':5000 if full else 500,'source_saved_full_Q':5000,'full_hexagon_replayed':full,'elliptic_O':[0,1,-1],'elliptic_P':[64233,11741,1138],'elliptic_R':[1,2,2],'elliptic_parameter':17,'prime_cutoff':199,'tower_difference':'18*(-10)**r*2**(r*(r-1)//2)','python':platform.python_version()}
print('CONFIGURATION BEFORE COMPUTATION\n'+json.dumps(config,indent=2),flush=True)
def run(argv,W,label):
 start=time.monotonic();p=subprocess.run(argv,cwd=W,text=True,capture_output=True,timeout=120)
 out=O/(label+'.log');out.write_text(p.stdout+p.stderr)
 runs.append({'argv':argv,'returncode':p.returncode,'seconds':time.monotonic()-start,'log':str(out.relative_to(R)),'log_sha256':sha(out)})
 assert p.returncode==0,(label,p.stderr[-2000:]);print(label,'PASS',flush=True);return p.stdout
with tempfile.TemporaryDirectory(prefix='rgphi-public-t007-') as t:
 W=Path(t)/'module';shutil.copytree(H,W,ignore=shutil.ignore_patterns('__pycache__'))
 for file,label in [('github/experimento07.py','original_frontier'),('independent_observer_scan.py','independent_observer'),('check_tower_and_lattice.py','tower_and_Gauss'),('elliptic_reconstruction.py','elliptic_29'),('elliptic_all_primes.py','elliptic_43'),('q_confusion_graph.py','q_confusion_graph'),('output_bit_completion.py','output_bit_completion')]:
  run([sys.executable,file,*(['--check'] if file.startswith('github/') else [])],W,label)
 run(['g++','-std=c++17','-O2','hexagon_scan.cpp','-o','hexagon_scan'],W,'compile_hexagon')
 raw=run([str(W/'hexagon_scan'),str(config['hexagon_Q'])],W,'hexagon_census');census=json.loads(raw.splitlines()[-1]);assert census['CRT_compatible']==0
 run([sys.executable,'check_hexagon.py'],W,'hexagon_direct_prefix')
 for name in ['INDEPENDENT_OBSERVER_SCAN.json','TOWER_LATTICE_RESULTS.json','ELLIPTIC_RECONSTRUCTION.json','ELLIPTIC_ALL_PRIMES.json','OUTPUT_BIT_CERTIFICATE.json','HEXAGON_CHECKS.json']:
  j=json.loads((W/name).read_text());assert j['status']=='PASS';shutil.copy2(W/name,O/name)
 j=json.loads((W/'ELLIPTIC_ALL_PRIMES.json').read_text());assert j['good_primes_used']==43 and j['minimum_norm_squared']==125907943435801460896187665440000*172**2
 (O/'HEXAGON_CENSUS.json').write_text(json.dumps(census,indent=2)+'\n')
 saved=json.loads((H/'saved/HEXAGON_Q5000.json').read_text());actual=json.loads((H/'saved/FULL_CENSUS_EXECUTION.json').read_text())
 assert saved['source_sha256']==sha(H/'hexagon_scan.cpp')==actual['source_sha256_before']==actual['source_sha256_after']
 if full:
  for k,v in census.items():
   if k!='seconds':assert saved[k]==v
up=json.loads((H/'UPSTREAM.json').read_text());assert sha(H/'github/experimento07.py')==up['script_sha256']
after={name:sha(R/name) for name in before};assert before==after
T=(1,0,3,2,4);S=(4,2,1,0,0);E=[0,1,4,4,4]
for w in ['XYYXXXXXYYYXXXXY','YXXXXYYYXXXXXYYX','XYYYYXXXYYYYYXXY','YXXYYYYYXXXYYYYX']:
 m=list(range(5))
 for ch in w:m=[(T if ch=='X' else S)[i] for i in m]
 assert m==E
assert [E[x] for x in E]==E
receipt={'status':'PASS','recorded_utc':started,'configuration':config,'runs':runs,'input_hashes_before':before,'input_hashes_after':after,'full_Q5000_replayed':full,'saved_full_Q5000_source_verified':True,'good_primes':43,'coefficient_norm_improvement_factor':172,'action_transfer':'all seed/tower words act as the same idempotent E','new_global_five_state_rows_closed':0,'scope':'Finite certificates and same-session self-review; proof and target branches separately recorded','outputs':{str(p.relative_to(R)):sha(p) for p in O.iterdir() if p.is_file() and p.name!='RUN_MANIFEST.json'}}
(O/'RUN_MANIFEST.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('PASS: T007 exact source replay, orthogonal counts, six-state stratum and complete 43-prime relation kernel.')
