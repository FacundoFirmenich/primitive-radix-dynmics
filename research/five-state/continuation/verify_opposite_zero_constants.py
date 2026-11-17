"""Exhaust the vanishing complementary constants in the residual square cycles."""

import json
import sys
from collections import Counter
from functools import lru_cache
from itertools import product
from math import gcd, lcm

from verify_exceptional_crt import ACTIONS, edge_certificate, states_for
from verify_square_cycle_fibres import square_cycle_conditions
from verify_square_prime_support import SYSTEMS


def det(a, b):
    return a[0]*b[1] - a[1]*b[0]


def evaluate(form, u, v):
    return form[0]*u + form[1]*v


@lru_cache(maxsize=None)
def positive_divisors(n):
    result = set()
    divisor = 1
    while divisor*divisor <= n:
        if n % divisor == 0:
            result.update((divisor, n//divisor))
        divisor += 1
    return tuple(sorted(result))


def line_catalogue(coefficients):
    """Use the two neighboring coordinates as projective parameters."""
    lines = set()
    for i in range(4):
        y, z, opposite = (i+1) % 4, (i-1) % 4, (i+2) % 4
        a, b = coefficients[i]
        for sy, sz, sign in product((-1, 1), repeat=3):
            # L_y = p*x_i+q*x_opposite, L_z = s*x_i+t*x_opposite.
            p, q = sy*coefficients[y][1], coefficients[y][0]
            s, t = coefficients[z][0], sz*coefficients[z][1]
            for k in range(-8*max(a,b)+1, 8*(a+b)):
                if k == 0:
                    continue
                rows = [None]*4
                rows[y], rows[z] = (1, 0), (0, 1)
                rows[i] = (2*a, 2*sign*b)
                rows[opposite] = (-2*a*q*s, -2*sign*b*t*p)
                den = lcm(abs(k), abs(k*q*t))
                result = [
                    (den, 0) if j == y else (0, den) if j == z else
                    tuple(n*(den//k) for n in rows[j]) if j == i else
                    tuple(n*(den//(k*q*t)) for n in rows[j])
                    for j in range(4)
                ]
                content = gcd(*(n for row in result for n in row))
                lines.add((y, z, tuple(tuple(n//content for n in row) for row in result)))
    return sorted(lines)


def small_forms(rows, coefficients, normalization):
    """For each obstruction return an integer bound on its linear form."""
    result = []
    for i in range(4):
        u, v = (i+1) % 4, (i-1) % 4
        f = rows[i]
        content = gcd(*f)
        primitive = tuple(c//content for c in f)
        if det(f, rows[u]) == 0 or det(f, rows[v]) == 0:
            result.append((normalization, primitive))
        a, b = coefficients[i]
        alpha = a*det(primitive, rows[u])
        beta = b*det(primitive, rows[v])
        obstruction = alpha*alpha-beta*beta
        if obstruction:
            result.append((abs(obstruction), primitive))
    return result


def chamber_forms(code, r, rows):
    a, q, c, d = rows
    def difference(left, right, scale=1):
        return tuple(x-scale*y for x,y in zip(left,right))
    def twice(row):
        return tuple(2*x for x in row)
    if code == 119772:
        return (*rows, difference(c,a), difference(q,c), difference(twice(a),q),
                difference(d,a,r), difference(twice(c),d))
    return (*rows, difference(twice(c),q,3), difference(d,c),
            difference(twice(a),d), difference(q,a))


def inverse_values(form, value, limit, inequalities):
    """Enumerate primitive parameters on the affine line inside the chamber."""
    a, b = form
    if b:
        base_u = value*pow(a, -1, abs(b)) % abs(b)
        base_v = (value-a*base_u)//b
        step_u, step_v = b, -a
    else:
        base_u, base_v = value//a, 0
        step_u, step_v = 0, 1
    constraints = [(evaluate(row,base_u,base_v),evaluate(row,step_u,step_v))
                   for row in inequalities]
    constraints.extend(((base_u,step_u),(base_v,step_v),
                        (limit+1-base_u,-step_u),(limit+1-base_v,-step_v)))
    # If b is nonzero, the u bound and 0 <= base_u < |b| imply this range.
    # Otherwise t is v itself.
    low, high = -limit-1, limit+1
    for at_zero, slope in constraints:
        if slope > 0:
            low = max(low, (-at_zero)//slope + 1)
        elif slope < 0:
            high = min(high, (at_zero-1)//(-slope))
        elif at_zero <= 0:
            return
    for t in range(low,high+1):
        u,v = base_u+t*step_u, base_v+t*step_v
        if gcd(u,v) == 1:
            yield u,v


def candidate_cores(code, factor, coefficients, catalogue):
    candidates = set()
    statistics = Counter()
    for y, z, rows in catalogue:
        k = rows[y][0]
        assert rows[z] == (0,k) and k > 0
        best = None
        bounds = sorted(small_forms(rows, coefficients, k))
        for bound, form in bounds:
            # Only coordinates whose normalized value can be H/4 or bigger qualify.
            content = max(gcd(*row) for row in rows
                          if tuple(c//gcd(*row) for c in row) == form)
            # The u/v coordinate forms are k*u and k*v. Highness yields Hparam <= this bound.
            limit = 4*bound*content//k
            if best and limit//max(1,abs(form[1])) > best[0]:
                continue
            values = positive_divisors(bound)
            cost = (len(values)*max(1, limit//max(1,abs(form[1]))), limit, form, values)
            if best is None or cost < best:
                best = cost
        if best is None:
            raise ArithmeticError(("No line obstruction", rows))
        _, limit, form, values = best
        statistics["parameter_bound_max"] = max(statistics["parameter_bound_max"],limit)
        inequalities = chamber_forms(code,factor,rows)
        for value in values:
            for u,v in inverse_values(form,value,limit,inequalities):
                raw = tuple(evaluate(row,u,v) for row in rows)
                if min(raw) <= 0 or max(raw) >= 4*min(raw):
                    continue
                g = gcd(*raw)
                core = tuple(c//g for c in raw)
                if any(gcd(core[i],core[(i+1)%4]) != 1 for i in range(4)):
                    continue
                if any((a*a*core[(i+1)%4]**2-b*b*core[(i-1)%4]**2)%core[i]
                       for i,(a,b) in enumerate(coefficients)):
                    continue
                candidates.add(core)
    return candidates, dict(statistics)


def replay():
    results = []
    for code, factor, shifts, coefficients in SYSTEMS:
        catalogue = line_catalogue(coefficients)
        cores, bounds = candidate_cores(code, factor, coefficients, catalogue)
        realizations = {}
        for a,q,c,d in sorted(cores):
            for shift in shifts:
                e_num = d+shift*a if code == 119772 else c+q
                if e_num % factor:
                    continue
                tup = (a,c,d,q,e_num//factor)
                states = states_for(code,factor,*tup)
                if not states or not square_cycle_conditions(code,factor,*tup):
                    continue
                cert = edge_certificate(states,*ACTIONS[code],factor)
                if cert is not None:
                    realizations[tup] = cert
        results.append({
            "code": code, "factor": factor, "line_parameterizations": len(catalogue),
            **bounds, "primitive_square_cores": sorted(cores),
            "realizations": sorted(realizations.items()),
        })
        print(f"verified {code}/{factor}: {len(catalogue)} line parameterizations", file=sys.stderr, flush=True)
    return results


if __name__ == "__main__":
    print(json.dumps(replay(),indent=2))
