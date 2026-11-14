"""Exhaust selected bounded cofactor chambers, with no coordinate cutoff."""
import argparse
import json
from functools import lru_cache
from itertools import product
from math import gcd

from sympy import divisors

from verify_exceptional_crt import ACTIONS, edge_certificate, merge_residues, states_for


@lru_cache(maxsize=65536)
def positive_divisors(n):
    return tuple(map(int, divisors(abs(n))))


def missing_coordinate(fixed, rules):
    """The missing coordinate lies in one progression or an empty intersection."""
    residues = []
    for coefficient, rhs, modulus in rules:
        overlap = gcd(coefficient,modulus)
        if rhs%overlap:
            return range(0)
        modulus //= overlap
        residue = (rhs//overlap*pow(coefficient//overlap,-1,modulus))%modulus
        residues.append((residue,modulus))
    solution = merge_residues(residues)
    if solution is None:
        return range(0)
    residue,step=solution
    start=fixed//4+1
    return range(start+(residue-start)%step,4*fixed,step)


def options(bound):
    for h in range(2, bound+1):
        for k in range(-10*h+1, 10*h):
            if gcd(h,k)==1:
                yield k,h


def tuples_from_pair(coeff, ratios, side, strict_factor):
    alpha,beta,gamma,delta = coeff
    (k,h),(l,j) = ratios
    if side=="AC":
        operands = ((beta*k*j,gamma*alpha*l*h),(k*j,delta*l*h))
    else:
        operands = ((l*h,alpha*k*j),(gamma*l*h,beta*delta*k*j))
    (b1,c1),(b2,c2)=operands
    n1,n2=b1*b1-c1*c1,b2*b2-c2*c2
    if not n1 and not n2:
        raise ArithmeticError("Both constants vanished")
    first = positive_divisors(4*n1) if n1 else ()
    second = positive_divisors(4*n2) if n2 else ()
    if not first:
        pairs = ((u,v) for v in second
                 for u in missing_coordinate(v,((1,alpha*v,abs(k)),(1,beta*v,abs(l)))
                                             if side=="AC" else ((gamma,v,abs(k)),(delta,v,abs(l)))))
    elif not second:
        pairs = ((u,v) for u in first
                 for v in missing_coordinate(u,((alpha,u,abs(k)),(beta,u,abs(l)))
                                             if side=="AC" else ((1,gamma*u,abs(k)),(1,delta*u,abs(l)))))
    else:
        pairs = ((u,v) for u in first for v in second if u < 4*v and v < 4*u)
    for u,v in pairs:
        if gcd(strict_factor,u*v)!=1:
            continue
        if side=="AC":
            d,q=u,v
            a_num,c_num=h*(d-alpha*q),j*(d-beta*q)
            if a_num%k or c_num%l:
                continue
            a,c=a_num//k,c_num//l
        else:
            a,c=u,v
            d_num,q_num=h*(c-gamma*a),j*(c-delta*a)
            if d_num%k or q_num%l:
                continue
            d,q=d_num//k,q_num//l
        if min(a,c,d,q)>0:
            yield a,c,d,q


def witnesses(code,r,side,bound):
    rows = list(options(bound))
    scale = (r,1,r,1) if code==119772 else (1,3,1,3)
    count=0
    tested=set()
    matches={}
    for signs in product((1,-1),repeat=2):
        coeff=list(scale)
        for i, sign in zip((0,1) if side=="AC" else (2,3), signs):
            coeff[i] *= sign
        for one,two in product(rows,repeat=2):
            modulus_overlap = 1 if r==2 else 2
            if modulus_overlap % gcd(one[1],two[1]):
                continue
            if gcd(r,one[1]*two[1]) != 1:
                continue
            count+=1
            for a,c,d,q in tuples_from_pair(coeff,(one,two),side,r):
                if not (a<q<2*a and c<d<2*c and gcd(a,q)==gcd(c,d)==1
                        and gcd(r,a*c*d*q)==1 and gcd(a,d)==gcd(c,q)==1
                        and modulus_overlap%gcd(a,c)==modulus_overlap%gcd(d,q)==0):
                    continue
                if code==119772:
                    if not (a<c<q and r*a<d<2*c):
                        continue
                    shifts=(-1,1) if r==2 else (1,2)
                    es=((d+j)//r for j in (j*a for j in shifts) if (d+j)%r==0)
                else:
                    if not 3*q<2*c<2*d<4*a or (c+q)%3:
                        continue
                    es=((c+q)//3,)
                for e in es:
                    tup=a,c,d,q,e
                    if tup in tested:
                        continue
                    tested.add(tup)
                    states=states_for(code,r,*tup)
                    value=edge_certificate(states,*ACTIONS[code],r) if states else None
                    if value:
                        matches[tup] = value
    return {"code":code,"factor":r,"side":side,"cofactor_bound":bound,
            "linear_quotient_pairs":count,"high_candidates":len(tested),
            "realizations":sorted((list(t),list(v)) for t,v in matches.items())}


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bound",type=int,default=8)
    parser.add_argument("--code",type=int,choices=(119772,606897))
    parser.add_argument("--factor",type=int,choices=(2,3))
    parser.add_argument("--side",choices=("AC","DQ"))
    args=parser.parse_args()
    for code,factor in ((119772,2),(119772,3),(606897,3)):
        if (args.code is not None and code!=args.code
                or args.factor is not None and factor!=args.factor):
            continue
        for side in ("AC","DQ"):
            if args.side is not None and side!=args.side:
                continue
            print(json.dumps(witnesses(code,factor,side,args.bound)),flush=True)
