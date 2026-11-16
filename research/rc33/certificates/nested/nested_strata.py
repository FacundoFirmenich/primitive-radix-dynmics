#!/usr/bin/env python3
"""Nested integer levels: exact all-height exhaustion of stated cofactor strata.

No coordinate cutoff. An unresolved degenerate level is reported as a blocker,
never silently omitted. Fractional coefficient denominators are strict-prime
units, and all core coordinates are assumed units at that prime.
"""
from fractions import Fraction as F
from math import gcd,lcm,isqrt
from itertools import combinations
from functools import reduce
from pathlib import Path
import sys,json,argparse,time
from nested_planes import BASE,states_for,edge_certificate,ACTIONS
OUT=Path(__file__).resolve().parent

def boxdiv(nlo,nhi,dlo,dhi):
    v=[n/d for n in (nlo,nhi) for d in (dlo,dhi)];return min(v),max(v)
def squared_range(a,b):return a*a,b*b
def scale_range(a,low,high):return (a*low,a*high) if a>=0 else (a*high,a*low)
def vertices(code,r):
    if code==119772:return [tuple(F(v,2) for v in x) for x in [(2,r,2*r,r),(2,r,2*r,4),(2,4,2*r,4),(2,4,8,4)]]
    return [tuple(F(v,8) for v in x) for x in [(6,12,12,8),(8,12,12,8),(8,12,16,8),(8,16,16,8)]]
MAPS={'A':(0,1,2,3),'C':(1,0,2,3),'D':(2,3,1,0),'Q':(3,2,1,0)}
def coefficients(code,r,node):
    a,b,g,d=map(F,(r,1,r,1) if code==119772 else (1,3,1,3))
    return {'A':(a,b,g,d),'C':(b,a,1/g,1/d),'D':(g,d,1/b,1/a),'Q':(d,g,b,a)}[node]
def chamber_slice(vs,mapping,alpha,k,h):
    def linear(x):
        a,c,d,q=[x[i] for i in mapping];return h*d-h*alpha*q-k*a
    points=[]
    for x in vs:
        if not linear(x):points.append(x)
    for x,y in combinations(vs,2):
        lx,ly=linear(x),linear(y)
        if lx*ly<0:
            t=lx/(lx-ly);points.append(tuple((1-t)*a+t*b for a,b in zip(x,y)))
    return sorted(set(points))
