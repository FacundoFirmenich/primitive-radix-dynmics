"""Exact reconstruction of FST16 claims from received prose, not its absent engine.

K=8*10**ell-9*val, K_j=C*343**j. The preserved FST14 engine supplies
terminal inversion; no FST15 source is represented as received or replayed.
"""
from dataclasses import dataclass
from math import gcd
import fst14 as terminal


def digits_value(s):
    if not isinstance(s,str) or any(c not in '0123456789' for c in s):
        raise ValueError('literal decimal string required')
    v=0
    for i in range(0,len(s),1000):
        chunk=s[i:i+1000];v=v*10**len(chunk)+int(chunk)
    return v


def decimal(v):
    if v==0:return '0'
    pieces=[];base=10**1000
    while v:
        v,r=divmod(v,base);pieces.append(r)
    return str(pieces[-1])+''.join(str(x).zfill(1000) for x in reversed(pieces[:-1]))


@dataclass
class Fibre:
    h:int
    ell:int

    def __post_init__(self):
        if type(self.ell) is not int or self.ell<0:raise ValueError('invalid length')
        self.C=terminal._K0(self.h)
        assert self.C%9==8 and self.C%3!=0
        self.m=10**self.ell
        self.A=terminal.fast_fiber_size(self.h,self.ell)

    def value(self,j):
        if type(j) is not int or not 0<=j<self.A:raise ValueError('rank outside fibre')
        v,r=divmod(8*self.m-self.C*343**j,9)
        assert r==0 and 0<=v<self.m
        return v

    def word(self,j):
        v=self.value(j)
        return decimal(v).zfill(self.ell) if self.ell else ''

    def window_numeric(self,prefix,depth,lo=0,hi=None):
        if not 0<=depth<=self.ell:raise ValueError('prefix exceeds length')
        hi=self.A if hi is None else hi
        if not 0<=lo<=hi<=self.A:raise ValueError('invalid rank interval')
        scale=10**(self.ell-depth);lower=prefix*scale;upper=(prefix+1)*scale
        def first(pred):
            a,b=lo,hi
            while a<b:
                c=(a+b)//2
                if pred(self.value(c)):b=c
                else:a=c+1
            return a
        if self.C>0:return first(lambda v:v<upper),first(lambda v:v<lower)
        return first(lambda v:v>=lower),first(lambda v:v>=upper)

    def window(self,prefix=''):
        return self.window_numeric(digits_value(prefix),len(prefix))


def value_mod_three(h,ell,j,t):
    if min(ell,j,t)<0:raise ValueError('nonnegative integer parameters required')
    C=terminal._K0(h);mod=3**(t+2)
    z=(8*pow(10,ell,mod)-C*pow(343,j,mod))%mod
    assert z%9==0
    return (z//9)%(3**t)


def lift_three(h,ell,residue,t):
    """Exactly three candidates at each level; no representative enumeration."""
    if type(t) is not int or t<0:raise ValueError('invalid precision')
    a=0;period=1;checks=0
    for level in range(1,t+1):
        candidates=[a+b*period for b in range(3)]
        matches=[j for j in candidates if value_mod_three(h,ell,j,level)==residue%(3**level)]
        checks+=3
        assert len(matches)==1,('3-adic isometry violation',h,ell,level)
        a=matches[0];period*=3
    return a,period,checks


def progression(L,U,a,M):
    if not 0<=L<=U or M<1:raise ValueError('invalid interval or period')
    first=L+(a-L)%M
    count=0 if first>=U else 1+(U-1-first)//M
    return dict(first=first if count else None,count=count,
                last=first+(count-1)*M if count else None)


def joint_query(h,ell,prefix='',suffix='',three_residue=None,t=0):
    f=Fibre(h,ell);L,U=f.window(prefix)
    if len(suffix)>ell:raise ValueError('suffix exceeds word length')
    out=terminal.suffix_rank_residue(h,suffix) if suffix else (0,1)
    if out is None:return dict(L=L,U=U,count=0,status='INCONSISTENT_SUFFIX')
    a,T=out;checks=0
    if three_residue is not None:
        b,n,checks=lift_three(h,ell,three_residue,t)
        assert gcd(T,n)==1
        a,M=terminal.generalized_crt(a,T,b,n)
    else:M=T
    answer=progression(L,U,a,M)
    N=answer['count']
    return dict(h=h,length=ell,L=L,U=U,A=f.A,residue=a,period=M,
                suffix_period=T,three_checks=checks,**answer,
                extra_bits=(N-1).bit_length() if N else None)


def select(query,k):
    if type(k) is not int or not 0<=k<query['count']:raise ValueError('selection outside query')
    return query['first']+k*query['period']


def dfa_predicates(delta,accept,ell):
    n=len(delta);accept=set(accept)
    if not n or any(len(row)!=10 or any(type(q) is not int or not 0<=q<n for q in row) for row in delta):
        raise ValueError('complete deterministic decimal DFA required')
    if not accept<=set(range(n)):raise ValueError('invalid accepting states')
    some=[[q in accept for q in range(n)]];every=[some[0][:]]
    for _ in range(ell):
        some.append([any(some[-1][r] for r in row) for row in delta])
        every.append([all(every[-1][r] for r in row) for row in delta])
    return some,every


def count_dfa(h,ell,delta,accept,a=0,M=1):
    """Iterative cylinder partition: no Python recursion-depth assumption."""
    f=Fibre(h,ell);some,every=dfa_predicates(delta,accept,ell)
    stack=[(0,0,0,0,f.A)];total=0;nodes=0;accepted_blocks=0;singleton_checks=0
    while stack:
        p,d,q,lo,hi=stack.pop();nodes+=1
        lo,hi=f.window_numeric(p,d,lo,hi)
        r=progression(lo,hi,a,M);count=r['count']
        if count==0 or not some[ell-d][q]:continue
        if every[ell-d][q]:
            total+=count;accepted_blocks+=1;continue
        if count==1:
            singleton_checks+=1
            for digit in f.word(r['first'])[d:]:q=delta[q][int(digit)]
            total+=q in accept;continue
        assert d<ell
        for digit in range(9,-1,-1):stack.append((10*p+digit,d+1,delta[q][digit],lo,hi))
    return dict(count=total,nodes=nodes,accepted_blocks=accepted_blocks,
                singleton_checks=singleton_checks,initial_candidates=f.A)


def starts_88():
    return [[3]*8+[1,3],[3]*8+[2,3],[2]*10,[3]*10],{2}
