from pathlib import Path
import subprocess,random,json,math,time
import sympy as sp
from index_geometry import make_packet,recover,F,BRANCHES
R=Path(__file__).resolve().parent

def scan(params,box):
 raw=' '.join(map(str,[*params,*box]))+'\n'
 p=subprocess.run([str(R/'square_levels')],input=raw,text=True,capture_output=True);assert p.returncode==0,p.stderr
 hs=set();counts=None
 for row in p.stdout.splitlines():
  a=row.split()
  if a[0]=='H':hs.add(tuple(map(int,a[1:])))
  elif a[0]=='C':counts=list(map(int,a[1:]))
 assert counts is not None
 return hs,counts
if __name__=='__main__':
 print('BEFORE exact dimensionless C++/GMP quadratic-square filter; random.Random seed=20261120; 100 signed coefficient fixtures; K,J=-10..10. Known carriers from CORE_GATE_RESULTS.json; full input coordinates follow.',flush=True)
 rng=random.Random(20261120);total=0
 for _ in range(100):
  while True:
   u=rng.randint(1,15);v,w,P,h,z=[rng.randint(-15,15) for _ in range(5)];U=P*w+u*z
   if U:break
  ps=[u,v,w,P,h,z];hs,counts=scan(ps,[-10,11,-10,11]);want=set()
  for K in range(-10,11):
   V=u*h-P*K
   for J in range(-10,11):
    W=u*J-P*v;al=u*U*U+v*U*W+w*W*W
    q=(v*v-4*u*w)*V*V-2*K*(2*u*U+v*W)*V+K*K*W*W+4*u*al
    if q>=0 and math.isqrt(q)**2==q:want.add((K,J))
  assert hs==want,(ps,hs^want);assert counts[0]==441;total+=441
 fixtures=json.loads((R/'CORE_GATE_RESULTS.json').read_text())['positive_controls'];controls=[]
 for fx in fixtures:
  r=fx['r'];A,C,D,Q,E=fx['coordinates_ACDQE'];j=(r*E-D)//A;L=E//math.gcd(E,math.lcm(A,C,D,Q));kap=L*abs(j)*(Q-j*(C-A))//E
  print('POSITIVE_INPUT',dict(r=r,A=A,C=C,D=D,Q=Q,E=E,j=j,lam=L,kappa=kap),flush=True)
  branch=next(b for b,rr,jj in BRANCHES if rr==r and jj==j and not b.startswith('606'))
  p=make_packet(L,branch,r,j,kap);u,v,w,P,h,z=p['params']
  K=F(u*(C*C-A*A)+v*C*Q+w*Q*Q,A*Q);J=F(P*(A*A-C*C)+h*A*Q+z*Q*Q,C*Q);assert K.denominator==J.denominator==1
  K=int(K);J=int(J);hs,ct=scan(p['params'],[K-1,K+2,J-1,J+2]);assert (K,J) in hs
  rs=recover(p,K,J);assert any(q['core']==[A,C,D,Q,E] and q['realizations'] for q in rs)
  controls.append(dict(r=r,L=L,K=K,J=J,core=[A,C,D,Q,E],tile_pairs=ct[0],recovered=True))
 u,v,w,U,V,W,K=sp.symbols('u v w U V W K');a=u*U**2+v*U*W+w*W**2;b=2*u*U*V+v*V*W-K*W**2;c=u*(V**2-W**2)
 q=(v*v-4*u*w)*V**2-2*K*(2*u*U+v*W)*V+K**2*W**2+4*u*a
 assert sp.expand(b*b-4*a*c-W*W*q)==0
 out=dict(status='PASS',signed_coefficient_pairs=total,positive_carriers=controls,symbolic_discriminant_factorization=True,mods=[16,7,11,13,17,19,23],scope='Exact square filter and two full ten-edge positive controls; not a global scan.')
 (R/'SQUARE_LEVEL_TESTS.json').write_text(json.dumps(out,indent=2)+'\n');print('PASS',json.dumps(out),flush=True)
