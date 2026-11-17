#!/usr/bin/env python3
"""Auditoría exacta y reproducible del puente seno-π / dinámica radix–Möbius.

Fuentes: 01_MAIN_EN (1).pdf (secciones 2, 5, 8 y 10),
03_COMPANION_EN.pdf (secciones 1, 2 y 4), 02_SUPPLEMENT_EN.pdf.
Ningún dato sintético: usa sólo el testigo y las constantes de los manuscritos,
la base 100 que aparece en la dinámica decimal de π y π calculado con mpmath.
"""
import json
from collections import Counter
from fractions import Fraction
from math import gcd, lcm
from pathlib import Path
from mpmath import mp

ROOT = Path(__file__).resolve().parent
R = 88011536665779
M = 223336848698040
STATES = (
    Fraction(406, 731), Fraction(712, 731),
    Fraction(712, 1265), Fraction(1218, 1265),
    Fraction(406, 557),
)
T_TARGETS = (1, 0, 3, 2, 4)
S_TARGETS = (4, 2, 1, 0, 0)


def radix(B, x):
    p, q = x.numerator, x.denominator
    residue = (B*p) % q
    if residue == 0:
        return Fraction(0, 1)
    return Fraction(residue, q)


def mobius(B, x):
    # Φ(T_B(Φ^{-1}(p/q))) con Φ^{-1}(p/q)=(q-p)/p
    p, q = x.numerator, x.denominator
    residue = (B*(q-p)) % p
    return Fraction(p, p+residue)


def witness_check(B):
    outcomes=[]
    for i, x in enumerate(STATES):
        tx, sx = radix(B, x), mobius(B, x)
        gt, gs = gcd(B, x.denominator), gcd(B, x.numerator)
        assert tx==STATES[T_TARGETS[i]], (B, i, tx)
        assert sx==STATES[S_TARGETS[i]], (B, i, sx)
        assert gt == 1 and gs == (3 if i==3 else 1)
        outcomes.append(dict(i=i, T=T_TARGETS[i], S=S_TARGETS[i], delta_T=gt, delta_S=gs))
    return outcomes


def composition_monoid():
    # f is the map induced by a chronological word; append one letter on the right.
    identity=tuple(range(5))
    seen={identity}
    pending=[identity]
    while pending:
        f=pending.pop()
        for g in (T_TARGETS, S_TARGETS):
            h=tuple(g[f[i]] for i in range(5))
            if h not in seen:
                seen.add(h)
                pending.append(h)
    ranks=dict(sorted(Counter(len(set(f)) for f in seen).items()))
    assert len(seen)==36
    assert ranks=={2:8,3:18,4:8,5:2}
    word=(S_TARGETS,T_TARGETS,S_TARGETS,T_TARGETS,S_TARGETS)
    f=identity
    for g in word:
        f=tuple(g[f[i]] for i in range(5))
    assert f==(2,2,0,0,0),f
    return {"size":len(seen),"rank_distribution":ranks,"STSTS":f}


def prime_power_atoms_odd(N):
    out=[]
    n=N
    p=2
    while p*p<=n:
        if n%p==0:
            pp=1
            while n%p==0:
                n//=p
                pp*=p
            if p%2==1:out.append(pp)
        p+=1
    if n>1 and n%2==1:out.append(n)
    return out


def c15(N):
    pp=prime_power_atoms_odd(N)
    big=sum(z>=15 for z in pp)
    return big+(len(pp)-big)//2


def cofactor_h(Mv, W):
    return Mv//gcd(Mv,abs(W))


def known_cofactors():
    A,C,D,Q,E,r=406,712,1265,731,557,3
    out={}
    for sign in (-1,1):
        out[str(sign)]={
            "h_A":cofactor_h(A,D-sign*r*Q),
            "h_C":cofactor_h(C,D-sign*Q),
            "h_D":cofactor_h(D,C-sign*r*A),
            "h_Q":cofactor_h(Q,C-sign*A),
        }
    L=lcm(A,C,D,Q)
    assert E//gcd(E,L)==557
    assert min(z for a in out.values() for z in a.values())==4
    return {"signed":out,"L":L,"lambda":E//gcd(E,L)}


def pi_phase_numerics():
    mp.dps=150
    res=[]
    for k in range(9):
        pow10=10**(2*k+5)
        theta=mp.frac(pow10*mp.pi)
        z=1/(1+theta)
        theta_next=mp.frac(100*theta)
        z_next=1/(1+theta_next)
        s_z=1/(1+mp.frac(100*(1/z-1)))
        assert abs(z_next-s_z)<mp.mpf("1e-105")
        pi_approx=(10**(k+3))*mp.sin(mp.pi/(10**(k+3)))
        tau=pow10*(mp.pi-pi_approx)
        assert 0<tau<1
        mark=int(theta<tau)
        res.append({"k":k,"theta":mp.nstr(theta,23),"z":mp.nstr(z,23),"tau":mp.nstr(tau,23),"crosses_borrow_threshold":mark})
    return {"cutoff_limit":mp.nstr(1/(1+mp.pi**3/60),60),"tau_limit":mp.nstr(mp.pi**3/60,60),"samples":res}


def signed_root_verification():
    # For the actual witness Q=731=17*43, its square-root classes mod Q are four.
    # The unsquared transition chooses B=171 mod 731.
    Q=731
    roots=[b for b in range(Q) if (b*b-1)%Q==0]
    assert len(roots)==4
    assert R%Q==171
    assert (R%17,R%43)==(1,42)
    assert 171 in roots
    return {"modulus":Q,"all_roots_of_unity_mod_Q":roots,
            "witness_residue":R%Q,"prime_power_signs":{"17":"+1","43":"-1"}}


def main():
    checks=[witness_check(R+j*M) for j in range(3)]
    result={
        "origin": "exact-manuscript-witness-and-pi",
        "base_residue_R":R,
        "base_modulus_M":M,
        "witness_states":[str(s) for s in STATES],
        "witness_maps":checks[0],
        "CRT_replays":3,
        "monoid":composition_monoid(),
        "known_carrier_signed_cofactors":known_cofactors(),
        "witness_root_sign_lift":signed_root_verification(),
        "base100":{"B":100,"B_minus_1":99,"B_plus_1":101,
                   "odd_atoms_minus":prime_power_atoms_odd(99),
                   "odd_atoms_plus":prime_power_atoms_odd(101),
                   "c15_minus":c15(99),"c15_plus":c15(101),
                   "five_state_nonpermutation_excluded_by_companion_cor_4_5":c15(99)<4 or c15(101)<4},
        "pi_phase":pi_phase_numerics(),
    }
    (ROOT/"RESULTADOS_EXACTOS.json").write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding="utf-8")
    print("PASS witness x3 bases CRT, monoid=36, factor-three strict edge, h_min=4")
    print("PASS B=100: c15(99)=%d, c15(101)=%d (required >=4 for r=2)"%(c15(99),c15(101)))
    print("PASS z_{k+1}=S_100(z_k), precision mpmath %s digits, 9 first transitions"%mp.dps)
    print("results",ROOT/"RESULTADOS_EXACTOS.json")

if __name__ == "__main__":
    main()
