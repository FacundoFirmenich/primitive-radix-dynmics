"""Independent exact audit of the received FST16 statements and local additions."""
from pathlib import Path
from math import gcd,isqrt
from collections import Counter
from random import Random
import hashlib,json,platform,time
import inverse16 as I

R=Path(__file__).resolve().parent


def valuation(n,p):
    assert n
    n=abs(n);v=0
    while n%p==0:n//=p;v+=1
    return v


def suffix_candidate_checks(h,suffix):
    C=I.terminal._K0(h);m0=10**len(suffix);g=gcd(C,m0)
    if (-9*int(suffix))%g:return None,0
    m=m0//g;z=(-9*int(suffix)//g*pow(C//g,-1,m))%m if m>1 else 0
    checks=0;sols=[]
    for p in [2,5]:
        e=0;v=m
        while v%p==0:e+=1;v//=p
        if e==0:sols.append((0,1));continue
        order=I.terminal.order_two_power(1) if p==2 else I.terminal.order_five_power(1)
        candidates=[j for j in range(order) if pow(343,j,p)==z%p];checks+=order
        if not candidates:return None,checks
        a=candidates[0]
        for k in range(2,e+1):
            neworder=I.terminal.order_two_power(k) if p==2 else I.terminal.order_five_power(k)
            pool=[a+b*order for b in range(neworder//order)]
            candidates=[j for j in pool if pow(343,j,p**k)==z%(p**k)];checks+=len(pool)
            if not candidates:return None,checks
            a=candidates[0];order=neworder
        sols.append((a,order))
    return I.terminal.generalized_crt(*sols[0],*sols[1]),checks


def main():
    print('CONFIG BEFORE COMPUTATION:',json.dumps(dict(
        domain='dimensionless exact integer/rational3-adic arithmetic; no empirical frequencies',
        equations=['K=8*10^ell-9*val','K_j=C*343^j','v_j=(8*10^ell-C*343^j)/9',
                   'v3(v_j-v_k)=v3(j-k)','rank set=[L,U) intersect(a+T*3^t Z)'],
        inputs=dict(q=343,C_mod9=8,h=[-31,-13,-4,-1,2,5,8,11,17,782],
                    large_example=dict(h=8,C=8,length=10000,prefix='88',suffix='88',index=3000,
                                       ternary_precisions=[2,6,7,8]),
                    extra_erasure_primes=[2,7,109,163],DFA_seed=16017),
        source='Received prose only; original FST15/FST16 ZIP, Python suites and atlas not supplied',
        dependency='Preserved FST14 engine with its previously declared baseline adapter',
        python=platform.python_version())),flush=True)
    started=time.monotonic();checks=Counter();hs=[-31,-13,-4,-1,2,5,8,11,17,782]
    for h in hs:
        C=I.terminal._K0(h)
        assert C%9==8 and C%3!=0
        for ell in [0,1,8]:
            vals=[(8*10**ell-C*343**j)//9 for j in range(33)]
            for j in range(33):
                for k in range(j):
                    assert valuation(vals[j]-vals[k],3)==valuation(j-k,3)
                    checks['valuation_pairs']+=1
            for t in range(6):
                M=3**t;res=[I.value_mod_three(h,ell,j,t) for j in range(M)]
                assert set(res)==set(range(M));checks['permutation_values']+=M
                for j in range(0,M,max(1,M//12)):
                    a,n,c=I.lift_three(h,ell,res[j],t)
                    assert a==j and n==M and c==3*t;checks['lift_inverses']+=1
    # General erasure base: a scaled isometry, with a genuine counterexample
    # to an unrestricted assertion that every erased prime is an isometry.
    general=[]
    for p in [2,7,109,163]:
        assert all(p%d for d in range(2,isqrt(p)+1))
        d=1
        while pow(p,d,9)!=1:d+=1
        q=p**d;s=valuation(q-1,3)
        for j in range(1,82):
            assert valuation(8*(q**j-1)//9,3)==s-2+valuation(j,3)
            checks['general_prime_pairs']+=1
        general.append(dict(erased_prime=p,exponent_step=d,q=q,v3_q_minus_1=s,
                            value_shift=s-2,image_coset_modulus=3**(s-2)))
    assert [x['value_shift'] for x in general]==[0,0,1,2]
    # Distinguish value residues from unnormalized key residues.
    shifts=[]
    for t in range(1,7):
        vals={I.value_mod_three(8,7,j,t) for j in range(3**t)}
        keys={(8*pow(343,j,3**t))%(3**t) for j in range(3**t)}
        assert len(vals)==3**t and len(keys)==3**max(0,t-2)
        shifts.append(dict(t=t,value_classes=len(vals),key_classes=len(keys)))
    # Prefix intervals and combined modular selection, against direct fibres.
    for h in hs:
        for ell in range(0,19):
            f=I.Fibre(h,ell);words=[f.word(j) for j in range(f.A)]
            for prefix in ['','0','8','88','98','000']:
                if len(prefix)>ell:continue
                lo,hi=f.window(prefix)
                assert list(range(lo,hi))==[j for j,w in enumerate(words) if w.startswith(prefix)]
                checks['prefix_intervals']+=1
                for suffix in ['','0','8','88','02']:
                    if len(suffix)>ell:continue
                    for t in [0,1,3]:
                        c=2%(3**t)
                        ans=I.joint_query(h,ell,prefix,suffix,c,t)
                        expected=[j for j,w in enumerate(words) if w.startswith(prefix) and w.endswith(suffix)
                                  and int(w or '0')%(3**t)==c]
                        assert ans['count']==len(expected)
                        assert [I.select(ans,k) for k in range(ans['count'])]==expected
                        checks['joint_queries']+=1
    # Arbitrary DFA count: compare with direct word recognition.
    rng=Random(16017)
    def accepts(delta,accept,w):
        q=0
        for c in w:q=delta[q][int(c)]
        return q in accept
    for n in range(1,6):
        for case in range(8):
            delta=[[rng.randrange(n) for _ in range(10)] for _ in range(n)]
            accept={q for q in range(n) if rng.randrange(2)}
            for ell in range(13):
                for h in [8,-1,17,2]:
                    f=I.Fibre(h,ell)
                    for a,M in [(0,1),(1,2),(2,9)]:
                        ans=I.count_dfa(h,ell,delta,accept,a,M)
                        direct=sum(j%M==a%M and accepts(delta,accept,f.word(j)) for j in range(f.A))
                        assert ans['count']==direct;checks['DFA_cases']+=1
    # Sharp uniform width bounds, including shifted intervals.
    for L in range(12):
        for W in range(1,30):
            for M in range(1,20):
                counts=[I.progression(L,L+W,a,M)['count'] for a in range(M)]
                assert max(counts)==(W+M-1)//M
                assert (max(counts)<=1)==(M>=W);checks['sharp_width_cases']+=1
    f=I.Fibre(8,10000);lo,hi=f.window('88')
    c2=I.value_mod_three(8,10000,3000,2)
    c6=I.value_mod_three(8,10000,3000,6)
    c7=I.value_mod_three(8,10000,3000,7)
    rows=[I.joint_query(8,10000,'88'),I.joint_query(8,10000,'88','88'),
          I.joint_query(8,10000,'88','88',c2,2),I.joint_query(8,10000,'88','88',c6,6),
          I.joint_query(8,10000,'88','88',c7,7)]
    assert [r['count'] for r in rows]==[3944,986,110,2,1]
    assert (f.A,lo,hi)==(3945,0,3944)
    assert (rows[-1]['residue'],rows[-1]['period'],rows[-1]['three_checks'])==(3000,8748,21)
    sol,terminal_checks=suffix_candidate_checks(8,'88')
    assert sol==(0,4) and terminal_checks==5
    delta,accept=I.starts_88();dfa=I.count_dfa(8,10000,delta,accept)
    assert (dfa['initial_candidates'],dfa['count'],dfa['nodes'])==(3945,3944,21)
    word=f.word(3000);assert len(word)==10000 and word.startswith('88') and word.endswith('88')
    # Nullary and impossible constraints are not promoted to log2(0) codes.
    assert I.Fibre(8,0).word(0)=='' and I.joint_query(8,1,'','0')['count']==0
    for bad in [-1,1]:
        try:I.Fibre(8,0).word(bad)
        except ValueError:pass
        else:raise AssertionError('invalid nullary rank accepted')
    result=dict(status='PASS',seconds=time.monotonic()-started,checks=dict(checks),
        original_FST15_16_suites_replayed=False,original_FST15_16_inputs_received=False,
        large_example=dict(reconstruction='h=8,C=8 independently supplies all reported counts; omitted parameters reconstructed, not a recovered original certificate',
            A=f.A,prefix_interval=[lo,hi],rows=rows,suffix_candidate_congruence_checks=terminal_checks,
            DFA=dfa,word3000_sha256=hashlib.sha256(word.encode()).hexdigest(),
            without_suffix_uniform_t=8,without_suffix_period=6561),
        generalized_erasure=general,key_value_precision_shift=shifts,
        invariants='exact integer decisions; no floating logarithm or generic sublinear-DFA claim')
    (R/'EXACT_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2),flush=True)


if __name__=='__main__':main()
