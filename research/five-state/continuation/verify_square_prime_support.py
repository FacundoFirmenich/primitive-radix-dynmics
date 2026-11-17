"""Audit the local linear ranks and the exact 2-adic loss."""

from itertools import combinations
from math import prod

from sympy import Matrix, eye, factorint

from verify_exceptional_crt import ACTIONS, edge_certificate, states_for


SYSTEMS = (
    (119772, 2, (-1, 1), ((2, 1), (1, 1), (1, 1), (2, 1))),
    (119772, 3, (1, 2), ((3, 1), (1, 1), (1, 1), (3, 1))),
    (606897, 3, (0,), ((1, 1), (1, 3), (1, 3), (1, 1))),
)


def overlap_indices(code, shift):
    if code == 606897:
        return (0, 3)
    if shift == 2:
        return (1, 2, 3)
    return (1, 2)


def local_basis_checks():
    coordinates = eye(4)
    checked = 0
    for code, _, shifts, coefficients in SYSTEMS:
        for shift in shifts:
            fifth = (coordinates[3, :] + shift * coordinates[0, :]
                     if code == 119772 else coordinates[2, :] + coordinates[1, :])
            for i in overlap_indices(code, shift):
                a, b = coefficients[i]
                for sign in (-1, 1):
                    neighbor = a * coordinates[(i + 1) % 4, :] + sign * b * coordinates[(i - 1) % 4, :]
                    rows = Matrix.vstack(coordinates[i, :], neighbor, fifth)
                    if not any(rows.extract(range(3), columns).det()
                               for columns in combinations(range(4), 3)):
                        raise ArithmeticError((code, shift, i, sign))
                    checked += 1
    return checked


def valuation(n, prime):
    count = 0
    while n % prime == 0:
        n //= prime
        count += 1
    return count


def positive_control():
    a, c, d, q, e = 406, 712, 1265, 731, 557
    states = states_for(119772, 3, a, c, d, q, e)
    if edge_certificate(states, *ACTIONS[119772], 3) != (88011536665779, 223336848698040):
        raise ArithmeticError("The ten-edge CRT control failed")
    if sorted(valuation(d + sign * q, 2) for sign in (-1, 1)) != [1, 2]:
        raise ArithmeticError("Unexpected 2-adic allocation at C")
    core = (a, q, c, d)
    primes = factorint(prod(core) * e)
    checked = 0
    for p in primes:
        i = max(range(4), key=lambda j: valuation(core[j], p))
        k = valuation(core[i], p)
        gain = valuation(e, p)
        if k:
            alpha, beta = SYSTEMS[1][3][i]
            signs = [alpha * core[(i + 1) % 4] + s * beta * core[(i - 1) % 4]
                     for s in (-1, 1)]
            gain += k + max(valuation(value, p) for value in signs)
        required = 2 * sum(valuation(x, p) for x in core) + valuation(e, p)
        if gain < required - (3 if p == 2 else 0):
            raise ArithmeticError((p, gain, required))
        checked += 1
    return checked


if __name__ == "__main__":
    print(f"independent overlap triples: {local_basis_checks()}")
    print(f"prime exponents checked on exact CRT realization: {positive_control()}")
