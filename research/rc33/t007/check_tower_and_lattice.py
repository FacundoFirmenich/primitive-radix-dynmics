from pathlib import Path
from itertools import product
from math import isqrt,comb,gcd
import json,platform
R=Path(__file__).resolve().parent
U='XYYXXXXXYYYXXXXY';V=U[::-1]
CONFIG={'units':'dimensionless exact integers; external action letters X,Y; ordered noncontiguous subsequences', 'seed':[U,V], 'probe':'X**(5+r) Y', 'tower':'u[r+1]=u[r]v[r], v[r+1]=v[r]u[r]', 'predicted_difference':'18*(-10)**r*2**(r*(r-1)//2)', 'full_deck_levels':[0,5],'single_probe_levels':[0,9], 'lattice':{'N':486350841114209042571600,'L':581981400,'a0':397929094518522627660600,'u':[-6721598835151200,-8984879105202000],'v':[21459192394840200,-13425212699098200]},'python':platform.python_version()}
print('CONFIGURATION BEFORE COMPUTATION\n'+json.dumps(CONFIG,indent=2),flush=True)
def count(w,p):
 a=[1]+[0]*len(p)
 for ch in w:
  for j in range(len(p),0,-1):
   if p[j-1]==ch:a[j]+=a[j-1]
 return a[-1]
# Deliberately pattern-by-pattern DP, distinct from source full-deck state update.
pairs=[(U,V),('XYYYYXXXYYYYYXXY','YXXYYYYYXXXYYYYX')]
pat=[''.join(ds) for ds in product('XY',repeat=6)]
patterns=[]
for x,y in pairs:
 assert all(count(x,p)==count(y,p) for k in range(6) for p in map(''.join,product('XY',repeat=k)))
 patterns.append({p for p in pat if count(x,p)!=count(y,p)})
assert len(patterns[0]&patterns[1])==52
rows=[];u,v=U,V
for r in range(10):
 probe='X'*(5+r)+'Y';difference=count(u,probe)-count(v,probe);want=18*(-10)**r*2**(r*(r-1)//2)
 assert difference==want
 if r<=5:
  for k in range(6+r):
   for pat in product('XY',repeat=k):
    p=''.join(pat);assert count(u,p)==count(v,p)
 rows.append({'r':r,'length':len(u),'indistinguishable_through':5+r,'exact_first_separating_order':6+r,'probe_difference':difference})
 u,v=u+v,v+u
print('Tower checks PASS',flush=True)
lat=CONFIG['lattice'];N,L,a0=lat['N'],lat['L'],lat['a0'];u,v=lat['u'],lat['v'];a=sum(x*x for x in u);b=sum(x*x for x in v);d=sum(x*y for x,y in zip(u,v))
for w in [u,v]:assert w[1]%L==0 and (w[0]-a0*(w[1]//L))%N==0
assert abs(u[0]*v[1]-u[1]*v[0])==N*L and 2*abs(d)<=a<=b
assert a==125907943435801460896187665440000 and isqrt(a)==11220870885800329
out={'status':'PASS','patterns_split_both_pairs':52,'tower':rows,'lattice':{'basis_verified':True,'Gauss_reduced':True,'minimum_norm_squared':a,'integer_lower_bound_norm':isqrt(a),'rational_relation_validity':'requires the local-prime constraints; curve reconstructed in a separate audit'},'universal_tower_derivation':{'seed_X_count':10,'seed_probe_difference':18,'recurrence':'Delta[r+1]=-10*2**r*Delta[r]','formula':'18*(-10)**r*2**(r*(r-1)//2)'},'review':'same-session self-review with orthogonal finite implementation'}
(R/'TOWER_LATTICE_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
