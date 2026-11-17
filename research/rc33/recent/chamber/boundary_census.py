"""Complete finite census by t=A-E in the reflected 606897/3 chamber."""
import argparse
from array import array
from collections import Counter
from functools import lru_cache
from fractions import Fraction
from itertools import product
from math import gcd, isqrt, lcm
from pathlib import Path
import hashlib
import json
import platform
import time

ROOT = Path(__file__).resolve().parent
KNOWN = (406, 712, 1265, 731, 557)
KNOWN_CRT = (88011536665779, 223336848698040)
T_INDEX = (1, 0, 3, 2, 4)
S_INDEX = (4, 2, 1, 0, 0)


def merge_residues(residues):
    b, m = 0, 1
    for r, n in residues:
        g = gcd(m, n)
        if (r-b) % g:
            return None
        step = ((r-b)//g * pow(m//g, -1, n//g)) % (n//g)
        b, m = (b+m*step) % lcm(m, n), lcm(m, n)
    return b, m


def transform(x, base, letter):
    if letter == 'S':
        y = base*(1/x-1)
        y -= y.numerator//y.denominator
        return 1/(1+y)
    y = base*x
    return y-y.numerator//y.denominator


def full_edge_crt(coords, reflected=True):
    a, c, d, q, e = coords
    pairs = ((q,a),(q,c),(d,c),(d,3*a),(e,a)) if reflected else (
        (a,q),(c,q),(c,d),(3*a,d),(a,e))
    if any(gcd(p,v) != 1 for p,v in pairs):
        return None
    states = tuple(Fraction(p,v) for p,v in pairs)
    if len(set(states)) != 5 or any(not Fraction(1,2)<x<1 for x in states):
        return None
    maps = (S_INDEX,T_INDEX) if reflected else (T_INDEX,S_INDEX)
    strict_letter = 0 if reflected else 1
    residues = []
    for li, mapping in enumerate(maps):
        for i, j in enumerate(mapping):
            x, y = states[i], states[j]
            p, q0, u, v = x.numerator, x.denominator, y.numerator, y.denominator
            delta = 3 if (li,i)==(strict_letter,3) else 1
            if (q0 if li == 0 else p) != delta*(v if li == 0 else u):
                return None
            modulus, coeff, rhs = (q0,p,delta*u) if li==0 else (p,q0-p,delta*(v-u))
            residue = rhs*pow(coeff,-1,modulus) % modulus
            if gcd(residue,modulus) != delta:
                return None
            residues.append((residue,modulus))
    crt = merge_residues(residues)
    if crt is None:
        return None
    b, period = crt
    base = b if b>=2 else b+period
    for li, mapping in enumerate(maps):
        for i, j in enumerate(mapping):
            assert transform(states[i],base,'TS'[li]) == states[j]
            delta = gcd(base, states[i].denominator if li==0 else states[i].numerator)
            assert delta == (3 if (li,i)==(strict_letter,3) else 1)
    return crt


def reduced_crt(coords):
    a,c,d,q,e = coords
    if any(x%3==0 for x in coords):
        return None
    if any(gcd(x,y)!=1 for x,y in ((a,q),(a,d),(a,e),(c,q),(c,d))):
        return None
    if any(n%m for m,n in ((a,d*d-9*q*q),(c,d*d-q*q),
                            (d,c*c-9*a*a),(q,c*c-a*a))):
        return None
    return merge_residues(((e*pow(q,-1,a),a),(c*pow(a,-1,q),q),
                           (d*pow(q,-1,c),c),(3*a*pow(c,-1,d),d),(1,e),(0,3)))


def smallest_prime_table(n):
    spf = array('I', range(n+1))
    for p in range(2,isqrt(n)+1):
        if spf[p] == p:
            for k in range(p*p,n+1,p):
                if spf[k] == k:
                    spf[k] = p
    return spf


def factor(n,spf):
    r = {}
    while n>1:
        p = spf[n]
        r[p] = r.get(p,0)+1
        n //= p
    return r


def product_divisors(x,y,spf):
    f = factor(x,spf)
    for p,e in factor(y,spf).items():
        f[p] = f.get(p,0)+e
    div = [1]
    for p,e in f.items():
        div = [d*p**k for d in div for k in range(e+1)]
    return div


def make_roots(spf):
    @lru_cache(maxsize=100000)
    def roots(n):
        local = []
        for p,k in factor(n,spf).items():
            m = p**k
            choices = (1,m-1) if p!=2 or k==2 else ((1,) if k==1 else (1,m-1,1+m//2,m//2-1))
            local.append((m,choices))
        # Pairwise-coprime prime powers, including all four 2-adic roots.
        values = (0,)
        modulus = 1
        for m, choices in local:
            values = tuple((v+modulus*((r-v)*pow(modulus,-1,m)%m))%(modulus*m)
                           for v in values for r in choices)
            modulus *= m
        assert modulus == n
        return values
    return roots


def census(T):
    start = time.monotonic()
    # A <= |t²-u²| < 5T²/4, hence Q is smaller still.
    spf = smallest_prime_table(max(3*T,5*T*T//4)+1)
    roots = make_roots(spf)
    counts = Counter()
    samples, three_samples, hits = [], [], []
    digest = hashlib.sha256()
    for t in range(1,T+1):
        for u in range(1,(3*t-2)//2+1):
            counts['tu_pairs'] += 1
            if u==t:
                counts['duplicate_Q_E'] += 1
                continue
            for a in product_divisors(t+u,abs(t-u),spf):
                if a<=6*t:
                    continue
                counts['A_divisor_candidates'] += 1
                if a%3==0 or gcd(a,t*u)!=1:
                    continue
                q,e,d = a-u,a-t,2*a-3*t
                if q%3==0 or e%3==0:
                    continue
                counts['primitive_A_Q_E_candidates'] += 1
                for root in roots(q):
                    v = u*root % q
                    z = 3*t-2*u-v
                    if not v>0 or not z>0:
                        continue
                    counts['Q_square_candidates'] += 1
                    c = d+z
                    if c%3==0 or gcd(c,q*d)!=1:
                        continue
                    counts['primitive_core_candidates'] += 1
                    coords = (a,c,d,q,e)
                    if (c*c-9*a*a)%d:
                        continue
                    counts['three_square_candidates'] += 1
                    if len(three_samples)<1000:
                        three_samples.append({'core':coords,'t_u_v_z':(t,u,v,z),
                                              'fourth_remainder':(d*d-q*q)%c})
                    if (d*d-q*q)%c:
                        continue
                    counts['four_square_candidates'] += 1
                    digest.update((','.join(map(str,coords))+'\n').encode())
                    crt = reduced_crt(coords)
                    direct = full_edge_crt(coords)
                    assert crt == direct, (coords,crt,direct)
                    if len(samples)<50:
                        samples.append({'core':coords,'t_u_v_z':(t,u,v,z),'crt':crt})
                    if crt is not None:
                        hits.append({'core':coords,'crt':crt})
                if t%200==0 and counts['primitive_A_Q_E_candidates']%50000==0:
                    print(json.dumps({'progress_t':t,'counts':dict(counts)}),flush=True)
    return {'maximum_t':T,'coverage':'all integer tuples in the open reflected chamber with 1<=A-E<=T',
            'does_not_assume_h14_certificate':True,'counts':dict(counts),
            'four_square_candidates_sha256':digest.hexdigest(),'samples':samples,
            'three_square_samples':three_samples,
            'realizations':hits,'roots_cache':str(roots.cache_info()),
            'seconds':time.monotonic()-start}


if __name__=='__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--max-t',type=int,default=600)
    args = ap.parse_args()
    if args.max_t<1:
        ap.error('max-t must be positive')
    config = {'max_t':args.max_t,'arithmetic':'exact integer/rational',
              'units':'dimensionless','equations':['A | t²-u²','A>6t',
              '2u+v+z=3t','Q | v²-u²'],'python':platform.python_version(),
              'known_core':KNOWN,'known_crt':KNOWN_CRT,
              'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    print(json.dumps(config,ensure_ascii=False),flush=True)
    assert reduced_crt(KNOWN)==KNOWN_CRT
    assert full_edge_crt(KNOWN,reflected=False)==KNOWN_CRT
    assert full_edge_crt(KNOWN,reflected=True) is None
    result={'config':config,'positive_control':'passed','census':census(args.max_t)}
    (ROOT/f'BOUNDARY_CENSUS_T{args.max_t}.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2),flush=True)
