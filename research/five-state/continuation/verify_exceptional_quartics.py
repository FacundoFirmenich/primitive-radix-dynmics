"""Audit the direct degree-four quotient construction for the exceptional graphs."""

from itertools import combinations_with_replacement

from sympy import Matrix, Poly, factor, prod, rem, symbols


def main():
    A, C, D, Q = variables = symbols("A C D Q")
    monomials = [prod(term) for term in combinations_with_replacement(variables, 4)]
    systems = {
        "119772 factor 2": ((A, 4*Q**2-D**2), (C, Q**2-D**2), (D, C**2-4*A**2), (Q, C**2-A**2)),
        "606897 factor 3": ((A, Q**2-D**2), (C, 9*Q**2-D**2), (D, C**2-A**2), (Q, C**2-9*A**2)),
    }
    for name, conditions in systems.items():
        rows = []
        for modulus, condition in conditions:
            boundary = condition.subs(modulus, 0)
            variable = next(value for value in variables if boundary.has(value))
            reductions = [Poly(rem(m.subs(modulus, 0), boundary, variable), *variables)
                          for m in monomials]
            terms = sorted({term for reduction in reductions for term in reduction.monoms()})
            rows.extend([reduction.coeff_monomial(term) for reduction in reductions] for term in terms)
        basis = [factor(sum(c*m for c,m in zip(vector, monomials)))
                 for vector in Matrix(rows).nullspace()]
        if basis != [A*C*D*Q]:
            raise ArithmeticError((name, basis))
        print(name, "rank", len(monomials)-len(basis), "kernel", basis)


if __name__ == "__main__":
    main()
