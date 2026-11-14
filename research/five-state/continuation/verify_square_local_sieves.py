"""Replay direct localized edge constraints in the five open real chambers."""
import argparse
import json
from math import gcd, isqrt

from verify_exceptional_crt import ACTIONS, merge_residues


def valuation(value, prime):
    value = abs(value)
    if not value:
        return float("inf")
    exponent = 0
    while value%prime==0:
        value //= prime
        exponent += 1
    return exponent


def state_pairs(code,r,a,c,d,q,e):
    return ((a,q),(c,d),(c,q),(a,e),(r*a,d)) if code==119772 else (
        (a,q),(c,d),(e,q),(c,3*q),(a,d))


def raw_check(code,r,coordinates,base,primes):
    pairs = state_pairs(code,r,*coordinates)
    (t,s,marked) = ACTIONS[code]
    if len(set(pairs))!=5 or not all(q<2*a<2*q for a,q in pairs):
        raise ArithmeticError(("high chamber", coordinates))
    for prime in primes:
        if any(gcd(a,q)%prime==0 for a,q in pairs):
            raise ArithmeticError(("local primitiveness",prime,coordinates))
        for letter,edges in enumerate((t,s)):
            for i,j in enumerate(edges):
                a,q=pairs[i]; u,v=pairs[j]
                factor=r if marked==(letter,i) else 1
                modulus, target, x, y = (q,v,a,u) if letter==0 else (a,u,q-a,v-u)
                vmod = valuation(modulus,prime)
                if modulus!=factor*target:
                    raise ArithmeticError(("fibre",prime,letter,i))
                if min(vmod,valuation(base,prime))!=valuation(factor,prime):
                    raise ArithmeticError(("defect",prime,letter,i))
                if (base*x-factor*y)%prime**vmod:
                    raise ArithmeticError(("edge",prime,letter,i))


def witness(code,r,j,ray,primes):
    specs=[[] for _ in range(4)]
    base_specs=[]
    for p in primes:
        modulus=4 if p==2 else p
        values=[1,1,1,1]
        if code==119772:
            if p==2 and r==3 and j==1:
                values[3]=2
            elif p not in (2,r) and (r-j)%p==0:
                values[3]=2
        else:
            if p==2:
                values[3]=2
            elif p!=3 and (3*values[3]-values[2])%p==0:
                values[3]=2
        for row,value in zip(specs,values,strict=True):
            row.append((value,modulus))
        base_specs.append((0 if p==r else 1,p))
    residues=[merge_residues(row) for row in specs]
    period=residues[0][1]
    a,c_or_d,q,e=tuple(value+((period*100*s-value)//period)*period
                      for s,(value,period) in zip(ray,residues,strict=True))
    if code==119772:
        c,d=c_or_d,r*e-j*a
    else:
        c,d=3*e-q,c_or_d
    base,period_b=merge_residues(base_specs)
    if base<2:
        base+=period_b
    coordinates=(a,c,d,q,e)
    raw_check(code,r,coordinates,base,primes)
    return {"code":code,"factor":r,"shift":j,"coordinate_modulus":period,"base":base,"tuple":coordinates}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prime-limit",type=int,default=43)
    args=parser.parse_args()
    primes=[p for p in range(2,args.prime_limit+1)
            if all(p%d for d in range(2,isqrt(p)+1))]
    cases=((119772,2,-1,(100,170,180,115)),(119772,2,1,(100,145,170,175)),
           (119772,3,1,(100,170,180,140)),(119772,3,2,(300,510,540,520)),
           (606897,3,1,(96,185,100,92)))
    print(json.dumps({"primes":primes,"results":[witness(*row,primes) for row in cases]},indent=2))


if __name__=="__main__":
    main()
