from pathlib import Path
from math import gcd
from collections import Counter
import json,time
from paired_fibres import paired,neighbours
from fibre_arithmetic import ROOT,SEEDS,chamber,primitive,rem

print('BEFORE: exact Z/Q, dimensionless; r=2 normal, r=3 normal/reflected; AC fixes (D,Q), DQ fixes (A,C). Independent brute-force unknown coordinates 1..32 for fixed coordinates 1..16. Four masked-opposite-pair positive controls. Constructed gcd barrier: source (376,637,1265,731), target (406,712,1265,731).',flush=True)


def independent(r,orientation,unknown,fixed):
    out=[]
    for u in range(1,33):
        for v in range(1,33):
            A,C,D,Q=(u,v,*fixed) if unknown=='AC' else (*fixed,u,v)
            if orientation=='reflected':
                real=3*A<2*D<2*C<4*Q<4*A
            else:
                real=A<C<Q<2*A and r*A<D<2*C
            if not real:continue
            if gcd(r,A*C*D*Q)!=1:continue
            if any(gcd(a,b)!=1 for a,b in [(A,Q),(Q,C),(C,D),(D,A)]):continue
            if (r-1)%gcd(A,C) or (r-1)%gcd(D,Q):continue
            if (D*D-r*r*Q*Q)%A or (D*D-Q*Q)%C or (C*C-r*r*A*A)%D or (C*C-A*A)%Q:continue
            out.append((A,C,D,Q))
    return sorted(out)


tic=time.monotonic();cases=0
for r,orientation in [(2,'normal'),(3,'normal'),(3,'reflected')]:
    for unknown in ['AC','DQ']:
        for u in range(1,17):
            for v in range(1,17):
                result=paired(r,orientation,unknown,(u,v))
                assert result['square_cores']==independent(r,orientation,unknown,(u,v))
                cases+=1

controls=[]
for fixture in json.loads((ROOT/'CORE_GATE_RESULTS.json').read_text())['positive_controls']:
    r=fixture['r'];A,C,D,Q,E=fixture['coordinates_ACDQE'];x=(A,C,D,Q)
    print('CONTROL_INPUT',dict(r=r,coordinates=[A,C,D,Q,E]),flush=True)
    for unknown,fixed in [('AC',(D,Q)),('DQ',(A,C))]:
        result=paired(r,'normal',unknown,fixed)
        assert x in result['square_cores']
        assert any(tuple(p['core'])==x for p in result['realizations'])
        controls.append(result)

source=(376,637,1265,731);target=(406,712,1265,731)
assert chamber(3,source,'normal') and primitive(3,source)
assert chamber(3,target,'normal') and primitive(3,target) and not any(rem(3,target))
assert gcd(406,637)==7 and gcd(376,712)==8
assert not primitive(3,(406,637,1265,731))
assert not primitive(3,(376,712,1265,731))
assert target in neighbours(3,'normal','AC',(1265,731))
initial=[]
for x in SEEDS:
    A,C,D,Q=x
    for unknown,fixed in [('AC',(D,Q)),('DQ',(A,C))]:
        initial.append(paired(3,'reflected',unknown,fixed))

result={'status':'PASS','independent_fixed_pair_contexts':cases,'independent_unknown_bound':32,'masked_pair_controls':controls,'constructed_barrier':{'source':source,'target':target,'A_first_opposite_gcd':7,'C_first_opposite_gcd':8,'paired_move_recovers_target':True,'scope':'Two direct one-coordinate orders fail; no claim that all longer paths fail.'},'initial_target_contexts':initial,'seconds':time.monotonic()-tic}
(ROOT/'PAIRED_TEST_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print('PAIRED_TEST_PASS',dict(contexts=cases,masked_controls=len(controls),initial_contexts=len(initial),initial_square_cores=sum(len(x['square_cores']) for x in initial),seconds=result['seconds']),flush=True)
