"""Explicit audit adapter, NOT a recovered original FST13 baseline."""
from exact_inverse import base
def _K0(h):return base(h)[0]
def cap_key_at_length(ell,sign):return 8*10**ell if sign>0 else 10**ell-9
def decode_rank(h,ell,j):
 if type(ell) is not int or ell<0 or type(j) is not int or j<0:raise ValueError('invalid length or rank')
 n=_K0(h)*343**j;m=10**ell
 if abs(n)>cap_key_at_length(ell,1 if n>0 else -1):raise ValueError('inadmissible rank')
 v=(8*m-n)//9
 assert 0<=v<m
 return '' if ell==0 else str(v).zfill(ell)
