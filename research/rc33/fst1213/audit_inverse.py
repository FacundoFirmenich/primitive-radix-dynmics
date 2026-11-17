from pathlib import Path
from collections import Counter,defaultdict
from fractions import Fraction
from math import gcd,lcm
import json,platform,hashlib,importlib.util,sys
import mpmath as mp
import exact_inverse as E
from validate_sine_patch import endpoint_profile
R=Path(__file__).resolve().parent
CONFIG={'equations':['K(w)=8*10**len(w)-9*val(w)','H=K/7**v7(K)','Amax=number of j>=0 with343**j<=10**ell','Qeffective=M/gcd(9,M)'],
 'units':'dimensionless exact integers; conditional entropies in bits',
 'words_all_lengths':[0,6],'inverse_roundtrips_max_length':4,'erasure_primes':[2,5,7,11,17,19,31,73,101],
 'length_examples':[0,1,2,3,6,10,20,50,100,1000],
 'DFA_modular_lengths':[0,3],'moduli':[1,80],'DFA_bounded_lengths':[0,30],
 'entropy_cutoff_f_inclusive':25,'interval_decimal_precision':80,
 'python':platform.python_version(),'mpmath':mp.__version__}
print('CONFIGURATION BEFORE COMPUTATION\n'+json.dumps(CONFIG,indent=2),flush=True)
rows=[];roundtrips=0
for ell in range(7):
    labels=Counter()
    for s in range(10**ell):
        n=8*10**ell-9*s;h=E.primitive(n,7);labels[h]+=1
        if ell<=4:
            w='' if not ell else str(s).zfill(ell);hp,ll,j=E.encode(w)
            assert E.decode(hp,ll,j)==w;roundtrips+=1
    hist=dict(sorted(Counter(labels.values()).items()));assert hist==E.multiplicities(ell),(ell,hist)
    assert max(labels.values())==E.max_count(ell)
    rows.append({'length':ell,'words':10**ell,'fibres':len(labels),'multiplicities':hist})
print('All small-universe distributions and inverse ranks PASS',flush=True)
sample_words=['','0','8','9','02','002','802','888','889','927','901961','59086']
prime_rows=[]
for p in CONFIG['erasure_primes']:
    d,q=E.cycle(p);assert q>10 and q%9==1
    for w in sample_words:
        h,ell,j=E.encode(w,p);assert E.decode(h,ell,j,p)==w
        h8=E.primitive(8,p);assert E.fibre_count(h8,ell,p)==E.max_count(ell,p)
    prime_rows.append({'p':p,'order_mod9':d,'q':q})
assert all(E.primitive(E.key(w),3)==E.key(w) for w in sample_words)
fusion_cases=0
sets=[set(),{2},{3},{5},{7},{2,7},{2,3},{3,7}]
for n in [8+9*k for k in range(-50,51)]:
    for a in sets:
        for b in sets:
            channels=[E.erased(n,a),E.erased(n,b)]
            got=(1 if n>0 else -1)*lcm(*map(abs,channels))
            assert got==E.erased(n,a&b);fusion_cases+=1
for p in CONFIG['erasure_primes']:
    d,_=E.cycle(p);a=8;b=8*p**d
    for extra in sets:assert E.erased(a,{p}|extra)==E.erased(b,{p}|extra)

allD=([[0]*10],{0})
no8=([[int(d==8) for d in range(10)],[1]*10],{0})
even8=([[(s+int(d==8))%2 for d in range(10)] for s in range(2)],{0})
sum3=([[(s+d)%3 for d in range(10)] for s in range(3)],{0})
transient=([[(s+1 if s<3 else 2) if d==8 else s for d in range(10)] for s in range(4)],{1,2})
dfas=[allD,no8,even8,sum3,transient];orbit_cases=0;regular_cases=0;bounded_roundtrips=0
for D,F in dfas:
    for n in [E.key(w) for w in sample_words]:
        c=E.canonical(n);o=E.prefix_orbit(D,F,c)
        assert 0<=o[0]<len(D) and 1<=o[1]<=len(D)
        for T in [0,1,2,5,20,100]:
            want=sum(E.run_dfa(D,F,'8'*t+c) for t in range(T+1))
            assert E.orbit_count(o,T)==want;orbit_cases+=1
    for h in [-1,8,782,2,17,5]:
        for L in [0,1,2,3,6,12,30]:
            words=[E.decode(h,ell,j) for ell in range(L+1) for j in range(E.fibre_count(h,ell)) if E.run_dfa(D,F,E.decode(h,ell,j))]
            assert E.regular_bounded_count(h,L,D,F)==len(words);regular_cases+=1
            ranks=[]
            for w in words:
                label,rank=E.rank_bounded(w,L,D,F);assert label==h
                assert E.decode_bounded(h,L,rank,D,F)==w;ranks.append(rank);bounded_roundtrips+=1
            assert sorted(ranks)==list(range(len(words)))

