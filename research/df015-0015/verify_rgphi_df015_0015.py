"""Exhaust the coprime chamber of DF015-0015 using integer arithmetic."""

import argparse
import json
from fractions import Fraction
from math import isqrt
from pathlib import Path


L = 4 * (81**3 - 1)


def coefficients(n, x):
    k = n + 148
    d = 81 * k
    return (
        12 * 81**2 * d**2 - d * k * (81 * x + L) - 4 * L**2,
        -12 * 81 * d**2 + d * k * x + 8 * L * x,
        4 * (d**2 - x**2),
    )


def cubic(n, A, C, D):
    return 4 * (C**3 + D**3) + (n + 148) * A * C * D - 4 * A**2 * (C + 81 * D)


def rational_roots(a, b, c):
    if a == 0:
        if b == 0 and c == 0:
            raise ArithmeticError("The entire line is a component")
        return [Fraction(-c, b)] if b else []
    discriminant = b * b - 4 * a * c
    if discriminant < 0:
        return []
    root = isqrt(discriminant)
    if root * root != discriminant:
        return []
    return sorted({Fraction(-b + root, 2 * a), Fraction(-b - root, 2 * a)})


def verify():
    curves = []
    for n in range(1, 20):
        d = 81 * (n + 148)
        lower = (L + Fraction(d, 2)) / 82
        upper = (L + Fraction(5 * d, 9)) / Fraction(819, 10)
        first = lower.numerator // lower.denominator + 1
        last = (upper.numerator - 1) // upper.denominator
        rational_fibres = []
        for x in range(first, last + 1):
            a, b, c = coefficients(n, x)
            # A cubic in v coincides with this quadratic at four exact inputs.
            for v in range(4):
                scaled = d**2 * cubic(n, Fraction(x - L * v, d), 1 - 81 * v, v)
                if scaled != (a * v + b) * v + c:
                    raise ArithmeticError((n, x, v, "polynomial mismatch"))
            roots = []
            for v in rational_roots(a, b, c):
                A, C, D = (x - L * v) / d, 1 - 81 * v, v
                if cubic(n, A, C, D) != 0 or C + 81 * D != 1:
                    raise ArithmeticError((n, x, v, "inverse mismatch"))
                chamber = A > 0 and 9 * A < 5 * C < 5 * D < 10 * A
                roots.append({"A_C_D_on_H_equals_1": list(map(str, (A, C, D))), "in_chamber": chamber})
            if roots:
                rational_fibres.append({"x": x, "roots": roots})
        curves.append({"n": n, "first_x": first, "last_x": last,
                       "x_count": last - first + 1, "rational_fibres": rational_fibres})
    return {
        "curve_count": len(curves),
        "x_count": sum(curve["x_count"] for curve in curves),
        "rational_fibre_count": sum(len(curve["rational_fibres"]) for curve in curves),
        "chamber_point_count": sum(
            root["in_chamber"] for curve in curves
            for fibre in curve["rational_fibres"] for root in fibre["roots"]
        ),
        "curves": curves,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    result = json.dumps(verify(), indent=2) + "\n"
    if args.out is None:
        print(result, end="")
    else:
        with args.out.open("x", encoding="utf-8", newline="\n") as stream:
            stream.write(result)
