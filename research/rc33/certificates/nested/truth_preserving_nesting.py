#!/usr/bin/env python3
"""Discriminate positive nesting from arithmetic-preserving renormalisation."""
from fractions import Fraction as F
from math import gcd,lcm
from functools import reduce
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parent
good=[]
for n in range(10,501):
    v=F(2*(n+1),8*n+1);w=F(2*n+1,8*n+3);z=F(2*(n+2),8*n+5)
    u=(1-2*v*(w+z))/(w+z+v*w*z)
    assert (u+2*v)*(w+z)+u*v*w*z==1
    h=[q.denominator for q in [u,v,w,z]]
    if any(gcd(h[i],h[j])>1 for i in range(4) for j in range(i)):continue
    y=(u+v)/(1-v*z);c=1+z*y;d=2*y-u
    if not 1<c<y<2 or not 2<d<2*c:continue
    den=lcm(c.denominator,d.denominator,y.denominator)
    X=[den,int(c*den),int(d*den),int(y*den)];g=reduce(gcd,X);X=[t//g for t in X];a,c,d,q=X
    if any(not t%2 for t in X) or any(gcd(X[i],X[j])>1 for i in range(4) for j in range(i)):continue
    minus=[2*q-d,d-q,2*a-c,c-a];plus=[2*q+d,d+q,2*a+c,c+a];moduli=[a,c,d,q]
    for M,lo,hi,ratio in zip(moduli,minus,plus,[u,v,w,z]):
        assert F(lo,M)==ratio
        H=M//gcd(M,lo);assert H==ratio.denominator
        assert ((lo*hi)%M==0)==(hi%H==0)
    residual=[hi%H for hi,H in zip(plus,h)]
    good.append({'n':n,'positive_ratios':list(map(str,[u,v,w,z])),'cofactor_denominators':h,'core':X,'conjugate_factor_residues':residual,'full_square_conditions':not any(residual)})
assert len(good)==65 and not any(x['full_square_conditions'] for x in good)
example=next(x for x in good if x['n']==12)
assert example['core']==[532009,782693,1114047,904253]
res={'identity':'M=g*h, Lminus=g*k, gcd(k,h)=1 implies M | Lminus*Lplus iff h | Lplus','tested_family_n':[10,500],'all_unit_pairwise_coprime_chamber_cores':len(good),'full_square_cores':0,'explicit_relaxation_counterexample':example,'scope':'refutes sufficiency of the positive nested identity plus cofactor and coordinate coprimality; does not refute the actual arithmetic target','source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
(R/'TRUTH_PRESERVING_NESTING_RESULTS.json').write_text(json.dumps(res,indent=2));print(json.dumps(res,indent=2))
