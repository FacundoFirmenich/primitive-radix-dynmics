"""Compare lattice reconstruction and divisor enumeration on the witness fibres."""

import json
from itertools import product

from verify_complement_descent import congruent_in_range, positive_divisors, square_core
from verify_exceptional_crt import ACTIONS, edge_certificate, merge_residues, states_for
from verify_square_cycle_fibres import roots


def lattice_fibre(d, q, code, r, scales):
    _, _, gamma, delta = scales
    signatures = {
        pair for u, v in product(roots(d), roots(q))
        if (pair := merge_residues(((gamma*u % d, d), (delta*v % q, q)))) is not None
    }
    start_a, stop_a = ((q//2+1, (d-1)//r+1) if code == 119772 else (d//2+1, q))
    start_c, stop_c = ((d//2+1, q) if code == 119772 else (3*q//2+1, d))
    cores = {
        (a, c, d, q)
        for residue, period in signatures
        for a in range(start_a, stop_a)
        for c in congruent_in_range(residue*a, period, start_c, stop_c)
        if square_core((a, c, d, q), code, r, scales)
    }
    return sorted(cores), len(signatures)


def divisor_fibres(a, c, d, q, code, r, scales):
    alpha, beta, gamma, delta = scales
    fixed_dq = sorted(
        (p, s, d, q)
        for p, s in product(positive_divisors(d*d-alpha*alpha*q*q),
                            positive_divisors(d*d-beta*beta*q*q))
        if square_core((p, s, d, q), code, r, scales)
    )
    fixed_ac = sorted(
        (a, c, p, s)
        for p, s in product(positive_divisors(c*c-gamma*gamma*a*a),
                            positive_divisors(c*c-delta*delta*a*a))
        if square_core((a, c, p, s), code, r, scales)
    )
    return fixed_dq, fixed_ac


def realizations(cores, code, r):
    matches = []
    for a, c, d, q in cores:
        numerators = (d+a, d+2*a) if code == 119772 else (c+q,)
        for numerator in numerators:
            if numerator % r:
                continue
            coordinates = (a, c, d, q, numerator//r)
            states = states_for(code, r, *coordinates)
            certificate = edge_certificate(states, *ACTIONS[code], r) if states else None
            if certificate is not None:
                matches.append((coordinates, certificate))
    return matches


def replay():
    rows = []
    witness = (406, 712, 1265, 731)
    for code, core, scales in (
        (119772, witness, (3, 1, 3, 1)),
        (606897, (731, 1265, 712, 406), (1, 3, 1, 3)),
    ):
        a, c, d, q = core
        fixed_dq, fixed_ac = divisor_fibres(*core, code, 3, scales)
        lattice, signatures = lattice_fibre(d, q, code, 3, scales)
        expected_cores = [witness] if code == 119772 else []
        if fixed_dq != lattice or lattice != expected_cores or fixed_ac != expected_cores:
            raise ArithmeticError((code, fixed_dq, lattice, fixed_ac))
        matches = realizations(sorted(set(fixed_dq + fixed_ac)), code, 3)
        expected_matches = [((*witness, 557), (88011536665779, 223336848698040))] if code == 119772 else []
        if matches != expected_matches:
            raise ArithmeticError((code, matches))
        rows.append({
            "code": code,
            "fixed_DQ": (d, q),
            "square_root_signatures": signatures,
            "cores_fixed_DQ": lattice,
            "fixed_AC": (a, c),
            "cores_fixed_AC": fixed_ac,
            "realizations": matches,
        })
    return rows


if __name__ == "__main__":
    print(json.dumps(replay(), indent=2))
