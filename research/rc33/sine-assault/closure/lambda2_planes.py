"""All-height rational-plane test for the possible completion index lambda=2."""
from fractions import Fraction as F
from math import gcd,lcm,isqrt
from pathlib import Path
import json,platform
R=Path(__file__).resolve().parent
print(json.dumps({'equations':['lambda=E/gcd(E,lcm(A,C,D,Q))','D=a*A+b*Q+c*C','A|D^2-9Q^2,C|D^2-Q^2,D|C^2-9A^2,Q|C^2-A^2'],
 'variables':{'q':'Q/A','s':'C/A','K,J':'integral quadratic levels'},'units':'dimensionless exact rational/integer','python':platform.python_version(),
 'planes':[{'branch':'reflected606897/3','a':5,'b':6,'c':-6,'q_bounds':['11/12','1'],'s_bounds':['3/2','19/12']},{'branch':'119772/3,j2','a':22,'b':12,'c':-24,'q_bounds':['3/2','2'],'s_bounds':['3/2','43/24']}]}),flush=True)
def add(x,y):return x[0]+y[0],x[1]+y[1]
def scale(k,x):return (k*x[0],k*x[1]) if k>=0 else (k*x[1],k*x[0])
def mul(x,y):
 v=[a*b for a in x for b in y];return min(v),max(v)
def div(x,y):assert y[0]>0;return mul(x,(1/y[1],1/y[0]))
def rational_roots(a,b,c):
 if a==0:
  if b:return [-F(c,b)]
  if c:return []
  raise ArithmeticError('identically zero polynomial: unresolved component')
 disc=b*b-4*a*c
 if disc<0:return []
 t=isqrt(disc)
 return list({F(-b+t,2*a),F(-b-t,2*a)}) if t*t==disc else []
results=[]
for branch,a,b,c,qlo,qhi,slo,shi in [('reflected606897/3',5,6,-6,F(11,12),F(1),F(3,2),F(19,12)),('119772/3,j2',22,12,-24,F(3,2),F(2),F(3,2),F(43,24))]:
 coeff=[c*c,2*b*c,b*b-9];g=1
 while all(x%(3*g)==0 for x in coeff):g*=3
 u,v,w=[x//g for x in coeff];P,H,Z=a*a,2*a*b,b*b-1
 q=(qlo,qhi);s=(slo,shi);q2=mul(q,q);s2=mul(s,s);sq=mul(s,q)
 K=div(add(add(scale(u,add(s2,(-F(1),-F(1)))),scale(v,sq)),scale(w,q2)),q)
 J=div(add(add(scale(P,add((F(1),F(1)),scale(-1,s2))),scale(H,q)),scale(Z,q2)),sq)
 ks=range(K[0].__floor__()+1,K[1].__ceil__());js=range(J[0].__floor__()+1,J[1].__ceil__())
 all_roots=chamber=primitive=full=0;hits=[];zeros=[]
 for k in ks:
  for j in js:
   U=P*w+u*Z;V=u*H-P*k;W=u*j-P*v
   assert W!=0,(branch,k,j)
   aa=u*U*U+v*U*W+w*W*W;bb=2*u*U*V+v*V*W-k*W*W;cc=u*(V*V-W*W)
   try:roots=rational_roots(aa,bb,cc)
   except ArithmeticError:zeros.append([k,j]);continue
   for y in roots:
    all_roots+=1;x=(U*y+V)/W
    assert u*(x*x-1)+v*x*y+w*y*y==k*y
    assert P*(1-x*x)+H*y+Z*y*y==j*x*y
    d=a+b*y+c*x;e=(1+d)/3 if branch.startswith('reflected') else (2+d)/3
    if not(qlo<y<qhi and slo<x<shi):continue
    if branch.startswith('reflected'):
     if not F(3,2)<d<x<2*y<2:continue
    if not branch.startswith('reflected') and not(F(3,2)<x<y<2 and 3<d<2*x and 1<e<2):continue
    chamber+=1
    vals=[F(1),x,d,y,e];m=lcm(*(t.denominator for t in vals));A,C,D,Q,E=[int(t*m) for t in vals]
    if any(gcd(i,jj)!=1 for i,jj in [(A,Q),(A,D),(A,E),(C,Q),(C,D)]) or any(t%3==0 for t in [A,C,D,Q,E]):continue
    primitive+=1
    if any(n%mod for mod,n in [(A,D*D-9*Q*Q),(C,D*D-Q*Q),(D,C*C-9*A*A),(Q,C*C-A*A)]):continue
    full+=1;lam=E//gcd(E,lcm(A,C,D,Q));hits.append(dict(core=[A,C,D,Q,E],lambda_value=lam,k=k,j=j))
 assert not zeros,zeros
 results.append(dict(branch=branch,plane=[a,b,c],level_coefficients=[u,v,w,P,H,Z],K_interval=list(map(str,K)),J_interval=list(map(str,J)),K_integer_range=[ks.start,ks.stop-1],J_integer_range=[js.start,js.stop-1],level_pairs=len(ks)*len(js),rational_roots=all_roots,chamber_roots=chamber,primitive_roots=primitive,four_square_roots=full,candidates=hits,positive_dimensional_components=zeros))
print(json.dumps(results,indent=2),flush=True)
(R/'LAMBDA2_RESULTS.json').write_text(json.dumps({'status':'PASS','results':results,'scope':'Exact finite rational-plane classification, all heights; no global classification beyond the specified lambda2 planes.'},indent=2)+'\n')
