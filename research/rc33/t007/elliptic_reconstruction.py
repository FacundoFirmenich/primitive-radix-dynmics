from pathlib import Path
from math import gcd
import json,time,sympy as s
from sympy.matrices.normalforms import hermite_normal_form
R=Path(__file__).resolve().parent
N=486350841114209042571600;L=581981400;a0=397929094518522627660600
CONF={'units':'exact projective arithmetic over finite fields','curve_parameter':17,'curve':'68A^3-34A^2(w+z)+17Azw-20A^2w-340A^2z+24Aw^2+148Awz+24Az^2-4(z^3+w^3)','origin':[0,1,-1],'P':[64233,11741,1138],'R':[1,2,2],'primes_max':199,'curve_and_point_source':'archived RGPHI_ARTICLE_EN.tex elliptic-frontier theorem and positive-rank proposition; O is its specified rational point','expected_HNF':[[N,a0],[0,L]]}
print('CONFIGURATION BEFORE COMPUTATION\n'+json.dumps(CONF,indent=2),flush=True)
def F(P,p):
 A,z,w=P;return (68*A**3-34*A*A*(w+z)+17*A*z*w-20*A*A*w-340*A*A*z+24*A*w*w+148*A*w*z+24*A*z*z-4*(z**3+w**3))%p

def grad(P,p):
 A,z,w=P
 return ((204*A*A-108*A*w-748*A*z+24*w*w+165*w*z+24*z*z)%p,(-374*A*A+165*A*w+48*A*z-12*z*z)%p,(-54*A*A+165*A*z+48*A*w-12*w*w)%p)

def norm(P,p):
 for a in P:
  if a%p:
   v=pow(a%p,-1,p);return tuple(x*v%p for x in P)
 raise ValueError('zero projective point')

def cross(P,Q,p):return ((P[1]*Q[2]-P[2]*Q[1])%p,(P[2]*Q[0]-P[0]*Q[2])%p,(P[0]*Q[1]-P[1]*Q[0])%p)
def third(P,Q,p):
 if P!=Q:
  c1=sum(a*b for a,b in zip(grad(P,p),Q))%p;c2=sum(a*b for a,b in zip(grad(Q,p),P))%p
  out=norm(tuple(c2*a-c1*b for a,b in zip(P,Q)),p)
 else:
  line=grad(P,p)
  for e in [(1,0,0),(0,1,0),(0,0,1)]:
   raw=cross(line,e,p)
   if raw!=(0,0,0):
    Q=norm(raw,p)
    if Q!=P:break
  c2=sum(a*b for a,b in zip(grad(Q,p),P))%p;c3=F(Q,p)
  out=norm(tuple(-c3*a+c2*b for a,b in zip(P,Q)),p)
 assert F(out,p)==0,(p,P,Q,out)
 return out

def add(P,Q,O,p):return third(third(P,Q,p),O,p)
A,z,w=s.symbols('A z w');expr=68*A**3-54*A*A*w-374*A*A*z+165*A*z*w+24*A*w*w+24*A*z*z-4*z**3-4*w**3
partials=[s.diff(expr,v) for v in (A,z,w)]
rows=[];bad=[];missing=[];B=s.eye(2);start=time.monotonic()
for p in list(s.primerange(2,200)):
 if p in [2,3]:bad.append(p);continue
 smooth=True
 for var,others in [(A,(z,w)),(z,(A,w)),(w,(A,z))]:
  gb=s.groebner([f.subs(var,1) for f in partials],*others,modulus=p)
  if list(gb)!=[1]:smooth=False;break
 if not smooth:bad.append(p);continue
 O=norm((0,1,-1),p);P=norm((64233,11741,1138),p);Q=norm((1,2,2),p)
 assert F(O,p)==F(P,p)==F(Q,p)==0
 group_count=sum(F((1,a,b),p)==0 for a in range(p) for b in range(p))+sum(F((0,1,b),p)==0 for b in range(p))+(F((0,0,1),p)==0)
 cur=O;log=None;order=None
 for j in range(group_count+1):
  if cur==Q:log=j
  if j and cur==O:order=j;break
  cur=add(cur,P,O,p)
 assert order and group_count%order==0,(p,group_count,order)
 if log is None:missing.append({'p':p,'order_P':order,'curve_points':group_count});continue
 row=(s.Matrix([[1,log]])*B);r1,r2=map(int,row);g=gcd(r1,order);height=g//gcd(g,r2);mod=order//g
 x=(-r2*height//g*pow(r1//g,-1,mod))%mod if mod>1 else 0
 B=hermite_normal_form(B*s.Matrix([[mod,x],[0,height]]))
 rows.append({'p':p,'curve_points':group_count,'order_P':order,'log_R_base_P':log})
 print('local',p,group_count,order,log,flush=True)
out={'status':'PASS','configuration':CONF,'local_constraints':rows,'good_primes_without_log':missing,'bad_primes':bad,'computed_HNF':[[int(x) for x in row] for row in B.tolist()],'matches_supplied_lattice':B==s.Matrix([[N,a0],[0,L]]),'runtime_seconds':time.monotonic()-start}
(R/'ELLIPTIC_RECONSTRUCTION.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
