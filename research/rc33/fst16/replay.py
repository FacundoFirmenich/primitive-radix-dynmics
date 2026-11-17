"""Bounded independent reconstruction; original FST15/16 artifacts are absent."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,platform,resource,shutil,subprocess,sys,tempfile,time
import argparse
p=argparse.ArgumentParser();p.add_argument('--output',required=True);args=p.parse_args()
C=Path(__file__).resolve().parent;O=Path(args.output).resolve();O.mkdir(parents=True,exist_ok=True)
assert O!=C and C not in O.parents
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
inputs=lambda:{p.relative_to(C).as_posix():sha(p) for p in sorted(C.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and p.name!='EXACT_RESULTS.json' and p.suffix!='.pyc'}
before=inputs();start=time.monotonic()
def limit():
 resource.setrlimit(resource.RLIMIT_CPU,(60,60));resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3))
with tempfile.TemporaryDirectory(prefix='rgphi-fst16-') as tmp:
 W=Path(tmp)/'source';shutil.copytree(C,W,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
 (W/'EXACT_RESULTS.json').unlink(missing_ok=True)
 p=subprocess.run([sys.executable,'audit16.py'],cwd=W,text=True,capture_output=True,timeout=90,preexec_fn=limit)
 (O/'AUDIT.log').write_text(p.stdout+p.stderr);assert p.returncode==0,p.stderr
 shutil.copy2(W/'EXACT_RESULTS.json',O/'EXACT_RESULTS.json')
after=inputs();assert before==after
d=json.loads((O/'EXACT_RESULTS.json').read_text());assert d['status']=='PASS'
assert not d['original_FST15_16_inputs_received'] and not d['original_FST15_16_suites_replayed']
m=dict(status='PASS',recorded_utc=datetime.now(timezone.utc).isoformat(),python=platform.python_version(),
 command=[sys.executable,'replay.py','--output',str(O)],seconds=time.monotonic()-start,
 CPU_seconds=60,memory_bytes=1024**3,wall_limit_seconds=90,
 input_artifacts=[dict(path=k,sha256=h,sha256_after=after[k]) for k,h in before.items()],
 output_sha256=sha(O/'EXACT_RESULTS.json'),original_FST15_16_artifacts_received=False,
 scope='Independent reconstruction from received prose; copied FST14 engine/adapters unchanged; no original suite, atlas, priority or global arithmetic closure claim.')
(O/'RUN_MANIFEST.json').write_text(json.dumps(m,indent=2)+'\n')
print('PASS:3-adic isometry, coprime inversion,10000-digit example, generalized contraction and exact DFA pruning.')
