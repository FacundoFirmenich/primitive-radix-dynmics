from pathlib import Path
from itertools import product
from math import gcd
import json,subprocess
R=Path(__file__).resolve().parent
print('CONFIG: exact integers; 720 marked maps per supplied word; independent direct loops Q<=30; strict T factor 4..7; all twelve transitions retained',flush=True)
rows=[]
for word in ['TTTSSS','TTSTSS','TSTSTS']:
 maps=[];count=0
 for choices in product(range(6),range(1,2),range(1,3),range(1,4),range(1,5),range(1,6)):
  count+=1;T=[None]*6;S=[None]*6
  for i,g in enumerate(word):(T if g=='T' else S).__setitem__(i,(i+1)%6);(S if g=='T' else T).__setitem__(i,choices[i])
  if sorted(T[1:])==list(range(1,6)) and sorted(S)==list(range(6)):maps.append({'T':T,'S':S})
 assert count==720 and len(maps)==1;rows.append({'word':word,'marked_skeletons':count,'survivors':maps})
# Small scan from literal ranges, not root or divisor parametrizations.
counts={'primitive_Q_A_pairs':0,'first_cycle_D_candidates':0,'second_cycle_C_candidates':0,'high_primitive_P_candidates':0,'E_divisors_in_chamber':0,'E_also_root_mod_C':0,'E_also_root_mod_P':0}
for d in range(4,8):
 for Q in range(1,31):
  for A in range(Q//2+1,Q):
   if gcd(A,Q)>1:continue
   counts['primitive_Q_A_pairs']+=1
   for D in range(A+1,2*A):
    if (D*D-Q*Q)%A:continue
    counts['first_cycle_D_candidates']+=1
    for C in range(D//2+1,D):
     if (C*C-A*A)%D:continue
     counts['second_cycle_C_candidates']+=1
     if gcd(d,Q)>1:continue
     for k in range(-3,4):
      if not k or 2*abs(k)>=d:continue
      P=d*A+k*Q
      if not(d*Q<2*P and P<d*Q and P<2*C) or gcd(P,d*Q)>1:continue
      counts['high_primitive_P_candidates']+=1
      for E in range(P+1,2*C):
       if (P*P-C*C)%E:continue
       counts['E_divisors_in_chamber']+=1
       if (E*E-D*D)%C:continue
       counts['E_also_root_mod_C']+=1
       if (E*E-d*d*Q*Q)%P:continue
       counts['E_also_root_mod_P']+=1
p=subprocess.run([str(R/'hexagon_scan'),'30'],capture_output=True,text=True,check=True)
fast=json.loads(p.stdout.splitlines()[-1]);assert all(fast[k]==v for k,v in counts.items()),(counts,fast)
# Directly check every large-run terminal core and its unit obstruction.
terminal=[(4,2733,2315,4122,4097,6723,6527),(4,4733,3912,6677,6340,12383,10915),(5,201,184,351,275,549,518)]
for d,Q,A,D,C,E,P in terminal:
 assert gcd(P,d*Q)==gcd(A,Q)==gcd(A,D)==gcd(C,D)==gcd(C,E)==gcd(P,E)==1
 assert all(den<num*2 and num<den for num,den in [(P,d*Q),(A,Q),(A,D),(C,D),(C,E),(P,E)])
 assert (D*D-Q*Q)%A==(C*C-A*A)%D==(E*E-D*D)%C==(P*P-C*C)%E==(E*E-d*d*Q*Q)%P==0
 assert any(gcd(d,v)>1 for v in [A,C,D,E])
(R/'HEXAGON_CHECKS.json').write_text(json.dumps({'status':'PASS','skeletons':rows,'direct_prefix_Q':30,'direct_counts':counts,'terminal_cores_Q5000_checked':terminal,'terminal_obstruction':'d divides B while at least one required unit coordinate shares a prime with d'},indent=2)+'\n')
print('PASS: skeletons, direct small-prefix coverage and all three terminal unit obstructions')
