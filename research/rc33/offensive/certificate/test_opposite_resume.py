from pathlib import Path
import json,subprocess,sqlite3,sys,hashlib,time
from fibre_arithmetic import ROOT,SEEDS

print('BEFORE: persistent paired worker, static fixture inputs, no live feeds; compare 80+80 completed contexts to 160 uninterrupted contexts; classes and all input seed values are fixed below. This is a resume/coverage control, not a global carrier enumeration.',flush=True)
seeds=[]
for x in SEEDS:seeds.append(dict(r=3,orientation='reflected',core=x,source={'kind':'recorded_near_miss'}))
for f in json.loads((ROOT/'CORE_GATE_RESULTS.json').read_text())['positive_controls']:
    seeds.append(dict(r=f['r'],orientation='normal',core=f['coordinates_ACDQE'][:4],source={'kind':'positive_control'}))
print('FIXTURE_SEEDS',json.dumps(seeds),flush=True)
fixture=ROOT/'RESUME_FIXTURE_SEEDS.json';fixture.write_text(json.dumps(dict(seeds=seeds),indent=2)+'\n')
folder=ROOT/'checks';folder.mkdir(exist_ok=True)
for stem in ['pair_resume','pair_reference']:
    for p in folder.glob(stem+'*'):p.unlink()

def run(stem,n):
    cmd=[sys.executable,'-B',str(ROOT/'opposite_worker.py'),'--db',str(folder/(stem+'.sqlite')),'--steps',str(n),'--snapshot','','--seed-file',str(fixture),'--no-live']
    p=subprocess.run(cmd,capture_output=True,text=True)
    with (ROOT/'OPPOSITE_RESUME_CHECK.log').open('a') as f:f.write(p.stdout+p.stderr)
    assert p.returncode==0,p.stdout+p.stderr


def state(stem):
    c=sqlite3.connect(folder/(stem+'.sqlite'))
    tables={}
    for t,key in [('contexts','k'),('results','k'),('hits','k'),('near','k'),('events','seq'),('meta','k')]:
        tables[t]=c.execute('SELECT * FROM '+t+' ORDER BY '+key).fetchall()
    c.close();return tables


tic=time.monotonic();run('pair_resume',80);run('pair_resume',80);run('pair_reference',160)
a,b=state('pair_resume'),state('pair_reference');assert a==b
known=sum(row[3] for row in a['hits']);new=len(a['hits'])-known
assert known==2
observed_processed=int(dict(a['meta'])['processed'])
result=dict(status='PASS',resume_equal=True,requested_reference_steps=160,processed=observed_processed,closed_for_static_inputs=not any(row[10]==0 for row in a['contexts']),known_carriers_recovered=known,new_carriers=new,contexts=len(a['contexts']),state_sha256=hashlib.sha256(repr(a).encode()).hexdigest(),seconds=time.monotonic()-tic)
(ROOT/'OPPOSITE_RESUME_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print('OPPOSITE_RESUME_PASS',json.dumps(result),flush=True)
