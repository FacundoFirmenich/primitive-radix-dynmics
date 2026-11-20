"""Exact Argüelles Loom / Mayan Factor computational bridge for RGΦ RC3.3.

Provenance: José Argüelles, The Mayan Factor (1987), ch. 4 and appendices;
52 GAP kin independently cross-checked against tzolkin.io (2021).
The 52-portal shape and modern Dreamspell castles are NOT attributed to the
pre-Columbian calendar. Nothing here asserts an arithmetic exclusion theorem
for the unsolved five-state RGΦ orientation.
Python 3.10+, standard library only. Source units: kin, not physical time.
"""
from __future__ import annotations

from collections import Counter
from fractions import Fraction
from itertools import product
from math import gcd, lcm
from typing import Iterable

# The 52 positions are copied as discrete numeric mathematical data, not artwork.
PORTALS = frozenset((
    1, 20, 22, 39, 43, 50, 51, 58, 64, 69, 72, 77, 85, 88, 93, 96,
    106, 107, 108, 109, 110, 111, 112, 113, 114, 115,
    146, 147, 148, 149, 150, 151, 152, 153, 154, 155,
    165, 168, 173, 176, 184, 189, 192, 197, 203, 210, 211, 218,
    222, 239, 241, 260,
))

# Franklin's original 8x8 semi-magic square: sum of each row, column, 2x2
# toroidal sub-square and every bent diagonal is 260 (not ordinary diagonals).
FRANKLIN = (
    (52, 61, 4, 13, 20, 29, 36, 45),
    (14, 3, 62, 51, 46, 35, 30, 19),
    (53, 60, 5, 12, 21, 28, 37, 44),
    (11, 6, 59, 54, 43, 38, 27, 22),
    (55, 58, 7, 10, 23, 26, 39, 42),
    (9, 8, 57, 56, 41, 40, 25, 24),
    (50, 63, 2, 15, 18, 31, 34, 47),
    (16, 1, 64, 49, 48, 33, 32, 17),
)


def require_kin(kin: int) -> int:
    if type(kin) is not int or not 1 <= kin <= 260:
        raise ValueError('kin debe ser entero de 1..260')
    return kin


def coordinates(kin: int) -> tuple[int, int]:
    """0-based row (seal), column (20-kin segment)."""
    return divmod(require_kin(kin) - 1, 20)[::-1]


def kin_at(row: int, col: int) -> int:
    if type(row) is not int or type(col) is not int or not 0 <= row < 20 or not 0 <= col < 13:
        raise ValueError('coordenadas fuera de 20x13')
    return 1 + row + 20 * col


def tone(kin: int) -> int:
    return (require_kin(kin) - 1) % 13 + 1


def seal(kin: int) -> int:
    return (require_kin(kin) - 1) % 20 + 1


def occult(kin: int) -> int:
    return 261 - require_kin(kin)


def row_reflection(kin: int) -> int:
    row, col = coordinates(kin)
    return kin_at(19 - row, col)


def column_reflection(kin: int) -> int:
    row, col = coordinates(kin)
    return kin_at(row, 12 - col)


def quartet(kin: int) -> tuple[int, ...]:
    """Orbit under the two *geometric* involutions on the 20x13 rectangle."""
    require_kin(kin)
    return tuple(sorted({kin, row_reflection(kin), column_reflection(kin), occult(kin)}))


def quartets() -> tuple[tuple[int, ...], ...]:
    return tuple(sorted({quartet(k) for k in PORTALS}))


def portal_grid() -> tuple[str, ...]:
    return tuple(''.join('#' if kin_at(r, c) in PORTALS else '.' for c in range(13))
                 for r in range(20))


def loom_edges() -> tuple[tuple[int, int], ...]:
    """Undirected 8-neighbor geometric adjacency restricted to portal cells."""
    result = set()
    for k in PORTALS:
        r, c = coordinates(k)
        for dr, dc in ((0, 1), (1, -1), (1, 0), (1, 1)):
            rr, cc = r + dr, c + dc
            if 0 <= rr < 20 and 0 <= cc < 13:
                j = kin_at(rr, cc)
                if j in PORTALS:
                    result.add(tuple(sorted((k, j))))
    return tuple(sorted(result))


def edge_invariants() -> dict:
    edges = loom_edges()
    distances = Counter(abs(tone(i) - tone(j)) for i, j in edges)
    return {'edges': len(edges), 'interval_histogram': dict(sorted(distances.items())),
            'sum_intervals': sum(k * v for k, v in distances.items())}


