"""Exclude the pure residue signs of the A fibre of DF015-0007/T."""
import json
from fractions import Fraction as F
from math import gcd, lcm

from verify_remaining_resultants import rational_roots


def replay():
    chamber = []
    primitive = []
    for k in range(3,7):
        for ell in range(-110,1):
            for d in rational_roots(82**2-ell**2, -80*k*ell, 81*k*k-9*82**2):
                c = F(k-ell*d,82)
                a = (d+1)/3
                if not F(3,2)<c<d<2*a or not F(3,4)<a<1:
                    continue
                chamber.append([str(a),str(c),str(d),k,ell])
                q = lcm(a.denominator,c.denominator,d.denominator)
                aa,cc,dd = int(a*q),int(c*q),int(d*q)
                if gcd(aa,q)==gcd(aa,dd)==gcd(cc,q)==gcd(cc,dd)==1:
                    primitive.append([aa,cc,dd,q])
    return {"number_of_pairs":444,"chamber_points":chamber,"primitive_points":primitive}


if __name__ == "__main__":
    result = replay()
    if result["primitive_points"]:
        raise ArithmeticError(result)
    print(json.dumps(result, indent=2))
