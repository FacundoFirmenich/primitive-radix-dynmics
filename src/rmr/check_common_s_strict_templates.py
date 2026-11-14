"""Regression checks for the symbolic common S-strict reduction.

Authority is proofs/FIVE_STATE_COMMON_S_STRICT_TEMPLATES.md.
"""
from random import Random

CASES={
575722:([2,4,3,0,1],[4,1,2,1,0],1),
575898:([3,4,0,2,1],[4,1,2,1,0],1),
575738:([3,2,4,0,1],[4,1,2,1,0],2),
576298:([3,4,1,0,2],[4,1,2,1,0],2),
}

def cycles(m):
    seen=set(); out=[]
    for s in range(5):
        if s in seen: continue
        path=[]; pos={}; u=s
        while u not in pos and u not in seen:
            pos[u]=len(path); path.append(u); u=m[u]
        seen.update(path)
        if u in pos: out.append(tuple(path[pos[u]:]))
    return sorted(len(c) for c in out if len(c)>1)

for code,(T,S,template) in CASES.items():
    assert S==[4,1,2,1,0]
    assert S[3]==1
    assert cycles(T)==[2,3]
    if template==1:
        assert set(T[i] for i in (0,2,3)) <= {0,2,3}
        assert {T[1],T[4]}=={1,4}
    else:
        assert {T[0],T[3]}=={0,3}
        assert set(T[i] for i in (1,2,4)) <= {1,2,4}

rng=Random(20261114)
for _ in range(10000):
    A=rng.randint(1,10**5); C=rng.randint(1,10**5); r=rng.choice((2,3))
    assert A**3-(r*C)**3 == (A-r*C)*(A*A+r*A*C+r*r*C*C)
    assert C**3-A**3 == (C-A)*(C*C+A*C+A*A)

print('PASS common_S_strict_templates bookkeeping=4 random_factorizations=10000')
print('BOUNDARY: regression only; symbolic proof is authoritative')
