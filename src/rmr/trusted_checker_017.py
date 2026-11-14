#!/usr/bin/env python3
from fractions import Fraction
from math import gcd, lcm

B0=88_011_536_665_779
M=223_336_848_698_040
F=[Fraction(406,731),Fraction(712,731),Fraction(712,1265),Fraction(1218,1265),Fraction(406,557)]
TM=[1,0,3,2,4]
SM=[4,2,1,0,0]

def T(B,x):
    y=B*x
    return y-(y.numerator//y.denominator)

def S(B,x):
    z=(1-x)/x
    return 1/(1+T(B,z))

assert M==lcm(731,712,1265,1218,406,557)
assert len(set(F))==5 and all(Fraction(1,2)<x<1 for x in F)
for t in range(1001):
    B=B0+t*M
    assert [T(B,x) for x in F]==[F[j] for j in TM]
    assert [S(B,x) for x in F]==[F[j] for j in SM]
    assert [gcd(x.denominator,B) for x in F]==[1,1,1,1,1]
    assert [gcd(x.numerator,B) for x in F]==[1,1,1,3,1]
    for start in range(5):
        seen={start};todo=[start]
        while todo:
            i=todo.pop()
            for j in (TM[i],SM[i]):
                if j not in seen:
                    seen.add(j);todo.append(j)
        assert len(seen)==5
assert SM.count(0)==2 and 3 not in SM
print('PASS')
print('counterfamily_bases_checked=1001')
print('five_state_closed_SCC=PASS')
print('unique_strict_edge=S3:x3->x0')
print('S_permutation=FALSE')
print('five_state_nonpermutation_family=PASS')
