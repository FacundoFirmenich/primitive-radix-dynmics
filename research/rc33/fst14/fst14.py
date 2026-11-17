#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FST-14: exact inversion of terminal decimal words in FST primitive-7 fibers.

No floating point; no invented measurements. Python 3.11+.
The FST-13 core and FST-12 core are imported as preserved baselines.

Mathematical family:
    K(w) = 8*10**len(w) - 9*int(w)
    H(w) = Pi_7(K(w))
    K_j = K_0*343**j, 0 <= j < A_h(ell)

Given exact h and ell and a literal suffix of d digits, j is characterized by
ONE congruence class modulo the effective order of 343 modulo
10**d / gcd(K_0,10**d), or has no solution.

Discrete logarithms modulo 2**a and 5**b are computed by prime-power
lifting, never by enumerating the full (potentially enormous) period.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import gcd, lcm
import fst13_baseline as old
import fst12_baseline as base

Q = 343


def _nonneg(n: int, what: str = 'value') -> int:
    if type(n) is not int or n < 0:
        raise ValueError(f'{what} must be nonnegative integer')
    return n


def _positive(n: int, what: str = 'value') -> int:
    if type(n) is not int or n < 1:
        raise ValueError(f'{what} must be positive integer')
    return n


def _K0(h: int) -> int:
    return old._K0(h)


def fast_fiber_size(h: int, ell: int) -> int:
    """Exact A_h(ell), at most O(log(A_h+1)) comparisons of big integers.

    Unlike FST-13's linear scan, this binary-search algorithm does not
    enumerate the candidate ranks. The ell-digit threshold is materialized.
    """
    _nonneg(ell, 'ell')
    k = abs(_K0(h))
    cap = old.cap_key_at_length(ell, 1 if h>0 else -1)
    if cap < k:
        return 0
    high = 1
    while k*pow(Q,high) <= cap:
        high *= 2
    low = high//2
    # j=low fits; j=high does not.
    while high-low>1:
        mid = (low+high)//2
        if k*pow(Q,mid) <= cap:
            low=mid
        else:
            high=mid
    return low+1


def order_two_power(e: int) -> int:
    _nonneg(e, 'e')
    if e <= 1:
        return 1
    return 2 ** max(1,e-3)


def order_five_power(e: int) -> int:
    _nonneg(e, 'e')
    if e==0:
        return 1
    return 4 * 5 ** max(0,e-2)


def universal_period(d: int) -> int:
    _positive(d, 'd')
    return lcm(order_two_power(d),order_five_power(d))


def _remove_up_to(n: int, p: int, bound: int) -> int:
    n = abs(n)
    e=0
    while e < bound and n % p == 0:
        n //=p
        e+=1
    return e


def effective_period(K0: int, d: int) -> int:
    _positive(d, 'd')
    if type(K0) is not int or K0 == 0:
        raise ValueError('K0 must be nonzero integer')
    e2 = d - _remove_up_to(K0,2,d)
    e5 = d - _remove_up_to(K0,5,d)
    return lcm(order_two_power(e2),order_five_power(e5))


