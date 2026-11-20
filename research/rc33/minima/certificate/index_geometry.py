"""Exact all-height enumeration at fixed completion index, by rational levels."""
from fractions import Fraction as F
from itertools import combinations
from math import gcd,lcm,isqrt
from pathlib import Path
import argparse,json,time
R=Path(__file__).resolve().parent
def roots(a,b,c):
 m=lcm(a.denominator,b.denominator,c.denominator);a,b,c=[int(t*m) for t in [a,b,c]]
 if a==0:
  if b:return {-F(c,b)}
  if c:return set()
  return None
 d=b*b-4*a*c
 if d<0:return set()
 t=isqrt(d)
 return {F(-b+t,2*a),F(-b-t,2*a)} if t*t==d else set()
def plus(x,y):return x[0]+y[0],x[1]+y[1]
def times(x,y):
 a=[u*v for u in x for v in y];return min(a),max(a)
def scaled(k,x):return (k*x[0],k*x[1]) if k>=0 else (k*x[1],k*x[0])
def divided(x,y):assert y[0]>0;return times(x,(1/y[1],1/y[0]))
def line(a,b,c):return list(map(F,[a,b,c]))
def linplus(x,y):return [a+b for a,b in zip(x,y)]
def linscale(k,x):return [k*a for a in x]
def value(row,q,s):return row[0]+row[1]*q+row[2]*s
BRANCHES=[('119772/2/j-1',2,-1),('119772/2/j1',2,1),('119772/3/j1',3,1),('119772/3/j2',3,2),('606897/3/reflected',3,1)]

def make_packet(L,branch,r,j,kap):
 if kap==L*abs(j):return None
 a=j*(r*L*abs(j)-kap);b=r*L*abs(j);c=-j*b;den=kap
 g=gcd(gcd(abs(a),abs(b)),gcd(abs(c),den));a//=g;b//=g;c//=g;den//=g
 d=line(F(a,den),F(b,den),F(c,den));e=linscale(F(1,r),linplus(d,line(j,0,0)))
 if branch.startswith('606'):
  inequalities=[linplus(d,line(-F(3,2),0,0)),linplus(line(0,0,1),linscale(-1,d)),line(0,2,-1),line(1,-1,0),linplus(e,line(-F(5,6),0,0)),linplus(line(1,0,0),linscale(-1,e))]
 else:
  inequalities=[line(0,1,-1),line(2,-1,0),line(-1,0,1),line(-F(r,2),0,1),linplus(d,line(-r,0,0)),linplus(line(0,0,2),linscale(-1,d)),linplus(e,line(-1,0,0)),linplus(line(2,0,0),linscale(-1,e))]
 if any(row==[0,0,0] for row in inequalities):return None
 vertices=set()
 for x,y in combinations(inequalities,2):
  det=x[1]*y[2]-x[2]*y[1]
  if not det:continue
  q=(x[2]*y[0]-x[0]*y[2])/det;s=(x[0]*y[1]-x[1]*y[0])/det
  if all(value(row,q,s)>=0 for row in inequalities):vertices.add((q,s))
 if len(vertices)<3:return None
 if not any((v[0]-u[0])*(w[1]-u[1])!=(v[1]-u[1])*(w[0]-u[0]) for u,v,w in combinations(vertices,3)):return None
 qbox=(min(v[0] for v in vertices),max(v[0] for v in vertices));sbox=(min(v[1] for v in vertices),max(v[1] for v in vertices))
 assert qbox[0]>0 and sbox[0]>0
 coeff=[c*c,2*b*c,b*b-r*r*den*den];g=1
 while all(t%(r*g)==0 for t in coeff):g*=r
 u,v,w=[F(t//g) for t in coeff];P,h,z=map(F,[a*a,2*a*b,b*b-den*den])
 sq=times(sbox,qbox);ss=times(sbox,sbox);qq=times(qbox,qbox)
 KB=divided(plus(plus(scaled(u,plus(ss,(-F(1),-F(1)))),scaled(v,sq)),scaled(w,qq)),qbox)
 JB=divided(plus(plus(scaled(P,plus((F(1),F(1)),scaled(-1,ss))),scaled(h,qbox)),scaled(z,qq)),sq)
 return dict(lambda_value=L,branch=branch,r=r,j=j,kappa=kap,plane=[a,b,c,den],d=list(map(str,d)),e=list(map(str,e)),inequalities=[list(map(str,row)) for row in inequalities],q_box=list(map(str,qbox)),s_box=list(map(str,sbox)),params=list(map(int,[u,v,w,P,h,z])),K_range=[KB[0].__ceil__(),KB[1].__floor__()+1],J_range=[JB[0].__ceil__(),JB[1].__floor__()+1])

def packets(L):
 out=[];symbolic=[]
 for branch,r,j in BRANCHES:
  if gcd(r,L)>1:
   symbolic.append(dict(branch=branch,reason='lambda divides E and gcd(r,E)=1',lambda_value=L));continue
  for kap in range(1,6*L):
   p=make_packet(L,branch,r,j,kap)
   if p is not None:out.append(p)
 return out,symbolic

def recover(p,K,J):
 u,v,w,P,h,z=map(F,p['params']);U=P*w+u*z;V=u*h-P*K;W=u*J-P*v;assert U!=0
 if W:
  rr=roots(u*U*U+v*U*W+w*W*W,2*u*U*V+v*V*W-K*W*W,u*(V*V-W*W));assert rr is not None
  candidates=[(q,(U*q+V)/W) for q in rr]
 else:
  q=-V/U;rr=roots(u,v*q,w*q*q-u-K*q);assert rr is not None
  candidates=[(q,s) for s in rr]
 out=[];r=p['r'];j=p['j'];L=p['lambda_value']
 for q,s in candidates:
  assert u*(s*s-1)+v*s*q+w*q*q==K*q and P*(1-s*s)+h*q+z*q*q==J*s*q
  inequalities=[list(map(F,row)) for row in p['inequalities']]
  if not all(value(row,q,s)>0 for row in inequalities):continue
  dr=value(list(map(F,p['d'])),q,s);er=value(list(map(F,p['e'])),q,s)
  nums=[F(1),s,dr,q,er];scale=lcm(*(t.denominator for t in nums));A,C,D,Q,E=[int(t*scale) for t in nums]
  if any(gcd(i,t)!=1 for i,t in [(A,Q),(A,D),(A,E),(C,Q),(C,D)]) or any(t%r==0 for t in [A,C,D,Q,E]):continue
  if (r-1)%gcd(A,C) or (r-1)%gcd(D,Q):continue
  if any(n%mod for mod,n in [(A,D*D-r*r*Q*Q),(C,D*D-Q*Q),(D,C*C-r*r*A*A),(Q,C*C-A*A)]):continue
  if E//gcd(E,lcm(A,C,D,Q))!=L:continue
  from fibre_arithmetic import complete
  orientation='reflected' if p['branch'].startswith('606') else 'normal'
  hits=[x for x in complete(r,(A,C,D,Q),orientation) if x['E']==E]
  out.append(dict(core=[A,C,D,Q,E],K=K,J=J,realizations=hits))
 return out
