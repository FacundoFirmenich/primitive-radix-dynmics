"""Exact opposite-coordinate reconstruction by a two-residue hash join."""
from collections import defaultdict
from functools import lru_cache
from math import gcd, prod
from sympy import factorint
from fibre_arithmetic import prime, ArithmeticDeferred, chamber, primitive, rem, complete


@lru_cache(maxsize=50000)
def factors(n):
    n = abs(int(n))
    if not n:
        raise ArithmeticDeferred('Zero numerator: this divisor fibre is not finite')
    ff = tuple(sorted((int(p), int(e)) for p, e in factorint(n).items()))
    if prod(p**e for p, e in ff) != n:
        raise ArithmeticDeferred('Incomplete factorization')
    for p, _ in ff:
        prime(p)
    return ff


def divisors_product(a, b):
    ff = defaultdict(int)
    for n in (a, b):
        for p, e in factors(n):
            ff[p] += e
    values = [1]
    for p, e in sorted(ff.items()):
        values = [v * p**k for v in values for k in range(e + 1)]
    assert len(values) == prod(e + 1 for e in ff.values())
    return values


def paired(r, orientation, unknown, fixed):
    """All square cores in this fixed-opposite-pair fibre, not a height sample.

    unknown='AC' fixes (D,Q); unknown='DQ' fixes (A,C).
    Each returned core is in common order (A,C,D,Q).
    """
    if r not in (2, 3) or orientation not in ('normal', 'reflected'):
        raise ValueError('Undeclared parameter regime')
    if orientation == 'reflected' and r != 3:
        raise ValueError('The reflected target has r=3')
    u, v = map(int, fixed)
    if min(u, v) <= 0:
        raise ValueError('Positive fixed coordinates required')
    result = dict(r=r, orientation=orientation, unknown=unknown,
                  fixed=[u, v], divisor_counts=[0, 0], candidate_counts=[0, 0],
                  cartesian_pairs=0, first_residue_pairs=0,
                  second_residue_pairs=0, joint_pairs=0, square_cores=[], realizations=[])
    if gcd(r, u*v) != 1 or (r-1) % gcd(u, v):
        result['empty_reason'] = 'fixed units or opposite gcd'
        return result
    if unknown == 'AC':
        D, Q = u, v
        # Every target chamber has Q<D<2Q.
        if not Q < D < 2*Q:
            result['empty_reason'] = 'fixed chamber projection'
            return result
        raw_left = divisors_product(D-r*Q, D+r*Q)
        raw_right = divisors_product(D-Q, D+Q)
        if orientation == 'reflected':
            in_left = lambda A: Q < A and 3*A < 2*D
            in_right = lambda C: D < C < 2*Q
        else:
            in_left = lambda A: Q < 2*A and r*A < D
            in_right = lambda C: D < 2*C and C < Q
        sig_left = lambda A: (r*r*A*A % D, A*A % Q)
        sig_right = lambda C: (C*C % D, C*C % Q)
        make_core = lambda A, C: (A, C, D, Q)
    elif unknown == 'DQ':
        A, C = u, v
        if not A < C < 2*A:
            result['empty_reason'] = 'fixed chamber projection'
            return result
        raw_left = divisors_product(C-r*A, C+r*A)
        raw_right = divisors_product(C-A, C+A)
        if orientation == 'reflected':
            in_left = lambda D: 3*A < 2*D and D < C
            in_right = lambda Q: C < 2*Q and Q < A
        else:
            in_left = lambda D: r*A < D < 2*C
            in_right = lambda Q: C < Q < 2*A
        sig_left = lambda D: (D*D % A, D*D % C)
        sig_right = lambda Q: (r*r*Q*Q % A, Q*Q % C)
        make_core = lambda D, Q: (A, C, D, Q)
    else:
        raise ValueError('unknown must be AC or DQ')
    result['divisor_counts'] = [len(raw_left), len(raw_right)]
    good = lambda n: gcd(r, n) == 1 and gcd(n, u) == gcd(n, v) == 1
    left = [n for n in raw_left if in_left(n) and good(n)]
    right = [n for n in raw_right if in_right(n) and good(n)]
    result['candidate_counts'] = [len(left), len(right)]
    result['cartesian_pairs'] = len(left)*len(right)
    buckets = defaultdict(list)
    marginal0, marginal1 = defaultdict(int), defaultdict(int)
    for b in right:
        sig = sig_right(b)
        buckets[sig].append(b)
        marginal0[sig[0]] += 1
        marginal1[sig[1]] += 1
    for a in left:
        sig = sig_left(a)
        result['first_residue_pairs'] += marginal0[sig[0]]
        result['second_residue_pairs'] += marginal1[sig[1]]
        for b in buckets.get(sig, ()):
            result['joint_pairs'] += 1
            x = make_core(a, b)
            assert not any(rem(r, x))
            if chamber(r, x, orientation) and primitive(r, x):
                result['square_cores'].append(x)
                result['realizations'].extend(complete(r, x, orientation))
    result['square_cores'].sort()
    return result


def neighbours(r, orientation, unknown, fixed):
    """All chamber/gcd-admissible paired divisor endpoints, including partial cores.

    This broader operation is for exploration only; paired() is the exact
    full-core completion instrument.
    """
    u, v = map(int, fixed)
    if gcd(r, u*v) != 1 or (r-1) % gcd(u, v):
        return []
    if unknown == 'AC':
        D, Q = u, v
        if not Q < D < 2*Q:
            return []
        left = divisors_product(D-r*Q, D+r*Q)
        right = divisors_product(D-Q, D+Q)
        make = lambda a, c: (a, c, D, Q)
    elif unknown == 'DQ':
        A, C = u, v
        if not A < C < 2*A:
            return []
        left = divisors_product(C-r*A, C+r*A)
        right = divisors_product(C-A, C+A)
        make = lambda d, q: (A, C, d, q)
    else:
        raise ValueError(unknown)
    out = []
    # Filter independent bounds before the product, then the exact chamber.
    if unknown == 'AC':
        if orientation == 'reflected':
            left = [a for a in left if Q < a and 3*a < 2*D]
            right = [c for c in right if D < c < 2*Q]
        else:
            left = [a for a in left if Q < 2*a and r*a < D]
            right = [c for c in right if D < 2*c and c < Q]
    elif orientation == 'reflected':
        left = [d for d in left if 3*A < 2*d and d < C]
        right = [q for q in right if C < 2*q and q < A]
    else:
        left = [d for d in left if r*A < d < 2*C]
        right = [q for q in right if C < q < 2*A]
    good = lambda n: gcd(r, n) == 1 and gcd(n, u) == gcd(n, v) == 1
    left, right = list(filter(good, left)), list(filter(good, right))
    for a in left:
        for b in right:
            x = make(a, b)
            if chamber(r, x, orientation) and primitive(r, x):
                out.append(x)
    return sorted(set(out))
