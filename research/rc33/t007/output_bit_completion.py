from pathlib import Path
from collections import deque
import json,hashlib
R=Path(__file__).resolve().parent;edges=json.loads((R/'Q_COLLISION_EDGES.json').read_text());adj={}
print('CONFIG: exact postprocessing of q=N(XXXXXY); complete binary universes n=16..20; output one bit; internal counter/codebook memory not counted as one bit; zero-error validation on every ambiguous O5 fibre',flush=True)
def count(w,p):
 d=[1]+[0]*len(p)
 for x in w:
  for i in range(len(p),0,-1):
   if p[i-1]==x:d[i]+=d[i-1]
 return d[-1]
for e in edges:
 a,b=e['q'];assert a!=b;adj.setdefault(a,set()).add(b);adj.setdefault(b,set()).add(a)
colour={}
for root in sorted(adj):
 if root in colour:continue
 colour[root]=0;todo=deque([root])
 while todo:
  a=todo.popleft()
  for b in sorted(adj[a]):
   if b not in colour:colour[b]=1-colour[a];todo.append(b)
   assert colour[b]!=colour[a]
# Orthogonal validation of every stored collision, not only graph edges.
from itertools import product
seen=set()
for e in edges:
 a,b=e['words'];qa,qb=e['q'];assert len(a)==len(b)==e['n']
 assert count(a,'XXXXXY')==qa and count(b,'XXXXXY')==qb
 signature=[]
 for k in range(1,6):
  for pat in product('XY',repeat=k):
   p=''.join(pat);ca=count(a,p);assert ca==count(b,p);signature.append(ca)
 assert colour[qa]!=colour[qb]
 key=(e['n'],tuple(signature));assert key not in seen;seen.add(key)
from collections import Counter
expected=json.loads((R/'INDEPENDENT_OBSERVER_SCAN.json').read_text())['rows']
assert Counter(e['n'] for e in edges)=={r['n']:r['ambiguous_O5_fibres'] for r in expected}
assert all(r['duplicate_O5_rows']==2*r['ambiguous_O5_fibres'] for r in expected)
out={'status':'PASS','word_lengths':[16,20],'complete_collision_fibres_checked':len(edges),'q_values':len(colour),'distinct_confusion_edges':sum(map(len,adj.values()))//2,'key_alphabet_size':2,'minimum_output_bits':1,'encoding':'K(w)=colour[N_w(XXXXXY)], default colour 0 off listed vertices','key_codebook':{str(k):v for k,v in sorted(colour.items())},'coverage_edges_sha256':hashlib.sha256((R/'Q_COLLISION_EDGES.json').read_bytes()).hexdigest(),'limits':'Bounded zero-error output-bit certificate. No one-bit instrument-memory claim and no guarantee beyond length 20. Simple key floor(q/2) mod2 already fails at n=19.'}
(R/'OUTPUT_BIT_CERTIFICATE.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='key_codebook'},indent=2))