def portal_invariants() -> dict:
    quads = quartets()
    return {
        'portals': len(PORTALS), 'grid': portal_grid(),
        'left': sum(coordinates(k)[1] < 6 for k in PORTALS),
        'central_column': sum(coordinates(k)[1] == 6 for k in PORTALS),
        'right': sum(coordinates(k)[1] > 6 for k in PORTALS),
        'quartet_count': len(quads), 'quartets': quads,
        'quartet_tone_sums': tuple(sum(tone(k) for k in q) for q in quads),
        'count_tone_seven': sum(tone(k) == 7 for k in PORTALS),
        'edges': edge_invariants(),
    }


def descriptors(kin: int) -> dict:
    """Dreamspell 5x52 castles, 20x13 waves, 65x4 harmonics, 52x5 chromatics.

    These are partitions by index; a calendrical convention, NOT a dynamics
    homomorphism for RGΦ's noninvertible second chart S.
    """
    k = require_kin(kin)
    return {'kin': k, 'tone': tone(k), 'seal': seal(k),
            'row_col': coordinates(k), 'is_portal': k in PORTALS,
            'castle': (k - 1) // 52 + 1,
            'wavespell': (k - 1) // 13 + 1,
            'harmonic': (k - 1) // 4 + 1,
            'chromatic': (k - 1) // 5 + 1,
            'occult_kin': occult(k)}


def reciprocal_certificate(kin: int) -> dict:
    k = require_kin(kin)
    a, b = descriptors(k), descriptors(occult(k))
    return {'kin_pair': (k, occult(k)), 'sum_kin': 261,
            'sum_tones': a['tone'] + b['tone'],
            'sum_seals': a['seal'] + b['seal'],
            'sum_castles': a['castle'] + b['castle'],
            'sum_wavespells': a['wavespell'] + b['wavespell'],
            'sum_harmonics': a['harmonic'] + b['harmonic'],
            'sum_chromatics': a['chromatic'] + b['chromatic'],
            'same_portal_membership': a['is_portal'] == b['is_portal']}


