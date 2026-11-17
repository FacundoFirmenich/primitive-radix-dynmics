"""Exclude uniform signs in the remaining factor-three 119772 moduli."""
import json
from fractions import Fraction as F
from itertools import product
from math import gcd, lcm

from verify_remaining_resultants import rational_roots


def replay():
    results = {}
    for case in ("C","A"):
        chamber = set()
        k_values = range(-81,82) if case=="C" else range(-200,201)
        ell_values = range(-1001,1002) if case=="C" else range(-600,601)
        for k, ell in product(k_values,ell_values):
            if case == "C":
                coeff = (81*k*k+540*k-5824,(-9*k*k-60*k+1376)*ell,
                         81*k*k+540*k-81*ell*ell+900)
            else:
                coeff = (81*k*k-240*k*ell-9*ell*ell+3442688,
                         640*k*ell+48*ell*ell-20656128,27541504-64*ell*ell)
            for y in rational_roots(*coeff):
                if not F(3,2)<y<2:
                    continue
                if case == "C":
                    x = (k*y+3*ell-24*y)/(3*k+10)
                    d = 3*x-y
                    if 27-27*x*x+8*x*y != k*d*y or 9-9*x*x+6*x*y+8*y*y != ell*y:
                        continue
                else:
                    denominator = k*y+ell*(8-3*y)
                    if denominator == 0:
                        continue
                    x = 656*(y-2)*(y-4)/denominator
                    d = 8-3*y
                    if 8*(8-6*y-8*x*x+y*y) != k*x*y or 8*(648-486*y+8*x*x+81*y*y) != ell*x*d:
                        continue
                if not F(3,2)<x<y<2 or not 3<d<2*x:
                    continue
                for j in (1,2):
                    e = (d+j)/3
                    if not 1<e<2 or case=="A" and e!=3-y:
                        continue
                    a = lcm(x.denominator,y.denominator,d.denominator,e.denominator)
                    c, q, dd, ee = int(x*a),int(y*a),int(d*a),int(e*a)
                    chamber.add((a,c,dd,q,ee,k,ell))
        results[case] = {"quotient_pairs":len(k_values)*len(ell_values),"chamber_points":sorted(chamber),
                         "survivors":[row for row in sorted(chamber)
                                      if gcd(3, row[0]*row[1]*row[2]*row[3]*row[4])==1]}
    if any(row["survivors"] for row in results.values()):
        raise ArithmeticError(results)
    return results


if __name__ == "__main__":
    print(json.dumps(replay(),indent=2))
