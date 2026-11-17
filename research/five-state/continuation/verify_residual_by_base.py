"""Classify the three residual orientations at a specified integer base."""

import argparse
import json
from bisect import bisect_left, bisect_right
from math import gcd

from sympy import divisors

from verify_exceptional_crt import ACTIONS, edge_certificate, states_for


def open_interval(values, lower, upper):
    return values[bisect_right(values, lower):bisect_left(values, upper)]


def possible_states(base, code, r, moduli):
    units = [n for n in moduli if n % r]
    if code == 119772:
        for a in units:
            for q in open_interval(units, r*a//2, 2*a):
                c = base*a % q
                if not a < c < q or c % r == 0 or gcd(a,q) != 1:
                    continue
                for d in open_interval(units,r*a,2*c):
                    for j in ((-1,1) if r == 2 else (1,2)):
                        e_num = d+j*a
                        e = e_num//r
                        if e_num % r == 0 and a < e < 2*a and (base-1) % e == 0:
                            yield a,c,d,q,e
        return
    for q in units:
        for a in open_interval(units,3*q//4,q):
            e = base*a % q
            if 6*e <= 5*q or (base-1) % e or gcd(a,q) != 1:
                continue
            c = 3*e-q
            if not 3*q < 2*c < 4*a:
                continue
            for d in open_interval(units,c,2*a):
                yield a,c,d,q,e


def classify(base):
    if base < 2:
        raise ValueError("The base must be at least two")
    # Factoring the two consecutive even/odd partners separately also exposes
    # which of them supplies each odd prime power in the cycle congruences.
    moduli = sorted({int(d*e) for d in divisors(base-1) for e in divisors(base+1)})
    results = []
    for code,r in ((119772,2),(119772,3),(606897,3)):
        candidates = set(possible_states(base,code,r,moduli)) if base % r == 0 else set()
        matches = []
        for coordinates in sorted(candidates):
            states = states_for(code,r,*coordinates)
            cert = edge_certificate(states,*ACTIONS[code],r) if states else None
            if cert is not None and (base-cert[0]) % cert[1] == 0:
                matches.append({"coordinates": coordinates, "residue_and_period": cert})
        results.append({"code": code, "factor": r, "pre_crt_candidates": len(candidates),
                        "realizations": matches})
    return {"base": base, "cycle_divisors": len(moduli), "rows": results}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("base", type=int)
    args = parser.parse_args()
    print(json.dumps(classify(args.base),indent=2))
