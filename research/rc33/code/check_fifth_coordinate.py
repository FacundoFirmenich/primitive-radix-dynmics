"""Exact finite leaves of the fifth-coordinate nonabsorption theorem.

The proof reduces E|lcm(A,C,D,Q) in the five declared chambers to four
small divisor lists or the bounded integer levels KE=-69..69, JE=1..99.
This is exhaustive on those reductions, not a coordinate-height scan.
The final coordinate caps assume B below the known fibre's least base;
they are search bounds, not claims of coverage or minimum-base proofs.
"""
from fractions import Fraction as F
from math import gcd, isqrt, lcm
from pathlib import Path
import hashlib
import json
import sympy as sp

R = Path(__file__).resolve().parents[1]
OUT = R / 'results/fifth_coordinate_checks.json'


def rational_sqrt(x):
    if x < 0:
        return None
    n, d = isqrt(x.numerator), isqrt(x.denominator)
    return F(n, d) if n*n == x.numerator and d*d == x.denominator else None


def run():
    # Native 606897 -> reflected completion order (A,C,D,Q)=(q,d,c,a).
    a,c,d,q = sp.symbols('a c d q')
    native = [(a,d*d-q*q),(c,d*d-9*q*q),
              (d,c*c-a*a),(q,c*c-9*a*a)]
    A,C,D,Q = q,d,c,a
    reflected = [(A,D*D-9*Q*Q),(C,D*D-Q*Q),
                 (D,C*C-9*A*A),(Q,C*C-A*A)]
    assert reflected == list(reversed(native))
    known_core = (406,712,1265,731)
    known_E, known_B = 557, 88_011_536_665_779
    known_L = lcm(*known_core)
    known_lambda = known_E//gcd(known_E,known_L)
    assert known_lambda == 557 and (known_B*known_B-1)%(known_lambda*known_L)==0
    small = []
    for r, t in [(2, 4), (3, 3), (3, 4), (3, 5)]:
        examined, retained = [], []
        for Q in sp.divisors(t*t-4):
            for A in range(Q//2+1, Q):
                if t*A % 2:
                    continue
                C = 2*Q-F(t*A, 2)
                E = A+Q-C
                D = r*E-A
                examined.append([A, int(Q)])
                if (max(A, F(r*A, 2)) < C < Q < 2*A and
                        r*A < D < 2*C and A < E < 2*A):
                    retained.append(list(map(str, [A, C, D, Q, E])))
        assert not retained
        small.append({'r': r, 't': t, 'examined_pairs': examined,
                      'retained': retained})
    assert [len(x['examined_pairs']) for x in small] == [9, 1, 9, 8]

    # Derive the two integral levels and their cancellation from the formulas.
    A, C, D, Q, KE, JE = sp.symbols('A C D Q K_E J_E')
    kn = (4*C-Q)*(4*C-3*Q)-16*A*A
    jn = 100*A*A-100*C*C+120*A*Q+35*Q*Q
    d = 10*A+6*Q-12*C
    assert sp.rem(sp.expand(d*d-9*Q*Q-9*kn), A, A) == 0
    assert sp.rem(sp.expand(jn-(d*d-Q*Q)), C, C) == 0
    assert sp.expand(25*kn+4*jn-(-400*C*Q+480*A*Q+215*Q*Q)) == 0
    assert F(16*F(5,3)**2+16*2*F(5,3)+12+16, F(11,6)) < 70
    assert F(100-225+240+140, F(3,2)*F(11,6)) < 100
    assert 100-100*F(5,3)**2+120*F(11,6) > 0

    points = set()
    survivors = []
    records = []
    for k in range(-69, 70):
        for j in range(1, 100):
            u, v = F(480-25*k,400+4*j), F(215,400+4*j)
            assert F(1,4) < v < F(3,4)
            aa = 16*v*v-16*v+3
            bb = 32*u*v-16*u-k
            cc = 16*u*u-16
            assert aa != 0
            sq = rational_sqrt(bb*bb-4*aa*cc)
            if sq is None:
                continue
            for y in {(-bb+sq)/(2*aa), (-bb-sq)/(2*aa)}:
                c = u+v*y
                assert (16*c*c-16*c*y+3*y*y-16) == k*y
                assert (100-100*c*c+120*y+35*y*y) == j*c*y
                points.add((c,y))
                d = 10+6*y-12*c
                e = (d+2)/3
                if F(3,2) < c < y < 2 and 3 < d < 2*c and 1 < e < 2:
                    survivors.append([k,j,str(c),str(y)])
                records.append({'K_E':k,'J_E':j,'C_over_A':str(c),'Q_over_A':str(y)})
    assert len(points) == 989 and not survivors
    # Evaluate exact integer caps for B<R, with the strict inequalities retained.
    base_limit = 88_011_536_665_779
    upper = (base_limit-1)**2-1
    caps = []
    for branch, coefficient, expected in [
            ('119772/r2/j-1',F(81,4),4422456),
            ('119772/r2/j1',F(6),5994210),
            ('119772/r3/j1_or_j2',F(27,4),5820279),
            ('606897/r3/native_Q',F(27,16),8231118)]:
        h = isqrt(isqrt((upper*coefficient.denominator)//coefficient.numerator))
        while coefficient*(h+1)**4 < upper:
            h += 1
        while coefficient*h**4 >= upper:
            h -= 1
        assert h == expected and coefficient*(h+1)**4 >= upper
        caps.append({'branch':branch,'coefficient':str(coefficient),
                     'last_possible_coordinate':h,'base_assumption':f'2<=B<{base_limit}',
                     'coverage_of_search_interval':'NOT_CLAIMED'})
    result = {'status':'PASS_EXACT_FINITE_LEAVES_OF_NONABSORPTION',
              'native_reflected_coefficients':'PASS: (1,3,1,3) -> (3,1,3,1)',
              'known_carrier_lambda':known_lambda,
              'small_cases':small,'level_pairs':139*99,
              'distinct_rational_points_before_chamber':989,
              'chamber_survivors':survivors,'coordinate_caps':caps,
              'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'scope':'Five residual completion chambers, including reflected 606897. No uniform lambda bound or global minimum base.',
              'review':'self-review; named source verifier was not supplied; the finite leaves were reconstructed here'}
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(result,indent=2)+'\n')
    (R/'results/fifth_coordinate_rational_points.json').write_text(json.dumps(records,indent=2)+'\n')
    print('PASS: fifth-coordinate nonabsorption; 27 small pairs and 13,761 exact level pairs; 989 rational points, zero in chamber')


if __name__ == '__main__':
    run()
