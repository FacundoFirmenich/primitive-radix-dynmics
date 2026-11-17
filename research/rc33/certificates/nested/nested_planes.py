#!/usr/bin/env python3
"""All-height nested quotient exhaustion on 119772 cofactor planes.

Fix (D-alpha*Q)/A=k/h, alpha=+/-r, r in {2,3}.
Use two integral quadratic levels J and K, then a rational quadratic.
The cutoff is on a stated cofactor stratum, never on coordinates.
"""
from fractions import Fraction as F
from math import gcd,lcm,isqrt
from functools import reduce
from pathlib import Path
import json,sys,time

BASE=Path(__file__).resolve().parent/'source-checker'
sys.path[:0]=[str(BASE/'src'),str(BASE/'research/five-state/continuation')]
from verify_exceptional_crt import states_for,edge_certificate,ACTIONS
OUT=Path(__file__).resolve().parent

def primitive(c,d,y):
    qs=[F(1),c,d,y];den=lcm(*(t.denominator for t in qs))
    vals=[int(t*den) for t in qs];g=reduce(gcd,vals)
    return tuple(v//g for v in vals)

def certified(t,r):
    a,c,d,q=t
    if not (a<c<q<2*a and r*a<d<2*c and gcd(a,q)==gcd(c,d)==gcd(a,d)==gcd(c,q)==1 and gcd(r,a*c*d*q)==1 and (r-1)%gcd(a,c)==(r-1)%gcd(d,q)==0):return []
    if (d*d-r*r*q*q)%a or (d*d-q*q)%c or (c*c-r*r*a*a)%d or (c*c-a*a)%q:return []
    res=[]
    for j in ((-1,1) if r==2 else (1,2)):
        if (d+j*a)%r:continue
        e=(d+j*a)//r
        states=states_for(119772,r,a,c,d,q,e)
        cert=edge_certificate(states,*ACTIONS[119772],r) if states else None
        if cert:res.append({'tuple':[a,c,d,q,e],'base_and_period':list(cert)})
    return res

def run(r,alpha,k,h):
    assert r in [2,3] and alpha in [r,-r] and gcd(k,h)==1 and k
    f=1 if r==2 else 2
    # J in (-k^2,15h^2). K in (-B,B), B=f*(3|k|+2rh(r²-1))/r.
    B=F(f*(3*abs(k)+2*r*h*(r*r-1)),r)
    Klo=-(B.numerator//B.denominator)-1;Khi=-Klo
    rational=set();high=set();degenerate=[];pairs=0
    def retain(y,c):
        d=alpha*y+F(k,h)
        if 1<c<y<2 and r<d<2*c:
            t=primitive(c,d,y);high.add(t)
    for K in range(Klo,Khi+1):
        U=f*h**3*(alpha*alpha-1)-h*alpha*k*K
        V=f*alpha*h*h*k*(r*r+1)-k*k*K
        # J=0 leaves one linear equation, then a rational square condition.
        if U:
            y=F(-V,U)
            if 1<y<2:
                c2=1-F(alpha*h*(r*r-1),k)*y+F(K,f*k)*(alpha*y+F(k,h))*y
                if c2>0 and isqrt(c2.numerator)**2==c2.numerator and isqrt(c2.denominator)**2==c2.denominator:
                    retain(y,F(isqrt(c2.numerator),isqrt(c2.denominator)))
        elif not V:degenerate.append({'J':0,'K':K,'kind':'linear_identity'})
        for J in range(-k*k+1,15*h*h):
            if not J:continue
            pairs+=1;L=f*h*J
            aa=f*h*k*U*U-h*K*alpha*L*L
            bb=2*f*h*k*U*V+f*alpha*h*h*(r*r-1)*L*L-K*k*L*L
            cc=f*h*k*(V*V-L*L)
            if not aa:
                if bb:
                    ys=[F(-cc,bb)]
                elif cc==0:
                    degenerate.append({'J':J,'K':K,'kind':'quadratic_identity'});continue
                else:continue
            else:
                disc=bb*bb-4*aa*cc
                if disc<0:continue
                sq=isqrt(disc)
                if sq*sq!=disc:continue
                ys=[F(-bb+sq,2*aa),F(-bb-sq,2*aa)]
            for y in ys:
                if 1<y<2:retain(y,F(U*y+V,L))
    assert not degenerate,degenerate
    real=[]
    for t in sorted(high):real.extend(certified(t,r))
    return {'r':r,'alpha':alpha,'k':k,'h':h,'level_pairs':pairs,'J_strict_bounds':[-k*k,15*h*h],'K_abs_bound':str(B),'high_primitive_quadratic_candidates':[list(t) for t in sorted(high)],'realizations':real,'degenerate_level_equations':degenerate,'coordinate_cutoff':None}

if __name__=='__main__':
    jobs=[(2,2,-5,3),(2,2,-1,3)]+[(2,-2,k,3) for k in [13,17,19,23]]+[(3,3,-5,2),(3,-3,17,2),(3,-3,19,2)]+[(3,3,-16,7)]
    allres=[]
    for job in jobs:
        start=time.monotonic();res=run(*job);res['seconds']=time.monotonic()-start;allres.append(res)
        print(json.dumps(res),flush=True)
    (OUT/'NESTED_PLANES_RESULTS.json').write_text(json.dumps(allres,indent=2))
