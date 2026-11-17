#!/usr/bin/env python3
"""Track arithmetic memory of complement mutations and true projective return."""
from fractions import Fraction as F
from pathlib import Path
from math import gcd
from functools import reduce
import json

R=Path(__file__).resolve().parent
def vp(n,p):
    if n==0:return None
    n=abs(n);v=0
    while n%p==0:n//=p;v+=1
    return v
def vf(x,p):return vp(x.numerator,p)-vp(x.denominator,p)
def complement(x,co):
    return [abs((a*a*x[(i+1)%4]**2-b*b*x[(i-1)%4]**2)/x[i]) for i,(a,b) in enumerate(co)]
co119=[(3,1),(1,1),(1,1),(3,1)];x=list(map(F,[406,731,712,1265]))
y=complement(x,co119);z=complement(y,co119)
assert all(a.denominator==1 for a in y)
assert vf(y[0],3)==vf(y[3],3)==0 and vf(y[1],3)>0 and vf(y[2],3)>0
assert vf(z[1],3)<0 and vf(z[2],3)<0
first=[vf(a,3) for a in y];second=[vf(a,3) for a in z]
# Verify the unit-square local input for both strict primes over prime powers.
local=[]
for p,m in [(2,256),(3,81)]:
    vals=[i for i in range(1,m) if i%p]
    lower=3 if p==2 else 1;count=0
    for a in vals:
        for b in vals:
            if a==b:continue
            if a*a==b*b:continue
            assert vp(a*a-b*b,p)>=lower;count+=1
    local.append({'prime':p,'unit_residue_representatives_below':m,'difference_checks':count,'required_min_valuation':lower})
# Known genuine strict TSTS cycle: projective return with nonzero content memory.
B=88011536665779;A,C,D,Q=406,712,1265,731
at=(B*A-C)//Q;ct=(B*C-3*A)//D;ub=(B*Q-D)//C;ud=(B*D-3*Q)//(3*A)
def mm(a,b):return [[sum(a[i][k]*b[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
T=lambda k:[[B,-k],[0,1]]
S=lambda u:[[1,0],[-u,B]]
M=mm(S(ud),mm(T(ct),mm(S(ub),T(at))));vec=[A,Q]
assert [sum(M[i][j]*vec[j] for j in range(2)) for i in range(2)]==[3*A,3*Q]
hist=[];v=vec[:]
for n in range(1,5):
    v=[sum(M[i][j]*v[j] for j in range(2)) for i in range(2)]
    assert F(*v)==F(A,Q) and v==[3**n*A,3**n*Q]
    hist.append({'returns':n,'same_projective_state':True,'removed_content':3**n,'v3_content':n})
res={'global_lemma':'A full parallel quadratic-complement step charges two coordinates at the strict prime, while two remain units; a second step has strict-prime denominators. No primitive normalization makes the first step an all-unit core.','r119_valuation_pattern':'(0,a,b,0), a,b>=1 (>=3 at r=2)','r606_valuation_pattern':'(a,0,0,b), a,b>=1','known_core_first_v3':first,'known_core_second_v3':second,'local_checks':local,'true_cycle_helical_control':hist,'scope':'obstruction to these descent maps, not impossibility of a genuine finite projective component','global_height_bound_obtained':False}
(R/'HELICAL_LIFT_RESULTS.json').write_text(json.dumps(res,indent=2));print(json.dumps(res,indent=2))
