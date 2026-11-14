"""Replay the square-cycle overlap conditions and bounded exceptional chambers."""

import argparse
import json
from functools import lru_cache
from math import gcd

from sympy import sqrt_mod

from verify_exceptional_crt import (
    ACTIONS, candidates_119772, candidates_606897, edge_certificate, states_for,
)


@lru_cache(maxsize=65536)
def roots(modulus):
    return tuple(int(root) for root in sqrt_mod(1, modulus, all_roots=True))


def square_cycle_conditions(code, r, a, c, d, q, e):
    if gcd(r, a*c*d*q*e) != 1:
        return False
    if code == 119772:
        return (
            (c*c-a*a) % q == (c*c-r*r*a*a) % d == (q*q-e*e) % a
            == (q*q-d*d) % c == (d-r*e) % a == 0
            and (r-1) % gcd(a,c) == (r-1) % gcd(q,d) == 0
            and (c-a) % gcd(e,q) == (r*a-c) % gcd(e,d) == (d-q) % gcd(e,c) == 0
        )
    return (
        c == 3*e-q
        and (q*q-d*d) % a == (9*q*q-d*d) % c == (c*c-a*a) % d == (e*e-a*a) % q == 0
        and 2 % gcd(a,c) == 2 % gcd(q,d) == 0
        and (d-q) % gcd(e,a) == (a-c) % gcd(e,d) == 0
    )


def by_denominator(maximum):
    for q in range(4, maximum + 1):
        if q % 3 == 0:
            continue
        for e in range(5*q//6 + 1, q):
            if e % 3 == 0 or gcd(e,q) != 1:
                continue
            c = 3*e-q
            if c % 3 == 0:
                continue
            for u in roots(q):
                a = e*u % q
                if a == e or 2*a <= c or a % 3 == 0 or 2 % gcd(a,c):
                    continue
                for v in roots(c):
                    d = c + 3*q*v % c
                    if not (d < 2*a and d % 3 and gcd(a,d) == 1 and 2 % gcd(q,d) == 0):
                        continue
                    yield a,c,d,q,e


def by_numerator(maximum):
    for a in range(3, maximum + 1, 2):
        for e in range(a + 2, 2*a, 2):
            if gcd(a,e) != 1:
                continue
            for d in (2*e-a, 2*e+a):
                if not 2*a < d < 4*a:
                    continue
                for u in roots(d):
                    c = 2*a*u % d
                    if not d < 2*c < 4*a or c % 2 == 0 or gcd(a,c) != 1:
                        continue
                    for v in roots(c):
                        q = c + d*v % c
                        if not (q < 2*a and q % 2 and q != e and gcd(q,a*d) == 1):
                            continue
                        yield a,c,d,q,e


def full_check(code, r, coordinates):
    states = states_for(code, r, *coordinates)
    if not states or len(set(states)) != 5:
        return None
    result = edge_certificate(states, *ACTIONS[code], r)
    if square_cycle_conditions(code, r, *coordinates) != (result is not None):
        raise ArithmeticError((code, coordinates, result))
    return result


def accepted(code, r, generator, maximum):
    checked = 0
    matches = []
    for coordinates in generator(maximum):
        checked += 1
        match = full_check(code, r, coordinates)
        if match:
            matches.append([list(coordinates), list(match)])
    return checked, sorted(matches)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--maximum", type=int, default=5000)
    parser.add_argument("--cross-check", type=int, default=200)
    args = parser.parse_args()
    assert full_check(119772, 3, (406,712,1265,731,557)) == (88011536665779,223336848698040)
    report = []
    for code, factor, bound, new, old in (
        (119772, 2, "A", by_numerator, candidates_119772),
        (606897, 3, "Q", by_denominator, candidates_606897),
    ):
        _, reference = accepted(code, factor, old, args.cross_check)
        if accepted(code, factor, new, args.cross_check)[1] != reference:
            raise ArithmeticError("Bounded enumeration disagrees with reference")
        checked, matches = accepted(code, factor, new, args.maximum)
        report.append({"code": code, "factor": factor, "bound": bound, "maximum": args.maximum,
                       "cross_check": args.cross_check, "crt_candidates_checked": checked,
                       "realizations": matches})
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
