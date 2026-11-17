"""Separate exact checks and rational interval certificates for the supplied bridge."""
from pathlib import Path
from fractions import Fraction as F
from math import gcd
import json, hashlib, sys
sys.set_int_max_str_digits(100000)
ROOT=Path(__file__).resolve().parent
CONFIG={'domain':'dimensionless exact arithmetic','pi_identity':'pi=16 atan(1/5)-4 atan(1/239)','atan_terms':180,'global_pi_bracket':['157/50','22/7'],'atan_remainder':'alternating series, next term bounds the remainder','phase_k':list(range(10)),'borrow_k':list(range(9)),'tau_bounds':'pi^3/60-pi^5/120*10^(-2k-7) < tau_k < previous +pi^7/5040*10^(-4k-13)','tau_series_applicability':'0 < pi*10^(-k-3) < 1','witness':{'A':406,'C':712,'D':1265,'Q':731,'E':557,'R':88011536665779,'M':223336848698040}}
print(json.dumps(CONFIG,ensure_ascii=False,indent=2))
def floor(x):return x.numerator//x.denominator
def frac(x):return x-floor(x)
def atan_bounds(d,n):
 s=sum((F((-1)**j,(2*j+1)*d**(2*j+1))for j in range(n)),F(0))
 next_term=F((-1)**n,(2*n+1)*d**(2*n+1))
 return min(s,s+next_term),max(s,s+next_term)
a,b=atan_bounds(5,180);c,d=atan_bounds(239,180)
lo,hi=16*a-4*d,16*b-4*c
assert F(157,50)<lo<hi<F(22,7) and hi-lo<F(1,10**240)
global_tau_lower=F(157,50)**3/60-F(22,7)**5/(120*10**7)
assert F(1,2)<global_tau_lower and F(22,7)**3/60<1
# Rational tangent check for the exact Machin identity (range selects pi/4).
t=F(1,5)
t2=2*t/(1-t*t);t4=2*t2/(1-t2*t2)
assert (t4-F(1,239))/(1+t4*F(1,239))==1
phases=[]
for k in range(10):
 scale=10**(2*k+5);Nl=floor(scale*lo);Nu=floor(scale*hi);assert Nl==Nu
 phases.append((Nl,scale*lo-Nl,scale*hi-Nl))
for k in range(9):
 N,tl,tu=phases[k];block=floor(100*tl);assert block==floor(100*tu)
 assert phases[k+1][0]==100*N+block
cert=[]
for k in range(9):
 n=2*k+5;N,theta_lo,theta_hi=phases[k]
 u=F(1,10**(2*k+7));v=F(1,10**(4*k+13))
 tau_lo=lo**3/60-hi**5*u/120
 tau_hi=hi**3/60-lo**5*u/120+hi**7*v/5040
 assert 0<tau_lo<tau_hi<1
 if theta_hi<tau_lo:mark=1
 elif theta_lo>tau_hi:mark=0
 else:raise AssertionError(('unresolved borrow',k))
 # Certify that the floors really differ by the reported mark.
 Plo=lo-F(1,10**n)*tau_hi;Phi=hi-F(1,10**n)*tau_lo
 PN=floor(10**n*Plo);assert PN==floor(10**n*Phi) and N-PN==mark
 # Natural depth convention J=1+v_10(N) on a crossing, and J=0 otherwise.
 trailing=0;temp=N
 while temp%10==0:trailing+=1;temp//=10
 J=(1+trailing)*mark
 first_difference=None
 for j in range(1,n+2):
  p_floor=floor(10**j*Plo);pi_floor=floor(10**j*lo)
  assert p_floor==floor(10**j*Phi) and pi_floor==floor(10**j*hi)
  if p_floor!=pi_floor:first_difference=j;break
 assert first_difference==n+1-J
 cert.append({'k':k,'decimal_scale_n':n,'integer_part':N,'borrow':mark,'natural_depth_J':J,'first_differing_decimal':first_difference,'theta_interval':[str(theta_lo),str(theta_hi)],'tau_interval':[str(tau_lo),str(tau_hi)]})
for i in range(1,len(cert)):
 advance=cert[i]['first_differing_decimal']-cert[i-1]['first_differing_decimal'];cert[i]['advance']=advance
 assert advance-2==cert[i-1]['natural_depth_J']-cert[i]['natural_depth_J']
W=CONFIG['witness'];A,C,D,Q,E,R,M=[W[s]for s in ['A','C','D','Q','E','R','M']]
states=[F(A,Q),F(C,Q),F(C,D),F(3*A,D),F(A,E)]
T=(1,0,3,2,4);S=(4,2,1,0,0)
def radix(B,x):return frac(B*x)
def phi(x):return 1/(1+x)
def sb(B,x):return phi(radix(B,1/x-1))
for base in [R,R+M,R+2*M]:
 assert [radix(base,x)for x in states]==[states[j]for j in T]
 assert [sb(base,x)for x in states]==[states[j]for j in S]
# Six shared CRT residues in 119772 coordinates, independently evaluated.
residues={str(m):(num*pow(den,-1,m))%m for m,num,den in [(A,E,Q),(Q,C,A),(C,D,Q),(D,3*A,C),(E,1,1),(3,0,1)]}
assert all(R%int(m)==u for m,u in residues.items())
reflected=[1/x for x in states];assert all(1<x<2 for x in reflected)
# Reflection (A',C',D',Q')=(Q,D,C,A), coefficients (3,1,3,1)->(1,3,1,3).
def signed_h(a,c,d,q,coeff,sgn):
 alpha,beta,gamma,delta=coeff
 return (a//gcd(a,d-sgn*alpha*q),c//gcd(c,d-sgn*beta*q),d//gcd(d,c-sgn*gamma*a),q//gcd(q,c-sgn*delta*a))
for sign in (-1,1):
 h=signed_h(A,C,D,Q,(3,1,3,1),sign)
 reflected_h=signed_h(Q,D,C,A,(1,3,1,3),sign)
 assert reflected_h==(h[3],h[2],h[1],h[0])
assert max(A,C,D,Q)==max(Q,D,C,A)

result={'status':'PASS','scope':'Self-review with a separate implementation and exact rational interval arithmetic; no global arithmetic classification is asserted.','configuration':CONFIG,'pi_interval':[str(lo),str(hi)],'exact_witness_edges_checked':30,'reflection_h_permutation_verified_on_witness':True,'global_tau_lower_bound':str(global_tau_lower),'shared_CRT_residues':residues,'reciprocal_witness_states':[str(x)for x in reflected],'borrow_certificates':cert,'certified_borrow_marks':[x['borrow']for x in cert],'natural_depth_convention':'For this added check only: J=0 without crossing; J=1+v_10(floor(10^(2k+5)*pi)) with crossing. The original note must specify whether its J uses this convention.','cofactor_two_adic_control':{'A':A,'h_A_plus_times_h_A_minus':7*29,'C':C,'gcd_h_C_plus_h_C_minus':gcd(4,178)},'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
(ROOT/'INDEPENDENT_RESULTS.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print('PASS: 30 exact edges; 6 shared CRT residues; 9 independent phase transitions; 9 rational borrow certificates; natural-depth telescope checked.')
print('Borrow marks:',result['certified_borrow_marks'])
print('First differing decimals:',[x['first_differing_decimal']for x in cert])
