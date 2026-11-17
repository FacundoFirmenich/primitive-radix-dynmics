#!/usr/bin/env python3
"""Exact reproducible cross-audit: FST-11 + three opaque source packets + radix--Möbius.

Operations act on whole source tokens X=4777, Y=6444, Z=7444.
The external serializer B=10000 is a declared numerical observer of token sequences.
No operation extracts/rotates/permutates internal digits of source atoms.
"""
from __future__ import annotations
from fractions import Fraction
from itertools import product
from math import gcd, lcm
from collections import defaultdict
from pathlib import Path
from importlib.util import spec_from_file_location, module_from_spec
from dataclasses import dataclass
import json

B = 10000
ATOM_VALUES = {'X':4777, 'Y':6444, 'Z':7444}
TOKEN_ALPHABET = tuple(ATOM_VALUES)
checks=[]
def chk(statement, name):
    if not statement:raise AssertionError(name)
    checks.append(name)


def nu(word:str)->int:
    """Serialize whole tokens as external base-B digits; token is never indexed."""
    out=0
    for token in word:
        out = B*out + ATOM_VALUES[token]
    return out


def Ka(anchor:str, word:str)->int:
    return ATOM_VALUES[anchor]*pow(B,len(word)) - (B-1)*nu(word)


def primitive(n:int, prime:int)->int:
    assert n and prime in (2,7)
    while n % prime==0: n//=prime
    return n


def recover_from_two(kx:int, ky:int)->str:
    d=ATOM_VALUES['Y']-ATOM_VALUES['X']
    delta=ky-kx
    if delta<=0 or delta%d:
        raise ValueError('inconsistent key difference')
    val=delta//d
    n=0
    while val>1:
        val, r=divmod(val,B)
        if r:raise ValueError('difference not an exact B power')
        n+=1
    numer=ATOM_VALUES['X']*pow(B,n)-kx
    if numer%(B-1):raise ValueError('nonintegral token serialization')
    nv=numer//(B-1)
    if not 0<=nv<pow(B,n):raise ValueError('bad serialized range')
    if n==0:
        if nv:return None
        return ''
    decoded=['']*n
    for i in range(n-1,-1,-1):
        nv,remainder=divmod(nv,B)
        decoder={v:k for k,v in ATOM_VALUES.items()}
        if remainder not in decoder: raise ValueError('slot not a valid complete atom')
        decoded[i]=decoder[remainder]
    if nv: raise ValueError('overflow')
    word=''.join(decoded)
    if Ka('X',word)!=kx or Ka('Y',word)!=ky:raise ValueError('checksum failed')
    return word


def verify_source_angle():
    # Note ANGULAR_OBSERVATION_AND_REAL_VIRTUALITY_T007(1).md
    # A fixed sin(theta) has two preimages except at pi/2. One bit discriminates.
    from math import asin,sin,pi,cos
    for rat in (Fraction(4777,6444),Fraction(4777,7444),Fraction(6444,7444)):
        theta=asin(float(rat));other=pi-theta
        chk(abs(sin(theta)-sin(other))<1e-14,'angular sine collision')
        chk(cos(theta)>0 and cos(other)<0,'angular phase sign distinguishes')
    return 'The angular analogy is illustrative and numeric, not a proof of geometric identity for token observations.'


def verify_digit_fst11():
    # Source is mounted at exactly this known input path.
    filename=Path('/mnt/data/fst11(2).py')
    spec=spec_from_file_location('fst11_uploaded_exact',filename)
    mod=module_from_spec(spec)
    assert spec and spec.loader
    import sys
    sys.modules[spec.name]=mod
    spec.loader.exec_module(mod)
    lit={}
    for label,v in ATOM_VALUES.items():
        literal=str(v)  # lexical observation of a COMPLETE, already supplied 4-digit symbol
        K=mod.arithmetic_key(literal)
        h7=mod.primitive(K,7);h2=mod.primitive(K,2)
        chk(mod.fuse_primitives(h7,h2,7,2)==K,'FST11 primitive fusion '+label)
        chk(mod.fused_word(h7,h2,len(literal))==literal,'FST11 literal recovery '+label)
        chk(mod.arithmetic_key('8'+literal)==K,'FST11 prefix8 invariance '+label)
        lit[label]={'literal':literal,'K':K,'Pi7':h7,'Pi2':h2,
                    'normal_form_h_j_t':list(mod.fiber_coordinates(literal))}
    chk(len(set(x['K'] for x in lit.values()))==3,'FST11 distinct triple K')
    chk(all(x['K']==x['Pi7'] for x in lit.values()),'Pi7 alone loses no information on three particular input literals')
    # New raw dual-anchor observation: K_8-K_7=10^literal_length (on all tested words).
    for s in ('','7','8','00','4777','6444','7444','8123','008123','888889','901961'):
        K8=mod.arithmetic_key(s)
        K7=7*10**len(s)-9*(int(s) if s else 0)
        chk(K8-K7==10**len(s),'digit raw dual-anchor length '+s)
    # Independently re-run published computational claims which code supports.
    all6=mod.collision_pair_count(mod.dfa_all(),6)
    chk(all6['by_j']=={1:2915,2:8} and all6['unordered_pairs']==2923,
        'FST11 one-million-language exact DP counts')
    chk(mod.boundary_ambiguity(mod.dfa_finite(['123','8123'])) is not None,
        'FST11 prefix collision constructive witness')
    return {'three_complete_literals':lit,'length_free_digit_dual_anchor_tested':True,
            'six_digit_all_language_counts':all6,
            'archive_tests_not_attached':'47/47 and 29/29 are documentation claims; underlying test suite and legacy archive were not supplied in this turn'}


