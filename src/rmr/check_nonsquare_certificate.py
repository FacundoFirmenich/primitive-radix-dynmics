#!/usr/bin/env python3
from math import isqrt
mods=[68,55,71]
sq={m:{(x*x)%m for x in range(m)} for m in mods}
for j in range(1,38):
    v=403*j*j+15314*j+190969
    assert isqrt(v)**2 != v
    assert any(v%m not in sq[m] for m in mods)
print('PASS')
print('j_range=1..37')
print('moduli=68,55,71')
