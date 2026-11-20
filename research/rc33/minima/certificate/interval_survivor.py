"""Exact common-survivor certificates, with no rational height/cardinality cutoff."""
from fractions import Fraction as F
from collections import deque
from bisect import bisect_left
from pathlib import Path
import json,time,argparse,os,platform
HALF=F(1,2);ONE=F(1)
def merge(xs):
 out=[]
 for a,b in sorted(xs):
  if not a<b:continue
  if out and a<out[-1][1]:out[-1]=(out[-1][0],max(out[-1][1],b))
  else:out.append((a,b))
 return out

def intersection(xs,ys):
 out=[];i=j=0
 while i<len(xs) and j<len(ys):
  a,b=xs[i];c,d=ys[j];l=max(a,c);u=min(b,d)
  if l<u:out.append((l,u))
  if b<d:i+=1
  elif d<b:j+=1
  else:i+=1;j+=1
 return merge(out)

def preimages(B,xs,letter):
 out=[]
 for l,u in xs:
  for k in range(B):
   if letter=='T':a,b=(k+l)/B,(k+u)/B
   else:
    c=B-1+k;a,b=B*l/(1+c*l),B*u/(1+c*u)
   a=max(a,HALF);b=min(b,ONE)
   if a<b:out.append((a,b))
 return merge(out)

def T(x,B):return B*x-(B*x).__floor__()
def S(x,B):return 1/(1+T(1/x-1,B))
def map_interval(B,I,g):
 a,b=I;m=(a+b)/2
 if g=='T':
  k=(B*m).__floor__();lo,hi=B*a-k,B*b-k
 else:
  k=(B*(1/m-1)).__floor__();c=B-1+k
  assert B-c*a>0 and B-c*b>0
  lo,hi=a/(B-c*a),b/(B-c*b)
 assert HALF<=lo<hi<=ONE,(B,I,g,k,lo,hi)
 return lo,hi,k

def graph(B,xs):
 starts=[x[0] for x in xs];edges={};digits={}
 for g in ['T','S']:
  es=[];ds=[]
  for I in xs:
   a,b,k=map_interval(B,I,g);j=max(0,bisect_left(starts,a)-1);targets=[]
   while j<len(xs) and xs[j][0]<b:
    if max(a,xs[j][0])<min(b,xs[j][1]):targets.append(j)
    j+=1
   es.append(targets);ds.append(k)
  edges[g]=es;digits[g]=ds
 alive=set(range(len(xs)))
 while True:
  bad={i for i in alive if any(not any(j in alive for j in edges[g][i]) for g in ['T','S'])}
  if not bad:break
  alive-=bad
 return alive,{g:{i:[j for j in edges[g][i] if j in alive] for i in alive} for g in ['T','S']},digits

def deterministic_points(B,xs,alive,edges,digits,g):
 nxt={i:edges[g][i][0] for i in alive};value={}
 for source in sorted(alive):
  if source in value:continue
  path=[];where={};i=source
  while i not in value and i not in where:where[i]=len(path);path.append(i);i=nxt[i]
  if i not in value:
   cycle=path[where[i]:];num=0
   for v in cycle:num=B*num+digits[g][v]
   value[i]=F(num,B**len(cycle)-1)
  for v in reversed(path):
   if v not in value:value[v]=(value[nxt[v]]+digits[g][v])/B
 points={i:(v if g=='T' else 1/(1+v)) for i,v in value.items()}
 return {i:x for i,x in points.items() if xs[i][0]<x<xs[i][1]}

