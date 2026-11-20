"""Independent cut-point reconstruction and finite-survivor checking."""
from pathlib import Path
from fractions import Fraction as Q
from bisect import bisect_right,bisect_left
from collections import deque
from datetime import datetime,timezone
import argparse,json,time,hashlib,os
R=Path(__file__).resolve().parent;HALF=Q(1,2);ONE=Q(1)
def maps(B,x):
 p,q=x.numerator,x.denominator
 return Q(B*p%q,q),Q(p,p+(B*(q-p))%p)
def member(xs,starts,x):
 i=bisect_right(starts,x)-1
 return i>=0 and xs[i][0]<x<xs[i][1]
def atomic_step(B,xs):
 cuts={HALF,ONE};starts=[a for a,b in xs]
 for a,b in xs:
  cuts.update((a,b))
  for k in range(B):
   for t in (a,b):
    x=(k+t)/B;y=B*t/(1+(B-1+k)*t)
    if HALF<x<ONE:cuts.add(x)
    if HALF<y<ONE:cuts.add(y)
 for k in range(B+1):
  a=Q(k,B);b=Q(B,B+k)
  if HALF<a<ONE:cuts.add(a)
  if HALF<b<ONE:cuts.add(b)
 cuts=sorted(cuts)
 def allowed(x):
  if not member(xs,starts,x):return False
  t,s=maps(B,x);return member(xs,starts,t) and member(xs,starts,s)
 # Every split is a previous boundary or an actual branch/preimage boundary.
 assert not any(allowed(x) for x in cuts[1:-1]),'Unexpected retained cut point'
 return [(a,b) for a,b in zip(cuts,cuts[1:]) if allowed((a+b)/2)]
def geometry_graph(B,xs):
 starts=[a for a,b in xs];edges=[[],[]];digits=[[],[]]
 for a,b in xs:
  x=(a+b)/2;ds=[(B*x).__floor__(),(B*(1/x-1)).__floor__()]
  for g,k in enumerate(ds):
   if g==0:lo,hi=B*a-k,B*b-k
   else:lo,hi=a/(B-(B-1+k)*a),b/(B-(B-1+k)*b)
   assert HALF<=lo<hi<=ONE
   j=max(0,bisect_left(starts,lo)-1);row=[]
   while j<len(xs) and xs[j][0]<hi:
    if lo<xs[j][1] and xs[j][0]<hi:row.append(j)
    j+=1
   edges[g].append(row);digits[g].append(k)
 n=len(xs);alive=[True]*n;degrees=[[len(v) for v in es] for es in edges];rev=[[[] for _ in xs] for _ in [0,1]]
 for g in [0,1]:
  for i,row in enumerate(edges[g]):
   for j in row:rev[g][j].append(i)
 queue=deque(i for i in range(n) if not degrees[0][i] or not degrees[1][i])
 while queue:
  v=queue.popleft()
  if not alive[v]:continue
  alive[v]=False
  for g in [0,1]:
   for w in rev[g][v]:
    degrees[g][w]-=1
    if alive[w] and degrees[g][w]==0:queue.append(w)
 good={i for i,v in enumerate(alive) if v}
 return good,[[[j for j in row if j in good] for row in es] for es in edges],digits

def terminal_components(B,points):
 points=set(points)
 while True:
  kept={x for x in points if all(y in points for y in maps(B,x))}
  if kept==points:break
  points=kept
 reaches={}
 for x in points:
  seen={x};todo=[x]
  while todo:
   for y in maps(B,todo.pop()):
    if y not in seen:seen.add(y);todo.append(y)
  reaches[x]=seen
 unseen=set(points);out=[]
 while unseen:
  x=min(unseen);block={y for y in reaches[x] if x in reaches[y]};unseen-=block
  if all(y in block for z in block for y in maps(B,z)):
   out.append(dict(states=sorted(map(str,block)),size=len(block),permutational=all(len({maps(B,z)[g] for z in block})==len(block) for g in [0,1])))
 return sorted(out,key=lambda q:q['states']),sorted(map(str,points))
def verify(row):
 B=row['B'];xs=[(HALF,ONE)]
 for h in row['history']:
  xs=atomic_step(B,xs);assert len(xs)==h['intervals'],(B,h,len(xs))
 if not xs:
  assert not row.get('components');return dict(B=B,status='PASS',components=[],depth=len(row['history']),all_cardinalities=True)
 good,edges,digits=geometry_graph(B,xs)
 if not good:
  assert not row.get('components');return dict(B=B,status='PASS',components=[],depth=len(row['history']),all_cardinalities=True)
 assert row['status']=='FINITE_REAL_SURVIVOR'
 assert xs==[tuple(map(Q,v)) for v in row['certificate']['intervals']]
 assert good==set(row['certificate']['alive'])
 g=0 if row['deterministic_letter']=='T' else 1
 assert all(len(edges[g][i])==1 for i in good)
 points=[]
 for i in good:
  path=[];where={};v=i
  while v not in where:where[v]=len(path);path.append(v);v=edges[g][v][0]
  r=where[v];cyc=path[r:];prefix=path[:r];c=p=0
  for v in cyc:c=B*c+digits[g][v]
  for v in prefix:p=B*p+digits[g][v]
  y=(p+Q(c,B**len(cyc)-1))/B**r;x=y if g==0 else 1/(1+y)
  if xs[i][0]<x<xs[i][1]:points.append(x)
 comps,pts=terminal_components(B,points)
 want=sorted([dict(states=sorted(x['states']),size=x['size'],permutational=x['permutational']) for x in row['components']],key=lambda q:q['states'])
 assert comps==want,(B,comps,want)
 assert pts==sorted(row['survivor_points'])
 return dict(B=B,status='PASS',components=comps,real_survivor_points=pts,depth=len(row['history']),all_cardinalities=True)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--max-base',type=int,default=38);ap.add_argument('--input',default='ALL_CARDINALITIES_B2_60.json');ap.add_argument('--output',default='INTERVAL_INDEPENDENT_CHECK.json');args=ap.parse_args()
 source=R/args.input;raw=source.read_bytes();digest=hashlib.sha256(raw).hexdigest();data=json.loads(raw);rows=[x for x in data['results'] if x['B']<=args.max_base and not x['status'].startswith('INCONCLUSIVE')]
 out=R/args.output;previous=json.loads(out.read_text()) if out.exists() else {};done={x['B']:x for x in previous.get('results',[])};tic=time.monotonic()
 print('BEFORE',json.dumps(dict(equations=['independent exact cut-point partition of H','direct rational T,S, separate finite closure'],units='dimensionless Z/Q',bases=[x['B'] for x in rows],input_sha256=digest,point_or_cardinality_cutoff=None,scope='Independent implementation, not external peer review')),flush=True)
 for row in rows:
  rdigest=hashlib.sha256(json.dumps(row,sort_keys=True).encode()).hexdigest()
  if row['B'] in done and done[row['B']].get('row_sha256')==rdigest:continue
  result=verify(row);result['row_sha256']=rdigest;done[row['B']]=result
  obj=dict(status='PASS_FOR_CHECKED_BASES',results=[done[k] for k in sorted(done)],seconds=time.monotonic()-tic,scope='All-cardinality scope at each checked base; unchecked bases receive no conclusion.')
  tmp=out.with_suffix('.tmp');tmp.write_text(json.dumps(obj,indent=2)+'\n');os.replace(tmp,out)
  print('INDEPENDENT_PASS',row['B'],'components',len(result['components']),'seconds',round(time.monotonic()-tic,3),flush=True)
 print('INTERVAL_CHECK_FINISHED',len(done),flush=True)
