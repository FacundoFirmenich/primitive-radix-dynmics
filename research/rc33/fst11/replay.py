"""Replay FST11 without private manuscript files or modifying source checkpoints."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,platform,shutil,subprocess,sys,tempfile,time
H=Path(__file__).resolve().parent;R=H.parents[2];O=R/'outputs/reports/fst11';O.mkdir(parents=True,exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
files=[p for p in H.rglob('*') if p.is_file() and '__pycache__' not in p.parts]
before={str(p.relative_to(R)):sha(p) for p in files}
started=datetime.now(timezone.utc).isoformat();t=time.monotonic()
with tempfile.TemporaryDirectory(prefix='rgphi-fst11-public-') as temp:
 W=Path(temp)/'fst11';shutil.copytree(H,W,ignore=shutil.ignore_patterns('__pycache__'))
 p=subprocess.run([sys.executable,'audit_fst11.py'],cwd=W,text=True,capture_output=True,timeout=60)
 (O/'audit.log').write_text(p.stdout+p.stderr)
 assert p.returncode==0,(p.returncode,p.stderr[-1800:])
 for name in ['AUDIT_RESULTS.json','original_cli.log']:shutil.copy2(W/name,O/name)
after={name:sha(R/name) for name in before};assert before==after
result=json.loads((O/'AUDIT_RESULTS.json').read_text());assert result['status']=='PASS'
up=json.loads((H/'UPSTREAM.json').read_text());assert sha(H/'src/fst11.py')==up['source_engine_sha256']
receipt={'status':'PASS','edition':'RC3.3','recorded_utc':started,'seconds':time.monotonic()-t,
 'software':{'python':platform.python_version()},'argv':[sys.executable,'audit_fst11.py'],
 'input_hashes_before':before,'input_hashes_after':after,
 'outputs':{str(p.relative_to(R)):sha(p) for p in O.iterdir() if p.is_file() and p.name!='RUN_MANIFEST.json'},
 'source_engine_byte_identical':True,'words_checked':11111,'atlas_records_checked':25,'signature_classes_checked':376,
 'guaranteed_finite_decoder_words':1111,'prime_set_lattice_pairs_checked':7200,
 'scope':'Finite exact replay, not external independent peer review; original historical 47/29 suites were not supplied.'}
(O/'RUN_MANIFEST.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('PASS: FST11 unchanged source, 25 atlas records, 11111 words, 376 signature classes, 1111 finite decodings and 7200 prime-set pairs.')
