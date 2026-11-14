"""Check the cofactor linearization and height bound on the known primitive tuple."""
import json
from fractions import Fraction
from itertools import combinations, product
from math import gcd

from sympy import Matrix

from verify_square_cycle_fibres import full_check


def replay():
    a, c, d, q, e = 406, 712, 1265, 731, 557
    coordinates = (a,c,d,q)
    if full_check(119772,3,(a,c,d,q,e)) != (88011536665779,223336848698040):
        raise ArithmeticError("Known tuple did not reproduce")
    profiles = []
    for signs in product((1,-1), repeat=4):
        alpha,beta,gamma,delta = tuple(s*r for s,r in zip(signs,(3,1,3,1),strict=True))
        ratios = (Fraction(d-alpha*q,a),Fraction(d-beta*q,c),
                  Fraction(c-gamma*a,d),Fraction(c-delta*a,q))
        h = tuple(x.denominator for x in ratios)
        k = tuple(x.numerator for x in ratios)
        matrix = Matrix(((-k[0],0,h[0],-alpha*h[0]),
                         (0,-k[1],h[1],-beta*h[1]),
                         (-gamma*h[2],h[2],-k[2],0),
                         (-delta*h[3],h[3],0,-k[3])))
        if matrix.rank() != 3 or matrix*Matrix(coordinates) != Matrix.zeros(4,1):
            raise ArithmeticError((signs,matrix))
        na = (k[3]*h[2])**2 - (alpha*k[2]*h[3])**2
        nc = (gamma*k[3]*h[2])**2 - (beta*delta*k[2]*h[3])**2
        nd = (beta*k[0]*h[1])**2 - (gamma*alpha*k[1]*h[0])**2
        nq = (k[0]*h[1])**2 - (delta*k[1]*h[0])**2
        if not (na or nc) or not (nd or nq):
            raise ArithmeticError("Degenerate constants")
        if any((4*n)%m for n,m in zip((na,nc,nd,nq),coordinates,strict=True)):
            raise ArithmeticError("State coordinates do not divide the paired constants")
        if any(max(coordinates) > 16*max(abs(x),abs(y)) for x,y in ((na,nc),(nd,nq))):
            raise ArithmeticError("Paired height bound violation")
        bounds = []
        for ids in combinations(range(4),3):
            reduced = matrix[list(ids),:]
            cofactor = [int((-1)**i*reduced[:,[j for j in range(4) if j!=i]].det()) for i in range(4)]
            if not any(cofactor):
                continue
            divisor = gcd(*cofactor)
            if tuple(x//divisor for x in cofactor) not in {coordinates,tuple(-x for x in coordinates)}:
                raise ArithmeticError((signs,ids,cofactor))
            if max(map(abs,cofactor)) > 6000*h[ids[0]]*h[ids[1]]*h[ids[2]]:
                raise ArithmeticError("Height bound violation")
            bounds.append(6000*h[ids[0]]*h[ids[1]]*h[ids[2]])
        profiles.append({"signs":signs,"cofactors":h,"minimum_bound":min(bounds),
                         "paired_constants":[na,nc,nd,nq]})
    return {"primitive_core":coordinates,"independent_sign_profiles":len(profiles),"profiles":profiles}


if __name__ == "__main__":
    print(json.dumps(replay(),indent=2))
