"""Execute the unchanged original atomic checker with one declared file-path redirect."""
from pathlib import Path
import importlib.util,hashlib,json,platform,sys
R=Path(__file__).resolve().parent
print(json.dumps({'equations':['K_a(W)=a*10000^n-9999*V(W)','K_Y-K_X=1667*10000^n','-3K_X+8K_Y-5K_Z=10000^n'],
 'parameters':{'atoms':{'X':4777,'Y':6444,'Z':7444},'external_radix':10000,'complete_token_lengths':[0,8],'original_engine_FST11':hashlib.sha256((R/'fst11.py').read_bytes()).hexdigest(),'illustrative_float_rational_inputs':['4777/6444','4777/7444','6444/7444'],'float_tolerance':'1e-14','float_formulas':['theta=asin(float(rational))','other=pi-theta','sin(theta),sin(other),cos(theta),cos(other)'],'float_units':'radians','float_checks_used_in_proofs':False},'python':platform.python_version(),'adapter':'file-location redirect only; both original Python files unchanged'}),flush=True)
loc=importlib.util.spec_from_file_location('atomic_received',R/'atomic_audit_original.py');mod=importlib.util.module_from_spec(loc);sys.modules[loc.name]=mod;loc.loader.exec_module(mod)
original=mod.spec_from_file_location
old_path=Path('/mnt/data/fst11(2).py')
def routed(name,path,*a,**kw):return original(name,R/'fst11.py' if Path(path)==old_path else path,*a,**kw)
mod.spec_from_file_location=routed
mod.main()
new=json.loads((R/'AUDITORIA_CUATRO_LINEAS.json').read_text());old=json.loads((R/'ATOMIC_ORIGINAL_RESULTS.json').read_text());assert new==old
assert new['verification']['check_count']==128076 and new['token_language_exhaustive']['enumerated_words']==9841
assert len(mod.checks)==128076
out={'status':'PASS','original_JSON_reproduced':True,'token_words':9841,'assertions_including_floating':128076,'exact_assertions':128070,'illustrative_floating_assertions':6,'illustrative_angle_pairs':3,'original_module_bytes_unchanged':True,'source_path_redirect':'/mnt/data/fst11(2).py -> preserved fst11.py','legacy_original_test_suites_replayed':False}
(R/'ATOMIC_AUDIT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
