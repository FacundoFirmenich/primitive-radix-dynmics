#!/usr/bin/env python3
"""Controles exactos de dos lemas; no pretende reemplazar demostraciones."""
from fractions import Fraction
from math import gcd, lcm


def radix(B, x):
    y = B * x
    return y - y.numerator // y.denominator


def mobius(B, x):
    inverse = (1 - x) / x
    t = radix(B, inverse)
    return 1 / (1 + t)


def sample_transitive(n):
    assert n >= 2
    q = 3 ** n - 1
    ps = [q - 3 ** j for j in range(n)]
    modulus = lcm(*ps)
    assert gcd(modulus, q) == 1
    B = 1 + modulus * ((2 * pow(modulus, -1, q)) % q)
    assert B >= 2 and B % q == 3 and (B - 1) % modulus == 0
    F = [Fraction(p, q) for p in ps]
    assert len(set(F)) == n and all(Fraction(1, 2) < x < 1 for x in F)
    assert all(radix(B, F[j]) == F[(j + 1) % n] for j in range(n))
    assert all(mobius(B, F[j]) == F[j] for j in range(n))
    return (n, B, q, ps)


def upper_lambda(a_num, a_den, exponent7=True):
    """Upper bound for 10^(2n+t) [pi - m sin(pi/m)], all n>=0.

    a=a_num/a_den degrees; pi<22/7; sin x > x-x^3/6,
    m=(180/a)10^n, so the upper bound is rational.
    """
    a = Fraction(a_num, a_den)
    t = 7 if exponent7 else 6
    return Fraction(10**t, 1) * Fraction(22, 7)**3 * a*a / (6*180*180)


if __name__ == '__main__':
    for n in (2, 3, 4, 5, 6):
        n, B, q, ps = sample_transitive(n)
        print(f'PASS family n={n}: B={B}; q={q}; p={ps}')
    vals = {
        '0.01': (1, 100),
        '0.018': (9, 500),
        '0.02': (1, 50),
        '0.024': (3, 125),
    }
    prev = Fraction(0)
    for name, (p, q) in vals.items():
        upper = upper_lambda(p, q)
        assert 0 < prev < upper if prev else 0 < upper
        assert upper < 1
        print(f'PASS decimal borrow bound {name}: lambda < {upper} < 1')
        prev = upper
    assert upper_lambda(3, 100, exponent7=False) < 1
    print('PASS 0.03 scale 10^(2n+6): lambda < 1')
    print('ALL_EXACT_CHECKS_PASS')
