"""Global bounded-quotient certificate for DF015-0005/T."""
import json
from fractions import Fraction
from math import gcd, isqrt

from sympy import divisors, resultant, symbols

from verify_catalogue_crosswalk import representative
from verify_exceptional_crt import edge_certificate
from verify_oriented_predecessors import fibre_coordinates, records

# State order: A/Q, C/(3Q), A/E or C/E, A/D, C/D.
ARCHIVE = {row["normal_form"]:row["graph"] for row in records()}


def replay():
    x = symbols("x")
    constants = {}
    cores = set()
    for k in range(44,62):
        constant = int(resultant(x**3-1,x*x+k*x+81,x))
        if constant == 0:
            raise ArithmeticError(f"Unexpected zero resultant for {k}")
        tested = 0
        for a in divisors(abs(constant)):
            if a % 3 == 0:
                continue
            for q in range(a+1,(6*a-1)//5+1):
                if gcd(a,q)!=1 or q % 3 == 0:
                    continue
                c = 3*a-q
                delta = (k*c)**2 - 4*(72*c*c-18*c*q-9*q*q)
                if delta < 0:
                    continue
                h = isqrt(delta)
                if h*h != delta or (k*c+h) % 2:
                    continue
                for d in {(k*c-h)//2,(k*c+h)//2}:
                    if c < d < 2*a and gcd(d,a*c)==1 and d%3:
                        tested += 1
                        if (9*q*q-d*d)%c == (c*c-a*a)%d == (d**3-q**3)%a == 0:
                            cores.add((a,c,d,q))
        constants[k]={"resultant":constant,"high_primitive_root_candidates":tested}
    report = {"quotients":constants,"core_coordinates":sorted(cores),"realizations":[]}
    t = (0,0,2,4,3)
    for form,s,last_a in (
        ("DF015-0005",(3,4,0,2,1),True),
    ):
        expected=representative(*ARCHIVE[form])[0]
        p,offset=fibre_coordinates(s,None,3,0)
        q,_=fibre_coordinates(t,1,3,offset)
        fibres=tuple((*p[i],q[i][0]-offset,q[i][1]) for i in range(5))
        correct=((0,1,0,1),(1,1,0,3),(int(not last_a),1,1,1),(0,1,2,1),(1,1,2,1))
        if representative(t,s,0,1,3)[0]!=expected or fibres!=correct:
            raise ArithmeticError(("Graph mismatch",form,fibres))
        for a,c,d,q in sorted(cores):
            u = a if last_a else c
            for e in range(u+1,2*u):
                pairs=((a,q),(c,3*q),(u,e),(a,d),(c,d))
                if len(set(pairs))!=5 or any(gcd(p,v)!=1 for p,v in pairs):
                    continue
                states=tuple(Fraction(p,v) for p,v in pairs)
                base=edge_certificate(states,t,s,(0,1),3)
                if base:
                    report["realizations"].append((form,(a,c,d,q,e),base))
    return report


if __name__=="__main__":
    print(json.dumps(replay(),indent=2))