def discrete_log_prime_power(target: int, p: int, e: int) -> tuple[int,int] | None:
    """Solve Q**j == target (mod p**e) via exact Hensel-style lifting."""
    _nonneg(e,'e')
    if p not in (2,5):
        raise ValueError('Only p=2 or p=5 supported')
    if e==0:
        return (0,1)
    target_original=target
    mod=p
    order=1
    while pow(Q,order,mod)!=1:
        order+=1
    j=next((a for a in range(order)
            if pow(Q,a,mod)==target_original%mod),None)
    if j is None:
        return None
    for _level in range(2,e+1):
        newmod=mod*p
        nextorder=order if pow(Q,order,newmod)==1 else order*p
        jnext=next((j+a*order for a in range(nextorder//order)
                    if pow(Q,j+a*order,newmod)==target_original%newmod),None)
        if jnext is None:
            return None
        j,mod,order=jnext,newmod,nextorder
    assert 0 <= j < order and pow(Q,j,mod) == target_original%mod
    return j,order


def generalized_crt(a: int, m: int, b: int, n: int) -> tuple[int,int] | None:
    """Solve x ≡ a (mod m), x ≡ b (mod n), with noncoprime moduli."""
    _positive(m,'m');_positive(n,'n')
    a%=m;b%=n
    g=gcd(m,n)
    if (b-a)%g:
        return None
    nn=n//g
    t=0 if nn==1 else (((b-a)//g)*pow(m//g,-1,nn))%nn
    M=lcm(m,n)
    x=(a+m*t)%M
    assert x %m==a and x%n==b
    return x,M


def suffix_of_rank(h:int, j:int, d:int)->str:
    _nonneg(j,'j');_positive(d,'d')
    K0=_K0(h)
    M=9*10**d
    r=(8*10**d - (K0*pow(Q,j,M))%M)%M
    assert r%9==0
    return str(r//9).zfill(d)


def suffix_rank_residue(h:int, suffix:str) -> tuple[int,int] | None:
    """Return unique j mod effective period matching literal suffix, or None.

    Complexity polynomial in length of suffix; crucially, does not enumerate
    the period T_d (~10**d/200 for d>=5).
    """
    if not isinstance(suffix,str) or not suffix or not suffix.isascii() or not suffix.isdecimal():
        raise ValueError('Suffix must be a nonempty literal decimal string')
    d=len(suffix)
    s=int(suffix)
    K0=_K0(h)
    m0=10**d
    g=gcd(abs(K0),m0)
    target=-9*s
    if target%g:
        return None
    m=m0//g
    if m==1:
        return 0,1
    inv=pow((K0//g)%m,-1,m)
    z=((target//g)*inv)%m
    e2=e5=0
    mm=m
    while mm%2==0:
        e2+=1;mm//=2
    while mm%5==0:
        e5+=1;mm//=5
    assert mm==1
    a=discrete_log_prime_power(z,2,e2)
    if a is None:return None
    b=discrete_log_prime_power(z,5,e5)
    if b is None:return None
    out=generalized_crt(a[0],a[1],b[0],b[1])
    if out is not None:
        j,T=out
        assert T==effective_period(K0,d)
        assert suffix_of_rank(h,j,d)==suffix
    return out


@dataclass(frozen=True)
class SuffixCertificate:
    h:int
    length:int
    suffix:str
    rank_limit:int
    period:int
    residue:int | None
    count:int
    status:str
    extra_bits:int
    first_rank:int | None
    last_rank:int | None


def suffix_certificate(h:int, ell:int, suffix:str)->SuffixCertificate:
    _nonneg(ell,'ell')
    if not isinstance(suffix,str) or len(suffix)>ell:
        raise ValueError('Suffix length must be at most the literal word length')
    _K0(h)
    A=fast_fiber_size(h,ell)
    sol=suffix_rank_residue(h,suffix)
    T=effective_period(_K0(h),len(suffix))
    j=sol[0] if sol is not None else None
    assert sol is None or sol[1]==T
    count=0 if j is None or j>=A else 1+(A-1-j)//T
    return SuffixCertificate(h=h,length=ell,suffix=suffix,rank_limit=A,
                             period=T,residue=j,count=count,
                             status='INCONSISTENT' if count==0 else 'UNIQUE' if count==1 else 'NOT_IDENTIFIABLE',
                             extra_bits=(count-1).bit_length() if count else 0,
                             first_rank=j if count else None,
                             last_rank=j+T*(count-1) if count else None)


def select_suffix_rank(cert: SuffixCertificate, k: int)->int:
    _nonneg(k,'k')
    if k>=cert.count or cert.residue is None:
        raise ValueError('Requested selection lies outside certified fiber')
    return cert.residue+k*cert.period


def decode_suffix_selection(cert: SuffixCertificate, k:int)->str:
    j=select_suffix_rank(cert,k)
    return old.decode_rank(cert.h,cert.length,j)


def minimum_suffix_digits(h:int,ell:int)->int:
    """Smallest d such that last d digits separate all ranks at this ell.

    d=0 means the full fiber is already a singleton (or empty).
    """
    _nonneg(ell,'ell')
    A=fast_fiber_size(h,ell)
    if A<=1:return 0
    K0=_K0(h)
    for d in range(1,ell+1):
        if effective_period(K0,d)>=A:
            return d
    raise AssertionError('Full literal word should always separate ranks')


if __name__ == '__main__':
    from dataclasses import asdict
    import json
    cases=[(782,1000,'02'),(782,1000,'00002'),(8,1000,'88'),(-1,20,'27')]
    print(json.dumps([asdict(suffix_certificate(*case)) for case in cases],ensure_ascii=False,indent=2))
    print('minimum d, h=782, ell=1000:',minimum_suffix_digits(782,1000))
