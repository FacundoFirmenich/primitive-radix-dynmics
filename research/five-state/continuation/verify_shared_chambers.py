"""Exhaust the necessary projective conditions for both shared S-strict templates."""

import argparse
from fractions import Fraction
from math import ceil, floor, isqrt, lcm, gcd as integer_gcd

from sympy import Poly, QQ, gcd, lambdify, resultant, symbols

from verify_shared_quotients import A, C, D, certificates, second_numerator


def box_bounds(polynomial, r, count=64):
    terms = Poly(polynomial, A, C).terms()
    low_c, high_c = Fraction(1, 2), Fraction(r, 2*r-1)
    step_c = (high_c-low_c)/count
    lowest, highest = None, None
    for j in range(count):
        c0, c1 = low_c+j*step_c, low_c+(j+1)*step_c
        q0, q1 = r-(r-1)*c1, r-(r-1)*c0
        step_a = (1-q0/2)/count
        for i in range(count):
            a0, a1 = q0/2+i*step_a, q0/2+(i+1)*step_a
            low, high = Fraction(0), Fraction(0)
            for (e, f), coefficient in terms:
                coefficient = int(coefficient)
                v0, v1 = a0**e*c0**f, a1**e*c1**f
                low += coefficient*(v0 if coefficient >= 0 else v1)
                high += coefficient*(v1 if coefficient >= 0 else v0)
            denominators = (a0*q0, a1*q1)
            local_min = min(low/d for d in denominators)
            local_max = max(high/d for d in denominators)
            lowest = local_min if lowest is None else min(lowest, local_min)
            highest = local_max if highest is None else max(highest, local_max)
    return ceil(lowest), floor(highest)


def roots(a, b, c):
    if a == 0:
        if b == c == 0:
            raise ArithmeticError("Entire resultant fibre requires separate analysis")
        return {Fraction(-c, b)} if b else set()
    d = b*b-4*a*c
    if d < 0:
        return set()
    z = isqrt(d)
    return {Fraction(-b+z, 2*a), Fraction(-b-z, 2*a)} if z*z == d else set()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--subdivisions", type=int, default=64)
    args = parser.parse_args()
    if args.subdivisions < 1:
        parser.error("subdivisions must be positive")
    X, Y = symbols("X Y")
    for template, r, scale, cubic in certificates():
        q = r-(r-1)*C
        P = (r-1)*scale*cubic.subs(D, 1)
        V = (r-1 if template == 1 else 1)*second_numerator(template,r).subs(D,1)
        F, G = P-X*A*q, V-Y*A*q
        x_min, x_max = box_bounds(P, r, args.subdivisions)
        y_min, y_max = box_bounds(V, r, args.subdivisions)
        R = Poly(resultant(F, G, A), C)
        factors = (C-3)*(C-2)**(4-template)*(C-1) if r == 2 else (C-2)*(C-1)*(2*C-3)**(4-template)
        R, remainder = R.div(Poly(factors, C))
        if not remainder.is_zero or R.degree() != 2:
            raise ArithmeticError("Unexpected resultant factorization")
        coefficients = lambdify((X,Y), R.all_coeffs(), "math")
        checked, projected, chamber, primitive = 0, 0, [], []
        for x in range(x_min, x_max+1):
            for y in range(y_min, y_max+1):
                checked += 1
                for c in roots(*coefficients(x,y)):
                    if not Fraction(1,2) < c < Fraction(r,2*r-1):
                        continue
                    projected += 1
                    common = gcd(Poly(F.subs({X:x,C:c}), A, domain=QQ),
                                 Poly(G.subs({Y:y,C:c}), A, domain=QQ))
                    if common.is_zero:
                        raise ArithmeticError("Unresolved positive-dimensional intersection")
                    for root in common.ground_roots():
                        a = Fraction(int(root.p), int(root.q))
                        q_value = r-(r-1)*c
                        if not q_value/2 < a < 1:
                            continue
                        chamber.append((x,y,str(a),str(c)))
                        den = lcm(a.denominator,c.denominator)
                        pp,cc = int(a*den),int(c*den)
                        qq = r*den-(r-1)*cc
                        if integer_gcd(pp,den)==integer_gcd(pp,qq)==integer_gcd(cc,den)==integer_gcd(cc,r)==1:
                            primitive.append((pp,cc,den,qq))
        print(f"template={template} r={r} X={x_min}..{x_max} Y={y_min}..{y_max} checked={checked} projected={projected}",flush=True)
        rejected = []
        for a,c,d,q_value in primitive:
            conditions = (
                (q_value*q_value-d*d) % a,
                (a*a-c*c if template == 1 else c**3-a**3) % d,
                (a**3-(r*c)**3 if template == 1 else a*a-(r*c)**2) % q_value,
            )
            if not any(conditions):
                raise ArithmeticError(("Survivor needs CRT", template, r, a,c,d,q_value))
            rejected.append(((a,c,d,q_value),conditions))
        print("chamber_count",len(chamber),"primitive_rejects",rejected,flush=True)
        expected = {(1,2):(1,1),(1,3):(22,1),(2,2):(0,0),(2,3):(2,0)}
        if (len(chamber), len(rejected)) != expected[template,r]:
            raise ArithmeticError("Unexpected chamber counts")



if __name__ == "__main__":
    main()
