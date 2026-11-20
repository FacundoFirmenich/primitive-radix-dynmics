"""Persistent alternating opposite-fibre search, with read-only live ingestion."""
from pathlib import Path
from datetime import datetime,timezone
from math import gcd
import argparse,json,sqlite3,hashlib,time,os,sys,fcntl
from paired_fibres import paired,neighbours
from half_duality import transfer_r3
from fibre_arithmetic import ROOT,chamber,primitive,rem,ArithmeticDeferred,complete

OLD=Path('/workspace/rgphi-tarasutra-sync-2026-11-19/sinus-pi/global-closure-2026-11-20/REPAIR_STATE.sqlite')
CLASSES=[(3,'reflected'),(3,'reflected'),(3,'normal'),(2,'normal')]
KNOWN={(f['r'],'normal',*f['coordinates_ACDQE']) for f in json.loads((ROOT/'CORE_GATE_RESULTS.json').read_text())['positive_controls']}


def now():return datetime.now(timezone.utc).isoformat()


def priority(r,o,x):
    A,C,D,Q=x;qp=sum(v==0 for v in rem(r,x));cs=0
    for j in ([1] if o=='reflected' else ([-1,1] if r==2 else [1,2])):
        if (D+j*A)%r:continue
        E=(D+j*A)//r
        real=(5*A<6*E<6*A) if o=='reflected' else A<E<2*A
        s=1+int(real)+int(E!=Q)+int(gcd(E,r)==1)
        if real:
            s+=sum((f%g==0) for g,f in [(gcd(E,C),D-Q),(gcd(E,Q),C-A),(gcd(E,D),r*A-C)])
        # Deterministic priority, not a probability or a rejection criterion.
        if r==3 and o=='normal' and j==2 and real:s+=2
        cs=max(cs,s)
    return qp,cs


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--db',default=str(ROOT/'OPPOSITE_STATE.sqlite'))
    ap.add_argument('--seed-file',default=str(ROOT/'GOOD_GCD_SEEDS.json'))
    ap.add_argument('--snapshot',default=str(ROOT/'PAIR_CONTEXTS_SNAPSHOT.jsonl'))
    ap.add_argument('--steps',type=int,default=5000);ap.add_argument('--forever',action='store_true')
    ap.add_argument('--no-live',action='store_true');args=ap.parse_args()
    sys.set_int_max_str_digits(0);os.nice(10)
    db=Path(args.db);lock=db.with_suffix('.lock').open('a');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    srcs=[Path(__file__),ROOT/'paired_fibres.py',ROOT/'half_duality.py',ROOT/'fibre_arithmetic.py']
    def fp():return hashlib.sha256(json.dumps({p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in srcs},sort_keys=True).encode()).hexdigest()
    frozen=fp();c=sqlite3.connect(db,timeout=30,isolation_level=None)
    c.execute('PRAGMA journal_mode=WAL');c.execute('PRAGMA synchronous=NORMAL')
    c.executescript('CREATE TABLE IF NOT EXISTS meta(k TEXT PRIMARY KEY,v TEXT);CREATE TABLE IF NOT EXISTS contexts(k TEXT PRIMARY KEY,r INTEGER,o TEXT,u TEXT,f1 TEXT,f2 TEXT,hd INTEGER,h TEXT,qp INTEGER,cs INTEGER,status INTEGER DEFAULT 0,origin TEXT);CREATE INDEX IF NOT EXISTS by_height ON contexts(r,o,status,hd,h,k);CREATE INDEX IF NOT EXISTS by_score ON contexts(r,o,status,qp DESC,cs DESC,hd,h,k);CREATE INDEX IF NOT EXISTS by_status ON contexts(status);CREATE TABLE IF NOT EXISTS results(k TEXT PRIMARY KEY,payload TEXT);CREATE TABLE IF NOT EXISTS hits(k TEXT PRIMARY KEY,r INTEGER,o TEXT,known INTEGER,payload TEXT,origin TEXT);CREATE TABLE IF NOT EXISTS near(k TEXT PRIMARY KEY,r INTEGER,o TEXT,a TEXT,c TEXT,d TEXT,q TEXT,qp INTEGER,cs INTEGER,origin TEXT);CREATE TABLE IF NOT EXISTS deferred(k TEXT PRIMARY KEY,reason TEXT);CREATE TABLE IF NOT EXISTS events(seq INTEGER PRIMARY KEY,k TEXT);CREATE TABLE IF NOT EXISTS ingests(k TEXT PRIMARY KEY,payload TEXT);')
    def get(k,d=None):
        row=c.execute('SELECT v FROM meta WHERE k=?',(k,)).fetchone();return row[0] if row else d
    def put(k,v):c.execute('INSERT OR REPLACE INTO meta VALUES(?,?)',(k,str(v)))
    def enqueue(r,o,u,fixed,pr,origin):
        f1,f2=map(int,fixed);h=str(max(f1,f2));key=f'{r}:{o}:{u}:{f1},{f2}'
        old=c.execute('SELECT qp,cs FROM contexts WHERE k=?',(key,)).fetchone()
        if old is None:c.execute('INSERT INTO contexts VALUES(?,?,?,?,?,?,?,?,?,?,0,?)',(key,r,o,u,str(f1),str(f2),len(h),h,*pr,json.dumps(origin,sort_keys=True)))
        elif tuple(pr)>tuple(old):c.execute('UPDATE contexts SET qp=?,cs=? WHERE k=?',(*pr,key))
    def vertex(r,o,x,origin):
        if (r,o) not in {(2,'normal'),(3,'normal'),(3,'reflected')}:
            raise ValueError('Undeclared arithmetic class')
        x=tuple(map(int,x))
        if not chamber(r,x,o) or not primitive(r,x):return
        A,C,D,Q=x;pr=priority(r,o,x)
        enqueue(r,o,'AC',(D,Q),pr,origin);enqueue(r,o,'DQ',(A,C),pr,origin)
        if pr[0]>=3:
            key=f'{r}:{o}:'+','.join(map(str,x))
            c.execute('INSERT OR IGNORE INTO near VALUES(?,?,?,?,?,?,?,?,?,?)',(key,r,o,*map(str,x),*pr,json.dumps(origin,sort_keys=True)))
        if pr[0]==4:
            for point in complete(r,x,o):register(r,o,point,origin)
    def register(r,o,point,origin,dual=True):
        A,C,D,Q=map(int,point['core']);E=int(point['E']);key=f'{r}:{o}:'+','.join(map(str,(A,C,D,Q,E)))
        if c.execute('SELECT 1 FROM hits WHERE k=?',(key,)).fetchone():return
        known=int((r,o,A,C,D,Q,E) in KNOWN)
        c.execute('INSERT INTO hits VALUES(?,?,?,?,?,?)',(key,r,o,known,json.dumps(point),json.dumps(origin,sort_keys=True)))
        print('KNOWN_CARRIER_REPLAY' if known else 'NEW_VERIFIED_CARRIER',json.dumps(dict(r=r,orientation=o,point=point,origin=origin)),flush=True)
        if r==3 and dual:
            transferred=transfer_r3(o,(A,C,D,Q),E,point['base'],point['period'])
            for hit in transferred['transfers']:
                target=transferred['target_orientation'];src=dict(kind='half_inversion_transfer',source_carrier=key,source_origin=origin)
                register(3,target,hit,src,False)
                a,cc,d,q=hit['core'];enqueue(3,target,'AC',(d,q),(4,20),src);enqueue(3,target,'DQ',(a,cc),(4,20),src)
    if get('fingerprint') is None:
        put('fingerprint',frozen);put('cursor',0);put('processed',0);put('old_rowid',0)
        if args.snapshot:
            p=Path(args.snapshot);digest=hashlib.sha256(p.read_bytes()).hexdigest()
            c.execute('BEGIN IMMEDIATE')
            for line in p.open():
                s=json.loads(line);enqueue(s['r'],s['orientation'],s['unknown'],s['fixed'],s['priority'],dict(kind='fixed_pair_snapshot',path=str(p),sha256=digest))
            put('initial_snapshot_sha256',digest);c.commit()
    elif get('fingerprint')!=frozen:raise RuntimeError('Frozen mathematical kernel changed; use a separate experiment database.')
    seedpath=Path(args.seed_file);last_ingest=0
    def ingest():
        if seedpath.exists():
            raw=seedpath.read_bytes();digest=hashlib.sha256(raw).hexdigest()
            if not c.execute('SELECT 1 FROM ingests WHERE k=?',(digest,)).fetchone():
                data=json.loads(raw);c.execute('BEGIN IMMEDIATE')
                for s in data['seeds']:vertex(s['r'],s['orientation'],s['core'],dict(kind='candidate_corpus',snapshot_sha256=digest,source=s.get('source',{})))
                c.execute('INSERT INTO ingests VALUES(?,?)',(digest,json.dumps(dict(path=str(seedpath),count=len(data['seeds']),observed_at=now()))));c.commit()
        if not args.no_live and OLD.exists():
            old=sqlite3.connect('file:'+str(OLD)+'?mode=ro',uri=True,timeout=30);old.execute('BEGIN')
            rows=old.execute('SELECT rowid,a,c,d,q,qp FROM states WHERE rowid>? AND qp>=2 ORDER BY rowid LIMIT 8192',(int(get('old_rowid',0)),)).fetchall()
            end=rows[-1][0] if rows else old.execute('SELECT coalesce(max(rowid),0) FROM states').fetchone()[0]
            old.commit();old.close();c.execute('BEGIN IMMEDIATE')
            for row in rows:vertex(3,'reflected',row[1:5],dict(kind='single_repair_live_context',source=str(OLD),rowid=row[0]))
            put('old_rowid',end);c.commit()
    print('BEFORE_OPPOSITE_WORKER',json.dumps(dict(units='dimensionless exact Z/Q',classes=CLASSES,core_coefficients_by_r={'2':[2,1,2,1],'3':[3,1,3,1]},moves='Alternating joint reconstruction of AC and DQ; all candidate divisors, double-residue join, original gcd/E/ten-edge gates',schedule='Class round-robin 2:1:1; per class three score turns and one height turn',normal_r3_j2_priority_bonus=2,seed_file=str(seedpath),initial_snapshot=args.snapshot,initial_snapshot_sha256=get('initial_snapshot_sha256'),live_old_source=str(OLD) if not args.no_live else None,trial_primality_threshold=100000,Lucas_bases_inclusive=[2,65],source_fingerprint=frozen,pid=os.getpid(),forever=args.forever,steps_this_packet=None if args.forever else args.steps,scope='Reachable opposite-context closure from recorded and live discovery inputs; not global classification.')),flush=True)
    steps=0;tic=time.monotonic();statuspath=db.with_suffix('.status.json')
    def status(state):
        z=dict(status=state,pid=os.getpid(),updated_at=now(),processed=int(get('processed',0)),pending=c.execute('SELECT count(*) FROM contexts WHERE status=0').fetchone()[0],deferred=c.execute('SELECT count(*) FROM contexts WHERE status=-1').fetchone()[0],contexts=c.execute('SELECT count(*) FROM contexts').fetchone()[0],known_carriers=c.execute('SELECT count(*) FROM hits WHERE known=1').fetchone()[0],new_carriers=c.execute('SELECT count(*) FROM hits WHERE known=0').fetchone()[0],near_vertices=c.execute('SELECT count(*) FROM near').fetchone()[0],old_source_cursor=int(get('old_rowid',0)),fingerprint=frozen,database=str(db),session_steps=steps,session_seconds=time.monotonic()-tic,scope='Exact paired fibres, discovery-input closure only.')
        tmp=statuspath.with_suffix('.tmp');tmp.write_text(json.dumps(z,indent=2)+'\n');os.replace(tmp,statuspath);print('OPPOSITE_STATUS',json.dumps(z),flush=True)
    try:
        ingest();status('running')
        while args.forever or steps<args.steps:
            if not args.no_live and time.monotonic()-last_ingest>20:ingest();last_ingest=time.monotonic()
            cursor=int(get('cursor',0));r,o=CLASSES[cursor%len(CLASSES)];turn=int(get(f'turn:{r}:{o}',0))
            order='hd,h,k' if turn%4==3 else 'qp DESC,cs DESC,hd,h,k'
            row=c.execute('SELECT k,u,f1,f2 FROM contexts WHERE r=? AND o=? AND status=0 ORDER BY '+order+' LIMIT 1',(r,o)).fetchone()
            if row is None:
                put('cursor',cursor+1)
                if c.execute('SELECT 1 FROM contexts WHERE status=0 LIMIT 1').fetchone() is None:
                    if args.forever and not args.no_live:status('waiting_for_input');time.sleep(1);continue
                    break
                continue
            key,u,f1,f2=row;fixed=tuple(map(int,(f1,f2)))
            try:
                result=paired(r,o,u,fixed);partial=neighbours(r,o,u,fixed)
                c.execute('BEGIN IMMEDIATE');put('cursor',cursor+1);put(f'turn:{r}:{o}',turn+1)
                for x in partial:vertex(r,o,x,dict(kind='paired_divisor_move',parent_context=key))
                for point in result['realizations']:register(r,o,point,dict(kind='paired_completion',context=key))
                # Keep compact complete-result evidence, including zero counts.
                compact={k:v for k,v in result.items() if k not in ['realizations','square_cores']}
                compact['square_core_count']=len(result['square_cores']);compact['realization_count']=len(result['realizations'])
                c.execute('INSERT OR REPLACE INTO results VALUES(?,?)',(key,json.dumps(compact)))
                c.execute('UPDATE contexts SET status=1 WHERE k=?',(key,));seq=int(get('processed',0))+1
                c.execute('INSERT INTO events VALUES(?,?)',(seq,key));put('processed',seq);c.commit();steps+=1
            except ArithmeticDeferred as e:
                if c.in_transaction:c.rollback()
                c.execute('BEGIN IMMEDIATE');put('cursor',cursor+1);put(f'turn:{r}:{o}',turn+1)
                c.execute('UPDATE contexts SET status=-1 WHERE k=?',(key,));c.execute('INSERT OR REPLACE INTO deferred VALUES(?,?)',(key,str(e)));c.commit()
            if steps and steps%500==0:
                if fp()!=frozen:raise RuntimeError('Frozen kernel changed during execution.')
                status('running')
        pending=c.execute('SELECT count(*) FROM contexts WHERE status=0').fetchone()[0]
        unknown=c.execute('SELECT count(*) FROM contexts WHERE status=-1').fetchone()[0]
        status('checkpointed' if pending else ('blocked_arithmetic' if unknown else 'closed_for_current_inputs'))
    except BaseException as e:
        if c.in_transaction:c.rollback()
        status('interrupted' if isinstance(e,KeyboardInterrupt) else 'failed');raise
    finally:c.close()


if __name__=='__main__':main()
