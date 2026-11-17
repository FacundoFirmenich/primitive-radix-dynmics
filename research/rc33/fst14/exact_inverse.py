"""Exact word-normalization contracts; no floating logarithms in integer decisions."""
from math import gcd,lcm

def key(w):
    if not isinstance(w,str) or any(c not in '0123456789' for c in w):raise ValueError('literal decimal word required')
    return 8*10**len(w)-9*int(w or '0')

def primitive(n,p):
    if not n:raise ValueError('zero has no primitive part')
    while n%p==0:n//=p
    return n

def erased(n,primes):
    for p in set(primes):n=primitive(n,p)
    return n

def canonical(n):
    if n%9!=8:raise ValueError('key outside 8+9Z')
    ell=0;m=1
    while not 9-m<=n<=8*m:ell+=1;m*=10
    s=(8*m-n)//9
    return '' if ell==0 else str(s).zfill(ell)

def cycle(p):
    if p==3:raise ValueError('three is the identity-erasure exception')
    d=1
    while pow(p,d,9)!=1:d+=1
    return d,p**d

def base(h,p=7):
    if not h or h%p==0:raise ValueError('inadmissible primitive label')
    d,q=cycle(p)
    for a in range(d):
        if h*pow(p,a,9)%9==8:return h*p**a,q
    raise ValueError('label outside the normalized image')

def fibre_count(h,ell,p=7):
    if not isinstance(ell,int) or ell<0:raise ValueError('nonnegative length required')
    n,q=base(h,p);cap=8*10**ell if n>0 else 10**ell-9
    n=abs(n);a=0
    while n<=cap:a+=1;n*=q
    return a

def decode(h,ell,j,p=7):
    if not isinstance(j,int) or not 0<=j<fibre_count(h,ell,p):raise ValueError('inadmissible rank')
    n,q=base(h,p);c=canonical(n*q**j)
    return '8'*(ell-len(c))+c

def encode(w,p=7):
    n=key(w);h=primitive(n,p);n0,q=base(h,p);j=0
    while n0!=n:n0*=q;j+=1
    return h,len(w),j

def max_count(ell,p=7):
    _,q=cycle(p);n=1;m=10**ell;a=0
    while n<=m:a+=1;n*=q
    return a

def bits(c):
    if c<1:raise ValueError('no code for an empty candidate set')
    return (c-1).bit_length()

def bounded_count(h,L,p=7):
    n,q=base(h,p);cap=8*10**L if n>0 else 10**L-9;count=0
    while abs(n)<=cap:count+=L-len(canonical(n))+1;n*=q
    return count

def pairs(ell,j):
    m=10**ell;q=343**j;den=9*q
    low=(8*m*(q-1)+den-1)//den;high=(8*m*q+m-9)//den
    return max(0,high-low+1)

def multiplicities(ell):
    es=[pairs(ell,0)];j=1
    while es[-1]:es.append(pairs(ell,j));j+=1
    es.extend([0,0])
    return {f:es[f-1]-2*es[f]+es[f+1] for f in range(1,len(es)-1) if es[f-1]-2*es[f]+es[f+1]}

def modular_class(ell,M,R):
    if M<1:raise ValueError('positive modulus required')
    g=gcd(9,M);Q=M//g;b=8*10**ell-R
    if b%g:return Q,None,0
    r=(b//g*pow(9//g,-1,Q))%Q
    return Q,r,0 if r>=10**ell else 1+(10**ell-1-r)//Q

def run_dfa(delta,accept,w,start=0):
    for x in w:start=delta[start][int(x)]
    return start in accept

def prefix_orbit(delta,accept,c):
    states=[];seen={};q=0
    while q not in seen:seen[q]=len(states);states.append(q);q=delta[q][8]
    mu=seen[q];period=len(states)-mu
    good=[i for i,s in enumerate(states) if run_dfa(delta,accept,c,s)]
    return mu,period,[t for t in good if t<mu],[t-mu for t in good if t>=mu]

def orbit_count(orbit,T):
    mu,period,finite,residues=orbit
    return sum(t<=T for t in finite)+sum(1+(T-mu-r)//period for r in residues if mu+r<=T)

def regular_bounded_count(h,L,delta,accept):
    n,q=base(h);cap=8*10**L if n>0 else 10**L-9;total=0
    while abs(n)<=cap:
        c=canonical(n);total+=orbit_count(prefix_orbit(delta,accept,c),L-len(c));n*=q
    return total

def rank_bounded(w,L,delta,accept):
    if len(w)>L or not run_dfa(delta,accept,w):raise ValueError('word outside the bounded regular domain')
    h,ell,j=encode(w);n,q=base(h);rank=0
    for i in range(j+1):
        c=canonical(n);o=prefix_orbit(delta,accept,c)
        rank+=orbit_count(o,L-len(c) if i<j else ell-len(c)-1);n*=q
    return h,rank

def decode_bounded(h,L,rank,delta,accept):
    if not isinstance(rank,int) or rank<0:raise ValueError('nonnegative rank required')
    n,q=base(h);cap=8*10**L if n>0 else 10**L-9
    while abs(n)<=cap:
        c=canonical(n);o=prefix_orbit(delta,accept,c);T=L-len(c);number=orbit_count(o,T)
        if rank<number:
            low=0;high=T
            while low<high:
                middle=(low+high)//2
                if orbit_count(o,middle)>rank:high=middle
                else:low=middle+1
            return '8'*low+c
        rank-=number;n*=q
    raise ValueError('rank outside the bounded regular fibre')

def modular_dfa_count(ell,M,R,delta,accept):
    Q,r,c=modular_class(ell,M,R)
    if c==0:return 0
    states={(0,0):1}
    for _ in range(ell):
        nxt={}
        for (s,z),n in states.items():
            for d in range(10):
                dest=(delta[s][d],(10*z+d)%Q);nxt[dest]=nxt.get(dest,0)+n
        states=nxt
    return sum(n for (s,z),n in states.items() if s in accept and z==r)