def finite_shift(word:str):
    if not word:raise ValueError('nonempty word')
    n=len(word)
    raw=Fraction(nu(word),pow(B,n))
    high=Fraction(1,1)/(1+raw)
    assert Fraction(1,2)<high<1
    return high


def Tb(r:Fraction)->Fraction:
    v=B*r
    return v-(v.numerator//v.denominator)


def Sb(h:Fraction)->Fraction:
    inner=(1-h)/h
    return 1/(1+Tb(inner))


def periodic_shift(word:str):
    n=len(word)
    frac=Fraction(nu(word),pow(B,n)-1)
    return 1/(1+frac)


def verify_radix_shift():
    data=[]
    for word in ('X','Y','Z','XY','XYZ','ZYX','XXXYZ'):
        high=finite_shift(word)
        r=Fraction(nu(word),B**len(word))
        tail=word[1:]
        chk(Tb(r)==Fraction(nu(tail),B**len(tail)),'radix shift external token sequence '+word)
        if len(word)>1:
            chk(Sb(high)==finite_shift(tail),'Mobius conjugacy for nonterminal tail '+word)
        else:
            chk(Sb(high)==1,'finite word exits high interval after final token '+word)
        data.append({'word':word,'h_in_H':str(high),'tail':tail,'S_B_h':str(Sb(high))})
    period=[]
    for w in ('X','Y','Z','XY','XYZ','ZYX'):
        h=periodic_shift(w)
        j=h; seen=[]
        for i in range(len(w)):
            chk(Fraction(1,2)<j<1,'periodic symbolic rational stays high '+w)
            seen.append(str(j));j=Sb(j)
        chk(j==h,'pure S_B cycle periodic token word '+w)
        period.append({'word':w,'period_divides':len(w),'images':seen,'returns':True})
    return {'finite_words_shift':data,'periodic_words':period,
            'interpretation':'These are S_B-only cycles; no closure under T_B has been shown.'}


def verify_anchor_matrix():
    cert=[]
    for t,a in ATOM_VALUES.items():
        # paper A_a=[[B,-a],[0,1]], so A_a^T acts on q=(B^n,-nu)
        for w in ('','XYZ','ZZYXX'):
            n=len(w);v=nu(w);q=(pow(B,n),-v)
            vprime=(B*q[0],-a*q[0]+q[1]);p=(pow(B,n+1),-nu(t+w))
            chk(vprime==p,'matrix radix transpose prefix '+t+w)
            chk(a*B-a*(B-1)==a,'fixed eigenvector radix '+t)
            chk(a*q[0]+(B-1)*q[1]==Ka(t,w),'matrix invariant key '+t+w)
        cert.append({'atom':t,'value':a,'A_matrix':[[B,-a],[0,1]],'fixed_vector':[a,B-1]})
    return cert


def verify_atom_language(max_len=8):
    all_total=0
    class_counts={}; pair=set(); keyed=[]
    signatures=set(); seen_anchor={a:defaultdict(set) for a in TOKEN_ALPHABET}
    for n in range(max_len+1):
        for tup in product(TOKEN_ALPHABET,repeat=n):
            word=''.join(tup);all_total+=1
            vals={a:Ka(a,word) for a in TOKEN_ALPHABET}
            recovered=recover_from_two(vals['X'],vals['Y'])
            chk(recovered==word,'dual-key exact recovery '+word)
            chk(vals['Y']-vals['X']==1667*pow(B,n),'length from two raw anchor keys '+word)
            chk(-3*vals['X']+8*vals['Y']-5*vals['Z']==pow(B,n), 'ternary affine length certificate '+word)
            chk(1667*vals['Z']+1000*vals['X']-2667*vals['Y']==0, 'three-key internal consistency '+word)
            chk(all(vals[a]!=0 for a in TOKEN_ALPHABET),'all token keys nonzero '+word)
            chk(all(primitive(vals[a],7)!=0 and primitive(vals[a],2)!=0 for a in TOKEN_ALPHABET),
                'prime-normalization feasible '+word)
            # FST-11 signed lcm restores each exact nonzero integer key, and the
            # pair of restored keys recovers the complete external token history.
            fused={}
            for a in ('X','Y'):
                u=vals[a]
                p7,p2=primitive(u,7),primitive(u,2)
                fused[a]=(1 if u>0 else -1)*lcm(abs(p7),abs(p2))
                chk(fused[a]==u,'two primitive channels restore signed key '+a+' '+word)
            chk(recover_from_two(fused['X'],fused['Y'])==word,
                'four-channel staged hyperaccess restores entire token word '+word)
            if n<max_len:
                for a in TOKEN_ALPHABET:
                    chk(Ka(a,a+word)==vals[a],'prefix invariance '+a+word)
            for a in TOKEN_ALPHABET:seen_anchor[a][vals[a]].add(word)
            sig=(vals['X'],vals['Y'])
            chk(sig not in signatures,'dual anchored pair injective '+word)
            signatures.add(sig)
            if n<=3:keyed.append({'word':word,'n':n,'external_value':nu(word),**{'K_'+a:vals[a] for a in TOKEN_ALPHABET}})
        class_counts[n]={'up_to_length':n,'words_total':sum(3**k for k in range(n+1)),
                         'distinct_K_X':len({k for k,ws in seen_anchor['X'].items() if any(len(w)<=n for w in ws)}),
                         'distinct_dual_key':sum(3**k for k in range(n+1))}
        chk(class_counts[n]['distinct_K_X']==3**n,'prefix kernel class cardinality n='+str(n))
    for a,groups in seen_anchor.items():
        for key,words in groups.items():
            stripped={w.lstrip(a) for w in words}
            chk(len(stripped)==1,'exact kernel prefix a '+a+' '+str(key))
    chk(all_total==(3**(max_len+1)-1)//2,'complete enumeration size')
    # K_X and second-order pair-count observers are incomparable in the
    # refinement order (neither kernel contains the other).
    def second_order(w):
        counts={t:0 for t in TOKEN_ALPHABET}
        pairs={(a,b):0 for a in TOKEN_ALPHABET for b in TOKEN_ALPHABET if a!=b}
        for t in w:
            for a in TOKEN_ALPHABET:
                if a!=t:pairs[(a,t)]+=counts[a]
            counts[t]+=1
        return tuple(counts.values()),tuple(pairs.values())
    chk(Ka('X','XYZ')==Ka('X','XXYZ') and second_order('XYZ')!=second_order('XXYZ'),
        'K_X kernel not contained in second-order kernel')
    chk(second_order('XYYX')==second_order('YXXY') and Ka('X','XYYX')!=Ka('X','YXXY'),
        'second-order kernel not contained in K_X kernel')
    return {'enumerated_words':all_total,'max_length':max_len,'class_count_by_max_length':class_counts,
            'example_keys_n_le_3':keyed,'single_anchor_classes':{a:len(seen_anchor[a]) for a in TOKEN_ALPHABET},
            'dual_anchor_distinct':len(signatures)}


def verify_minimal_affine_certificate():
    # L1 optimality among integer (a,b,c) with a+b+c=0 and ax+by+cz=1
    # Those equations reduce to 2667a+1000b=-1. Solved by (-3,8,-5).
    candidates=[]
    for a in range(-100,101):
        for b in range(-100,101):
            c=-a-b
            if a*ATOM_VALUES['X']+b*ATOM_VALUES['Y']+c*ATOM_VALUES['Z']==1:
                candidates.append((a,b,c))
    chk(candidates==[(-3,8,-5)],'unique affine certificate in coefficient box [-100,100]')
    # General solutions a=-3+1000t,b=8-2667t,c=-5+1667t.
    for t in range(-10,11):
        a=-3+1000*t;b=8-2667*t;c=-5+1667*t
        chk(a+b+c==0 and a*4777+b*6444+c*7444==1,'affine all solutions '+str(t))
        chk(abs(a)+abs(b)+abs(c)>=16,'affine L1 minimality '+str(t))
    return {'unique_minimum_L1':16,'coefficients':[-3,8,-5],
            'general_family':['-3+1000*t','8-2667*t','-5+1667*t'],
            'proof':'a congruent to -3 mod 1000; if a != -3 then |a|>=997 > 16; for a=-3, b=8,c=-5'}


def main():
    w=verify_atom_language(8)
    result={'contract':{'atoms':ATOM_VALUES,'radix':B,'internal_atom_access':False,
                         'scope':'All operations act on complete source atoms and on external token sequences; the FST11 literal words are a separate explicitly declared textual observer.'},
            'literal_fst11':verify_digit_fst11(),
            'anchor_matrices':verify_anchor_matrix(),
            'token_language_exhaustive':w,
            'affine_certificate':verify_minimal_affine_certificate(),
            'radix_Mobius_bridge':verify_radix_shift(),
            'angular_comparison_scope':verify_source_angle(),
            'verification':{'status':'PASS','check_count':len(checks),'check_sample':checks[:10]}}
    out=Path(__file__).with_name('AUDITORIA_CUATRO_LINEAS.json')
    out.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print('PASS:',len(checks),'exact + 3 indicative numerical angular comparisons.')
    print('Token sequences enumerated:',w['enumerated_words'])
    print('FST11 source native count:',result['literal_fst11']['six_digit_all_language_counts']['unordered_pairs'])
    print('Dual anchor length and primitive fusion audited; S_B finite/periodic shift audited.')

if __name__=='__main__':main()
