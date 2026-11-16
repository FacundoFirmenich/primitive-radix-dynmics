#!/usr/bin/env python3
"""Exact joint-fiber discriminator and additional h=1 replay.

Identifiability here is of a declared rational relaxation. No measure or
physical integration transition is postulated.
"""
from pathlib import Path
from math import gcd
from itertools import combinations
import json,hashlib,sys,datetime,sympy as s
from nested_strata import run_stratum
R=Path(__file__).resolve().parent
inputs=[Path(__file__),R/'nested_strata.py',R/'nested_planes.py',R/'NESTED_STRATA_RESULTS.json']
before={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs}
pure=[run_stratum(code,r,1) for code,r in [(119772,2),(119772,3),(606897,3)]]
assert sum(len(x['planes']) for x in pure)==9
assert all(x['all_nondegenerate'] and not x['realizations'] for x in pure)
assert all(not p['primitive_square_cores'] for x in pure for p in x['planes'])
(R/'PURE_SIGN_NESTED_REPLAY.json').write_text(json.dumps(pure,indent=2))
x,y,z=s.symbols('x y z');J=(9-9*x*x+24*y-128*y*y)/(x*y);K=2*(27*(x*x-1)-32*y)/((y+s.Rational(3,4))*y)
pt={x:s.Rational(203,356),y:s.Rational(731,712)}
assert J.subs(pt)==-178 and K.subs(pt)==-56
Jac=s.Matrix([[s.diff(J,x),s.diff(J,y)],[s.diff(K,x),s.diff(K,y)]]).subs(pt)
assert Jac.det()!=0
q1=-9*x*x-128*y*y+178*x*y+24*y*z+9*z*z;q2=54*x*x+56*y*y-22*y*z-54*z*z
det1=s.hessian(q1,(x,y,z)).det();det2=s.hessian(q2,(x,y,z)).det()
assert det1!=0 and det2!=0
rows=json.loads((R/'NESTED_STRATA_RESULTS.json').read_text())
names=['strict_prime_unit','gcd_AQ','gcd_QC','gcd_CD','gcd_DA','overlap_AC','overlap_DQ','square_A','square_C','square_D','square_Q']
critical=[];summary={}
for code,r in [(119772,2),(119772,3),(606897,3)]:
    cores=sorted(set(tuple(c) for row in rows if (row['code'],row['r'])==(code,r) for p in row['planes'] for c in p['high_candidates']))
    clauses=set()
    for a,c,d,q in cores:
        if (code,r,a,c,d,q)==(119772,3,406,712,1265,731):continue
        al,be,ga,de=(r,1,r,1) if code==119772 else (1,3,1,3)
        passes=[gcd(r,a*c*d*q)==1,gcd(a,q)==1,gcd(q,c)==1,gcd(c,d)==1,gcd(d,a)==1,(r-1)%gcd(a,c)==0,(r-1)%gcd(d,q)==0,(d*d-al*al*q*q)%a==0,(d*d-be*be*q*q)%c==0,(c*c-ga*ga*a*a)%d==0,(c*c-de*de*a*a)%q==0]
        mask=sum((not good)<<i for i,good in enumerate(passes));assert mask;clauses.add(mask)
    best=[]
    for n in range(1,len(names)+1):
        for ids in combinations(range(len(names)),n):
            mask=sum(1<<i for i in ids)
            if all(mask&clause for clause in clauses):best.append([names[i] for i in ids])
        if best:break
    critical.append({'code':code,'r':r,'minimum_postfilter_predicates':n,'minimum_sets':best})
    if (code,r)==(119772,3):
        uu={p for p in cores if gcd(3,p[0]*p[1]*p[2]*p[3])==1}
        aa={p for p in cores if (p[2]*p[2]-9*p[3]*p[3])%p[0]==0}
        assert len(cores)==1254 and len(uu)==172 and len(aa)==53 and uu&aa=={(406,712,1265,731)}
        summary={'all':len(cores),'strict_prime_unit':len(uu),'square_A':len(aa),'joint':len(uu&aa),'joint_core':[406,712,1265,731]}
res={'local_geometric_fiber':{'relaxation':'C4 cofactor plane; rational points in the open chamber','known_levels':[-178,-56],'Jacobian':str(Jac),'Jacobian_determinant':str(Jac.det()),'rank':2,'individual_projective_conic_hessian_determinants':[str(det1),str(det2)],'interpretation':'Each individual known level is a smooth rational conic; joint levels are transverse locally. Global finite exhaustion uses the earlier integer-level bounds, not the Jacobian alone.'},'postfilter_counts_119772_r3':summary,'minimum_joint_postfilters':critical,'cofactor_one_replay_planes':9,'cofactor_one_replay_realizations':0,'scope':'Postfilters on generated cofactor<=14 candidate fibers. Conditions used in generating the fibers are not removed. No probability or physical transition is inferred.'}
(R/'JOINT_FIBER_ATTACK_RESULTS.json').write_text(json.dumps(res,indent=2))
after={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs};assert before==after
(R/'JOINT_FIBER_RUN_MANIFEST.json').write_text(json.dumps({'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'argv':sys.argv,'input_hashes_before':before,'input_hashes_after':after,'status':'PASS_SCOPED_JOINT_FIBER_AND_H1_REPLAY'},indent=2))
print(json.dumps(res,indent=2))
