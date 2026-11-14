"""Exact chamber adjudication for five factor-three oriented rows."""
import json
from fractions import Fraction as F
from math import gcd, isqrt, lcm

from sympy import Poly, divisors, resultant, symbols

from verify_oriented_predecessors import fibre_coordinates, records

A, C, D, x = symbols("A C D x")
Q = 3*A-C
ARCHIVE = {row["normal_form"]:row["graph"] for row in records()}


def graph_check(number, expected_p, expected_q):
    t, s, letter, source, factor = ARCHIVE[f"DF015-{number:04d}"]
    if letter == 1:
        t, s = s, t
    assert factor == 3
    p, offset = fibre_coordinates(s,None,3,0)
    q, _ = fibre_coordinates(t,source,3,offset)
    assert tuple(p[i][0] for i in range(5)) == expected_p
    assert tuple(q[i][0]-offset for i in range(5)) == expected_q
    assert [i for i in range(5) if q[i][1]==3] == [source]


def congruence_identity(numerator, modulus, cycle):
    variable = modulus
    restriction = numerator.subs(variable,0)
    multiple = cycle.subs(variable,0)
    v = next(v for v in (A,C,D) if multiple.has(v))
    if not Poly(restriction,v).rem(Poly(multiple,v)).is_zero:
        raise ArithmeticError((numerator,modulus,cycle))


def two_cycle_cases():
    graph_check(6,(0,1,1,0,1),(0,0,1,2,2))
    graph_check(16,(0,1,1,0,1),(0,0,1,2,2))
    numerator = A*A-C*C+D*D
    congruence_identity(numerator,A,D*D-Q*Q)
    congruence_identity(numerator,D,C*C-A*A)
    lower_c = F(9,5)
    upper = (1-lower_c**2+4)/lower_c
    assert upper == F(44,45) < 1
    return {"forms":[6,16],"upper_bound":str(upper)}


def cubic_t_cases():
    graph_check(8,(0,1,0,1,2),(0,0,1,1,1))
    graph_check(18,(0,1,0,2,1),(0,0,1,1,1))
    first=81*A*A+C*C-D*D
    second=81*A**3-A*D*D-81*C**3+81*C*D*D
    for modulus,cycle in ((A,D*D-Q*Q),(C,D*D-9*Q*Q),(D,C**3-A**3)):
        if modulus != D:
            congruence_identity(first,modulus,cycle)
        congruence_identity(second,modulus,cycle)
    chamber_count=0
    checked=0
    zero=[]
    core=[]
    for k in range(41,45):
        # y*d = K - L*c, with 9/5<c<2 and 9/5<d<2.
        K,L = 6561+k,81*k+1
        ymin = int(min(F(K-L*c,d) for c in (F(9,5),2) for d in (F(9,5),2)))-1
        ymax = int(max(F(K-L*c,d) for c in (F(9,5),2) for d in (F(9,5),2)))+1
        for y in range(ymin,ymax+1):
            checked+=1
            if y==0:
                cs = [F(K,L)]
            else:
                cs = rational_roots(L*L-y*y, -2*K*L+k*y*y, K*K-81*y*y)
            for c in cs:
                d2=81+c*c-k*c
                if not F(9,5)<c<2 or d2<=0:
                    continue
                if y:
                    ds=[(K-L*c)/y]
                else:
                    ds=rational_roots(d2.denominator,0,-d2.numerator)
                for d in ds:
                    if not c<d<2 or d*d!=d2 or not F(3,2)*(3-c)<c:
                        continue
                    chamber_count+=1
                    a=lcm(c.denominator,d.denominator)
                    cc,dd,qq=int(a*c),int(a*d),int(a*(3-c))
                    if gcd(a,qq)!=1 or gcd(a,dd)!=1 or gcd(cc,dd)!=1 or gcd(cc,3*qq)!=1:
                        continue
                    if ((dd*dd-qq*qq)%a or (dd*dd-9*qq*qq)%cc or (cc**3-a**3)%dd):
                        continue
                    core.append([a,cc,dd,qq,k,y])
    return {"forms":[8,18],"quotient_pairs":checked,
            "chamber_points":chamber_count,"cores":core}


def rational_roots(a,b,c):
    if a==0:
        if b==0:
            if c==0:
                raise ArithmeticError("Positive-dimensional fibre")
            return []
        return [F(-c,b)]
    delta=b*b-4*a*c
    if delta<0:
        return []
    h=isqrt(delta)
    return sorted({F(-b-h,2*a),F(-b+h,2*a)}) if h*h==delta else []


def rectangle_17():
    graph_check(17,(0,1,1,2,2),(0,0,1,1,0))
    # A now denotes state 1's numerator. Its S cycle has length two.
    checked=0
    survivors=[]
    for k in range(44,62):
        constant=int(resultant(x*x-1,x*x+k*x+81,x))
        assert constant
        for a in divisors(abs(constant)):
            if a%3==0:
                continue
            for q in range(a+1,(6*a-1)//5+1):
                if q%3==0 or gcd(a,q)!=1:
                    continue
                c=3*a-q
                for d in rational_roots(1,-k*c,72*c*c-18*c*q-9*q*q):
                    checked+=1
                    if d.denominator!=1 or not c<d<2*a:
                        continue
                    d=int(d)
                    if d%3==0 or gcd(d,a*c)!=1:
                        continue
                    if (d*d-q*q)%a == (d*d-9*q*q)%c == (c*c-a*a)%d == 0:
                        survivors.append([a,c,d,q,k])
    return {"forms":[17],"quadratic_roots":checked,"cores":survivors}


if __name__ == "__main__":
    print(json.dumps([two_cycle_cases(),cubic_t_cases(),rectangle_17()],indent=2))
