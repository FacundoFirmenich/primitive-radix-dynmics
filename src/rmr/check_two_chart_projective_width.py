from math import gcd
from random import Random
rng=Random(20261114)
def det(M):return M[0][0]*M[1][1]-M[0][1]*M[1][0]
def mm(A,B):return [[sum(A[i][k]*B[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
def mv(A,v):return [A[0][0]*v[0]+A[0][1]*v[1],A[1][0]*v[0]+A[1][1]*v[1]]
def content(v):return gcd(abs(v[0]),abs(v[1]))
def invu(H):
    d=det(H); assert abs(d)==1
    return [[H[1][1]//d,-H[0][1]//d],[-H[1][0]//d,H[0][0]//d]]
def randH():
    H=[[1,0],[0,1]]
    for _ in range(5):
        n=rng.randint(-4,4)
        E=[[1,n],[0,1]] if rng.randint(0,1) else [[1,0],[n,1]]
        H=mm(E,H)
    if rng.randint(0,1): H=[H[1],H[0]]
    assert abs(det(H))==1
    return H
checks=0
for _ in range(20000):
    B=rng.randint(2,80); H=randH(); Hi=invu(H)
    p,q=rng.randint(-80,80),rng.randint(1,80)
    if p==0 or gcd(abs(p),q)!=1: continue
    v=[p,q]; k=rng.randint(0,B-1); A=[[B,-k],[0,1]]
    assert content(mv(A,v))==gcd(q,B)
    u=mv(Hi,v); C=mm(mm(H,A),Hi)
    assert content(mv(C,v))==gcd(abs(u[1]),B)
    checks+=1
print('PASS two_chart_local_law',checks)
