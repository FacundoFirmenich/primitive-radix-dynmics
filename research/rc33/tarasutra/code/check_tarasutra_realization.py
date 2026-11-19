"""Independent exact realization check. Standard library only; no search engine."""
from pathlib import Path
from fractions import Fraction as F
from math import gcd,lcm
import json,hashlib,gzip,sys
R=Path(__file__).resolve().parents[1]
C=R/'certificates/tarasutra-2026-11-19'
A,Cc,D,Q,E=1089859,1627375,3121631,2087631,2105745
B0=2720751096305053288157586672376
L=3245172386374697665101193455750
raw=((A,Q),(Cc,Q),(Cc,D),(2*A,D),(A,E))
t=(1,0,3,2,4);s=(4,2,1,0,0)
print(json.dumps({'before_execution':{'version':'RGPHI-RC3.3 / 2026-11-19',
 'units':'dimensionless exact integers and rationals',
 'equations':['T_B(x)=B*x-floor(B*x)','S_B(x)=1/(1+T_B(1/x-1))',
 'B=B0+n*L; n>=0'],
 'inputs':dict(A=A,C=Cc,D=D,Q=Q,E=E,r=2,B0=B0,L=L),
 'unknown':'global least base and other primitive carriers'}},indent=2))
assert all(gcd(p,q)==1 for p,q in raw)
x=tuple(F(p,q) for p,q in raw)
assert len(set(x))==5 and all(F(1,2)<v<1 for v in x)
assert D==2*E-A
def T(v,b): return b*v-(b*v).__floor__()
def S(v,b): return 1/(1+T(1/v-1,b))
def merge(a,m,b,n):
 g=gcd(m,n);assert (b-a)%g==0
 k=((b-a)//g*pow(m//g,-1,n//g))%(n//g) if n//g>1 else 0
 return (a+m*k)%lcm(m,n),lcm(m,n)
edges=[];congruences=[]
for name,f,targets in [('T',T,t),('S',S,s)]:
 for i,j in enumerate(targets):
  p,q=raw[i];pp,qq=raw[j]
  defect=2 if (name,i)==('S',3) else 1
  for b in (B0,B0+L,B0+2*L):
   assert f(x[i],b)==x[j]
   assert gcd(b,q if name=='T' else p)==defect
  modulus=q if name=='T' else p
  residue=(defect*(pp if name=='T' else qq)*pow(p if name=='T' else q,-1,modulus))%modulus
  congruences.append((residue,modulus))
  edges.append(dict(generator=name,source=i,target=j,defect=defect,residue=residue,modulus=modulus))
a,m=0,1
for b,n in congruences: a,m=merge(a,m,b,n)
assert (a,m)==(B0,L)
assert L==lcm(*(z for pair in raw for z in pair))
# L contains every primitive coordinate: every integer in the CRT class
# has the same gcds and branch remainders, hence the same ten images.
for i in range(5):
 seen={i};todo=[i]
 while todo:
  j=todo.pop()
  for k in (t[j],s[j]):
   if k not in seen: seen.add(k);todo.append(k)
 assert len(seen)==5
ratios={}
for label,num,den in [('A-',D+2*Q,A),('A+',D-2*Q,A),
 ('C-',D+Q,Cc),('C+',D-Q,Cc),('D-',Cc+2*A,D),('D+',Cc-2*A,D),
 ('Q-',Cc+A,Q),('Q+',Cc-A,Q)]:
 z=F(num,den);ratios[label]=[z.numerator,z.denominator]
assert min(v[1] for v in ratios.values())==63
assert ratios['Q-']==[82,63]
p=C/'discovery_chunk.json.gz';blob=p.read_bytes()
assert hashlib.sha256(blob).hexdigest()=='aa879e28e67016882fedb3002570762e895b2fb1a96e453f7a01a3a7aac8a762'
chunk=json.loads(gzip.decompress(blob));payload=chunk['payload']
encoded=json.dumps(payload,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
assert hashlib.sha256(encoded).hexdigest()==chunk['payload_sha256']=='bb473c6a06565ef78af99c2ce573ac9a84084f2569139f8275c563d89cb8a73a'
assert [A,Cc,D,Q] in payload['outputs']['T1']['high_candidates']
result=dict(status='PASS',claim='119772/r2 = DF015-0003/S is realized',
 core=dict(A=A,C=Cc,D=D,Q=Q,E=E,r=2),
 states=[str(v) for v in x],maps=dict(T=t,S=s),edges=edges,
 base_fibre=dict(residue=B0,modulus=L,parameter='n>=0'),
 signed_cofactors=ratios,minimum_signed_denominator=63,
 completion_index=E//gcd(E,lcm(A,Cc,D,Q)),
 discovery=dict(policy='T1',h=63,k=82,node='Q',sign=-1,
 completed_at=payload['completed_at'],payload_sha256=chunk['payload_sha256']),
 scope='Explicit realization and complete base fibre; no exhaustive global classification.')
print(json.dumps(result,ensure_ascii=False,indent=2))
if '--write' in sys.argv:
 (R/'results/TARASUTRA_R2_REALIZATION.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
