"""Check fixed minimum/uniqueness certificates; optionally replay their full domains."""
from pathlib import Path
import argparse,json,hashlib,shutil,subprocess,sys,importlib.util,time,platform

ROOT=Path(__file__).resolve().parents[3]
SRC=ROOT/'research/rc33/minima/certificate'
WORK=ROOT/'build/minima-replay'
ap=argparse.ArgumentParser();ap.add_argument('--full',action='store_true');args=ap.parse_args()
manifest=json.loads((SRC/'MANIFEST_SHA256.json').read_text())
for name,digest in manifest.items():assert hashlib.sha256((SRC/name).read_bytes()).hexdigest()==digest,name
WORK.mkdir(parents=True,exist_ok=True)
(ROOT/'outputs/reports/minima').mkdir(parents=True,exist_ok=True)
for name in manifest:shutil.copy2(SRC/name,WORK/name)
print('BEFORE',json.dumps(dict(units='dimensionless exact Z/Q',B_star=88011536665779,
    base_certificate_range=[2,53],index_certificate_range=[1,12],full_replay=args.full,
    equations=['K0=H; K(d+1)=H intersect T^-1(Kd) intersect S^-1(Kd)',
               'Delta=W^2 Z(K,J)','13 H^4 <32((Bstar-1)^2-1)',
               '16 lambda^5 <81((Bstar-1)^2-1)'],Python=platform.python_version(),
    fixed_manifest_sha256=hashlib.sha256((SRC/'MANIFEST_SHA256.json').read_bytes()).hexdigest(),
    scope='Saved full-domain certificates plus fresh controls; --full repeats every domain.')),
    flush=True)
tic=time.monotonic()
def run(argv,log):
    with (WORK/log).open('w') as f:p=subprocess.run(argv,cwd=WORK,stdout=f,stderr=subprocess.STDOUT)
    assert p.returncode==0,(argv,str(WORK/log))
run(['g++','-O3','-std=c++17','square_levels.cpp','-lgmpxx','-lgmp','-o','square_levels'],'compile.log')
sys.path.insert(0,str(WORK))
import index_geometry as geo
prefix=json.loads((WORK/'INDEX_PREFIX_1_12.json').read_text())
assert prefix['completed_indices']==[1,12]
assert [x['lambda_value'] for x in prefix['levels']]==list(range(1,13))
actual_tiles={x['key']:x for x in prefix['tiles']};expected=set();pairs=0
for level in prefix['levels']:
    L=level['lambda_value'];plans,skips=geo.packets(L)
    saved=json.loads((WORK/f'INDEX_{L}_PLAN.json').read_text())
    assert saved==dict(lambda_value=L,packets=plans,symbolic_exclusions=skips)
    lp=0
    for i,p in enumerate(plans):
        k0,k1=p['K_range'];j0,j1=p['J_range']
        for kl in range(k0,k1,64):
            for jl in range(j0,j1,4096):
                ku=min(kl+64,k1);ju=min(jl+4096,j1);key=f'{L}:{i}:{kl}:{ku}:{jl}:{ju}'
                expected.add(key);tile=actual_tiles[key];n=(ku-kl)*(ju-jl)
                assert tile['counts'][0]==n and tile['counts'][1]+tile['counts'][2]==n
                lp+=n
    assert lp==level['level_pairs'] and level['necessary_candidates']==level['carriers']==0
    pairs+=lp
assert expected==set(actual_tiles) and pairs==117093402
bases=json.loads((WORK/'FIXED_BASES_B2_53.json').read_text())['results']
checks={x['B']:x for x in json.loads((WORK/'INDEPENDENT_BASE_CHECKS.json').read_text())['results']}
assert set(checks)==set(range(2,54))
for row in bases:
    assert checks[row['B']]['row_sha256']==hashlib.sha256(json.dumps(row,sort_keys=True).encode()).hexdigest()
    assert checks[row['B']]['status']=='PASS' and all(x['permutational'] for x in row['components'])
for script in ['test_square_levels.py','test_index_resume.py','verify_basic_intervals.py']:
    run([sys.executable,'-B',script],script+'.log')
small=[row for row in bases if row['B'] in [2,7,19]]
(WORK/'SMALL_BASES.json').write_text(json.dumps(dict(results=small)))
if (WORK/'FRESH_SMALL_CHECK.json').exists():(WORK/'FRESH_SMALL_CHECK.json').unlink()
run([sys.executable,'-B','verify_intervals_v2.py','--input','SMALL_BASES.json',
     '--max-base','53','--output','FRESH_SMALL_CHECK.json'],'small-intervals.log')
if args.full:
    db=WORK/'full-index.sqlite'
    for p in WORK.glob('full-index.sqlite*'):p.unlink()
    run([sys.executable,'-B','index_worker.py','--db',str(db),'--start-index','1','--end-index','12'],'full-index.log')
    import sqlite3
    c=sqlite3.connect(db)
    for level in prefix['levels']:
        row=c.execute('SELECT pairs,necessary_candidates,carriers FROM levels WHERE lam=?',(level['lambda_value'],)).fetchone()
        assert row==(str(level['level_pairs']),0,0)
    fullout=WORK/'FRESH_ALL_BASES.json'
    if fullout.exists():fullout.unlink()
    run([sys.executable,'-B','verify_intervals_v2.py','--input','FIXED_BASES_B2_53.json',
         '--max-base','53','--output',str(fullout)],'full-intervals.log')
    assert len(json.loads(fullout.read_text())['results'])==52
for name,digest in manifest.items():assert hashlib.sha256((SRC/name).read_bytes()).hexdigest()==digest,name
out=dict(status='PASS',mode='full-domain replay' if args.full else 'archive, coverage and fresh controls',
    level_pairs_fixed_domain=pairs,bases_fixed_domain=52,minimum_base_all_cardinality_lower_bound=54,
    original_inputs_unchanged=True,full_domains_replayed_now=args.full,seconds=time.monotonic()-tic,
    scope='No global uniqueness or minimum-base assertion.')
(ROOT/'outputs/reports/minima/MINIMA_REPLAY.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS',json.dumps(out),flush=True)
