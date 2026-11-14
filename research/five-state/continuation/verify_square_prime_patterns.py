"""Count exact first-prime patterns and certify their lifts in the five shifts."""
from itertools import combinations

from sympy import Matrix, factorint
from verify_exceptional_crt import ACTIONS


def charts(code, r, j):
    a, q, c, e = tuple(Matrix.eye(4).row(i) for i in range(4))
    t, s, strict = ACTIONS[code]
    if code == 119772:
        d = r * e - j * a
        states = ((a, q), (c, d), (c, q), (a, e), (r*a, d))
        return (a, q, c, d, e), states, (t, s), strict
    d = c
    c = 3*e-q
    states = ((a,q),(c,d),(e,q),(c,3*q),(a,d))
    return (a,q,c,d,e), states, (t, s), strict


def certify_lifts(forms, states, actions, strict, r):
    for i, form in enumerate(forms):
        for sign in ((1, -1) if i < 4 else (1,)):
            _, *remainders = edge_rows(states, actions, strict, r, [form], sign, None)
            if i == 4:
                assert all(remainder.is_zero_matrix for remainder in remainders)
                continue
            basis = Matrix.vstack(form, remainders[0]).T
            for remainder in remainders:
                coeffs, _ = basis.gauss_jordan_solve(remainder.T)
                assert all(set(factorint(int(value.q))) <= {2, 3} for value in coeffs)


def local_projection_mod_four(code, r, j):
    """Return exact state counts at depth one and two at the prime two."""
    from itertools import product
    from math import gcd

    _, states, actions, strict = charts(code, r, j)
    def count(modulus):
        total = 0
        for point in product(range(modulus), repeat=4):
            pairs = [(sum(int(t)*x for t,x in zip(u,point)),
                      sum(int(t)*x for t,x in zip(v,point))) for u,v in states]
            if any(gcd(2, u, v) != 1 for u,v in pairs):
                continue
            for b in range(modulus):
                admissible = True
                for letter, action in enumerate(actions):
                    for i, target in enumerate(action):
                        x, y = pairs[i]
                        u, v = pairs[target]
                        factor = r if (letter,i) == strict else 1
                        source = y if letter == 0 else x
                        remainder = b*x-factor*u if letter == 0 else b*(y-x)-factor*(v-u)
                        divisor = gcd(modulus, source)
                        if remainder % divisor or gcd(b,divisor) != gcd(factor,divisor):
                            admissible = False
                            break
                    if not admissible:
                        break
                if admissible:
                    total += 1
                    break
        return total
    return count(2), count(4)


def edge_rows(states, actions, strict, r, mask, b, p):
    result = list(mask)
    for letter, action in enumerate(actions):
        for i, target in enumerate(action):
            x, y = states[i]
            u, v = states[target]
            factor = r if (letter,i) == strict else 1
            divisor = y if letter == 0 else x
            def same_modulus(row):
                minors = [int(row[k]*divisor[l]-row[l]*divisor[k])
                          for k,l in combinations(range(4),2)]
                return all(n % p == 0 if p else n == 0 for n in minors)

            if not any(same_modulus(row) for row in mask):
                continue
            result.append(b*x-factor*u if letter == 0 else b*(y-x)-factor*(v-u))
    return result


def rank_mod(rows, p):
    rows = [[int(x) % p for x in row] for row in rows]
    rank = 0
    for col in range(4):
        pivot = next((i for i in range(rank,len(rows)) if rows[i][col]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        leading = pow(rows[rank][col], -1, p)
        for i in range(rank+1,len(rows)):
            multiple = rows[i][col]*leading
            rows[i] = [(x-multiple*y) % p for x,y in zip(rows[i],rows[rank])]
        rank += 1
    return rank


def generic_rank(rows, bad):
    if not rows:
        return 0
    mat = Matrix.vstack(*rows)
    pivots = mat.rref()[1]
    rank = len(pivots)
    if rank:
        basis = mat[:,list(pivots)].T.rref()[1]
        witness = mat.extract(basis, pivots).det()
        bad.update(factorint(abs(int(witness))))
    return rank


def subsets(values):
    for size in range(len(values)+1):
        yield from combinations(values,size)


def mask_counts(code,r,j,p=None,bad=None):
    forms, states, actions, strict = charts(code,r,j)
    rank = (lambda rows: generic_rank(rows,bad)) if p is None else (lambda rows: rank_mod(rows,p))
    # At odd primes prime to r, distinct core moduli cannot both vanish
    # by the exact overlap criterion. If E vanishes, the base must be +1.
    for first, second in combinations(forms, 2):
        assert rank([first, second]) == 2
    if p is None:
        certify_lifts(forms, states, actions, strict, r)
    answer = {}
    for mask in ((), *((i,) for i in range(5)), *((i,4) for i in range(4))):
        vanished = [forms[i] for i in mask]
        units = [form for i,form in enumerate(forms) if i not in mask]
        signs = (1,) if 4 in mask else (1,-1) if mask else (1,)
        for sign in signs:
            rows = edge_rows(states,actions,strict,r,vanished,sign,p)
            if mask and mask != (4,):
                assert rank(rows) == len(mask)+1
            for numerator, denominator in states:
                if rank([*vanished,numerator]) == len(vanished) and rank(
                    [*vanished,denominator]
                ) == len(vanished):
                    rows = [*Matrix.eye(4).tolist()]
                    rows = [Matrix([row]) for row in rows]
                    break
            polynomial = [0]*5
            for subset in subsets(units):
                polynomial[4-rank([*rows,*subset])] += (-1)**len(subset)
            answer[mask,sign] = tuple(polynomial)
    return answer


if __name__ == "__main__":
    for code,r,j in ((119772,2,-1),(119772,2,1),(119772,3,1),(119772,3,2),(606897,3,0)):
        bad = {r}
        generic = mask_counts(code,r,j,bad=bad)
        assert bad <= {2,3}
        for prime in (3,5,7,11,17,31):
            if prime in bad:
                continue
            actual = mask_counts(code,r,j,p=prime)
            assert actual == generic
        leading = [sum(coef[i] for coef in generic.values()) for i in range(5)]
        assert leading == [11,-22,14,-4,1]
        assert all(any(generic[(i,),sign]) for i in range(4) for sign in (-1,1))
        print(code,r,j,"exceptional",sorted(bad),"state projections",leading,
              "depths 1 and 2 at the prime two",local_projection_mod_four(code,r,j),
              "mask/sign counts",generic,flush=True)
