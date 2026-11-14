from math import isqrt
for j in range(1, 19):
    q = 403*j*j + 15314*j + 190969
    assert isqrt(q)**2 != q
    if j % 2:
        assert q % 4 == 2
    elif j in (4, 8, 14, 18):
        assert q % 5 not in {k*k % 5 for k in range(5)}
    elif j in (2, 12, 16):
        assert q % 11 not in {k*k % 11 for k in range(11)}
    else:
        assert j in (6, 10)
        assert q % 17 not in {k*k % 17 for k in range(17)}
print("PASS 18/18; moduli 4,5,11,17")
