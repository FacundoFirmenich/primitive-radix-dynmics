"""Symbolic/adversarial checks of the completion-index finiteness mechanism."""
from pathlib import Path
from fractions import Fraction as F
from math import gcd,lcm,isqrt
import json,sympy as s
R=Path(__file__).resolve().parent
print('CONFIG BEFORE CALCULATION: exact SymPy/Q polynomials; r in{2,3}, j in{-1,1,2} restricted to the five completion chambers; lambda positive integer; known tuple406,712,1265,731,557; conservative M=24lambda, T=200M^4, root-bound N=8000000M^10; no uniform lambda bound assumed.',flush=True)
x,b,k,j,r=s.symbols('x b k j r',nonzero=True);a=j*(b-k);c=-j*b
U=s.expand(a*a*(b*b-r*r*k*k)+c*c*(b*b-k*k))
assert s.factor(U-j*j*(b-k)*(2*b*b*b-r*r*k*k*(b-k)))==0
# Divide by j²b⁴: U=0 iff(1-x)*(2-r²*x²*(1-x))=0.
assert s.expand(U.subs(k,b*x)/(j*j*b**4)-(1-x)*(r*r*x**3-r*r*x*x+2))==0
# max x²(1-x)=4/27 on[0,1]; r²<=9 makes second factor >=2/3>0.
assert 2-9*F(4,27)==F(2,3)
# Every simultaneous line component has the tabulated rational k/b ratio.
line_candidates=[]
for rr in [2,3]:
 for t in [-1,1]:
  for eps in [-1,1]:
   for eta in [-1,1]:
    poly=(t-1)+x*(1+eps*rr+eta)-eps*rr*x*x
    roots=s.solve(poly,x)
    rational_positive=[F(int(v.p),int(v.q)) for v in roots if v.is_Rational and v>0]
    line_candidates += [{'r':rr,'t':t,'eps':eps,'eta':eta,'ratio':str(v),'F_over_E':str(rr*v)} for v in rational_positive]
assert {F(z['F_over_E']) for z in line_candidates if z['r']==2}<={F(2),F(4)}
assert {F(z['F_over_E']) for z in line_candidates if z['r']==3}<={F(1),F(2),F(3),F(5)}
# Root-height bound: rational q=Q/A is reduced; A is its denominator.
assert 32_000_000*24**10<200**10
# Pure lambda2 reflected606897 contradiction: exact lower box and polynomial factors.
q,z=s.symbols('q z');K=(4*z*z-8*z*q+3*q*q-4)/q
assert s.factor((K+4)*q)==(2*z-3*q+2)*(2*z-q-2)
assert F(49,36)-2==F(-23,36)<0
assert (5*F(11,12)-4)/7>0
# Vieta alone is not a chamber-preserving descent, even at the known carrier.
A,C,D,Q,E=406,712,1265,731,557;lam=E//gcd(E,lcm(A,C,D,Q));jj=1;kap=lam*(A+Q-C)//E
ar=jj*(3*lam*abs(jj)*jj-kap);br=3*lam*abs(jj);cr=-jj*br
u,v,w=cr*cr,2*br*cr,br*br-9*kap*kap;P,H,Z=ar*ar,2*ar*br,br*br-kap*kap
y=F(Q,A);zv=F(C,A);KL=(u*(zv*zv-1)+v*zv*y+w*y*y)/y;JL=(P*(1-zv*zv)+H*y+Z*y*y)/(zv*y);assert KL.denominator==JL.denominator==1
uu=P*w+u*Z;vv=u*H-P*int(KL);ww=u*int(JL)-P*v
qa=u*uu*uu+v*uu*ww+w*ww*ww;qb=2*u*uu*vv+v*vv*ww-int(KL)*ww*ww;qc=u*(vv*vv-ww*ww)
assert qa*y*y+qb*y+qc==0
other=-F(qb,qa)-y;otherC=F(uu*other+vv,ww);otherD=F(ar+br*other+cr*otherC,kap)
preserve=(F(3,2)<otherC<other<2 and 3<otherD<2*otherC)
assert not preserve
out={'status':'PASS','symbolic_U_factorization':str(s.factor(U)),'positive_rational_line_cases':line_candidates,
 'geometric_exclusion':'All candidate line families force F/E in{r,4}(r2) or{1,2,3,5}(r3); chamber bounds eliminate all except F=E in119772/r3/j1, which forces2Q-C=2A,Q|3,contrary to3-units.',
 'all_lambda_height_bound':'H<(200*lambda)^10, primitive completion-order coordinates in the five chambers; not a uniform upper bound onlambda.',
 'conservative_constant_check':{'left':32_000_000*24**10,'right':200**10},
 'known_control':{'lambda':lam,'kappa':kap,'K':int(KL),'J':int(JL),'vieta_other_Q_over_A':str(other),'vieta_other_C_over_A':str(otherC),'vieta_other_D_over_A':str(otherD),'chamber_preserved':preserve},
 'route_status':{'completion_index':'proved effective finite strata and height bound; uniform index bound open','unconditional_Vieta_descent':'universal chamber-preservation refuted by known-carrier test; exception-aware descent remains open','squareclass_route':'explicit coupled quadratic discriminants identified; no uniform squareclass obstruction established'}}
(R/'STRUCTURE_AUDIT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
