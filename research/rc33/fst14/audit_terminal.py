"""Independent exact finite checks of the received FST14 engine, via declared adapters."""
import sys,json,platform,hashlib
from pathlib import Path
from math import gcd,lcm
import fst14 as f
import exact_inverse as e
R=Path(__file__).resolve().parent
print(json.dumps({'equations':['K(w)=8*10^ell-9*val(w)','K_j=K0*343^j','K0*343^j=-9*s mod 10^d','T=ord_(10^d/gcd(K0,10^d))(343)'],
 'variables':{'h':'signed primitive label','ell':'literal word length','d':'literal suffix length','j':'zero-based fibre index'},'units':'dimensionless exact integers',
 'python':platform.python_version(),'parameters':{'short_suffix_depths':[1,2,3],'deep_suffix_depths':[10,31,110],'deep_exponent':10**19+123456789,'labels':[8,782,-1,2,5,32,125,-10],'universal_order_depths':[1,7],'fibre_count_lengths':[0,100],'literal_lengths':[1,27],'literal_suffix_depths':[1,4],'CRT_moduli':[1,14],'fusion_lengths':[3,19],'example_lengths':[20,50,100,1000,10000]},'historical_baselines':'not supplied; explicit exact adapter'},ensure_ascii=False),flush=True)
assert (R/'fst14.py').read_bytes()==(R/'inputs/fst14.py').read_bytes() if (R/'inputs/fst14.py').exists() else True
labels=[8,782,-1,2,5,32,125,-10]
labels=[h for h in labels if any(h*7**a%9==8 for a in range(3)) and h%7]
orders=classes=decodes=crtchecks=fastcounts=0
for d in range(1,8):
 M=10**d;T=f.universal_period(d)
 assert T==2**max(2,d-3)*5**max(0,d-2) and pow(343,T,M)==1
 for p in (2,5):
  if T%p==0:assert pow(343,T//p,M)!=1
 assert 4*10**(d-1)//T==80 if d>=5 else True
 orders+=1
for h in labels:
 k=e.base(h)[0]
 for ell in range(0,101):
  assert f.fast_fiber_size(h,ell)==e.fibre_count(h,ell);fastcounts+=1
 for d in (1,2,3):
  M=10**d;orbit={};x=0;T=f.effective_period(k,d)
  # Independent suffix calculation: materialize one minimally long literal word per rank.
  for j in range(T):
   n=k*343**j;c=e.canonical(n);word='8'*max(0,d-len(c))+c;s=word[-d:]
   assert s not in orbit;orbit[s]=j
  assert len(orbit)==T and f.suffix_of_rank(h,T,d)==f.suffix_of_rank(h,0,d)
  for s in range(M):
   literal=str(s).zfill(d);sol=f.suffix_rank_residue(h,literal)
   assert sol==(orbit[literal],T) if literal in orbit else sol is None
   classes+=1
  orders+=1
 for ell in range(1,28):
  A=e.fibre_count(h,ell)
  for d in range(1,min(4,ell)+1):
   words=[e.decode(h,ell,j) for j in range(A)]
   assert (len({w[-d:] for w in words})==A)==(f.effective_period(k,d)>=A)
   for s in {w[-d:] for w in words}|{'0'*d}:
    expected=[j for j,w in enumerate(words) if w.endswith(s)];cert=f.suffix_certificate(h,ell,s)
    assert cert.count==len(expected)
    for i,j in enumerate(expected):assert f.select_suffix_rank(cert,i)==j and f.decode_suffix_selection(cert,i)==words[j];decodes+=1
   if A>1:
    actual=next(dd for dd in range(1,ell+1) if len({w[-dd:] for w in words})==A)
    assert f.minimum_suffix_digits(h,ell)==actual
for m in range(1,15):
 for n in range(1,15):
  for a in range(m):
   for b in range(n):
    got=f.generalized_crt(a,m,b,n);expected=next((x for x in range(lcm(m,n)) if x%m==a and x%n==b),None)
    assert got==((expected,lcm(m,n)) if expected is not None else None);crtchecks+=1
large=10**19+123456789;deep=[]
for h in (782,8,-1):
 for d in (10,31,110):
  s=f.suffix_of_rank(h,large,d);got=f.suffix_rank_residue(h,s);T=f.effective_period(e.base(h)[0],d)
  assert got==(large%T,T);deep.append({'h':h,'digits':d,'index':str(large),'residue':str(got[0]),'period':str(T)})
examples=[]
for ell in (20,50,100,1000,10000):examples.append({'ell':ell,'candidates':f.fast_fiber_size(782,ell),'minimum_suffix_digits':f.minimum_suffix_digits(782,ell)})
assert [x['candidates'] for x in examples]==[8,19,39,394,3944]
assert [x['minimum_suffix_digits'] for x in examples]==[3,3,4,5,7]
from dataclasses import asdict
cert02=asdict(f.suffix_certificate(782,1000,'02'));cert00002=asdict(f.suffix_certificate(782,1000,'00002'))
assert cert02['count']==99 and cert00002['count']==1 and cert00002['residue']==392
# New composition: observations at possibly different lengths reduce to the longest suffix.
fusions=0
for h in labels:
 for ell in range(3,20):
  for j in range(e.fibre_count(h,ell)):
   w=e.decode(h,ell,j);c=f.suffix_certificate(h,ell,w[-3:]);b=f.suffix_certificate(h,ell,w[-2:]);a=f.suffix_certificate(h,ell,w[-1:])
   assert c.period%b.period==0 and b.period%a.period==0
   assert c.residue%b.period==b.residue and b.residue%a.period==a.residue;fusions+=1
out={'status':'PASS','adapter_contract':'explicit independently checked three-function adapter; missing baselines not claimed',
 'orders_checked':orders,'suffix_classes_exhausted':classes,'literal_reconstructions':decodes,'fast_counts_checked':fastcounts,'generalized_CRT_cases':crtchecks,
 'nested_suffix_fusions':fusions,'labels':labels,'deep_lifts':deep,'examples':examples,'suffix_02':cert02,'suffix_00002':cert00002,
 'historical_50_tests_replayed':False,'historical_browser_tests_replayed':False,'new_global_RGPHI_rows_closed':0}
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
