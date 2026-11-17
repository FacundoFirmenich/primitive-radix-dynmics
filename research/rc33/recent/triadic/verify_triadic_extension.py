#!/usr/bin/env python3
"""Exact direct-graph audit of finite-abelian covers and FST-09 fibres.
Run: python verify_triadic_extension.py
No source script is imported. Configuration is printed before computations.
"""
from __future__ import annotations
import json,sys,hashlib,time,platform
from pathlib import Path
from collections import deque,Counter
from itertools import product,combinations
from math import gcd,lcm
from fractions import Fraction
from decimal import Decimal,localcontext

ROOT=Path(__file__).resolve().parent
CONFIG={
 'python':platform.python_version(),'arithmetic':'integers, exact rational arithmetic; separately labelled Decimal entropy approximation',
 'units':'dimensionless residues, integer evaluations and combinatorial bits; no physical parameters',
 'equations':{'cover':'T(i,r)=(Ti,r+a), S(i,r)=(Si,r+b)','K':'<a,2b>','N':'<2(b-a)>','components':'|G|/|K|','period':'|K|/|N|','FST_K':'8*10**ell-9*s','FST_H':'K/7**v7(K)','FST_recorder':'floor(v7(K)/3)'},
 'values':{'X':4777,'Y':6444,'Z':7444,'FST_prime':7,'FST_A':343,'FST_P02':13841287201},
 'bases':[{'T':[1,0,3,2,4],'S':[4,2,1,0,0],'c':[0,0,1,1,1],'o':4}, {'T':[0,1],'S':[1,0],'c':[0,1],'o':0}],
 'abelian_moduli':[[1],[2],[3],[4],[2,2],[3,3],[4,4],[2,3],[2,2,2],[2,3,4]],
 'general_group_weights':'every ordered pair a,b of group elements for both bases',
 'concrete_joint_moduli':'all m=1..80, plus 125 and 128; both full covers and counter-only walks',
 'FST_full_enumeration_ell':[1,2,3,4,5,6],
 'FST_modular_precision_ell':[1,2,3,4],'FST_n':[0,1,5],
 'FST_02_brute_ell':[2,3,4,5,6,7],
 'FST_02_formula_ell':'2..20','entropy_Decimal_precision':60,'entropy_terms':'f=2..39',
 'probability_convention':'iid T with a in (0,1); exact stationary control a=2/5',
 'matrix_order':'right multiplication in chronological written order; [A,B]=ABA^-1B^-1'
}
print('CONFIGURATION BEFORE COMPUTATION\n'+json.dumps(CONFIG,indent=2),flush=True)
start=time.monotonic()

def add(x,y,mods):return tuple((a+b)%m for a,b,m in zip(x,y,mods))
def neg(x,mods):return tuple(-a%m for a,m in zip(x,mods))
def mul(k,x,mods):return tuple(k*a%m for a,m in zip(x,mods))
def subgroup(gens,mods):
 z=tuple(0 for _ in mods);seen={z};q=deque([z])
 while q:
  x=q.popleft()
  for a in gens:
   y=add(x,a,mods)
   if y not in seen:seen.add(y);q.append(y)
 return seen

def directed_components(adj):
 # SCC = forward reachability intersect backward reachability, not the source Kosaraju routine.
 n=len(adj);rev=[[] for _ in range(n)]
 for i,edges in enumerate(adj):
  for j in edges:rev[j].append(i)
 def reach(root,graph):
  seen={root};q=[root]
  for i in q:
   for j in graph[i]:
    if j not in seen:seen.add(j);q.append(j)
  return seen
 todo=set(range(n));out=[]
 while todo:
  root=next(iter(todo));comp=reach(root,adj)&reach(root,rev)
  todo.difference_update(comp)
  dist={root:0};q=[root]
  for i in q:
   for j in adj[i]:
    assert j in comp,'component not closed'
    if j not in dist:dist[j]=dist[i]+1;q.append(j)
  assert len(dist)==len(comp)
  period=0
  for i in comp:
   for j in adj[i]:period=gcd(period,dist[i]+1-dist[j])
  out.append((comp,period))
 return out

