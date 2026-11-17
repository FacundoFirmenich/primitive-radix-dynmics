from __future__ import annotations
from fractions import Fraction
from math import gcd, floor

PHI_MATRIX=((0,1),(1,1))

def T(x: Fraction, B: int) -> Fraction:
    return Fraction((B*x.numerator) % x.denominator, x.denominator)

def phi(x: Fraction) -> Fraction:
    return Fraction(1, 1+x)

def phi_inv(x: Fraction) -> Fraction:
    return Fraction(1-x, x)

def S(x: Fraction, B: int) -> Fraction:
    return phi(T(phi_inv(x), B))

def defects(x: Fraction, B: int) -> tuple[int,int]:
    return gcd(x.denominator,B), gcd(x.numerator,B)

def branch_digit_T(x: Fraction, B: int) -> int:
    return (B*x.numerator)//x.denominator

def branch_digit_S(x: Fraction, B: int) -> int:
    return (B*(x.denominator-x.numerator))//x.numerator

def matmul(A,B):
    return tuple(tuple(sum(A[i][k]*B[k][j] for k in range(2)) for j in range(2)) for i in range(2))

def matvec(A,v):
    return (A[0][0]*v[0]+A[0][1]*v[1], A[1][0]*v[0]+A[1][1]*v[1])

def A_matrix(k:int,B:int): return ((B,-k),(0,1))
def C_matrix(k:int,B:int): return ((1,0),(1-B-k,B))
