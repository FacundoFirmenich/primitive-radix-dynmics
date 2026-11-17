"""Separate reconstructions of reduced five-family, dual and two-step partitions."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import json
R=Path(__file__).resolve().parent
cert=json.loads((R/'EXACT_CERTIFICATE.json').read_text());bounds={r['m']:tuple(map(F,r['threshold_interval'])) for r in cert['critical_words']}
M=[5,9,10,12,15];orig={m:20*m for m in M}
print('CONFIG BEFORE CALCULATION: exact rational enclosures from Machin40 and uniform Taylor bounds; reduced families5,9,10,12,15; original angles m/500 degrees; phase z={10^(2n+7)*pi/90}; forward100; dual phase9z with normalized threshold9*tau/m; d1,2,3 carry tests; no pi trajectory data supplied.',flush=True)
def partition(observers):
 cuts={}
 def put(key,lo,hi):
  if key in cuts:assert cuts[key]==(lo,hi)
  else:cuts[key]=(lo,hi)
 for shift,m,coef in observers:
  # obs frac(m*x)<coef*tau_original ; shift distinguishes temporal labels only.
  lo,hi=bounds[orig[shift]]
  for j in range(m):
   base=F(j,m);put(('start',base),base,base)
   put(('moving',orig[shift],base,coef/m),base+coef*lo/m,base+coef*hi/m)
 put(('start',F(1)),F(1),F(1));ordered=sorted(cuts.values())
 assert all(a[1]<b[0] for a,b in zip(ordered,ordered[1:])), 'envelopes overlap'
 patterns=[]
 for a,b in zip(ordered,ordered[1:]):
  x=(a[1]+b[0])/2;p=''
  for shift,m,coef in observers:
   t=m*x;t-=t.__floor__();lo,hi=bounds[orig[shift]]
   if t<coef*lo:p+='1'
   elif t>coef*hi:p+='0'
   else:raise AssertionError(('unresolved',shift,x))
  patterns.append(p)
 count=Counter(patterns)
 return dict(endpoints=len(ordered),cells=len(patterns),patterns=len(count),max_cells_per_pattern=max(count.values()),pattern_counts=dict(sorted(count.items())),pattern_bits=(len(count)-1).bit_length(),cell_bits=(len(patterns)-1).bit_length(),conditional_cell_bits=(max(count.values())-1).bit_length())
natural=partition([(m,m,F(1)) for m in M]);assert(natural['endpoints'],natural['patterns'],natural['max_cells_per_pattern'])==(86,13,34)
dual=partition([(m,m,F(1)) for m in M]+[(m,9,F(9,m)) for m in M]);assert(dual['endpoints'],dual['patterns'],dual['max_cells_per_pattern'])==(114,21,33)
# Applying the same uniform bounds to time n+1 is valid; the next-step observer is frac(100*m*z).
two=partition([(m,m,F(1)) for m in M]+[(m,100*m,F(1)) for m in M]);assert(two['endpoints'],two['patterns'],two['max_cells_per_pattern'])==(8552,150,2074)
fifteen=Counter((R/'CELL_PATTERNS.csv').read_text().splitlines()[1:]) # parse column separately
fifteen=Counter(line.split(',')[1] for line in (R/'CELL_PATTERNS.csv').read_text().splitlines()[1:]);assert max(fifteen.values())==730
# Carry vectors of full phases, not binary borrowing masks.
def carries(mult):
 ends=sorted({F(j,m) for m in mult for j in range(m+1)})
 return [tuple((m*(a+b)/2).__floor__() for m in mult) for a,b in zip(ends,ends[1:])]
checks=[]
for d,mults in [(1,[5,12]),(1,[5,12,15]),(2,[5,12]),(3,[5,12])]:
 mod=10**d;cs=carries(mults);observations={};aliases=[]
 for k in range(mod):
  for c in cs:
   obs=tuple((m*k+t)%mod for m,t in zip(mults,c))
   if obs in observations and observations[obs]!=k:aliases.append([obs,observations[obs],k])
   observations[obs]=k
 if d>=2 or len(mults)==3:assert not aliases
 else:assert aliases
 checks.append(dict(digits=d,multipliers=mults,carry_cells=len(cs),complete_cases=mod*len(cs),cross_prefix_aliases=len(aliases),alias_example=aliases[:1]))
out=dict(status='PASS',natural=natural,dual=dual,two_step=two,fifteen_max_cell_fibre=730,full_phase_prefix_checks=checks,
 older_pi_samples_replayed=False,scope='Complete potential-phase partitions, uniform all n>=0; no normality or visit-frequency assertion.')
(R/'EXTENDED_PARTITIONS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:{a:b for a,b in v.items() if a!='pattern_counts'} if isinstance(v,dict) else v for k,v in out.items()},indent=2))
