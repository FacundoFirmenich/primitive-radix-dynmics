from pathlib import Path
from fractions import Fraction as F
from math import gcd,lcm,isqrt,prod
from collections import Counter
from functools import lru_cache
from sympy import factorint
import json
ROOT=Path(__file__).resolve().parent
DATA=json.loads((ROOT/'CANDIDATE_DIAGNOSTIC.json').read_text())
SEEDS=[tuple(x['common_core']) for x in next(r for r in DATA['diagnostics'] if r['code']==606897)['coprime_quadratic_near_misses']]
class ArithmeticDeferred(Exception):pass
@lru_cache(maxsize=100000)
def prime(n):
 n=int(n)
 if n<2:raise ArithmeticDeferred('Invalid prime factor')
 if n<100000:
  if any(n%d==0 for d in range(2,isqrt(n)+1)):raise ArithmeticDeferred('Composite factor')
  return True
 factors={int(p):int(e) for p,e in factorint(n-1).items()}
 if prod(p**e for p,e in factors.items())!=n-1:raise ArithmeticDeferred('Incomplete n-1 factorization')
 for p in factors:prime(p)
 for p in factors:
  if not any(pow(a,n-1,n)==1 and gcd(pow(a,(n-1)//p,n)-1,n)==1 for a in range(2,66)):
   raise ArithmeticDeferred('No Lucas certificate in declared base range for '+str(n))
 return True
def chamber(r,x,kind='reflected'):
 A,C,D,Q=x
 return 3*A<2*D<2*C<4*Q<4*A if kind=='reflected' else A<C<Q<2*A and r*A<D<2*C
def primitive(r,x):
 A,C,D,Q=x
 return gcd(r,A*C*D*Q)==1 and all(gcd(u,v)==1 for u,v in [(A,Q),(Q,C),(C,D),(D,A)]) and (r-1)%gcd(A,C)==0 and (r-1)%gcd(D,Q)==0
def rem(r,x):
 A,C,D,Q=x
 return [(D*D-r*r*Q*Q)%A,(D*D-Q*Q)%C,(C*C-r*r*A*A)%D,(C*C-A*A)%Q]
def divisors(r,x,node):
 A,C,D,Q=x
 lo,hi=[(D-r*Q,D+r*Q),(D-Q,D+Q),(C-r*A,C+r*A),(C-A,C+A)][node]
 if not lo or not hi:raise ArithmeticDeferred('Zero quadratic numerator: unbounded fibre')
 factors=Counter()
 for v in [lo,hi]:
  ff={int(p):int(e) for p,e in factorint(abs(v)).items()}
  if prod(p**e for p,e in ff.items())!=abs(v):raise ArithmeticDeferred('Incomplete factorization')
  for p in ff:prime(p)
  factors.update(ff)
 vals=[1]
 for p,e in sorted(factors.items()):vals=[a*p**k for a in vals for k in range(e+1)]
 assert len(vals)==prod(e+1 for e in factors.values())
 return vals
def merge(rows):
 a,m=0,1
 for b,n in rows:
  g=gcd(m,n)
  if (b-a)%g:return None
  nn=n//g;k=((b-a)//g*pow(m//g,-1,nn))%nn if nn>1 else 0
  a=(a+m*k)%lcm(m,n);m=lcm(m,n)
 return a,m
def complete(r,x,kind='reflected'):
 A,C,D,Q=x;out=[]
 for j in ([1] if kind=='reflected' else ([-1,1] if r==2 else [1,2])):
  if (D+j*A)%r:continue
  E=(D+j*A)//r
  if not (5*A<6*E<6*A if kind=='reflected' else A<E<2*A) or E==Q or gcd(E,r)>1:continue
  rows=[(E*pow(Q,-1,A)%A,A),(D*pow(Q,-1,C)%C,C),(r*A*pow(C,-1,D)%D,D),(C*pow(A,-1,Q)%Q,Q),(0,r),(1,E)]
  fibre=merge(rows)
  if not fibre:continue
  b,m=fibre;b=b if b>=2 else b+m
  raw=((Q,A),(Q,C),(D,C),(D,r*A),(E,A)) if kind=='reflected' else ((A,Q),(C,Q),(C,D),(r*A,D),(A,E))
  states=[F(p,q) for p,q in raw]
  assert len(set(states))==5 and all(F(1,2)<v<1 for v in states) and all(gcd(p,q)==1 for p,q in raw)
  tm,sm=(((4,2,1,0,0),(1,0,3,2,4)) if kind=='reflected' else ((1,0,3,2,4),(4,2,1,0,0)))
  for name,mapping in [('T',tm),('S',sm)]:
   for i,k in enumerate(mapping):
    p,q=raw[i];want=r if (name,i)==(('T',3) if kind=='reflected' else ('S',3)) else 1
    if name=='T':y=F((b*p)%q,q);delta=gcd(b,q)
    else:y=F(p,p+(b*(q-p))%p);delta=gcd(b,p)
    assert y==states[k] and delta==want
  out.append({'core':x,'E':E,'j':j,'base':b,'period':m})
 return out
def score(x):
 A,C,D,Q=x;qp=sum(v==0 for v in rem(3,x));cs=0
 if (A+D)%3==0:
  E=(A+D)//3;g=gcd(E,C*Q)
  cs=1+int(gcd(E,3)==1)+int(E!=Q)+int((A+Q-C)%g==0)+int(A-E>=5001)
 return qp,cs
