"""Independent finite-domain and root completeness checks; exact arithmetic."""
import hashlib
import json
from math import gcd, isqrt
from pathlib import Path
import time
import boundary_census as fast

ROOT=Path(__file__).resolve().parent


def trial_divisors(n):
    small=[d for d in range(1,isqrt(n)+1) if n%d==0]
    return small+[n//d for d in reversed(small) if d*d!=n]


def direct_boundary(T):
    # Deliberately no unity roots or SPF table. Each allowed C is tested.
    triples=[]
    fours=[]
    for t in range(1,T+1):
        for u in range(1,(3*t-2)//2+1):
            if u==t:
                continue
            for a in trial_divisors(abs(t*t-u*u)):
                if a<=6*t or a%3==0 or gcd(a,t*u)!=1:
                    continue
                q,e,d=a-u,a-t,2*a-3*t
                if q%3==0 or e%3==0:
                    continue
                for c in range(d+1,2*q):
                    if c%3==0 or gcd(c,q*d)!=1:
                        continue
                    if (c*c-a*a)%q or (c*c-9*a*a)%d:
                        continue
                    coords=(a,c,d,q,e)
                    triples.append(coords)
                    if (d*d-q*q)%c==0:
                        fours.append(coords)
    return sorted(triples),sorted(fours)


def quartic_human_certificate():
    # Quartic proof: on A=0, divisibility by D²-9Q² plus the other
    # ideals permits only k_A*C²*(D²-9Q²); analogous formulas hold.
    # Pairwise coordinate-plane intersections force these four equations.
    import sympy as s
    ka,kq,kc,kd=s.symbols('k_A k_Q k_C k_D')
    matrix,_=s.linear_eq_to_matrix([ka-kq,kq+kc,kc-9*kd,kd+9*ka],(ka,kq,kc,kd))
    assert matrix.det()!=0
    return {'coefficient_matrix':[[int(x) for x in row] for row in matrix.tolist()],
            'determinant':int(matrix.det()),'consequence':'all k_i vanish; P is a multiple of A*C*D*Q'}


if __name__=='__main__':
    config={'root_moduli_inclusive':[2,2500],'direct_census_max_t':180,
            'units':'dimensionless','arithmetic':'exact integer/rational',
            'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    print(json.dumps(config),flush=True)
    start=time.monotonic()
    roots=fast.make_roots(fast.smallest_prime_table(2501))
    for n in range(2,2501):
        direct=[x for x in range(n) if x*x%n==1]
        assert sorted(roots(n))==direct,(n,roots(n),direct)
    r=fast.census(180)
    t3,t4=direct_boundary(180)
    assert t3==sorted(tuple(x['core']) for x in r['three_square_samples'])
    assert t4==sorted(tuple(x['core']) for x in r['samples'])
    # Algebraic completeness, independent of software: t+u<5t/2,
    # and u<t or t<u<3t/2 imply 0<|t²-u²|<5t²/4.
    # Check the parametrization and the four congruence expansions over Q.
    import sympy as s
    a,t,u,v,z=s.symbols('A t u v z')
    q,e,d,c=a-u,a-t,2*a-3*t,2*a-2*u-v
    assert s.expand(s.rem(d*d-9*q*q,a,a)-9*(t*t-u*u))==0
    assert s.expand(s.rem(c*c-a*a,a-u,a)-(v*v-u*u))==0
    assert s.expand(c-d-(3*t-2*u-v))==0
    assert s.expand(s.rem(4*(d*d-q*q),c,a)-(4*(3*t-2*u-v)**2-v*v))==0
    result={'config':config,'all_roots_complete':True,'direct_vs_roots_census_equal':True,
            'three_square_cores_at_180':t3,'four_square_cores_at_180':t4,
            'quartic_certificate':quartic_human_certificate(),'symbolic_boundary_identities':True,
            'seconds':time.monotonic()-start}
    (ROOT/'INDEPENDENT_VALIDATION.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='config'},indent=2),flush=True)
