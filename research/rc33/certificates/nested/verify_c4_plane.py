#!/usr/bin/env python3
"""Separate exact derivation: 4(D-Q)=3C at 119772/r3, all heights.

Uses explicit independent integer polynomials, not the generic rotated solver.
"""
from fractions import Fraction as F
from math import gcd,lcm,isqrt
from functools import reduce
from pathlib import Path
import json
out=Path(__file__).resolve().parent
candidates=set();pairs=0
for J in range(-359,-98):
    for K in range(-68,-37):
        pairs+=1;U=-3072-4*K;V=320-3*K;L=24*J
        a=216*U*U-4*K*L*L
        b=432*U*V-(256+3*K)*L*L
        c=216*V*V-216*L*L
        assert a!=0
        disc=b*b-4*a*c
        if disc<0:continue
        sq=isqrt(disc)
        if sq*sq!=disc:continue
        for y in [F(-b+sq,2*a),F(-b-sq,2*a)]:
            if not 1<y<F(5,4):continue
            c0=(U*y+V)/L;d=y+F(3,4)
            # Rotated coordinates (Anew,Cnew,Dnew,Qnew)=(Cold,Aold,Dold,Qold).
            if not y/2<c0<min(F(2,3),d/3):continue
            v=[c0,F(1),d,y];den=lcm(*(x.denominator for x in v));v=[int(x*den) for x in v];g=reduce(gcd,v);v=tuple(x//g for x in v)
            candidates.add(v)
assert candidates=={(406,712,1265,731)},candidates
A,C,D,Q=next(iter(candidates));R1=16*(D*D-9*Q*Q)-9*A*A;R2=27*(A*A-C*C)-32*C*Q
assert R1%(A*Q)==0 and 2*R2%(D*Q)==0
res={'plane':'4(D-Q)=3C','level_pairs':pairs,'high_rational_candidates':[list(x) for x in sorted(candidates)],'known_levels':[R1//(A*Q),2*R2//(D*Q)],'coordinate_cutoff':None,'implementation':'separate explicit integer quadratic elimination'}
(out/'C4_PLANE_SEPARATE_CHECK.json').write_text(json.dumps(res,indent=2));print(json.dumps(res,indent=2))
