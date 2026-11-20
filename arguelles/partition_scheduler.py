"""Lossless RC3.3 integer-Q work scheduler using 260-kin/52-castle indexing.

Only job assignment and coverage are affected. No calendrical label excludes a
candidate or proves a Diophantine necessary condition. Full integer intervals
may be split into 5 castles, 20 waves, 65 harmonics, or 52 portal/nonportal.
For provenance/replay, labels are computed from Q mod260, not a calendar date.
"""
from __future__ import annotations

from hashlib import sha256
from typing import Iterable
from .loom_bridge import descriptors, PORTALS
from .iching_loom_coupler import split_joint_phase


def assignment(q: int) -> dict:
    if type(q) is not int or q < 1:
        raise ValueError('Q es entero positivo')
    kin = 1 + q % 260
    d = descriptors(kin)
    yi = split_joint_phase(q)
    return {'q':q, 'kin':kin,'castle':d['castle'],'wavespell':d['wavespell'],
            'harmonic':d['harmonic'],'chromatic':d['chromatic'],
            'portal':d['is_portal'],
            'i_ching_hexagram':yi['hexagram'],'yao_line':yi['line'],
            'phase_mod_24960':yi['phase']}


def next_in_residue(lo:int,residue:int,period:int=260) -> int:
    if any(type(v) is not int for v in (lo,residue,period)) or period<1 or not 0<=residue<period:
        raise ValueError('parámetros enteros/rango válido')
    return lo + (residue - lo) % period


def count_residue(lo:int,hi:int,residue:int,period:int=260) -> int:
    if type(lo) is not int or type(hi) is not int or hi<lo:
        raise ValueError('intervalo [lo,hi] no vacío')
    first=next_in_residue(lo,residue,period)
    return max(0,(hi-first)//period+1)


def partitions(lo:int,hi:int,by:str='castle') -> dict:
    """Exact bounded counts by residue without scanning [lo,hi] or any Q.

    Sources of labels are 260 residue classes; every residue is assigned once.
    """
    if type(lo) is not int or type(hi) is not int or lo<1 or hi<lo:
        raise ValueError('1<=lo<=hi')
    kinds={'castle','wavespell','harmonic','chromatic','portal'}
    if by not in kinds:
        raise ValueError('categoría inválida')
    output={}
    for residue in range(260):
        kin=1+residue
        label=descriptors(kin)[by] if by!='portal' else ('P' if kin in PORTALS else 'N')
        output[label]=output.get(label,0)+count_residue(lo,hi,residue)
    assert sum(output.values())==hi-lo+1
    return dict(sorted(output.items(),key=lambda kv: str(kv[0])))


def iter_castle(lo:int,hi:int,castle:int):
    """Enumerates one of five disjoint, collectively exhaustive work lanes."""
    if type(castle) is not int or not 1<=castle<=5:
        raise ValueError('castillo 1..5')
    if lo<1 or hi<lo:
        raise ValueError('1<=lo<=hi')
    for r in range((castle-1)*52,castle*52):
        q=next_in_residue(lo,r)
        while q<=hi:
            yield q
            q+=260


def verify_castle_plan(lo:int,hi:int) -> dict:
    """Full Q coverage certificate; no candidates/solver work are simulated."""
    by_lane=[list(iter_castle(lo,hi,c)) for c in range(1,6)]
    flattened=[q for lane in by_lane for q in lane]
    actual=set(flattened)
    expected=set(range(lo,hi+1))
    ok=len(flattened)==len(actual)==len(expected) and actual==expected
    digest=sha256(','.join(str(q) for q in sorted(flattened)).encode('ascii')).hexdigest()
    return {'Q_interval':[lo,hi], 'expected_count':hi-lo+1,
            'lane_counts':[len(x) for x in by_lane],
            'portal_class_counts':partitions(lo,hi,'portal'),
            'coverage_exact':ok,'overlap_count':len(flattened)-len(actual),
            'missing_count':len(expected-actual),
            'sorted_Q_sha256':digest,
            'solver_calls':0,
            'interpretation':'SCHEDULER_ONLY_NO_ARITHMETIC_EXCLUSION'}