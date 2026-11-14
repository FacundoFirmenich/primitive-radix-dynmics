"""Independent exact factorization of the DF015-0015 chamber fibres."""

from fractions import Fraction
from math import gcd, lcm

from sympy import Poly, QQ, expand, symbols


def main():
    A, C, D, H, X, n = symbols("A C D H X n")
    L = 2125760
    cubic = 4 * (C**3 + D**3) + (n + 148) * A * C * D - 4 * A**2 * (C + 81 * D)
    residue = expand(cubic.subs(C, H - 81 * D) + D**2 * (81 * (n + 148) * A + L * D))
    if residue.subs(H, 0) != 0:
        raise ArithmeticError("Congruence mismatch")

    fibre_count = 0
    roots = []
    for index in range(1, 20):
        d = 81 * (index + 148)
        lower = (L + Fraction(d, 2)) / 82
        upper = (L + Fraction(5 * d, 9)) * Fraction(10, 819)
        if not 25990 < lower < upper < 26054:
            raise ArithmeticError("Integer envelope must be extended")
        polynomial = expand(cubic.subs({n: index, C: 1 - 81 * D, A: (X - L * D) / d}))
        for x in range(25990, 26055):
            if not 164 * x > 2 * L + d or not 7371 * x < 90 * L + 50 * d:
                continue
            fibre_count += 1
            for root in Poly(polynomial.subs(X, x), D, domain=QQ).ground_roots():
                v = Fraction(int(root.p), int(root.q))
                point = ((x - L * v) / d, 1 - 81 * v, v)
                scale = lcm(*(value.denominator for value in point))
                a, c, e = (int(scale * value) for value in point)
                if gcd(a, c, e) != 1 or cubic.subs({n: index, A: a, C: c, D: e}) != 0:
                    raise ArithmeticError("Invalid projective inverse")
                roots.append((index, x, a, c, e, a > 0 and 9 * a < 5 * c < 5 * e < 10 * a))

    print("Integer fibres:", fibre_count)
    print("Rational roots:", len(roots))
    print("Chamber points:", sum(hit[-1] for hit in roots))
    for hit in sorted(roots):
        print(*hit)
    if fibre_count != 772 or len(roots) != 6 or any(hit[-1] for hit in roots):
        raise ArithmeticError("Unexpected classification")


if __name__ == "__main__":
    main()
