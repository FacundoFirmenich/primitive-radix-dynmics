from pathlib import Path
import subprocess,sys,sqlite3,json,time
R=Path(__file__).resolve().parent;D=R/'resume-check';D.mkdir(exist_ok=True)
print('BEFORE: exact index-worker checkpoint regression: indices1..2 then3 versus indices1..3; no live databases modified; compare all semantic rows, excluding completion timestamps.',flush=True)
def run(name,end):
 p=subprocess.run([sys.executable,'-B',str(R/'index_worker.py'),'--db',str(D/(name+'.sqlite')),'--start-index','1','--end-index',str(end)],capture_output=True,text=True)
 (D/(name+str(end)+'.log')).write_text(p.stdout+p.stderr);assert p.returncode==0,p.stderr
for name in ['split','whole']:
 for p in D.glob(name+'.sqlite*'):p.unlink()
run('split',2);run('split',3);run('whole',3)
def state(name):
 c=sqlite3.connect(D/(name+'.sqlite'));out={}
 for t,k in [('meta','k'),('tiles','k'),('necessary','k'),('hits','k')]:out[t]=c.execute('SELECT * FROM '+t+' ORDER BY '+k).fetchall()
 out['levels']=[v[:-1] for v in c.execute('SELECT * FROM levels ORDER BY lam')];return out
a,b=state('split'),state('whole');assert a==b
out=dict(status='PASS',completed_indices=[1,2,3],checkpoint_equal=True,tiles=len(a['tiles']),timestamp_fields_excluded=True)
(R/'INDEX_RESUME_TESTS.json').write_text(json.dumps(out,indent=2)+'\n');print('PASS',json.dumps(out),flush=True)