def source_core(z,mapping):
    den=lcm(*(x.denominator for x in z));v=[int(x*den) for x in z];gg=reduce(gcd,v);v=[x//gg for x in v]
    out=[0]*4
    for i,j in enumerate(mapping):out[j]=v[i]
    return tuple(out)
def chamber(code,r,x):
    a,c,d,q=x
    return (a<c<q<2*a and r*a<d<2*c) if code==119772 else (3*q<2*c<2*d<4*a<4*q)
def primitive_core(code,r,x):
    a,c,d,q=x
    co=(r,1,r,1) if code==119772 else (1,3,1,3)
    al,be,ga,de=co
    if not chamber(code,r,x) or gcd(r,a*c*d*q)!=1:return False
    if any(gcd(u,v)!=1 for u,v in [(a,q),(q,c),(c,d),(d,a)]):return False
    if (r-1)%gcd(a,c) or (r-1)%gcd(d,q):return False
    return ((d*d-al*al*q*q)%a==(d*d-be*be*q*q)%c==(c*c-ga*ga*a*a)%d==(c*c-de*de*a*a)%q==0)
def realize(code,r,x):
    a,c,d,q=x;es=[]
    if code==119772:
        for j in ([-1,1] if r==2 else [1,2]):
            if not (d+j*a)%r:es.append((d+j*a)//r)
    elif not (c+q)%3:es=[(c+q)//3]
    out=[]
    for e in es:
        states=states_for(code,r,a,c,d,q,e)
        cert=edge_certificate(states,*ACTIONS[code],r) if states else None
        if cert:out.append({'coordinates':[a,c,d,q,e],'base_and_period':list(cert)})
    return out

def plane(code,r,node,sign,k,h):
    mapping=MAPS[node];aa,bb,gg,dd=coefficients(code,r,node);aa*=sign
    points=chamber_slice(vertices(code,r),mapping,aa,k,h)
    if len(points)<2:return None
    vn=[tuple(x[i]/x[mapping[0]] for i in mapping) for x in points]
    clo,chi=min(x[1] for x in vn),max(x[1] for x in vn)
    dlo,dhi=min(x[2] for x in vn),max(x[2] for x in vn)
    ylo,yhi=min(x[3] for x in vn),max(x[3] for x in vn)
    if min(clo,dlo,ylo)<=0:raise ArithmeticError('Nonpositive chart')
    z1=lcm((dd*dd*h*h).denominator,(dd*dd*h*h*bb*bb).denominator)
    z2=lcm((k*dd*dd).denominator,(aa*h*(gg*gg-dd*dd)).denominator)
    f=1 if r==2 else 2
    jnlo=z1*(dd*dd*h*h*(dlo*dlo-bb*bb*yhi*yhi)-k*k*chi*chi)
    jnhi=z1*(dd*dd*h*h*(dhi*dhi-bb*bb*ylo*ylo)-k*k*clo*clo)
    jlo,jhi=boxdiv(jnlo,jnhi,clo*ylo,chi*yhi)
    v1=scale_range(F(k),clo*clo-dd*dd,chi*chi-dd*dd)
    v2=scale_range(aa*h*(gg*gg-dd*dd),ylo,yhi)
    klo,khi=boxdiv(f*z2*(v1[0]+v2[0]),f*z2*(v1[1]+v2[1]),dlo*ylo,dhi*yhi)
    JL,JH=jlo.numerator//jlo.denominator-1,jhi.numerator//jhi.denominator+1
    KL,KH=klo.numerator//klo.denominator-1,khi.numerator//khi.denominator+1
    candidates=set();degenerate=[];pairs=0
    def retain(y,c):
        d=aa*y+F(k,h)
        if min(c,d,y)>0:
            src=source_core((F(1),c,d,y),mapping)
            if chamber(code,r,src):candidates.add(src)
    for K in range(KL,KH+1):
        u=z1*dd*dd*h*h*(aa*aa-bb*bb)-F(z1*k*K,f*z2)*aa
        v=z1*aa*h*k*(gg*gg+dd*dd)-F(z1*k*k*K,f*z2*h)
        den=lcm(u.denominator,v.denominator);U,V=int(u*den),int(v*den)
        if JL<=0<=JH:
            if U:
                y=F(-V,U)
                if ylo<y<yhi:
                    c2=dd*dd-aa*h*(gg*gg-dd*dd)*y/k+F(K,f*z2*k)*(aa*y+F(k,h))*y
                    if c2>0 and isqrt(c2.numerator)**2==c2.numerator and isqrt(c2.denominator)**2==c2.denominator:retain(y,F(isqrt(c2.numerator),isqrt(c2.denominator)))
            elif not V:degenerate.append([0,K,'linear_identity'])
        p0=F(z2*k);p1=-F(K,f)*aa;p2=z2*aa*h*(gg*gg-dd*dd)-F(K*k,f*h);p3=-z2*k*dd*dd
        fac=lcm(*(x.denominator for x in [p0,p1,p2,p3]));p0,p1,p2,p3=[int(x*fac) for x in [p0,p1,p2,p3]]
        for J in range(JL,JH+1):
            if not J:continue
            pairs+=1;L=den*J
            aq=p0*U*U+p1*L*L;bq=2*p0*U*V+p2*L*L;cq=p0*V*V+p3*L*L
            if not aq:
                if bq:ys=[F(-cq,bq)]
                elif cq:continue
                else:degenerate.append([J,K,'quadratic_identity']);continue
            else:
                disc=bq*bq-4*aq*cq
                if disc<0:continue
                sd=isqrt(disc)
                if sd*sd!=disc:continue
                ys=[F(-bq+sd,2*aq),F(-bq-sd,2*aq)]
            for y in ys:
                if ylo<y<yhi:retain(y,F(U*y+V,L))
    cores=[x for x in sorted(candidates) if primitive_core(code,r,x)]
    realized=[v for x in cores for v in realize(code,r,x)]
    return {'code':code,'r':r,'node':node,'sign':sign,'k':k,'h':h,'coefficients':list(map(str,[aa,bb,gg,dd])),'z1':z1,'z2':z2,'level_bounds':{'J':[JL,JH],'K':[KL,KH]},'level_pairs':pairs,'high_candidates':[list(x) for x in sorted(candidates)],'primitive_square_cores':[list(x) for x in cores],'realizations':realized,'degenerate':degenerate,'coordinate_cutoff':None}

def run_stratum(code,r,h):
    results=[];skipped=[];v=vertices(code,r)
    for node in MAPS:
        mapping=MAPS[node];al=coefficients(code,r,node)[0]
        for sign in [1,-1]:
            vals=[(x[mapping[2]]-sign*al*x[mapping[3]])/x[mapping[0]] for x in v]
            low,high=min(vals),max(vals)
            for k in range((h*low).numerator//(h*low).denominator, (h*high).numerator//(h*high).denominator+2):
                if not low<F(k,h)<high or gcd(k,h)!=1 or not k:continue
                if r==2 and k%2!=(1 if node in ['A','D'] else 0):
                    skipped.append([node,sign,k,'parity']);continue
                # If the subtracted term contains r, the other term is a unit mod r.
                if ((code==119772 and node in ['A','D']) or (code==606897 and node in ['C','Q'])) and k%r==0:
                    skipped.append([node,sign,k,'strict_prime_unit']);continue
                res=plane(code,r,node,sign,k,h)
                if res:results.append(res)
    return {'code':code,'r':r,'h':h,'planes':results,'skipped_ratios':skipped,'all_nondegenerate':all(not x['degenerate'] for x in results),'realizations':[v for x in results for v in x['realizations']]}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--max-h',type=int,default=4);args=ap.parse_args()
    allres=[]
    for code,r in [(119772,2),(119772,3),(606897,3)]:
        for h in range(2,args.max_h+1):
            if gcd(h,r)>1:continue
            t=time.monotonic();res=run_stratum(code,r,h);res['seconds']=time.monotonic()-t;allres.append(res)
            (OUT/'NESTED_STRATA_RESULTS.json').write_text(json.dumps(allres,indent=2))
            print(json.dumps({'code':code,'r':r,'h':h,'planes':len(res['planes']),'level_pairs':sum(p['level_pairs'] for p in res['planes']),'primitive_square_cores':sum(len(p['primitive_square_cores']) for p in res['planes']),'realizations':res['realizations'],'nondegenerate':res['all_nondegenerate'],'seconds':res['seconds']}),flush=True)
