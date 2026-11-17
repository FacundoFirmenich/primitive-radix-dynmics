"""Verify the bounded integer quotients for the four shared S-strict systems."""

from math import lcm

from sympy import Poly, Rational, cancel, expand, symbols


A, C, D = symbols("A C D")


def certificates():
    yield 1, 2, 1, A**3 - 32*A**2*C + 64*A**2*D - A*C**2 + 2*A*C*D + 32*C**3 - 128*C**2*D + 96*C*D**2
    yield 1, 3, 2, 2*A**3 - 486*A**2*C + 729*A**2*D - 2*A*C**2 + 3*A*C*D + 486*C**3 - 1458*C**2*D + 972*C*D**2
    yield 2, 2, 2, -8*A**3 + A**2*D + 64*A*C*D + 8*C**3 - 32*C**2*D + 24*C*D**2
    yield 2, 3, 6, -54*A**3 + A**2*D + 729*A*C*D + 54*C**3 - 162*C**2*D + 108*C*D**2


def second_numerator(template, r):
    if template == 1:
        if r == 2:
            return A**3 - A*C**2 + 2*A*C*D + 64*C**2*D - 256*C*D**2 + 192*D**3
        return 4*(2*A**3 - 2*A*C**2 + 3*A*C*D + 729*C**2*D - 2187*C*D**2 + 1458*D**3)
    if r == 2:
        return A**2 + 16*C**2 - 64*C*D + 48*D**2
    return 4*(A**2 + 81*C**2 - 243*C*D + 162*D**2)


def verify_congruence(numerator, modulus, original, variable, zero):
    restriction = numerator.subs(variable, zero)
    multiplier = cancel(restriction / original.subs(variable, zero))
    reduced = Poly(multiplier, A, C, D)
    denominator = lcm(*(int(value.q) for value in reduced.coeffs()))
    if denominator != 1:
        raise ArithmeticError((modulus, "nonintegral multiplier", multiplier))
    quotient = Poly(cancel((numerator - multiplier * original) / modulus), A, C, D)
    if expand(numerator - multiplier * original - modulus * quotient.as_expr()) != 0:
        raise ArithmeticError((modulus, "identity failed"))
    if any(value.q != 1 for value in quotient.coeffs()):
        raise ArithmeticError((modulus, "nonintegral quotient", quotient))


def main():
    for template, r, scale, P in certificates():
        Q = r*D - (r-1)*C
        left = A**2-C**2 if template == 1 else C**3-A**3
        right = A**3-(r*C)**3 if template == 1 else A**2-(r*C)**2
        numerator = scale * P
        verify_congruence(numerator, A, Q**2-D**2, A, 0)
        verify_congruence(numerator, D, left, D, 0)
        verify_congruence(numerator, Q, right, D, Rational(r-1, r)*C)
        bound = 2*(r-1)*sum(abs(value) for value in Poly(numerator,A,C,D).coeffs())
        print(f"Template {template}, r={r}: integral X with |X| < {bound}")
        second = second_numerator(template, r)
        verify_congruence(second, A, Q**2-D**2, A, 0)
        if template == 1:
            verify_congruence(second, D, left, D, 0)
        verify_congruence(second, Q, right, D, Rational(r-1, r)*C)
        multiplier = r-1 if template == 1 else 1
        bound = 2*multiplier*sum(abs(value) for value in Poly(second,A,C,D).coeffs())
        print(f"Template {template}, r={r}: second integral Y with |Y| < {bound}")


if __name__ == "__main__":
    main()