def components(B,points):
 values=set(points.values())
 while True:
  bad={x for x in values if T(x,B) not in values or S(x,B) not in values}
  if not bad:break
  values-=bad
 # Finite transitive closure, then terminal SCCs. Domains kept small by caller.
 vs=sorted(values);idx={x:i for i,x in enumerate(vs)}
 adj=[(idx[T(x,B)],idx[S(x,B)]) for x in vs]
 # Iterative Kosaraju, avoiding recursion depth assumptions.
 seen=set();order=[]
 for i in range(len(vs)):
  if i in seen:continue
  seen.add(i);stack=[(i,0)]
  while stack:
   v,k=stack[-1]
   if k<2:
    w=adj[v][k];stack[-1]=(v,k+1)
    if w not in seen:seen.add(w);stack.append((w,0))
   else:order.append(v);stack.pop()
 rev=[[] for _ in vs]
 for i,row in enumerate(adj):
  for j in row:rev[j].append(i)
 seen=set();sccs=[]
 for v in reversed(order):
  if v in seen:continue
  block=set([v]);seen.add(v);q=[v]
  while q:
   z=q.pop()
   for w in rev[z]:
    if w not in seen:seen.add(w);block.add(w);q.append(w)
  if all(w in block for z in block for w in adj[z]):
   sccs.append(dict(states=[str(vs[z]) for z in sorted(block)],size=len(block),permutational=all(len({adj[z][g] for z in block})==len(block) for g in [0,1])))
 return sccs,[str(x) for x in vs]

def solve(B,max_depth=12,max_intervals=30000,max_seconds=20):
 xs=[(HALF,ONE)];history=[];tic=time.monotonic()
 for depth in range(1,max_depth+1):
  if len(xs)*B>max_intervals*8:
   return dict(B=B,status='INCONCLUSIVE_RESOURCE_LIMIT',history=history,seconds=time.monotonic()-tic)
  xs=intersection(intersection(preimages(B,xs,'T'),preimages(B,xs,'S')),xs)
  history.append(dict(depth=depth,intervals=len(xs)))
  if not xs:return dict(B=B,status='EMPTY_REAL_SURVIVOR',history=history,seconds=time.monotonic()-tic,components=[])
  if len(xs)>max_intervals or time.monotonic()-tic>max_seconds:
   return dict(B=B,status='INCONCLUSIVE_RESOURCE_LIMIT',history=history,seconds=time.monotonic()-tic)
  alive,edges,digits=graph(B,xs)
  if not alive:return dict(B=B,status='EMPTY_GRAPH_CORE',history=history,seconds=time.monotonic()-tic,components=[])
  for g in ['T','S']:
   if all(len(edges[g][i])==1 for i in alive):
    pts=deterministic_points(B,xs,alive,edges,digits,g)
    cs,allpoints=components(B,pts)
    return dict(B=B,status='FINITE_REAL_SURVIVOR',history=history,depth=depth,deterministic_letter=g,alive_intervals=len(alive),survivor_points=allpoints,components=cs,seconds=time.monotonic()-tic,certificate=dict(intervals=[[str(a),str(b)] for a,b in xs],alive=sorted(alive),digits=digits,edges={g:{str(i):row for i,row in edges[g].items()} for g in ['T','S']}))
 return dict(B=B,status='INCONCLUSIVE_DEPTH_LIMIT',history=history,seconds=time.monotonic()-tic)

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--min-base',type=int,default=2);ap.add_argument('--max-base',type=int,default=20);ap.add_argument('--depth',type=int,default=12);ap.add_argument('--max-intervals',type=int,default=30000);ap.add_argument('--seconds',type=float,default=20);ap.add_argument('--output',default='INTERVAL_SURVIVORS.json');args=ap.parse_args()
 print('BEFORE',json.dumps(dict(equations=['K0=(1/2,1)','K(d+1)=H intersect T^-1(Kd) intersect S^-1(Kd)'],open_endpoints=True,arithmetic='exact rational; dimensionless',B_range=[args.min_base,args.max_base],max_depth=args.depth,resource_interval_cap=args.max_intervals,resource_seconds=args.seconds,Python=platform.python_version(),scope='Empty or deterministic finite survivor certificates apply at every cardinality. Resource/depth limits give no exclusion.')),flush=True)
 os.nice(10);rows=[]
 for B in range(args.min_base,args.max_base+1):
  row=solve(B,args.depth,args.max_intervals,args.seconds);rows.append(row)
  Path(args.output).write_text(json.dumps(dict(results=rows),indent=2)+'\n')
  print('BASE',B,row['status'],row.get('history',[])[-1],row.get('components',[]),'seconds',round(row['seconds'],3),flush=True)
