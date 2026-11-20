from pathlib import Path
from fractions import Fraction as F
import json
import interval_survivor as a
import interval_survivor_v2 as b
R=Path(__file__).resolve().parent
print('BEFORE: exact dimensionless endpoint regressions; B2..12; reduced or unreduced fractions q2..40; three interval refinements; open touching point3/4 explicitly excluded.',flush=True)
xs=[(F(1,2),F(3,4)),(F(3,4),F(1))]
assert a.merge(xs)==xs and b.merge(xs)==xs
checks=0;layers=0
for B in range(2,13):
 xs=[(F(1,2),F(1))]
 for d in range(3):
  one=a.intersection(a.intersection(a.preimages(B,xs,'T'),a.preimages(B,xs,'S')),xs)
  ti=b.preimages_in_domain(B,xs,'T',xs);two=b.preimages_in_domain(B,xs,'S',ti)
  assert one==two;(layers:=layers+1)
  for q in range(2,41):
   for p in range(q//2+1,q):
    x=F(p,q);expected=any(l<x<u for l,u in xs) and all(any(l<y<u for l,u in xs) for y in [a.T(x,B),a.S(x,B)])
    assert any(l<x<u for l,u in one)==expected;checks+=1
  xs=one
out=dict(status='PASS',grid_endpoint_checks=checks,matching_refinement_layers=layers,touching_endpoints_preserved=True)
(R/'INTERVAL_BASIC_TESTS.json').write_text(json.dumps(out,indent=2)+'\n');print(out,flush=True)
