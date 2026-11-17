#!/usr/bin/env python3
"""Exact heuristic discriminators: positive nesting, mutations, branch digits."""
from pathlib import Path
from fractions import Fraction as F
from itertools import permutations
from math import gcd
from functools import reduce
import json,sympy as s
R=Path(__file__).resolve().parent
u,v,w,z,r,t=s.symbols('u v w z r t')
f119=(u+r*v)*(w+z)+u*v*w*z-(r-1)**2
f606=(u+v)*(3*w+z)+u*v*w*z-4
M119=s.Matrix([[u,0,1,-r],[0,-v,1,-1],[-r,1,w,0],[-1,1,0,-z]])
M606=s.Matrix([[-u,0,1,-1],[0,v,1,-3],[-1,1,-w,0],[-3,1,0,z]])
assert s.expand(M119.det()-f119)==s.expand(M606.det()-f606)==0
# This rational family has a valid real chamber and all four reduced
# quotient denominators growing; it is only a relaxed model.
vv=ww=zz=t;uu=s.factor((1-4*t*t)/(2*t+t**3))
yy=s.factor((uu+t)/(1-t*t));cc=s.factor(1+t*yy);dd=s.factor(2*yy-uu)
samples=[]
for n in [101,1001,10001]:
    tv=F(1,4)+F(1,n);uv=(1-4*tv*tv)/(2*tv+tv**3);yv=(uv+tv)/(1-tv*tv);cv=1+tv*yv;dv=2*yv-uv
    assert (uv+2*tv)*(2*tv)+uv*tv**3==1
    assert 1<cv<yv<2 and 2<dv<2*cv
    samples.append({'n':n,'positive_ratios':[str(uv),str(tv),str(tv),str(tv)],'reduced_denominators':[uv.denominator,tv.denominator,tv.denominator,tv.denominator],'arithmetic_status':'not claimed a core; shared denominators violate the coprime cofactor jurisdiction'})
# All-coordinate and partial divisor complements, with every relabelling.
X=[406,731,712,1265];co=[(3,1),(1,1),(1,1),(3,1)]
N=[a*a*X[(i+1)%4]**2-b*b*X[(i-1)%4]**2 for i,(a,b) in enumerate(co)]
mutation=[]
for mask in range(1,16):
    Y=[abs(N[i]//X[i]) if mask>>i&1 else X[i] for i in range(4)]
    g=reduce(gcd,Y);Y=[x//g for x in Y];valid=[]
    for perm in permutations(Y):
        if any(gcd(perm[i],perm[(i+1)%4])!=1 for i in range(4)):continue
        if all((a*a*perm[(i+1)%4]**2-b*b*perm[(i-1)%4]**2)%perm[i]==0 for i,(a,b) in enumerate(co)):valid.append(list(perm))
    mutation.append({'mask':mask,'new_primitive_coordinates':Y,'height':max(Y),'same_weighted_cycle_valid_relabellings':valid})
B,at,bt,ct,dt=s.symbols('B at bt ct dt');T=lambda k:s.Matrix([[B,-k],[0,1]]);S=lambda k:s.Matrix([[1,0],[1-B-k,B]])
W=S(dt)*T(ct)*S(bt)*T(at);ub=B+bt-1;ud=B+dt-1
trace=at*ct*ub*ud+B*(at+ct)*(ub+ud)+2*B*B
assert s.expand(s.trace(W)-trace)==0
a,c,d,q=406,712,1265,731;b=88011536665779
ar=F(b*a-c,q);cr=F(b*c-3*a,d);ur=F(b*q-d,c);vr=F(b*d-3*q,3*a)
assert all(x.denominator==1 for x in [ar,cr,ur,vr])
assert 3*(ar*cr*ur*vr+b*(ar+cr)*(ur+vr))==(b*b-3)**2
result={'positive_119_equation':str(f119),'positive_606_equation':str(f606),'determinants_verified':True,'relaxed_all_denominators_grow_family':{'u':str(uu),'Q_over_A':str(yy),'C_over_A':str(cc),'D_over_A':str(dd),'samples':samples},'mutation_checks':mutation,'branch_trace_formula':str(trace),'witness_trace_identity_pass':True,'height_bound_from_trace_alone':False}
(R/'NESTING_ROUTE_DISCRIMINATORS.json').write_text(json.dumps(result,indent=2));print('PASS exact identities; relaxed-model obstruction and mutation scope recorded')
