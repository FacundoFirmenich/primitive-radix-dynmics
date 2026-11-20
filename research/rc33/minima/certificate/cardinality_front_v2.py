"""Persistent base-by-base all-cardinality certificate search with fair retries."""
from pathlib import Path
from datetime import datetime,timezone
import json,sqlite3,subprocess,sys,os,time,hashlib,fcntl
R=Path(__file__).resolve().parent

def now():return datetime.now(timezone.utc).isoformat()
def atomic(p,d):
 t=p.with_suffix(p.suffix+'.tmp');t.write_text(json.dumps(d,indent=2)+'\n');os.replace(t,p)
def main():
 os.nice(10);lock=(R/'CARDINALITY_FRONT.lock').open('a');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
 files=[Path(__file__),R/'interval_survivor_v2.py',R/'verify_intervals_v2.py'];hashes={x.name:hashlib.sha256(x.read_bytes()).hexdigest() for x in files}
 print('BEFORE',json.dumps(dict(timestamp=now(),equations=['exact common-survivor intervals','deterministic-letter finite graph certificate'],units='dimensionless exact rational',initial_base=2,base_upper_cutoff=None,initial_depth=8,max_intervals_per_attempt=200000,initial_soft_seconds=180,fairness='three new/pending bases then one smallest deferred base',scope='Only independently checked successful certificates exclude a base. Time/depth limits never exclude.',source_hashes=hashes)),flush=True)
 c=sqlite3.connect(R/'CARDINALITY_FRONT.sqlite',isolation_level=None);c.execute('PRAGMA journal_mode=WAL');c.executescript('CREATE TABLE IF NOT EXISTS jobs(B INTEGER PRIMARY KEY,status TEXT,attempts INTEGER,payload TEXT);CREATE TABLE IF NOT EXISTS meta(k TEXT PRIMARY KEY,v TEXT);')
 folder=R/'cardinality-front';folder.mkdir(exist_ok=True)
 def status(state,B=None):
  checked={x[0]:json.loads(x[1]) for x in c.execute("SELECT B,payload FROM jobs WHERE status='verified'")};low=2
  while low in checked and not any(not z['permutational'] for z in checked[low]['components']):low+=1
  wins=[(b,z) for b,v in checked.items() for z in v['components'] if not z['permutational']]
  atomic(R/'CARDINALITY_FRONT.status.json',dict(status=state,pid=os.getpid(),updated_at=now(),base=B,verified_bases=len(checked),first_unexcluded_base=low,nonpermutation_witnesses=wins,all_cardinality_minimum_proved=bool(wins and min(x[0] for x in wins)==low),scope='Exact checked bases only; no inference for unverified bases.'))
 while True:
  q=R/'CARDINALITY_BATCH.status.json'
  if not q.exists() or json.loads(q.read_text()).get('status')=='completed_requested_bases':break
  status('waiting_for_initial_batch');time.sleep(5)
 # Import primary certificates as candidates; each is checked before admission.
 for filename in ['ALL_CARDINALITIES_B2_60.json','INTERVAL_B53_DEEP.json']:
  p=R/filename
  if p.exists():
   for row in json.loads(p.read_text())['results']:
    state='deferred' if row['status'].startswith('INCONCLUSIVE') else 'pending'
    c.execute('INSERT OR IGNORE INTO jobs VALUES(?,?,?,?)',(row['B'],state,0,json.dumps(row)))
    if state=='pending':c.execute("UPDATE jobs SET status='pending',payload=? WHERE B=? AND status='deferred'",(json.dumps(row),row['B']))

 # Seed already independently verified publication certificates; retain gaps.
 fixed=json.loads((R/'fixed-certificates/FIXED_BASES_B2_53.json').read_text())['results']
 proofs={v['B']:v for v in json.loads((R/'fixed-certificates/INDEPENDENT_BASE_CHECKS.json').read_text())['results']}
 for row in fixed:
  digest=hashlib.sha256(json.dumps(row,sort_keys=True).encode()).hexdigest()
  assert proofs[row['B']]['status']=='PASS' and proofs[row['B']]['row_sha256']==digest
  c.execute('INSERT OR REPLACE INTO jobs VALUES(?,?,?,?)',(row['B'],'verified',0,json.dumps(row)))
 max_seed=c.execute('SELECT max(B) FROM jobs').fetchone()[0] or 1
 for B in range(2,max_seed+1):c.execute('INSERT OR IGNORE INTO jobs VALUES(?,?,?,?)',(B,'pending',0,'null'))
 cursor=int((c.execute("SELECT v FROM meta WHERE k='cursor'").fetchone() or [0])[0])
 while True:
  assert all(hashlib.sha256(x.read_bytes()).hexdigest()==hashes[x.name] for x in files),'Frozen cardinality kernel mismatch'
  item=None
  if cursor%4==3:item=c.execute("SELECT B,status,attempts,payload FROM jobs WHERE status='deferred' ORDER BY B LIMIT 1").fetchone()
  if item is None:item=c.execute("SELECT B,status,attempts,payload FROM jobs WHERE status='pending' ORDER BY B LIMIT 1").fetchone()
  if item is None:
   B=(c.execute('SELECT max(B) FROM jobs').fetchone()[0] or 1)+1;c.execute('INSERT INTO jobs VALUES(?,?,?,?)',(B,'pending',0,'null'));item=(B,'pending',0,'null')
  B,state,attempts,payload=item;status('running',B);row=json.loads(payload)
  if row is None or state=='deferred':
   out=folder/f'B{B}_attempt{attempts}.json';log=folder/f'B{B}_attempt{attempts}.log';seconds=min(900,180*(attempts+1));depth=8+attempts
   with log.open('w') as f:p=subprocess.run([sys.executable,'-B',str(R/'interval_survivor_v2.py'),'--min-base',str(B),'--max-base',str(B),'--depth',str(depth),'--max-intervals','200000','--seconds',str(seconds),'--output',str(out)],stdout=f,stderr=subprocess.STDOUT)
   if p.returncode:raise RuntimeError('Primary certificate failed: '+str(log))
   row=json.loads(out.read_text())['results'][0]
  attempts+=1
  if row['status'].startswith('INCONCLUSIVE'):c.execute('UPDATE jobs SET status=?,attempts=?,payload=? WHERE B=?',('deferred',attempts,json.dumps(row),B))
  else:
   inp=folder/f'B{B}_certificate.json';proof=folder/f'B{B}_checked.json';log=folder/f'B{B}_check.log';atomic(inp,dict(results=[row]))
   if proof.exists():
    try:json.loads(proof.read_text())
    except (ValueError,OSError):proof.rename(proof.with_suffix('.interrupted.json'))
   if not proof.exists():
    with log.open('w') as f:p=subprocess.run([sys.executable,'-B',str(R/'verify_intervals_v2.py'),'--input',str(inp),'--max-base',str(B),'--output',str(proof)],stdout=f,stderr=subprocess.STDOUT)
    if p.returncode:raise RuntimeError('Independent certificate failed: '+str(log))
   receipt=json.loads(proof.read_text());assert len(receipt['results'])==1 and receipt['results'][0]['B']==B and receipt['results'][0]['status']=='PASS'
   expected=hashlib.sha256(json.dumps(row,sort_keys=True).encode()).hexdigest();assert receipt['results'][0]['row_sha256']==expected
   c.execute('UPDATE jobs SET status=?,attempts=?,payload=? WHERE B=?',('verified',attempts,json.dumps(row),B));print('VERIFIED_BASE',B,row['components'],flush=True)
  cursor+=1;c.execute("INSERT OR REPLACE INTO meta VALUES('cursor',?)",(str(cursor),));status('running',B)
if __name__=='__main__':main()