modular_cases=0;dfa_cases=0
for ell in range(4):
    m=10**ell
    for M in range(1,81):
        counts=Counter((8*m-9*s)%M for s in range(m))
        for r in range(M):
            Q,rr,n=E.modular_class(ell,M,r);assert n==counts[r];modular_cases+=1
        assert (len(counts)==m)==(M//gcd(9,M)>=m)
        if M<=20:
            for D,F in dfas[:4]:
                accepted=Counter()
                for s in range(m):
                    w='' if not ell else str(s).zfill(ell)
                    if E.run_dfa(D,F,w):accepted[(8*m-9*s)%M]+=1
                for r in [0,M//2,M-1]:
                    assert E.modular_dfa_count(ell,M,r,D,F)==accepted[r];dfa_cases+=1

maxrows=[]
for ell in CONFIG['length_examples']:
    a=E.max_count(ell);maxrows.append({'length':ell,'maximum_candidates':a,'fixed_bits':E.bits(a)})
assert E.max_count(1000)==395 and E.bits(395)==9
assert E.bounded_count(8,1000)==197913 and E.bits(197913)==18
for L in range(31):assert E.bounded_count(8,L)==sum(E.max_count(ell) for ell in range(L+1))
phase_words=['0000000','0000001']
for w in phase_words:assert E.fibre_count(E.primitive(E.key(w),7),7)==1
phase_positions=[Fraction(50000001,10**8),Fraction(50000002,10**8)]
assert len({int(x*10**7) for x in phase_positions})==1
assert len({int(x*10**8) for x in phase_positions})==2
synthetic=[[str(x),str(x)] for x in [Fraction(500000011,10**9),Fraction(500000021,10**9)]]
assert endpoint_profile(synthetic,7)['max_interior_boundaries_per_cylinder']==2
assert endpoint_profile(synthetic,8)['max_interior_boundaries_per_cylinder']==1
assert endpoint_profile([['0','0'],['1/2','1/2'],['1','1']],7)['max_interior_boundaries_per_cylinder']==0
reported_costs={n:E.bits(n) for n in [13,21,55,150]}

mp.mp.dps=100;mp.iv.dps=80;q=343;F=25;n=F+1;x=Fraction(1,q)
tail=Fraction((q-1)**2,q**(n+1))*(Fraction(n*n,1)/(1-x)+Fraction(2*n,1)*x/(1-x)**2+x*(1+x)/(1-x)**3)
assert tail<Fraction(280,10**63)
ent=mp.iv.mpf(0);lengthmean=mp.iv.mpf(0)
for f in range(2,F+1):
    mass=mp.iv.mpf((q-1)**2*f)/q**(f+1)
    ent+=mass*mp.iv.ln(f)/mp.iv.ln(2);lengthmean+=mass*E.bits(f)
t=mp.iv.mpf(tail.numerator)/tail.denominator
def bracket(v):return {'lower':mp.nstr(mp.mpf(v._mpi_[0]),82),'upper_including_tail':mp.nstr(mp.mpf((v+t)._mpi_[1]),82)}
entropy={'cutoff_inclusive':F,'tail_upper_rational':[tail.numerator,tail.denominator],
 'entropy_interval_bits':bracket(ent),'mean_fixed_index_length_interval_bits':bracket(lengthmean),
 'rounding_contract':'mpmath interval arithmetic with 80 decimal digits; geometric tail is an exact rational upper bound for both quantities'}
out={'status':'PASS','configuration':CONFIG,'direct_word_distributions':rows,'inverse_roundtrips':roundtrips,
 'prime_dichotomy_checks':prime_rows,'prime_erasure_fusion_cases':fusion_cases,'unary_orbit_cases':orbit_cases,
 'regular_bounded_count_cases':regular_cases,'bounded_regular_rank_roundtrips':bounded_roundtrips,'modular_classes_checked':modular_cases,'modular_DFA_cases':dfa_cases,
 'maximum_examples':maxrows,'bounded_L1000':197913,'entropy':entropy,
 'phase_contract_check':{'singleton_example_words':phase_words,'positions':[str(x) for x in phase_positions],
 'shared_prefix_digits':7,'separated_at_digits':8,'reported_state_count_costs':reported_costs,
 'actual_15_family_or_1922_endpoint_census':'NOT_REPLAYED: original definitions and endpoint list were not available; costs are conditional on the reported cardinalities.'},
 'non_claims':['Finite computations do not prove non-context-freeness or natural boundaries; the manuscript gives proofs with checked classical inputs.',
 'Historical FST12/FST13 Python suites and ZIPs were not supplied; no historical 47/20/15 replay is claimed.',
 'No temporal optimality or global RGphi realization closure.']}
(R/'EXACT_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['status','inverse_roundtrips','prime_erasure_fusion_cases','unary_orbit_cases','regular_bounded_count_cases','modular_classes_checked','modular_DFA_cases','maximum_examples','bounded_L1000','entropy']},indent=2))
