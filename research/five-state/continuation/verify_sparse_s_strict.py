"""Finite resultant certificate for four sparse S-strict orientations."""

import json
from fractions import Fraction
from math import gcd

from sympy import Poly, Rational, ceiling, diff, divisors, factorint, floor, resultant, symbols

from verify_exceptional_crt import edge_certificate, merge_residues
from verify_catalogue_crosswalk import representative
from verify_oriented_predecessors import fibre_coordinates, records


X = symbols("X")
T = (2,3,0,1,4)
MAPS = {(2,4):(0,0,3,4,2), (2,12):(0,0,4,2,3),
        (3,8):(0,0,3,4,2), (3,18):(0,0,4,2,3)}


def bounded_quotients(r):
    d = r-(r-1)*X
    n = X**2+r*(r+1)*X
    lower = (r-1)*(d/4-n/d)
    upper = (r-1)*(1-n)/d
    # On the chamber n and n/d increase, and 1-n is negative and decreases.
    if diff(n,X).subs(X,Rational(1,2)) <= 0 or n.subs(X,Rational(1,2)) <= 1:
        raise ArithmeticError("Endpoint monotonicity hypotheses failed")
    minimum = lower.subs(X,Rational(r,2*r-1))
    maximum = upper.subs(X,Rational(1,2))
    return range(int(floor(minimum))+1, int(ceiling(maximum)))


def common_roots(first, second, modulus):
    progressions = [(0, 1)]
    for prime, exponent in factorint(modulus).items():
        prime, exponent = int(prime), int(exponent)
        if prime <= 3:
            roots = [i for i in range(prime) if not (first(i) % prime or second(i) % prime)]
        else:
            common = Poly(first.as_expr(), X, modulus=prime).gcd(
                Poly(second.as_expr(), X, modulus=prime)
            )
            roots = [int(root) % prime for root in common.ground_roots()]
        power = prime
        for _ in range(1, exponent):
            lifted = power * prime
            # At least one derivative is a unit, or all admissible lifts are retained.
            new = []
            for root in roots:
                constraints = [(int(poly(root))//power, int(poly.diff()(root)) % prime)
                               for poly in (first, second)]
                unit = next(((h,v) for h,v in constraints if v), None)
                digits = [(-unit[0]*pow(unit[1],-1,prime)) % prime] if unit else range(prime)
                for digit in digits:
                    if all((h+v*digit) % prime == 0 for h,v in constraints):
                        new.append(root+power*digit)
            roots, power = new, lifted
        progressions = [merge_residues((entry,(root,power)))
                        for entry in progressions for root in roots]
    return [root for root, _ in progressions]


def replay():
    campaigns = []
    for r in (2,3):
        core = set()
        runs = []
        d_ratio = r-(r-1)*X
        first = Poly(d_ratio**3-1, X)
        for k in bounded_quotients(r):
            second = Poly((r-1)*(X*X+r*(r+1)*X) + k*d_ratio, X)
            constant = int(resultant(first, second))
            if constant == 0:
                raise ArithmeticError("A common component needs separate adjudication")
            tested = 0
            for c in divisors(abs(constant)):
                for x_mod_c in common_roots(first, second, c):
                    for q in range(c+1,2*c):
                        tested += 1
                        if gcd(c,q) != 1:
                            continue
                        a = x_mod_c*q % c
                        d = r*q-(r-1)*a
                        if not (a < q < 2*a and r*a < d < 2*r*a and c < d < 2*c):
                            continue
                        if gcd(r,a*c*d*q) != 1 or gcd(a*c,d*q) != 1:
                            continue
                        if (c*c-a*a) % q or (c*c-r*r*a*a) % d or (d*d-q*q) % a:
                            continue
                        if (r-1)*(c*c-a*a-r*(r+1)*a*q) != k*q*d:
                            continue
                        core.add((a,c,d,q))
            runs.append({"quotient":k,"resultant":constant,"pairs_tested":tested})
        for (factor, index), s in MAPS.items():
            if factor != r:
                continue
            key = representative(T,s,1,1,r)[0]
            archived = next(row for row in records() if row["normal_form"] == f"DF015-{index:04d}")
            if key != representative(*archived["graph"])[0]:
                raise ArithmeticError("Certificate graph does not match archived normal form")
            p, offset = fibre_coordinates(s,1,r,0)
            q, _ = fibre_coordinates(T,None,r,offset)
            expected = ((0,1,0),(0,r,1),(1,1,0),(1,1,1),(1,1,2))
            if tuple((*p[i],q[i][0]-offset) for i in range(5)) != expected:
                raise ArithmeticError("Prescribed action graph does not induce the stated fibres")
            survivors = []
            checked = 0
            for a,c,d,q in sorted(core):
                for e in range(c+1,2*c):
                    pairs = ((a,q),(r*a,d),(c,q),(c,d),(c,e))
                    if len(set(pairs)) != 5 or any(gcd(p,v) != 1 for p,v in pairs):
                        continue
                    checked += 1
                    states = tuple(Fraction(p,v) for p,v in pairs)
                    result = edge_certificate(states, T, s, (1,1),r)
                    if result is not None:
                        survivors.append([[a,c,d,q,e], list(result)])
            campaigns.append({"factor":r,"form":f"DF015-{index:04d}","quotients":runs,
                              "core_coordinates":sorted(core),"crt_candidates":checked,
                              "realizations":survivors})
    return campaigns


if __name__ == "__main__":
    print(json.dumps(replay(), indent=2))