def generalized_crt(a: int, m: int, b: int, n: int) -> tuple[int, int] | None:
    """All solutions t ≡ a (mod m), t ≡ b (mod n); no fictitious alignments."""
    if any(type(x) is not int for x in (a, m, b, n)) or m <= 0 or n <= 0:
        raise ValueError('m,n deben ser positivos; residuos enteros')
    g = gcd(m, n)
    if (b - a) % g:
        return None
    v = n // g
    u = 0 if v == 1 else (((b - a) // g) * pow(m // g, -1, v)) % v
    modulus = lcm(m, n)
    return ((a + m * u) % modulus, modulus)


def phase_bridge(periods: Iterable[int] = (260, 64), base: int = 20) -> dict:
    """Smith-independent exact orbit-class count; NOT a historical kin/hex mapping."""
    ms = tuple(periods)
    if not ms or any(type(x) is not int or x <= 0 for x in ms):
        raise ValueError('períodos positivos')
    if type(base) is not int or base < 2:
        raise ValueError('base >=2')
    L = lcm(*ms)
    size = 1
    for n in ms:
        size *= n
    q = size // L
    return {'periods': ms, 'ambient_size': size, 'temporal_orbit': L,
            'orbit_classes': q, 'noncanonical': True,
            'radix_base': base}


def finite_radix_orbit(modulus: int, base: int, seed: int) -> dict:
    """Functional dynamics x -> B*x mod m: exact preperiod, period, trace."""
    if any(type(x) is not int for x in (modulus, base, seed)) or modulus <= 0 or base < 2:
        raise ValueError('m>0, B>=2, seed entero')
    found = {}
    x = seed % modulus
    path = []
    while x not in found:
        found[x] = len(path)
        path.append(x)
        x = (base * x) % modulus
    preperiod = found[x]
    return {'m': modulus, 'base': base, 'seed': seed % modulus,
            'preperiod': preperiod, 'period': len(path) - preperiod,
            'trace': tuple(path), 'cycle': tuple(path[preperiod:]),
            'kernel_size': gcd(base, modulus),
            'image_size': modulus // gcd(base, modulus)}


def rational_residue(numerator: int, denominator: int, modulus: int) -> int | None:
    """Avoid false inversion: returns None when denominator non-unit modulo m."""
    if any(type(x) is not int for x in (numerator, denominator, modulus)) or denominator == 0 or modulus < 2:
        raise ValueError('racional y módulo inválidos')
    q = Fraction(numerator, denominator)
    if gcd(q.denominator, modulus) != 1:
        return None
    return (q.numerator * pow(q.denominator, -1, modulus)) % modulus


def witness_modular_readings(states: Iterable[Fraction], moduli: Iterable[int]) -> dict:
    """Exact observation partitions and an explicit abstention map."""
    xs = tuple(Fraction(x) for x in states)
    result = {}
    for m in moduli:
        if type(m) is not int or m < 2:
            raise ValueError('m>=2')
        labels = tuple(rational_residue(x.numerator, x.denominator, m) for x in xs)
        defined = {i: v for i, v in enumerate(labels) if v is not None}
        fibres = tuple(sorted(tuple(i for i, val in defined.items() if val == v)
                              for v in set(defined.values())))
        result[m] = {'readings': labels, 'defined': len(defined),
                     'abstentions': tuple(i for i, v in enumerate(labels) if v is None),
                     'fibres': fibres, 'rank': len(fibres)}
    return result


def franklin_certificate() -> dict:
    M = FRANKLIN
    return {'distinct_1_64': sorted(sum((list(r) for r in M), [])) == list(range(1, 65)),
            'row_sums': tuple(map(sum, M)),
            'column_sums': tuple(sum(M[r][c] for r in range(8)) for c in range(8)),
            'half_row_sums': tuple(sum(M[r][c:c + 4]) for r in range(8) for c in (0, 4)),
            'toroidal_2x2_sums': tuple(sorted({sum(M[(r + dr) % 8][(c + dc) % 8]
                                               for dr, dc in product((0, 1), repeat=2))
                                         for r, c in product(range(8), repeat=2)})),
            'ordinary_diagonal_sums': (sum(M[i][i] for i in range(8)),
                                       sum(M[i][7-i] for i in range(8)))}


def harmonics_1366560() -> dict:
    """Number theory on Argüelles's preferred 1,366,560; not a physical law."""
    H = 1366560
    periods = (260, 360, 365, 584, 2920, 18980, 37960)
    return {'harmonic': H, 'exact_quotients': {p: (H // p if H % p == 0 else None)
                                              for p in periods},
            'calendar_round': lcm(260, 365), 'venus_solar': lcm(584, 365),
            'thirteen_moons': 13 * 28, 'difference_365_364': 1}


def full_audit() -> dict:
    p = portal_invariants()
    f = franklin_certificate()
    checks = {
        'B01_grid': all(kin_at(*coordinates(k)) == k for k in range(1, 261)),
        'B02_portals_52': p['portals'] == 52,
        'B03_halves_26_26_center_0': (p['left'], p['central_column'], p['right']) == (26, 0, 26),
        'B04_quartets_13x4': len(p['quartets']) == 13 and all(len(q) == 4 for q in p['quartets']),
        'B05_quartet_sum_28': all(s == 28 for s in p['quartet_tone_sums']),
        'B06_tone_7_eight': p['count_tone_seven'] == 8,
        'B07_edges_60': p['edges']['edges'] == 60,
        'B08_interval_270': p['edges']['sum_intervals'] == 270,
        'B09_reflection_orbits': all(row_reflection(k) in PORTALS and column_reflection(k) in PORTALS
                                     for k in PORTALS),
        'B10_castles_5x52': Counter(descriptors(k)['castle'] for k in range(1, 261)) == {i:52 for i in range(1,6)},
        'B11_wavespells_20x13': Counter(descriptors(k)['wavespell'] for k in range(1,261)) == {i:13 for i in range(1,21)},
        'B12_harmonics_65x4': Counter(descriptors(k)['harmonic'] for k in range(1,261)) == {i:4 for i in range(1,66)},
        'B13_chromatics_52x5': Counter(descriptors(k)['chromatic'] for k in range(1,261)) == {i:5 for i in range(1,53)},
        'B14_occult_261': all(reciprocal_certificate(k)['sum_kin'] == 261 and
                              reciprocal_certificate(k)['sum_tones'] == 14 and
                              reciprocal_certificate(k)['sum_seals'] == 21 and
                              reciprocal_certificate(k)['sum_castles'] == 6 and
                              reciprocal_certificate(k)['sum_wavespells'] == 21 and
                              reciprocal_certificate(k)['sum_harmonics'] == 66 and
                              reciprocal_certificate(k)['sum_chromatics'] == 53 and
                              reciprocal_certificate(k)['same_portal_membership']
                              for k in range(1, 261)),
        'B15_crt_260_64': phase_bridge()['orbit_classes'] == 4 and generalized_crt(0, 260, 1, 64) is None,
        'B16_franklin_260': f['distinct_1_64'] and set(f['row_sums']) == {260}
                            and set(f['column_sums']) == {260} and set(f['half_row_sums']) == {130}
                            and set(f['toroidal_2x2_sums']) == {130},
        'B17_radix_noninvertible': finite_radix_orbit(260, 20, 1)['kernel_size'] == 20,
        'B18_rational_abstain': rational_residue(1, 13, 260) is None,
        'B19_harmonics': harmonics_1366560()['calendar_round'] == 18980,
    }
    return {'pass': all(checks.values()), 'checks': checks, 'loom': p,
            'franklin': f, 'phase_260_64': phase_bridge(),
            'harmonics': harmonics_1366560(),
            'status': 'SCOPED_INSTRUMENT_NOT_RGPHI_GLOBAL_PROOF'}