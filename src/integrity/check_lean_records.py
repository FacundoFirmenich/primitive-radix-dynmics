"""Verify the committed Lean receipt; this command does not execute Lean."""
from pathlib import Path
import hashlib,json,re
R=Path(__file__).resolve().parents[2];L=R/'formal/lean'
def read(p):return json.loads((L/p).read_text())
a=read('records/current/AUDIT.json');c=read('COVERAGE.json')
assert a['status']=='PASS' and a['named_theorems']==144 and a['modules']==17
assert a['custom_axioms']==[] and not a['sorry_admit_native_decide']
assert a['kernel_trust_argument']==0 and a['mutation_pairs']==7
assert set(a['standard_axioms_used'])=={'propext','Classical.choice','Quot.sound'}
assert a['mathlib_revision']=='c44e0c8ee63ca166450922a373c7409c5d26b00b'
assert len(c['claims'])==6 and c['status']=='partial formalization'
assert all(x['status']=='PROVED_LEAN_KERNEL' for x in c['claims'])
assert len(a['declarations'])==144 and len({d['name'] for d in a['declarations']})==144
for p,h in a['source_hashes'].items():assert hashlib.sha256((L/p).read_bytes()).hexdigest()==h,p
for p,h in read('SOURCE_SHA256.json').items():assert hashlib.sha256((L/p).read_bytes()).hexdigest()==h,p
for command in a['commands']:
 expected=command['expected'];actual=command['exit_code']
 assert (expected==0 and actual==0) or (expected!=0 and actual!=0),command
assert sum(x['label'].endswith('-reject') for x in a['commands'])==7
assert sum(x['label'].endswith('-control') for x in a['commands'])==7
assert len(list((L/'RadixMobius').glob('*.lean')))==17
assert not (L/'.lake').exists(),'dependency cache must not enter the publication'
print('PASS:144 Lean statements,17 modules,7 mutation pairs; committed receipt/source hashes agree. Lean not rerun by this integrity command.')
