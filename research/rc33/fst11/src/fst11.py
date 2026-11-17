#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FST-11: exact arithmetic, regular languages, and complementary access.

No physical hypotheses, no floating point, no synthetic research data.
All words retain their literal lengths and leading zeros.

The key K(w)=8*10**len(w)-9*val(w) is nonzero and 8 mod 9.
Its exact kernel consists of prefixing the symbol '8'.
For each fixed length, H_7(K(w)) collisions have 343^j scaling.
A digit-carry finite transducer counts prescribed scaling relations on
arbitrary regular languages specified by finite deterministic automata.
"""
from __future__ import annotations
from collections import deque, defaultdict
from dataclasses import dataclass
from functools import lru_cache
from math import gcd, lcm, isqrt
from typing import Iterable

DIGITS = '0123456789'

def is_prime(n:int)->bool:
    if not isinstance(n,int) or n<2:return False
    if n==2:return True
    if n%2==0:return False
    return all(n%d!=0 for d in range(3,isqrt(n)+1,2))

def word_check(w: str) -> str:
    if not isinstance(w, str) or any(ch not in DIGITS for ch in w):
        raise ValueError('Expected a literal decimal word; empty word is allowed')
    return w

def arithmetic_key(w: str) -> int:
    word_check(w)
    return 8*10**len(w) - 9*(int(w) if w else 0)

def canonical(w: str) -> str:
    """Canonical quotient representative: remove ONLY leading 8s."""
    return word_check(w).lstrip('8')

def canonical_from_key(K: int) -> str:
    """Unique canonical word for K = 8 (mod 9), including empty word."""
    if not isinstance(K, int) or K % 9 != 8:
        raise ValueError('K must be congruent to 8 modulo 9')
    ell = 0
    while True:
        m = 10**ell
        s_num = 8*m-K
        if s_num % 9 == 0:
            s = s_num//9
            if 0 <= s < m:
                w = str(s).zfill(ell) if ell else ''
                assert w == canonical(w) and arithmetic_key(w) == K
                return w
        ell += 1

def word_from_key(K: int, ell: int) -> str:
    """Recover exact word given K and word length ell; error if not admissible."""
    if not isinstance(ell,int) or ell < 0 or not isinstance(K,int):
        raise ValueError('Invalid K or length')
    numerator = 8*10**ell-K
    if numerator%9: raise ValueError('K not on 8 mod 9 lattice')
    v=numerator//9
    if not 0 <= v < 10**ell: raise ValueError('Not admissible at length')
    w = str(v).zfill(ell) if ell else ''
    assert arithmetic_key(w)==K
    return w

def vp(n: int, p: int) -> int:
    if n == 0 or not is_prime(p): raise ValueError('Nonzero n and prime p required')
    v=0
    while n%p==0:
        v+=1; n//=p
    return v

def primitive(n: int, prime: int) -> int:
    return n//(prime**vp(n,prime))

def primitive_set(n: int, erased_primes: Iterable[int]) -> int:
    if n == 0: raise ValueError('Cannot normalize 0')
    for p in set(erased_primes):
        if not is_prime(p): raise ValueError('All normalization bases must be prime')
        n//=p**vp(n,p)
    return n

def fuse_primitives(a: int, b: int, p: int=7, q: int=2) -> int:
    """Recover n from Pi_p(n)=a, Pi_q(n)=b, distinct prime divisors."""
    if not is_prime(p) or not is_prime(q) or p == q or a==0 or b==0 or (a>0)!=(b>0):
        raise ValueError('Need distinct primes and consistent nonzero signs')
    n=(1 if a>0 else -1)*lcm(abs(a),abs(b))
    if primitive(n,p)!=a or primitive(n,q)!=b:
        raise ValueError('Inconsistent primitive observations')
    return n

def fused_word(a:int,b:int,length:int,p:int=7,q:int=2)->str:
    return word_from_key(fuse_primitives(a,b,p,q),length)


def primitive_image_member(h:int)->bool:
    """Exactly the image of Pi_7(K(.)) over all finite decimal words."""
    return isinstance(h,int) and h!=0 and h%7!=0 and h%9 in (2,5,8)

def fiber_base_exponent(h:int)->int:
    """Unique a0 in {0,1,2} with 7**a0*h == 8 (mod 9)."""
    if not primitive_image_member(h):
        raise ValueError('h is not in the primitive image')
    return {8:0,5:1,2:2}[h%9]

def fiber_word(h:int,j:int,t:int=0)->str:
    """Unique word with H_7(K)=h, scaling depth j, prefix-8 count t."""
    if not isinstance(j,int) or not isinstance(t,int) or j<0 or t<0:
        raise ValueError('j,t must be nonnegative integers')
    K=h*7**(fiber_base_exponent(h)+3*j)
    w='8'*t+canonical_from_key(K)
    assert primitive(arithmetic_key(w),7)==h
    return w

def fiber_coordinates(w:str)->tuple[int,int,int]:
    """Bijective classification: (primitive h, 343-scaling j, 8-prefix t)."""
    k=arithmetic_key(w);h=primitive(k,7);a=vp(k,7)
    a0=fiber_base_exponent(h)
    assert a>=a0 and (a-a0)%3==0
    j=(a-a0)//3; t=len(w)-len(canonical(w))
    assert fiber_word(h,j,t)==w
    return h,j,t

@dataclass(frozen=True)
class DFA:
    """Complete deterministic finite automaton over decimal digits, MSD-first."""
    delta: tuple[tuple[int,...], ...]
    start: int
    accept: frozenset[int]
    def __post_init__(self):
        n=len(self.delta)
        if not n or not (0<=self.start<n) or any(not 0<=a<n for a in self.accept):
            raise ValueError('Invalid DFA states')
        if any(len(row)!=10 or any(not 0<=j<n for j in row) for row in self.delta):
            raise ValueError('DFA transitions must be 10 integers in [0,n)')
    @property
    def states(self)->int:return len(self.delta)
    def step(self,q:int,digit:int)->int:return self.delta[q][digit]
    def run(self,w:str)->bool:
        word_check(w)
        q=self.start
        for x in w:q=self.delta[q][ord(x)-48]
        return q in self.accept
    def reversed_for_lsd(self)->'DFA':
        """Subset construction on reversed DFA: accepts reversed words."""
        n=self.states
        pre=[tuple(frozenset(q for q in range(n) if self.delta[q][a]==r) for r in range(n)) for a in range(10)]
        start=frozenset(self.accept)
        subsets=[start]; seen={start:0}; trans=[]; accept=set()
        for ss in subsets:
            if self.start in ss: accept.add(seen[ss])
            row=[]
            for a in range(10):
                nxt=frozenset(q for r in ss for q in pre[a][r])
                if nxt not in seen:
                    seen[nxt]=len(subsets);subsets.append(nxt)
                row.append(seen[nxt])
            trans.append(tuple(row))
        return DFA(tuple(trans),0,frozenset(accept))


def dfa_all()->DFA:
    return DFA(((0,)*10,),0,frozenset({0}))

def dfa_no_digit(forbidden: str='7')->DFA:
    if len(forbidden)!=1 or forbidden not in DIGITS:raise ValueError('One digit')
    f=int(forbidden)
    return DFA((tuple(1 if i==f else 0 for i in range(10)), (1,)*10),0,frozenset({0}))

def dfa_digit_sum_mod(mod:int, target:int=0)->DFA:
    if mod<1:raise ValueError('mod>=1')
    return DFA(tuple(tuple((q+d)%mod for d in range(10)) for q in range(mod)),0,frozenset({target%mod}))

def dfa_endswith(suffix:str)->DFA:
    word_check(suffix)
    if not suffix:return dfa_all()
    n=len(suffix)
    trans=[]
    for j in range(n+1):
        row=[]
        for digit in DIGITS:
            candidate=suffix[:j]+digit
            nxt=max(i for i in range(n+1) if candidate.endswith(suffix[:i]))
            row.append(nxt)
        trans.append(tuple(row))
    return DFA(tuple(trans),0,frozenset({n}))

def dfa_finite(words:Iterable[str])->DFA:
    ws=list(words)
    for w in ws:word_check(w)
    trie=[{}];accept=set()
    for w in ws:
        cur=0
        for ch in w:
            d=int(ch)
            if d not in trie[cur]:
                trie[cur][d]=len(trie);trie.append({})
            cur=trie[cur][d]
        accept.add(cur)
    dead=len(trie)
    rows=[tuple(trie[q].get(d,dead) for d in range(10)) for q in range(dead)]
    rows.append((dead,)*10)
    return DFA(tuple(rows),0,frozenset(accept))

def product_common_suffix(A:DFA,qA:int,B:DFA,qB:int)->str|None:
    """Shortest word accepted from both arbitrary DFA states, or None."""
    first=(qA,qB)
    queue=deque([first]); parent={first:None}
    while queue:
        q,r=queue.popleft()
        if q in A.accept and r in B.accept:
            out=[]; current=(q,r)
            while parent[current] is not None:
                previous, digit=parent[current]
                out.append(DIGITS[digit]);current=previous
            return ''.join(reversed(out))
        for d in range(10):
            nxt=(A.delta[q][d],B.delta[r][d])
            if nxt not in parent:
                parent[nxt]=((q,r),d);queue.append(nxt)
    return None

def boundary_ambiguity(A:DFA)->tuple[str,str]|None:
    """Decide L ∩ 8^+L != empty, with exact shortest-prefix witness."""
    visited=set();q=A.delta[A.start][8];j=1
    while q not in visited:
        visited.add(q)
        w=product_common_suffix(A,A.start,A,q)
        if w is not None:
            assert A.run(w) and A.run('8'*j+w)
            return w,'8'*j+w
        j+=1; q=A.delta[q][8]
    return None

def canonical_image_dfa(A:DFA)->DFA:
    """Exact regular image {strip_leading_8(w) : w in L(A)}."""
    initial=set();q=A.start
    while q not in initial:
        initial.add(q);q=A.delta[q][8]
    start=(frozenset(initial),False)
    states=[start]; index={start:0};rows=[];accept=set()
    for subset,used in states:
        idx=index[(subset,used)]
        if subset & A.accept: accept.add(idx)
        row=[]
        for d in range(10):
            if not used and d==8:
                next_state=(frozenset(),True)
            else:
                next_state=(frozenset(A.delta[q][d] for q in subset),True)
            if next_state not in index:
                index[next_state]=len(states);states.append(next_state)
            row.append(index[next_state])
        rows.append(tuple(row))
    return DFA(tuple(rows),0,frozenset(accept))



def cylinder_scaling_compatible(suffix:str,j:int)->bool:
    """Whether a 343^j scaling preserves the literal terminal word suffix.

    This is an admissibility condition, not an existence guarantee at a
    particular length: s and scaled s must still fit the same length.
    """
    word_check(suffix)
    if j<1:raise ValueError('j>=1')
    if not suffix:return True
    D=10**len(suffix);c=int(suffix)
    return (pow(343,j,D)-1)*c%D==0

def collision_exponent_bound(ell:int)->int:
    """Largest j>=0 for which 343**j<=8*10**ell."""
    if ell<0:raise ValueError('ell>=0')
    cap=8*10**ell
    j=0;m=1
    while m*343<=cap:
        m*=343;j+=1
    return j

def carry_pair_count(A:DFA,ell:int,j:int=1)->int:
    """Count ordered x->y admissible in L_ell with K(y)=343**j K(x).

    Uses exact LSD first carry transduction, with generic MSD DFA reversed.
    Each unordered colliding pair appears exactly once over j>=1.
    """
    if ell<0 or j<1:raise ValueError('ell>=0, j>=1')
    if j>collision_exponent_bound(ell):return 0
    P=343**j;h=8*(P-1)//9
    R=A.reversed_for_lsd()
    current={(R.start,R.start,0):1}
    for _ in range(ell):
        nxt=defaultdict(int)
        for (qx,qy,c),ways in current.items():
            for x in range(10):
                t=P*x+c;y=t%10;d=t//10
                nx=R.delta[qx][x];ny=R.delta[qy][y]
                nxt[(nx,ny,d)]+=ways
        current=nxt
    return sum(ways for (qx,qy,c),ways in current.items()
               if c==h and qx in R.accept and qy in R.accept)

def collision_pair_count(A:DFA,ell:int)->dict:
    by_j={j:carry_pair_count(A,ell,j) for j in range(1,collision_exponent_bound(ell)+1)}
    return {'ell':ell,'accepted':language_size(A,ell), 'exponent_bound':collision_exponent_bound(ell),
            'by_j':by_j,'unordered_pairs':sum(by_j.values())}

def language_size(A:DFA,ell:int)->int:
    if ell<0: raise ValueError('ell>=0')
    counts={A.start:1}
    for _ in range(ell):
        nxt=defaultdict(int)
        for q,c in counts.items():
            for x in range(10):nxt[A.delta[q][x]]+=c
        counts=nxt
    return sum(v for q,v in counts.items() if q in A.accept)

def exhaustive_fibers(A:DFA,ell:int,max_words:int=100000)->dict:
    """QA only, enumeration bounded and clearly disclosed."""
    if 10**ell>max_words: raise ValueError('Exhaustive QA is capped')
    groups=defaultdict(list)
    accepted=[]
    for v in range(10**ell):
        w=str(v).zfill(ell) if ell else ''
        if A.run(w):
            accepted.append(w)
            groups[primitive(arithmetic_key(w),7)].append(w)
    sizes=defaultdict(int)
    for group in groups.values():sizes[len(group)]+=1
    pairs=sum(len(g)*(len(g)-1)//2 for g in groups.values())
    return {'ell':ell,'accepted':len(accepted),'classes':len(groups),
            'fiber_histogram':dict(sorted(sizes.items())),'unordered_pairs':pairs,
            'examples':[g for g in groups.values() if len(g)>1][:4]}



def count_words_mod(A:DFA,ell:int,modulus:int,residue:int)->int:
    """Exact number of accepted length-ell words with val(w)==residue mod modulus.

    Reversed DFA + modular Horner carries; no enumeration of 10**ell words.
    """
    if ell<0 or modulus<1:raise ValueError('ell>=0, modulus>=1')
    R=A.reversed_for_lsd()
    cur={(R.start,0):1};tenpow=1%modulus
    for _ in range(ell):
        nxt=defaultdict(int)
        for (q,r),ways in cur.items():
            for d in range(10):
                nxt[(R.delta[q][d],(r+tenpow*d)%modulus)]+=ways
        cur=nxt
        tenpow=(tenpow*10)%modulus
    return sum(v for (q,r),v in cur.items() if q in R.accept and r==residue%modulus)

def finite_hyperaccess_count(A:DFA,ell:int,p:int,a:int,k:int,up:int,
                             q:int,b:int,t:int,uq:int)->dict:
    """Exact finite-observation ambiguity count, exploiting regular-language prior.

    No uniform M>=10^ell requirement; any M is allowed. The CRT residue
    class captures *all* words with the two observed valuation/unit signatures.
    """
    if min(ell,a,b)<0 or k<1 or t<1 or not is_prime(p) or not is_prime(q) or p==q or gcd(p*q,9)!=1:
        raise ValueError('Invalid channel configuration')
    if up%p==0 or uq%q==0:raise ValueError('Unit residue must be nonzero modulo its prime')
    mp=p**(a+k);mq=q**(b+t)
    kmod,M=crt((p**a*up)%mp,mp,(q**b*uq)%mq,mq)
    sres=((8*10**ell-kmod)*pow(9,-1,M))%M
    count=count_words_mod(A,ell,M,sres)
    return {'ell':ell,'modulus':M,'word_residue':sres,
            'compatible_count':count,
            'status':'UNIQUE' if count==1 else ('INCONSISTENT' if count==0 else 'NOT_IDENTIFIABLE')}

def crt(a:int,m:int,b:int,n:int)->tuple[int,int]:
    if m<1 or n<1 or gcd(m,n)!=1:raise ValueError('Coprime moduli required')
    return (a+m*((b-a)*pow(m,-1,n)%n))%(m*n),m*n

def finite_hyperaccess_decode(ell:int, p:int, a:int,k:int,up:int,
                              q:int,b:int,t:int,uq:int)->str:
    """Reconstruct entire word from two finite p-adic signatures.
    Sufficient certificate: p^(a+k) q^(b+t)>=10^ell, p,q distinct from 3.
    The result is checked against the supplied signatures.
    """
    if min(ell,a,k,b,t)<0 or not is_prime(p) or not is_prime(q) or p==q or gcd(9,p*q)!=1:
        raise ValueError('Invalid precision/primes; require p,q !=3')
    if k<1 or t<1 or up%p==0 or uq%q==0:
        raise ValueError('Need at least one unit digit per channel')
    m=p**(a+k);n=q**(b+t)
    Kres,N=crt((p**a*up)%m,m,(q**b*uq)%n,n)
    if N<10**ell:
        raise ValueError('Certificate insufficient for uniform reconstruction')
    s=((8*10**ell-Kres)*pow(9,-1,N))%N
    if s>=10**ell:raise ValueError('No admissible word for supplied signatures')
    w=str(s).zfill(ell) if ell else ''
    K=arithmetic_key(w)
    if vp(K,p)!=a or vp(K,q)!=b or primitive(K,p)%p**k!=up%p**k or primitive(K,q)%q**t!=uq%q**t:
        raise ValueError('Observations inconsistent')
    return w


def precision_signature(w:str,p:int,k:int)->tuple[int,int]:
    if k<1:raise ValueError('k>=1')
    K=arithmetic_key(w)
    return vp(K,p),primitive(K,p)%(p**k)

if __name__=='__main__':
    import json
    dfa=dfa_all()
    print(json.dumps({'canonical_123':canonical_from_key(arithmetic_key('8123')),
                      'boundary_example':['123','8123'],
                      'collisions_unrestricted_ell6':collision_pair_count(dfa,6),
                      'collisions_suffix02_ell6':collision_pair_count(dfa_endswith('02'),6),
                      'finite_gap':exhaustive_fibers(dfa_finite(['888889','901961']),6,max_words=1000000)},indent=2))