def graph(base,mods,a,b):
 elems=list(product(*(range(m) for m in mods)));inds={v:i for i,v in enumerate(elems)};n=len(elems)
 adj=[]
 for i in range(len(base['T'])):
  for r in elems:
   adj.append((base['T'][i]*n+inds[add(r,a,mods)],base['S'][i]*n+inds[add(r,b,mods)]))
 return adj,elems

cases=vertices=0
for mods0 in CONFIG['abelian_moduli']:
 mods=tuple(mods0);elems=list(product(*(range(m) for m in mods)))
 for a,b in product(elems,repeat=2):
  D=add(b,neg(a,mods),mods);K=subgroup((a,mul(2,b,mods)),mods);N=subgroup((mul(2,D,mods),),mods)
  I=len(elems)//len(K);d=len(K)//len(N)
  assert N<=K and len(K)%len(N)==0
  for base in CONFIG['bases']:
   adj,es=graph(base,mods,a,b);cs=directed_components(adj)
   assert len(cs)==I
   assert all(len(c)==len(base['T'])*len(K) and per==d for c,per in cs)
   for i in range(len(base['T'])):
    for j,r in enumerate(es):
     old=add(r,mul(-base['c'][i],D,mods),mods)
     for dest in adj[i*len(es)+j]:
      ii,jj=divmod(dest,len(es));new=add(es[jj],mul(-base['c'][ii],D,mods),mods)
      assert add(add(new,neg(old,mods),mods),neg(a,mods),mods) in N
   cases+=1;vertices+=len(adj)
print('General finite-abelian covers passed:',cases,flush=True)

