"""Replay the retained near-solutions with the archived ten-edge checker."""
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parent
SRC=ROOT/'sources'
sys.path.insert(0,str(SRC/'src'))
spec=importlib.util.spec_from_file_location('archived',SRC/'verify_exceptional_crt.py')
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
print(json.dumps({'arithmetic':'exact rational','source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  'input':'BOUNDARY_CENSUS_T5000.json','coordinate_map':'(A_native,C_native,D_native,Q_native,E)=(Q,D,C,A,E)'}),flush=True)
assert m.edge_certificate(m.states_for(119772,3,406,712,1265,731,557),*m.ACTIONS[119772],3)==(88011536665779,223336848698040)
r=json.loads((ROOT/'BOUNDARY_CENSUS_T5000.json').read_text())['census']['three_square_samples']
assert len(r)==157
for row in r:
    a,c,d,q,e=row['core']
    assert m.validate_606897(q,d,c,a,e) is None
out={'archived_checker_positive_control':True,'terminal_three_square_cores_checked':len(r),
     'native_reflection_checked':True,'survivors':0,
     'scope':'independent checker, same underlying mathematical criterion; not an independent full census'}
(ROOT/'TERMINAL_CHECK.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2),flush=True)
