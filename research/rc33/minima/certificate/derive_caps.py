from pathlib import Path
import json,platform
R=Path(__file__).resolve().parent
Bstar=88011536665779
print(json.dumps({'stage':'BEFORE','units':'dimensionless exact integers','Python':platform.python_version(),'B_star':Bstar,'B_max':Bstar-1,'variables':{'H':'max(A,C,D,Q,E)','lambda':'E/gcd(E,L)','L':'lcm(A,C,D,Q)'},'assumptions':['five classified residual chambers','lambda*L divides B^2-1','L>H^4/32','H<(200*lambda)^10','lambda<=E<=H'],'equations':['H^41 < 6400^10*(B^2-1)^10','lambda^5 < 32*(B^2-1)'],'unknowns':{'uniform_global_lambda_bound':None,'all_cardinality_minimal_witness_bound':None}},indent=2),flush=True)
def root(n,k):
 assert n>=0 and k>=1
 lo=0;hi=1<<((n.bit_length()+k-1)//k)
 while lo+1<hi:
  m=(lo+hi)//2
  if m**k<=n:lo=m
  else:hi=m
 return hi if hi**k<=n else lo
Bmax=Bstar-1;N=Bmax*Bmax-1
Hcap=root(6400**10*N**10-1,41)
Lcap=root(32*N-1,5)
assert Hcap**41<6400**10*N**10<=(Hcap+1)**41
assert Lcap**5<32*N<=(Lcap+1)**5
# Existing chamber inequalities imply stronger individual bounds E<cH.
# Fractions c=num/den; then lambda^5 <32*c^4*N.
chambers=[('119772/r2,j=-1',1,2),('119772/r2,j=1',3,4),('119772/r3,j=1',4,9),('119772/r3,j=2',5,9),('606897/r3,reflected',2,3)]
rows=[]
for name,num,den in chambers:
 k=(32*num**4*N-1)//den**4
 cap=root(k,5)
 assert den**4*cap**5<32*num**4*N<=den**4*(cap+1)**5
 rows.append(dict(chamber=name,E_over_H_strict_upper=f'{num}/{den}',lambda_cap=cap))
res=dict(status='PASS',B_star=Bstar,B_range_inclusive=[2,Bmax],H_cap_inclusive=Hcap,lambda_cap_inclusive=Lcap,chamber_lambda_caps=rows,scope='Finite necessary search envelope below the known base, for all classified five-state chambers; no exhaustive enumeration or least-base conclusion.',proof='lambda<=H and lambda*L>lambda*H^4/32>=lambda^5/32; combine with lambda*L<=B^2-1. Use H^41 bound separately.',not_settled=['global uniqueness','minimum base at five states','minimum base at arbitrary cardinality'])
(R/'BELOW_KNOWN_BASE_CAPS.json').write_text(json.dumps(res,indent=2)+'\n')
print('RESULT',json.dumps(res,indent=2),flush=True)

# Strengthen using the already proved exclusions lambda<=5 and gcd(r,E)=1.
# Since lambda divides E, lambda=6 is impossible for either r=2 or r=3.
print('BEFORE_TIGHTENING',json.dumps(dict(excluded_indices=[1,2,3,4,5],strict_factor_values=[2,3],unit_condition='gcd(r,E)=1 and lambda divides E',deduced_minimum_index=7,L_lower_bounds=['H^4/16 for normal r2','H^4/32 for normal r3','3H^4/32 for reflected r3'],chamber_E_over_H=[list(x) for x in chambers])),flush=True)
Hcap7=root((32*N-1)//7,4)
assert 7*Hcap7**4<32*N<=7*(Hcap7+1)**4
rows7=[]
for name,num,den in chambers:
    # L > a H^4 / b.
    a,b=(1,16) if 'r2' in name else ((3,32) if 'reflected' in name else (1,32))
    k=(b*num**4*N-1)//(a*den**4)
    cap=root(k,5)
    assert a*den**4*cap**5<b*num**4*N<=a*den**4*(cap+1)**5
    hc=root((b*N-1)//(a*7),4)
    assert a*7*hc**4<b*N<=a*7*(hc+1)**4
    rows7.append(dict(chamber=name,L_strict_lower=f'{a}/{b} H^4',E_over_H_strict_upper=f'{num}/{den}',lambda_cap_inclusive=cap,H_cap_inclusive=hc))
from sympy import integer_nthroot
for row in rows7:
    name=row['chamber'];num,den=next((n,d) for nm,n,d in chambers if nm==name)
    a,b=(1,16) if 'r2' in name else ((3,32) if 'reflected' in name else (1,32))
    assert integer_nthroot((b*num**4*N-1)//(a*den**4),5)[0]==row['lambda_cap_inclusive']
res['tightened']=dict(minimum_index=7,H_cap_inclusive=Hcap7,lambda_cap_inclusive=max(x['lambda_cap_inclusive'] for x in rows7),chambers=rows7,independent_integer_root_check='SymPy integer_nthroot agrees with binary-search implementation')
(R/'BELOW_KNOWN_BASE_CAPS.json').write_text(json.dumps(res,indent=2)+'\n')
print('TIGHTENED_RESULT',json.dumps(res['tightened'],indent=2),flush=True)
