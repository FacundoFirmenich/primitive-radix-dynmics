"""Exact, explicitly conventional 260-kin × 384-yao phase coupling.

This is a modern algebraic product clock, NOT a pre-Columbian Maya/Chinese
correspondence and NOT a homomorphism for RGΦ S_B without additional proof.
The six lines are indexed 1..6 from bottom to top; hexagram rank 1..64 is
an abstract identifier (not the six-bit King Wen semantic position).
"""
from __future__ import annotations
from math import gcd,lcm
from .loom_bridge import generalized_crt,require_kin

def yao_index(hexagram: int, line: int) -> int:
    """Line-major enumeration, 0..383; preserves hexagram modulo 64."""
    if type(hexagram) is not int or not 1 <= hexagram <= 64:
        raise ValueError('hexagrama: entero 1..64')
    if type(line) is not int or not 1 <= line <= 6:
        raise ValueError('yao: línea 1..6')
    return 64*(line-1)+(hexagram-1)

def inverse_yao_index(j: int) -> tuple[int,int]:
    if type(j) is not int or not 0 <= j < 384:
        raise ValueError('índice 0..383')
    line0,hex0=divmod(j,64)
    return hex0+1,line0+1

def join_kin_yao(kin:int,hexagram:int,line:int) -> dict:
    """Completes one synchronized phase t when the residues agree modulo 4."""
    k=require_kin(kin)
    j=yao_index(hexagram,line)
    x=generalized_crt(k-1,260,j,384)
    return {'kin':k,'hexagram':hexagram,'line':line,
            'yao_index':j,'compatible':x is not None,
            'phase':x[0] if x else None,
            'joint_period':lcm(260,384),
            'component':((j-(k-1))%4),
            'noncanonical_symbolic_observer':True}

def split_joint_phase(phase:int) -> dict:
    if type(phase) is not int:
        raise ValueError('fase entera')
    t=phase%lcm(260,384)
    kin=1+t%260
    hexagram,line=inverse_yao_index(t%384)
    result=join_kin_yao(kin,hexagram,line)
    assert result['compatible'] and result['phase']==t
    return result

def coupling_invariants()->dict:
    m,n=260,384
    return {'m':m,'n':n,'gcd':gcd(m,n),'lcm':lcm(m,n),
            'ambient_states':m*n,'classes':gcd(m,n),
            'members_per_class':lcm(m,n),
            'compatible_states':lcm(m,n),
            'label_to_joint': 'Z/24960 <-> compatible (kin, hexagram, yao)',
            'calibration': 'zero phase = kin1, hexagram1, line1',
            'classification':'MODERN_CLOCK_NOT_ANCIENT_HISTORIC_CLAIM'}