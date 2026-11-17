"""Exact cross-checks of the supplied FST-11 implementation and atlas tables.
No claim that the unattached historical test suites were rerun.
"""
from pathlib import Path
from itertools import product
from collections import defaultdict,Counter
import sys,json,hashlib,time,subprocess,platform,re
R=Path(__file__).resolve().parent;sys.path.insert(0,str(R/'src'));import fst11 as f
CONFIG={'equations':{'K':'8*10**len(w)-9*val(w)','primitive':'K/p**v_p(abs(K)); sign retained','normal_form':'8**t C(7**(a0(h)+3*j)*h)','carry':'P*x=y+c*10**ell','CRT':'M=p**(a+k)*q**(b+t)'},'units':'dimensionless exact integers and literal decimal words','constants':{'base':10,'coefficient':8,'slope':9,'normalizing_primes':[7,2],'scale':343},'domains':{'all_words_max_length':4,'all_keys_abs_bound':10000,'normal_h_abs_bound':120,'normal_j':[0,4],'normal_t':[0,3],'regular_language_lengths':[0,4],'atlas_languages':5,'atlas_lengths':[2,6],'modulus_counts':[1,2,7,14,49,64,98,343],'modulus_count_max_length':3,'finite_signature_lengths':[0,2],'signature_precision_pairs':[[1,1],[2,1]],'signature_primes':[7,2]},'python':platform.python_version(),'finite_decode_max_length':3,'prime_set_test_integer_bounds':[-100,100],'randomness':False,'non_claims':['No FST10 archive or original 47-test suite supplied','No global RGphi existence, uniqueness or least-base closure','No novelty certification']}
print('CONFIGURATION BEFORE COMPUTATION\n'+json.dumps(CONFIG,ensure_ascii=False,indent=2),flush=True)
t0=time.monotonic();before=json.loads((R/'INPUTS.json').read_text());results={}
def K(w):
 v=0
 for ch in w:v=10*v+ord(ch)-48
 return 8*10**len(w)-9*v

def norm(n,p=7):
 while n%p==0:n//=p
 return n

def words(ell):
 for ds in product('0123456789',repeat=ell):yield ''.join(ds)

# Original documented CLI, unchanged source; capture separately.
p=subprocess.run([sys.executable,'src/fst11.py'],cwd=R,text=True,capture_output=True);(R/'original_cli.log').write_text(p.stdout+p.stderr);assert p.returncode==0
cli=json.loads(p.stdout);assert cli['collisions_unrestricted_ell6']['unordered_pairs']==2923;results['original_cli']='PASS'
count=0
for ell in range(5):
 for w in words(ell):
  k=K(w);assert f.arithmetic_key(w)==k
  h,j,t=f.fiber_coordinates(w);assert f.fiber_word(h,j,t)==w
  assert f.fused_word(norm(k),norm(k,2),ell)==w
  can=w.lstrip('8');assert f.canonical_from_key(k)==can
  for t in range(3):assert K('8'*t+w)==k
  count+=1
results['exhaustive_words_length_0_to_4']=count
for k in range(-10000,10001):
 if k%9==8:
  w=f.canonical_from_key(k);assert K(w)==k and not w.startswith('8')
results['key_inverse_lattice_points']=sum(k%9==8 for k in range(-10000,10001))
for h in range(-120,121):
 if f.primitive_image_member(h):
  for j in range(5):
   for t in range(4):assert f.fiber_coordinates(f.fiber_word(h,j,t))==(h,j,t)
results['two_axis_normal_form']='PASS'
languages={'Todos':f.dfa_all(),'Termina 02':f.dfa_endswith('02'),'Sin cifra 7':f.dfa_no_digit('7'),'Suma de cifras 0 mod 3':f.dfa_digit_sum_mod(3),'Extremos sin intermedio':f.dfa_finite(['888889','901961'])}
tables=json.loads((R/'inputs/ATLAS_COUNTS.json').read_text())['case_counts']
for row in tables:
 actual=f.collision_pair_count(languages[row['language']],row['ell'])
 assert actual['accepted']==row['accepted'] and actual['unordered_pairs']==row['unordered_pairs']
 assert {str(k):v for k,v in actual['by_j'].items()}==row['by_j'],row
