"""Exhaust the cofactor plane of the known factor-three witness."""
from fractions import Fraction
from math import isqrt, lcm

from verify_exceptional_crt import ACTIONS, edge_certificate, states_for


def roots(a, b, c):
    if not a:
        if b:
            return (-c / b,)
        if not c:
            raise ArithmeticError("Identically zero polynomial")
        return ()
    discriminant = b * b - 4 * a * c
    if discriminant < 0:
        return ()
    n = isqrt(discriminant.numerator)
    d = isqrt(discriminant.denominator)
    if (n * n, d * d) != (discriminant.numerator, discriminant.denominator):
        return ()
    square_root = Fraction(n, d)
    return ((-b + square_root) / (2 * a), (-b - square_root) / (2 * a))


def rational_points(j, k):
    m = Fraction(96 * k - 392, j)
    t = Fraction(3360, j) - Fraction(512 * k, 7 * j)
    for y in roots(8*m*m - 3*k, 16*m*t - 84 + Fraction(16*k, 7), 8*t*t - 8):
        yield m * y + t, y


def main():
    chamber = set()
    for k in range(-27, 0):
        for j in range(1, 291):
            for c, y in rational_points(j, k):
                d = 3*y - Fraction(16, 7)
                if Fraction(3, 2) < c < y < 2 and 3 < d < 2*c:
                    a = lcm(c.denominator, d.denominator, y.denominator)
                    chamber.add((a, int(c*a), int(d*a), int(y*a)))
    matches = {}
    for a,c,d,q in chamber:
        for shift in (1, 2):
            e, remainder = divmod(d + shift*a, 3)
            if remainder:
                continue
            states = states_for(119772, 3, a,c,d,q,e)
            result = edge_certificate(states, *ACTIONS[119772], 3) if states else None
            if result:
                matches[a,c,d,q,e] = result
    assert matches == {(406,712,1265,731,557): (88011536665779,223336848698040)}
    assert chamber == {(406, 712, 1265, 731), (76223441, 143229744, 281410822, 151878610)}
    print(len(chamber), sorted(chamber), matches)


if __name__ == "__main__":
    main()
