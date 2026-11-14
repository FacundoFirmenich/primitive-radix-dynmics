"""Realization certificates and bounded exhaustive searches for the exceptional rows."""

import argparse
import json
from fractions import Fraction
from math import gcd, lcm

from sympy import divisors, sqrt_mod

from rmr.core import S, T, defects


ACTIONS = {
    119772: ((2, 4, 0, 3, 1), (3, 2, 1, 0, 0), (1, 4)),
    606897: ((2, 4, 0, 0, 1), (4, 3, 2, 1, 0), (0, 3)),
}


def merge_residues(residues):
    value, modulus = 0, 1
    for residue, new_modulus in residues:
        overlap = gcd(modulus, new_modulus)
        gap = residue - value
        if gap % overlap:
            return None
        step_modulus = new_modulus // overlap
        step = (gap // overlap * pow(modulus // overlap, -1, step_modulus)) % step_modulus
        value = (value + modulus * step) % lcm(modulus, new_modulus)
        modulus = lcm(modulus, new_modulus)
    return value, modulus


def edge_certificate(states, t, s, strict, factor):
    if len(set(states)) != 5 or any(not Fraction(1, 2) < value < 1 for value in states):
        return None
    congruences = []
    for letter, mapping in enumerate((t, s)):
        for source, target in enumerate(mapping):
            x, y = states[source], states[target]
            p, q = x.numerator, x.denominator
            u, v = y.numerator, y.denominator
            delta = factor if (letter, source) == strict else 1
            if (q if letter == 0 else p) != delta * (v if letter == 0 else u):
                return None
            modulus, coefficient, rhs = (q, p, delta*u) if letter == 0 else (p, q-p, delta*(v-u))
            residue = rhs * pow(coefficient, -1, modulus) % modulus
            if gcd(residue, modulus) != delta:
                return None
            congruences.append((residue, modulus))
    result = merge_residues(congruences)
    if result is None:
        return None
    representative, modulus = result
    B = representative if representative >= 2 else representative + modulus
    for letter, (action, mapping) in enumerate(((T, t), (S, s))):
        for index, state in enumerate(states):
            if action(state, B) != states[mapping[index]]:
                raise ArithmeticError("Runtime disagrees with CRT")
            if defects(state, B)[letter] != (factor if (letter, index) == strict else 1):
                raise ArithmeticError("Runtime defect disagrees with CRT")
    return result


def states_for(code, r, a, c, d, q, e):
    if code == 119772:
        pairs = ((a, q), (c, d), (c, q), (a, e), (r*a, d))
    else:
        pairs = ((a, q), (c, d), (e, q), (c, 3*q), (a, d))
    if any(not v < 2*u < 2*v or gcd(u, v) != 1 for u, v in pairs):
        return None
    return tuple(Fraction(u, v) for u, v in pairs)


def validate_606897(a, c, d, q, e):
    states = states_for(606897, 3, a, c, d, q, e)
    generic = edge_certificate(states, *ACTIONS[606897], 3) if states else None
    reduced = None
    if (states and len(set(states)) == 5 and c == 3*e-q and gcd(3,a*c*d*q*e) == 1
            and (q*q-d*d) % a == (9*q*q-d*d) % c
            == (c*c-a*a) % d == (e*e-a*a) % q == 0):
        reduced = merge_residues((
            (e*pow(a,-1,q),q), (a*pow(c,-1,d),d),
            (d*pow(q,-1,a),a), (3*q*pow(d,-1,c),c), (1,e), (0,3),
        ))
    if reduced != generic:
        raise ArithmeticError(("Reduced and full CRT disagree", a, c, d, q, e, reduced, generic))
    return reduced


def candidates_606897(max_q):
    for q in range(2, max_q+1):
        if q % 3 == 0:
            continue
        units = sqrt_mod(1, q, all_roots=True)
        for e in range(5*q//6+1, q):
            if e % 3 == 0 or gcd(e,q) != 1:
                continue
            c = 3*e-q
            for unit in units:
                a = unit*e % q
                if a % 3 == 0 or 2*a <= c or a == e:
                    continue
                for d in divisors(c*c-a*a):
                    if c < d < 2*a and d % 3 and gcd(d,a*c) == 1:
                        yield int(a), c, int(d), q, e


def candidates_119772(max_a):
    for a in range(3, max_a+1,2):
        for e in range(a+2,2*a,2):
            if gcd(a,e) != 1:
                continue
            for d in (2*e-a, 2*e+a):
                if not 2*a < d < 4*a or gcd(a,d) != 1:
                    continue
                for unit in sqrt_mod(1, d, all_roots=True):
                    c = 2*a*unit % d
                    if c % 2 == 0 or not d < 2*c < 4*a:
                        continue
                    for q in divisors(c*c-a*a):
                        if c < q < 2*a and q % 2 and q != e and gcd(a*c,q) == 1:
                            yield a, int(c), d, int(q), e


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-coordinate", type=int, required=True)
    args = parser.parse_args()
    if args.max_coordinate < 2:
        parser.error("the bound must be at least two")
    reference = states_for(119772,3,406,712,1265,731,557)
    if edge_certificate(reference,*ACTIONS[119772],3) != (88011536665779,223336848698040):
        raise ArithmeticError("Archived positive control did not reproduce")
    results = []
    for code, factor, bound, candidates in (
        (119772,2,"A",candidates_119772(args.max_coordinate)),
        (606897,3,"Q",candidates_606897(args.max_coordinate)),
    ):
        checked = 0
        realizations = []
        for a,c,d,q,e in candidates:
            checked += 1
            states = states_for(code,factor,a,c,d,q,e)
            if code == 606897:
                result = validate_606897(a,c,d,q,e)
            else:
                result = edge_certificate(states,*ACTIONS[code],factor) if states else None
            if result is not None:
                realizations.append({"coordinates": [a,c,d,q,e], "base_and_period": list(result)})
        results.append({"code":code,"factor":factor,"bound":bound,"maximum":args.max_coordinate,
                        "crt_candidates_checked":checked,"realizations":realizations})
    print(json.dumps({"archived_positive_control":"passed","searches":results}, indent=2))


if __name__ == "__main__":
    main()
