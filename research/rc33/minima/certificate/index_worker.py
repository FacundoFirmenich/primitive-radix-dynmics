"""Resumable all-height index search with separate uniqueness/minimum objectives."""
from pathlib import Path
from datetime import datetime,timezone
import sqlite3,json,hashlib,subprocess,sys,time,os,fcntl,argparse,platform
from index_geometry import packets,recover
from half_duality import transfer_r3
R=Path(__file__).resolve().parent;BSTAR=88011536665779

def now():return datetime.now(timezone.utc).isoformat()
def atomic(p,obj):
 t=p.with_suffix(p.suffix+'.tmp');t.write_text(json.dumps(obj,indent=2)+'\n');os.replace(t,p)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--db',default=str(R/'INDEX_STATE.sqlite'));ap.add_argument('--start-index',type=int,default=1);ap.add_argument('--end-index',type=int);ap.add_argument('--forever',action='store_true');args=ap.parse_args()
 os.nice(10);db=Path(args.db);lock=db.with_suffix('.lock').open('a');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
 paths=[Path(__file__),R/'index_geometry.py',R/'square_levels.cpp',R/'square_levels',R/'fibre_arithmetic.py',R/'half_duality.py']
 hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in paths};finger=hashlib.sha256(json.dumps(hashes,sort_keys=True).encode()).hexdigest()
 c=sqlite3.connect(db,isolation_level=None);c.execute('PRAGMA journal_mode=WAL')
 c.executescript('CREATE TABLE IF NOT EXISTS meta(k TEXT PRIMARY KEY,v TEXT);CREATE TABLE IF NOT EXISTS levels(lam INTEGER PRIMARY KEY,plan TEXT,pairs TEXT,qr_filtered TEXT,exact_tests TEXT,square_pairs TEXT,necessary_candidates INTEGER,carriers INTEGER,completed TEXT);CREATE TABLE IF NOT EXISTS tiles(k TEXT PRIMARY KEY,lam INTEGER,plane INTEGER,klo INTEGER,khi INTEGER,jlo INTEGER,jhi INTEGER,counts TEXT);CREATE TABLE IF NOT EXISTS hits(k TEXT PRIMARY KEY,lam INTEGER,branch TEXT,known INTEGER,beats_base INTEGER,payload TEXT);CREATE TABLE IF NOT EXISTS necessary(k TEXT PRIMARY KEY,lam INTEGER,payload TEXT);')
 def get(k,d=None):
  a=c.execute('SELECT v FROM meta WHERE k=?',(k,)).fetchone();return a[0] if a else d
 def put(k,v):c.execute('INSERT OR REPLACE INTO meta VALUES(?,?)',(k,str(v)))
 if get('fingerprint') is None:put('fingerprint',finger);put('index',args.start_index)
 assert get('fingerprint')==finger,'Frozen kernel mismatch'
 known={(fx['r'],'normal',*fx['coordinates_ACDQE']) for fx in json.loads((R/'CORE_GATE_RESULTS.json').read_text())['positive_controls']}
 print('BEFORE',json.dumps(dict(timestamp=now(),equations=['kappa*E=lambda*abs(j)*(Q-j*(C-A))','two exact integral quadratic levels K,J','Delta=W^2*Z(K,J)'],units='dimensionless Z/Q',B_star=BSTAR,start_index=args.start_index,end_index=args.end_index,continuous=args.forever,mods=[16,7,11,13,17,19,23],K_tile=64,J_tile=4096,hashes=hashes,python=platform.python_version(),scope='Each completed index covers all heights in the five chambers; no uniform index bound or global minimum claimed.'),sort_keys=True),flush=True)
 status=db.with_suffix('.status.json');t0=time.monotonic()
 def report(state,lam,plane=None):
  last=c.execute('SELECT max(lam) FROM levels').fetchone()[0]
  obj=dict(status=state,pid=os.getpid(),updated_at=now(),index=lam,plane=plane,completed_from=args.start_index,completed_through=last,tiles=c.execute('SELECT count(*) FROM tiles').fetchone()[0],known_carriers=c.execute('SELECT count(*) FROM hits WHERE known=1').fetchone()[0],new_carriers=c.execute('SELECT count(*) FROM hits WHERE known=0').fetchone()[0],better_base_candidates=c.execute('SELECT count(*) FROM hits WHERE beats_base=1').fetchone()[0],fingerprint=finger,seconds=time.monotonic()-t0,scope='Index domain only; minimum and uniqueness are separate objectives.')
  atomic(status,obj);return obj
 while True:
  lam=int(get('index'))
  if args.end_index is not None and lam>args.end_index:report('completed_requested_indices',lam);break
  if not args.forever and args.end_index is None and lam>args.start_index:report('completed_requested_indices',lam);break
  plan,symbolic=packets(lam);planfile=db.parent/f'INDEX_{lam}_PLAN.json'
  if not planfile.exists():atomic(planfile,dict(lambda_value=lam,packets=plan,symbolic_exclusions=symbolic))
  counts=[0,0,0,0];nc=0;carriers=0
  for pi,p in enumerate(plan):
   k0,k1=p['K_range'];j0,j1=p['J_range']
   for kl in range(k0,k1,64):
    ku=min(kl+64,k1)
    for jl in range(j0,j1,4096):
     ju=min(jl+4096,j1);key=f'{lam}:{pi}:{kl}:{ku}:{jl}:{ju}'
     old=c.execute('SELECT counts FROM tiles WHERE k=?',(key,)).fetchone()
     if old:
      cs=json.loads(old[0]);counts=[a+b for a,b in zip(counts,cs)];continue
     assert all(hashlib.sha256(q.read_bytes()).hexdigest()==hashes[q.name] for q in paths),'Kernel mutated'
     print('BEFORE_TILE',json.dumps(dict(lambda_value=lam,branch=p['branch'],kappa=p['kappa'],params=p['params'],K=[kl,ku],J=[jl,ju])),flush=True)
     raw=' '.join(map(str,[*p['params'],kl,ku,jl,ju]))+'\n'
     q=subprocess.run([str(R/'square_levels')],input=raw,text=True,capture_output=True)
     assert q.returncode==0,q.stderr
     square=[];cs=None
     for line in q.stdout.splitlines():
      a=line.split()
      if a[0]=='H':square.append(tuple(map(int,a[1:])))
      elif a[0]=='C':cs=list(map(int,a[1:]))
     assert cs and cs[0]==(ku-kl)*(ju-jl) and cs[3]==len(square)
     c.execute('BEGIN IMMEDIATE')
     for K,J in square:
      for nr in recover(p,K,J):
       nk=f"{p['r']}:{p['branch']}:"+','.join(map(str,nr['core']));c.execute('INSERT OR IGNORE INTO necessary VALUES(?,?,?)',(nk,lam,json.dumps(dict(packet=p,point=nr))))
       for hit in nr['realizations']:
        A,C,D,Q=hit['core'];E=hit['E'];ori='reflected' if p['branch'].startswith('606') else 'normal';is_known=int((p['r'],ori,A,C,D,Q,E) in known);beat=int(hit['base']<BSTAR)
        payload=dict(r=p['r'],orientation=ori,point=hit,K=K,J=J,lambda_value=lam,known=bool(is_known),beats_known_base=bool(beat))
        c.execute('INSERT OR IGNORE INTO hits VALUES(?,?,?,?,?,?)',(nk,lam,p['branch'],is_known,beat,json.dumps(payload)))
        print('VERIFIED_CARRIER',json.dumps(payload),flush=True)
        if p['r']==3:
         dual=transfer_r3(ori,(A,C,D,Q),E,hit['base'],hit['period'])
         if dual['transfers']:print('VERIFIED_DUAL_TRANSFER',json.dumps(dual),flush=True)
     c.execute('INSERT INTO tiles VALUES(?,?,?,?,?,?,?,?)',(key,lam,pi,kl,ku,jl,ju,json.dumps(cs)));c.execute('COMMIT')
     counts=[a+b for a,b in zip(counts,cs)];report('running',lam,pi)
  nc=c.execute('SELECT count(*) FROM necessary WHERE lam=?',(lam,)).fetchone()[0];carriers=c.execute('SELECT count(*) FROM hits WHERE lam=?',(lam,)).fetchone()[0]
  c.execute('BEGIN IMMEDIATE');c.execute('INSERT OR REPLACE INTO levels VALUES(?,?,?,?,?,?,?,?,?)',(lam,json.dumps(dict(packets=len(plan),symbolic_exclusions=symbolic)),*map(str,counts),nc,carriers,now()));put('index',lam+1);c.execute('COMMIT')
  print('COMPLETE_INDEX',json.dumps(dict(lambda_value=lam,packets=len(plan),counts=counts,necessary=nc,carriers=carriers)),flush=True);report('running',lam+1)
if __name__=='__main__':main()
