"""Exact algebraic tests for the chamber-separation route portfolio."""
import hashlib
import json
import time
from pathlib import Path
import sympy as s

ROOT = Path(__file__).resolve().parent
A, Q, C, D = x = s.symbols('A Q C D')
# Common 119772/3 coordinates, ordered around the square.
N = (D**2-9*Q**2, C**2-A**2, D**2-Q**2, C**2-9*A**2)


def homogeneous_monomials(degree):
    return [A**a*Q**q*C**c*D**(degree-a-q-c)
            for a in range(degree+1) for q in range(degree-a+1)
            for c in range(degree-a-q+1)]


def invariant_space(t):
    start = time.monotonic()
    mons = homogeneous_monomials(4*t)
    rows = []
    for xi, ni in zip(x, N):
        G = s.groebner([xi**k*ni**(t-k) for k in range(t+1)], *x)
        remainders = [s.Poly(G.reduce(m)[1], *x).as_dict() for m in mons]
        exponents = sorted(set().union(*(r.keys() for r in remainders)))
        rows.extend([[r.get(e, 0) for r in remainders] for e in exponents])
    matrix = s.Matrix(rows)
    basis = matrix.nullspace()
    polynomials = [s.expand(sum(c*m for c, m in zip(v, mons))) for v in basis]
    # This verifies the claimed basis, independently of how it is displayed.
    for p in polynomials:
        for xi, ni in zip(x, N):
            G = s.groebner([xi**k*ni**(t-k) for k in range(t+1)], *x)
            assert G.reduce(p)[1] == 0
    return {'t': t, 'degree': 4*t, 'monomials': len(mons),
            'constraint_rows': matrix.rows, 'rank': len(mons)-len(basis),
            'nullity': len(basis), 'basis': list(map(str, polynomials)),
            'seconds': time.monotonic()-start}


def mutation_obstructions():
    # Native 606897 coordinates for this calculation only.
    a, c, d, q, sw, tw = s.symbols('a c d q s t')
    anew = sw*(d*d-q*q)/a
    cnew = tw*(9*q*q-d*d)/c
    # Multiply by a²c² to clear units. Reducing with the old square
    # relation exposes constants that a valid mutated core would divide.
    at_d = s.rem(s.expand((cnew*cnew-anew*anew)*a*a*c*c),
                 d, d)
    at_d = s.rem(at_d, c*c-a*a, c)
    at_q = s.rem(s.expand((cnew*cnew-9*anew*anew)*a*a*c*c),
                 q, q)
    at_q = s.rem(at_q, c*c-9*a*a, c)
    assert s.expand(at_d-a*a*q**4*(81*tw**2-sw**2)) == 0
    assert s.expand(at_q-a*a*d**4*(tw**2-81*sw**2)) == 0
    # These cancelled factors are units when the retained pair is coprime.
    # If both retained coordinates are even, integer-weight replacements
    # are even and cannot preserve adjacent coprimality in the first place.
    return {'coordinate_convention': 'native 606897 only',
            'mutation': [str(anew), str(cnew)],
            'D_obstruction': 'D | 81*t^2-s^2',
            'Q_obstruction': 'Q | t^2-81*s^2',
            'unweighted': 'D | 80 and Q | 80',
            'cancellation_hypothesis': 'gcd(D,Q)=1; even retained pair cannot preserve adjacent primitiveness for these integer weights',
            'provenance': 'reproduces SQUARE_CYCLE_COMPLEMENT_DESCENT.md; not claimed new',
            'cleared_residues': [str(s.factor(at_d)), str(s.factor(at_q))]}


if __name__ == '__main__':
    print(json.dumps({'arithmetic': 'exact Q', 'variables': ['A','Q','C','D'],
                      'units': 'dimensionless integers', 'ideal_powers': [1,2,3,4],
                      'source': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}), flush=True)
    result = {'invariant_spaces': [invariant_space(t) for t in (1,2,3,4)],
              'mutation_obstructions': mutation_obstructions()}
    (ROOT/'ALGEBRA_RESULTS.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2), flush=True)