results['atlas_all_25_embedded_records_recomputed']=len(tables)
for name,A in languages.items():
 rev=A.reversed_for_lsd()
 for ell in range(5):
  groups=defaultdict(list);accepted=[]
  for w in words(ell):
   assert rev.run(w[::-1])==A.run(w)
   if A.run(w):groups[norm(K(w))].append(w);accepted.append(w)
  pairs=sum(len(g)*(len(g)-1)//2 for g in groups.values())
  assert f.collision_pair_count(A,ell)['unordered_pairs']==pairs,(name,ell)
  assert f.language_size(A,ell)==len(accepted)
  if ell<=3:
   for m in CONFIG['domains']['modulus_counts']:
    hist=Counter(int(w or '0')%m for w in accepted)
    for residue in range(min(m,5)):
     assert f.count_words_mod(A,ell,m,residue)==hist[residue]
results['direct_fibre_DFA_reversal_and_modular_counts']='PASS (five languages, literal lengths 0..4; modular counts 0..3)'
# Canonical DFA and prefix-ambiguity are compared to finite-language definitions.
fixtures=[[],[''],['8','88'],['02','802','8802','9','888'],['123','8123'],['1','22','333']]
for ws in fixtures:
 A=f.dfa_finite(ws);C=f.canonical_image_dfa(A);target={w.lstrip('8') for w in ws}
 for ell in range(4):
  for w in words(ell):assert C.run(w)==(w in target)
 ambiguous=any(u!=v and K(u)==K(v) for u in ws for v in ws)
 witness=f.boundary_ambiguity(A);assert (witness is not None)==ambiguous
 if witness:
  u,v=witness;assert A.run(u) and A.run(v) and K(u)==K(v) and u!=v
  assert 1<=len(v)-len(u)<=A.states and len(u)<=A.states*A.states-1
results['canonical_language_and_bounded_witness']='PASS (six finite-language fixtures)'
# Every observed finite signature class is cross-checked, not a random sample.
signature_cases=0
for name,A in list(languages.items())[:4]:
 for ell in range(3):
  for kp,kq in [(1,1),(2,1)]:
   hist=Counter()
   for w in words(ell):
    if A.run(w):hist[(f.precision_signature(w,7,kp),f.precision_signature(w,2,kq))]+=1
   for ((a,up),(b,uq)),n in hist.items():
    r=f.finite_hyperaccess_count(A,ell,7,a,kp,up,2,b,kq,uq);assert r['compatible_count']==n
    signature_cases+=1
results['all_observed_signature_classes_checked']=signature_cases
w='002';a,up=f.precision_signature(w,7,1);b,uq=f.precision_signature(w,2,2)
restricted=f.finite_hyperaccess_count(f.dfa_endswith('02'),3,7,a,1,up,2,b,2,uq)
unrestricted=f.finite_hyperaccess_count(f.dfa_all(),3,7,a,1,up,2,b,2,uq)
assert restricted['modulus']==56 and restricted['compatible_count']==1 and unrestricted['compatible_count']==18
results['language_assisted_identification']={'word':w,'K':K(w),'a7':a,'unit7_mod7':up,'a2':b,'unit2_mod4':uq,'unrestricted':unrestricted,'ends02':restricted}
assert f.carry_pair_count(languages['Extremos sin intermedio'],6,1)==0 and f.carry_pair_count(languages['Extremos sin intermedio'],6,2)==1
results['missing_middle']={'words':['888889','901961'],'K':[-1,-117649],'j1_pairs':0,'j2_pairs':1}
# Integer-only Beatty cutpoints: no floating logarithm or inferred proof.
lengths=[]
for j in range(41):
 n=343**j;ell=0;m=1
 while m<n:ell+=1;m*=10
 can=f.canonical_from_key(8*n);assert len(can)==ell;lengths.append(ell)
assert set(b-a for a,b in zip(lengths,lengths[1:]))=={2,3}
results['canonical_h8_first_41_lengths']=lengths
# Exercise the guaranteed finite decoder and zero-candidate decision explicitly.
decode_cases=0
for ell in range(4):
 for w in words(ell):
  a,up=f.precision_signature(w,7,3);b,uq=f.precision_signature(w,2,4)
  assert f.finite_hyperaccess_decode(ell,7,a,3,up,2,b,4,uq)==w
  decode_cases+=1
results['guaranteed_finite_decoder_words']=decode_cases
assert f.finite_hyperaccess_count(f.dfa_finite([]),3,7,0,1,2,2,1,2,3)['status']=='INCONSISTENT'
sets=[set(),{2},{3},{7},{2,7},{3,5}]
for n in range(-100,101):
 if n==0:continue
 for S in sets:
  for T in sets:
   a=abs(f.primitive_set(n,S));b=abs(f.primitive_set(n,T))
   from math import lcm,gcd
   assert lcm(a,b)==abs(f.primitive_set(n,S&T))
   assert gcd(a,b)==abs(f.primitive_set(n,S|T))
results['prime_set_lattice_pairs_checked']=200*len(sets)**2
for row in before:assert hashlib.sha256((R/row['path']).read_bytes()).hexdigest()==row['sha256']
results['status']='PASS';results['runtime_seconds']=time.monotonic()-t0
(R/'AUDIT_RESULTS.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2),flush=True)