X,Y,Z=4777,6444,7444
assert -3*X+8*Y-5*Z==1 and gcd(Y-X,Z-X)==1
records=[]
for m in list(range(1,81))+[125,128]:
 I=gcd(m,9554000);per=m*gcd(m,2)//I
 Iold=gcd(m*m,m*X,2*m*Y,2*m*Z,2*X*(Z-Y))
 h=gcd(m,2*(Z-Y));g=gcd(m,2*(m//h)*(Y-X));pold=g//gcd(g,X)
 assert (I,per)==(Iold,pold)
 base=CONFIG['bases'][0];adj,es=graph(base,(m,m),(X,X),(Y,Z));cs=directed_components(adj)
 assert len(cs)==I and all(len(c)==5*m*m//I and p==per for c,p in cs)
 if gcd(m,X*(Z-Y))==1 and m>1:
  for r,s in es:
   phase=lambda r,s:pow(X,-1,m)*(r-(Y-X)*pow(Z-Y,-1,m)*(s-r))%m
   for da,db in [(X,X),(Y,Z)]:assert (phase((r+da)%m,(s+db)%m)-phase(r,s))%m==1
 J=gcd(m,4777000);pcounter=m//J
 adj_counter,es0=graph({'T':[0],'S':[0]},(m,m),(X,X),(Y,Z))
 cc=directed_components(adj_counter)
 assert len(cc)==J and all(len(c)==m*m//J and pp==pcounter for c,pp in cc)
 records.append({'m':m,'components':I,'period':per,'states':len(adj),'counter_only_components':J,'counter_only_period':pcounter})
print('Concrete all-moduli boundary controls passed:',len(records),flush=True)

# Smith normal form and exact spectral/gauge controls.
import sympy as sp
from sympy.matrices.normalforms import smith_normal_form
M=sp.Matrix([[X,2*Y],[X,2*Z]]);SNF=smith_normal_form(M,domain=sp.ZZ)
assert abs(SNF[0,0])==1 and abs(SNF[1,1])==9554000
fourier={}
for m in [11,13,19]:
 critical=[(j,k) for j,k in product(range(m),repeat=2) if 2*(j*(Y-X)+k*(Z-X))%m==0]
 assert len(critical)==m
 assert all(j!=0 and k!=0 for j,k in critical if (j,k)!=(0,0))
 fourier[str(m)]=critical
assert set(fourier['11'])=={(j,j) for j in range(11)}
# Exact minimum modulus for irreducible, periodic joint cover and two aperiodic scalar covers.
valid_m=[m for m in range(2,81) if gcd(m,9554000)==1 and gcd(m,3334)==gcd(m,5334)==1]
assert min(valid_m)==11
# The observation hierarchy is cumulative; pair counts alone do not include actor counts.
a=sp.Symbol('a',real=True);T=CONFIG['bases'][0]['T'];S=CONFIG['bases'][0]['S'];c=CONFIG['bases'][0]['c']
P=sp.zeros(5)
for i in range(5):P[i,T[i]]+=a;P[i,S[i]]+=1-a
pi=sp.Matrix([[sp.Rational(5,17),sp.Rational(7,34),sp.Rational(5,34),sp.Rational(1,17),sp.Rational(5,17)]])
assert pi*P.subs(a,sp.Rational(2,5))==pi
# The cyclic phase classes modulo eleven each have stationary mass 1/11.
for t in range(11):
 assert sum(pi[i]/121 for i in range(5) for r,s in product(range(11),repeat=2) if 2*(r+s)%11==t)==sp.Rational(1,11)

# Exact algebra, all order-two subsequences and UT4 word order.
U=sp.Matrix([[1,0,0],[-3,8,-5],[1,-3,2]])
assert U.det()==1 and U*sp.Matrix([X,Y,Z])==sp.Matrix([4777,1,333])
assert U.inv()==sp.Matrix([[1,0,0],[1,2,5],[1,3,8]])
A,B,C=[sp.eye(4) for _ in range(3)]
A[0,1]=X;B[1,2]=Y;C[2,3]=Z
comm=lambda A,B:A*B*A.inv()*B.inv()
assert comm(comm(A,B),C)==sp.eye(4)+X*Y*Z*sp.eye(4)[:,0]*sp.eye(4)[3,:]
words=['XYZYX','YXZXY']
def counts(w,k):return Counter(''.join(w[i] for i in inds) for inds in combinations(range(len(w)),k))
assert counts(words[0],1)==counts(words[1],1) and counts(words[0],2)==counts(words[1],2)
assert [counts(w,3)['XYZ'] for w in words]==[1,0]
mat=[]
for w in words:
 v=sp.eye(4)
 for q in w:v=v*{'X':A,'Y':B,'Z':C}[q]
 mat.append(v)
assert mat[0]-mat[1]==X*Y*Z*sp.eye(4)[:,0]*sp.eye(4)[3,:]
assert counts('X',2)==counts('Y',2) and counts('X',1)!=counts('Y',1)
# Weighted UT4 matrices are conjugate over Q to the standard Parikh generators.
Dmat=sp.diag(X*Y*Z,Y*Z,Z,1)
for matrix,(i,j) in zip([A,B,C],[(0,1),(1,2),(2,3)]):
 target=sp.eye(4);target[i,j]=1
 assert Dmat.inv()*matrix*Dmat==target
# At fixed length, the first collision of total value and actor counts is length 2667.
assert -1000*X+2667*Y-1667*Z==0 and -1000+2667-1667==0
assert gcd(1000,2667,1667)==1
L=lcm(X,Y,Z);assert L==57287140668 and X*Y*Z==4*L
moments=[X**n+Y**n+Z**n for n in range(13)]
H=sp.Matrix(3,3,lambda i,j:moments[i+j]);assert H.det()==19765929000321000000
assert all(moments[n+3]==18665*moments[n+2]-114312112*moments[n+1]+229148562672*moments[n] for n in range(10))

# FST-09 full exact fibres, multiplicities, and the new optimal recorder.
def val7(n):
 a=0
 while n%7==0:a+=1;n//=7
 return a,n

def Cpath(m,r,A=343,A0=None,Q=9,size=None):
 if r==0:return m if size is None else size
 A0=8*m if A0 is None else A0;size=m if size is None else size
 ar=A**r;B=(ar-1)*A0//Q
 assert (ar-1)*A0%Q==0
 return (B+size-1)//ar-(B-1)//ar

def logfloor(n,b):
 r=0
 while b**(r+1)<=n:r+=1
 return r
fst=[]
for ell in CONFIG['FST_full_enumeration_ell']:
 m=10**ell;fibres=Counter();seen_extra=set()
 for s in range(m):
  K=8*m-9*s;a,H0=val7(K);fibres[H0]+=1
  r={8:0,5:1,2:2}[H0%9];j=a//3
  assert a==r+3*j and 7**(r+3*j)*H0==K
  if j:
   assert (H0,j) not in seen_extra;seen_extra.add((H0,j))
  assert 0<=j<1+logfloor(m,343)
 multiplicities=Counter(fibres.values());fmax=max(fibres.values())
 assert len(fibres)==m-Cpath(m,1)
 assert fmax==1+logfloor(m,343) and fibres[8]==fmax
 for r in range(fmax+2):assert Cpath(m,r)==sum(max(f-r,0)*n for f,n in multiplicities.items())
 for f in range(1,fmax+2):assert multiplicities[f]==Cpath(m,f-1)-2*Cpath(m,f)+Cpath(m,f+1)
 fst.append({'ell':ell,'suffixes':m,'classes':len(fibres),'maximum_fibre':fmax,'optimal_recorder_values':fmax,'multiplicities':dict(multiplicities)})
print('FST full enumerations and optimal recorder passed.',flush=True)
precision=[]
for ell in CONFIG['FST_modular_precision_ell']:
 m=10**ell;kmin=1
 while 7**kmin<m:kmin+=1
 for n in CONFIG['FST_n']:
  for k in sorted({max(1,kmin-1),kmin}):
   signatures=set();q=7**k;inv=pow(144*10**(n+ell),-1,q)
   for s in range(m):
    a,H0=val7(8*m-9*s);u=H0*inv%q;signatures.add((a,u))
    if q>=m:
     hh=(144*10**(n+ell)*u)%q;rec=(8*m-7**a*hh)*pow(9,-1,7**(k+a))%(7**(k+a))
     assert rec==s
   assert (len(signatures)==m)==(q>=m)
   precision.append({'ell':ell,'n':n,'k':k,'injective':len(signatures)==m})
P02=13841287201;assert P02==7**12
for ell in CONFIG['FST_02_brute_ell']:
 m=10**ell;M=m//100;A0=8*m-18;cnt=Counter(val7(A0-900*t)[1] for t in range(M))
 assert len(cnt)==M-Cpath(m,1,P02,A0,900,M)
 assert len(cnt)==M
restricted=[]
for ell in range(2,21):
 m=10**ell;M=m//100;lost=Cpath(m,1,P02,8*m-18,900,M)
 assert (lost>0)==(ell>=13)
 restricted.append({'ell':ell,'classes_lost':lost})
 if ell>=13:
  for K in [782,782*P02]:
   s=(8*m-K)//9;assert 8*m-9*s==K and 0<=s<m and s%100==2 and val7(K)[1]==782
assert [r['classes_lost'] for r in restricted if r['ell'] in [13,14,15]]==[7,72,723]
with localcontext() as ctx:
 ctx.prec=60
 entropy=(Decimal(342)/343)**2*sum(Decimal(f)*(Decimal(f).ln()/Decimal(2).ln())/(Decimal(343)**(f-1)) for f in range(2,40))
 entropy_string=str(entropy)
 assert abs(entropy-Decimal('0.0058373324'))<Decimal('0.00000000005')

result={'config':CONFIG,'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'general_finite_abelian':{'cases':cases,'vertices':vertices,'passed':True},
 'concrete_joint':records,'Smith_form':[list(map(int,SNF.row(i))) for i in range(2)],
 'mixed_critical_characters':fourier,'minimum_marginal_mixing_joint_clock_modulus':min(valid_m),'optimal_FST_recorder':fst,'FST_precision_checks':precision,
 'restricted_02':restricted,'entropy_approximation_bits':entropy_string,
 'observer_definition_counterexample':{'histories':['X','Y'],'same_pair_counts':True,'different_actor_counts':True},
 'algebra_passed':True,'seconds':time.monotonic()-start,'sympy_version':sp.__version__}
(ROOT/'EXACT_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print('PASS. General graphs',cases,'visited vertices',vertices,'concrete joint graphs',len(records))
print('FST optimal recorder:',fst)
print('Entropy approximation:',entropy_string)
