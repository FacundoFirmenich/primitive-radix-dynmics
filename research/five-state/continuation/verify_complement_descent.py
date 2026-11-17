"""Exhaust the unweighted opposite-pair divisor-complement moves."""

import json
from functools import lru_cache
from math import gcd

from sympy import divisors

from verify_exceptional_crt import ACTIONS, edge_certificate, states_for
from verify_square_cycle_fibres import roots


@lru_cache(maxsize=32768)
def positive_divisors(n):
    return tuple(map(int, divisors(abs(n)))) if n else ()


def congruent_in_range(residue, modulus, low, high):
    """Integers congruent to residue in [low,high)."""
    return range(low+(residue-low)%modulus,high,modulus)


def cores_at_coordinate(station, x, code, factor, scales):
    alpha,beta,gamma,delta = scales
    if station == "D":
        d = x
        for a in range(d//4+1,d):
            if gcd(a,d) != 1 or a % factor == 0:
                continue
            for root in roots(d):
                c = gamma*a*root % d
                for q in positive_divisors(c*c-delta*delta*a*a):
                    yield a,c,d,q
    elif station == "Q":
        q = x
        for a in range(q//2+1,q):
            if gcd(a,q) != 1 or a % factor == 0:
                continue
            for root in roots(q):
                c = delta*a*root % q
                if code == 606897:
                    c += q
                for d in positive_divisors(c*c-gamma*gamma*a*a):
                    yield a,c,d,q
    elif station == "A":
        a = x
        for q in range(a+1,2*a):
            if gcd(a,q) != 1 or q % factor == 0:
                continue
            for root in roots(a):
                for d in congruent_in_range(alpha*q*root % a,a,a+1,4*a):
                    for c in positive_divisors(d*d-beta*beta*q*q):
                        yield a,c,d,q
    else:
        c = x
        for d in range(c+1,2*c):
            if gcd(c,d) != 1 or d % factor == 0:
                continue
            for root in roots(c):
                for q in congruent_in_range(d*pow(beta,-1,c)*root % c,c,c//2+1,2*c):
                    for a in positive_divisors(d*d-alpha*alpha*q*q):
                        yield a,c,d,q


def square_core(core,code,r,scales):
    a,c,d,q = core
    alpha,beta,gamma,delta = scales
    if min(core) < 2 or gcd(r,a*c*d*q) != 1:
        return False
    if code == 119772:
        if not (a < c < q < 2*a and r*a < d < 2*c):
            return False
    elif not (3*q < 2*c < 2*d < 4*a < 4*q):
        return False
    return (gcd(a,q) == gcd(c,q) == gcd(a,d) == gcd(c,d) == 1
            and (r-1) % gcd(a,c) == (r-1) % gcd(d,q) == 0
            and (d*d-alpha*alpha*q*q) % a == (d*d-beta*beta*q*q) % c == 0
            and (c*c-gamma*gamma*a*a) % d == (c*c-delta*delta*a*a) % q == 0)


def replay():
    control = (406, 712, 1265, 731, 557)
    if (
        not square_core(control[:4], 119772, 3, (3, 1, 3, 1))
        or edge_certificate(states_for(119772, 3, *control), *ACTIONS[119772], 3)
        != (88011536665779, 223336848698040)
    ):
        raise ArithmeticError("The known five-state realization did not reproduce")
    results = []
    for code,r in ((119772,2),(119772,3),(606897,3)):
        scales = (r,1,r,1) if code == 119772 else (1,3,1,3)
        alpha,beta,gamma,delta = scales
        # If both retained moduli were even, both replacement moduli
        # would also be even, violating adjacent coprimality.
        moves = {
            "AC": (("D",beta**4-(alpha*gamma)**4),("Q",1-delta**4)),
            "AC_swap": (("D",alpha**4-beta**4),),
            "DQ": (("A",1-alpha**4),("C",gamma**4-(beta*delta)**4)),
            "DQ_swap": (("C",gamma**4-delta**4),),
        }
        for move, tests in moves.items():
            constraints = {station: abs(constant) for station, constant in tests if constant}
            station = min(constraints,key=constraints.get)
            cores = {
                core for value in positive_divisors(constraints[station]) if value > 1 and value % r
                for core in cores_at_coordinate(station,value,code,r,scales)
                if square_core(core,code,r,scales)
                and (gcd(core[2],core[3]) if move.startswith("AC") else gcd(core[0],core[1])) == 1
                and all(bound % core["ACDQ".index(key)] == 0 for key,bound in constraints.items())
            }
            results.append({
                "code":code,"factor":r,"move":move,"constraints":constraints,
                "source_cores":sorted(cores),
            })
    return results


if __name__ == "__main__":
    print(json.dumps(replay(),indent=2))
