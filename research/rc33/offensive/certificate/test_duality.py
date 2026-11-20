from pathlib import Path
from fractions import Fraction as F
from math import gcd,lcm
import json,time
from half_duality import T,S,psi,dual_base_fibre,transfer_r3
from fibre_arithmetic import ROOT

print('BEFORE: exact dimensionless rational identities for Psi(x)=1/(2x); q=2..50, q/2<p<q, B=2..15. Positive closed controls: B=13, F={3/4}; B=211, F={5/8,7/8}; its dual {4/5,4/7}. Mixed-denominator negative control: B=41,F={3/4,3/5}. The two known nonpermutation carriers are retained as valid carriers and tested only for dual admissibility.',flush=True)
tic=time.monotonic();identities=0;high_identities=0
for q in range(2,51):
    for p in range(q//2+1,q):
        x=F(p,q)
        for B in range(2,16):
            eps=(B/x).__floor__()%2
            assert T(psi(x),B)==psi(S(x,B))-F(1-eps,2)
            identities+=1
            if F(1,2)<T(x,B)<1:
                assert S(psi(x),B)==psi(T(x,B));high_identities+=1

examples=[]
for base,states,period,expected in [(13,(F(3,4),),12,True),(211,(F(5,8),F(7,8)),280,True),(211,(F(4,5),F(4,7)),280,True),(41,(F(3,4),F(3,5)),60,False)]:
    assert all(T(x,base) in states and S(x,base) in states for x in states)
    gate=dual_base_fibre(states,base,period)
    assert gate['tests'][0]['admissible']==expected
    examples.append(dict(base=base,states=list(map(str,states)),period=period,gate=gate))

known=[]
for fixture in json.loads((ROOT/'CORE_GATE_RESULTS.json').read_text())['positive_controls']:
    r=fixture['r'];A,C,D,Q,E=fixture['coordinates_ACDQE'];B,L=fixture['full_base']
    print('NONPERMUTATION_CONTROL_INPUT',dict(r=r,A=A,C=C,D=D,Q=Q,E=E,B=B,L=L),flush=True)
    states=(F(A,Q),F(C,Q),F(C,D),F(r*A,D),F(A,E))
    digits=[(B*(1/x-1)).__floor__() for x in states]
    j=(r*E-D)//A
    assert r*(digits[4]-digits[3])==j*B
    gate=dual_base_fibre(states,B,L)
    assert not gate['fibres']
    known.append(dict(r=r,j=j,base=B,period=L,S_digits=digits,
                      digit_difference=digits[4]-digits[3],gate=gate,
                      original_carrier_still_valid=True))
    if r==3:
        assert j==1 and B%6==3 and (digits[4]-digits[3])%2==1
        assert not transfer_r3('normal',(A,C,D,Q),E,B,L)['transfers']

result=dict(status='PASS',rational_identity_cases=identities,high_intertwining_cases=high_identities,positive_and_negative_closed_controls=examples,known_nonpermutation_controls=known,seconds=time.monotonic()-tic,scope='Elementary identities and the stated parity criterion. No j=2 nonpermutation positive witness is claimed.')
(ROOT/'DUALITY_TEST_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print('DUALITY_TEST_PASS',dict(identity_cases=identities,high_cases=high_identities,seconds=result['seconds']),flush=True)
