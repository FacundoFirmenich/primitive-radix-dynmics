"""Replay and cross-check the arithmetic integrated into canonical RC3.3.

Assertion tested: every numerator, sign and position for any signed cofactor
denominator h<=14 in the three declared residual systems is covered by the
bounded integer-level reduction; only the known carrier survives.  This is
an all-height bounded-cofactor assertion, never an unbounded-h conclusion.
The packing replay tests necessary filters, not realization of survivors.
"""
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from importlib.util import spec_from_file_location, module_from_spec
from itertools import combinations
from math import gcd
from pathlib import Path
from datetime import datetime, timezone
import importlib
import json
import platform
import subprocess
import sys
import time
import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
NEST = ROOT/'certificates/nested'
PACK = ROOT/'certificates/prime-packing'
RESULTS = ROOT/'results'
RESULTS.mkdir(exist_ok=True)


def sha(p):
    return sha256(p.read_bytes()).hexdigest()


def inputs():
    return {str(p.relative_to(ROOT)):sha(p)
            for base in [NEST, PACK] for p in sorted(base.rglob('*'))
            if p.is_file() and p.suffix in {'.py','.md'} and '__pycache__' not in p.parts}


def fresh_vertices(code,r):
    """Enumerate vertices from the written chamber halfspaces, not a table."""
    x,y,z = sp.symbols('x y z')
    if code == 119772: # (C,D,Q), A=1
        inequalities = [x-1,z-x,2-z,y-r,2*x-y]
        embed = lambda v:(F(1),v[0],v[1],v[2])
    else: # (A,C,D), Q=1
        inequalities = [2*y-3,z-y,2*x-z,2-2*x]
        embed = lambda v:(v[0],v[1],v[2],F(1))
    out = set()
    for walls in combinations(inequalities,3):
        mat,rhs = sp.linear_eq_to_matrix(walls,(x,y,z))
        if mat.det() == 0:
            continue
        v = mat.inv()*rhs
        sub = dict(zip((x,y,z),v))
        if all(expr.subs(sub)>=0 for expr in inequalities):
            out.add(embed(tuple(F(int(q.p),int(q.q)) for q in v)))
    assert len(out) == 4
    return out


def coverage_and_algebra():
    # Reconstruct the central cancellation with general rational coefficients.
    A,C,Q,al,be,ga,de,k,h,z1,z2,f = sp.symbols('A C Q al be ga de k h z1 z2 f',nonzero=True)
    D=al*Q+k*A/h
    R1=de**2*h**2*(D**2-be**2*Q**2)-k**2*C**2
    R2=k*(C**2-de**2*A**2)+al*h*(ga**2-de**2)*A*Q
    K=f*z2*R2/(D*Q)
    u=z1*de**2*h**2*(al**2-be**2)-z1*k*K*al/(f*z2)
    v=z1*al*h*k*(ga**2+de**2)-z1*k**2*K/(f*z2*h)
    assert sp.factor(z1*R1/Q-u*Q-v*A) == 0

    sys.path.insert(0,str(NEST))
    module = importlib.import_module('nested_strata')
    strata=json.loads((NEST/'NESTED_STRATA_RESULTS.json').read_text())
    pure=json.loads((NEST/'PURE_SIGN_NESTED_REPLAY.json').read_text())
    assert len(strata)==24 and len(pure)==3
    all_rows=strata+pure
    actual={(row['code'],row['r'],p['node'],p['sign'],p['k'],p['h'])
            for row in all_rows for p in row['planes']}
    assert len(actual)==702
    expected=set()
    mappings={'A':(0,1,2,3),'C':(1,0,2,3),'D':(2,3,1,0),'Q':(3,2,1,0)}
    for code,r in [(119772,2),(119772,3),(606897,3)]:
        vertices=fresh_vertices(code,r)
        assert vertices == set(module.vertices(code,r))
        a,b,g,d=map(F,(r,1,r,1) if code==119772 else (1,3,1,3))
        coefficients={'A':(a,b,g,d),'C':(b,a,1/g,1/d),
                      'D':(g,d,1/b,1/a),'Q':(d,g,b,a)}
        for node,mapping in mappings.items():
            assert coefficients[node] == module.coefficients(code,r,node)
            for sign in [-1,1]:
                alpha=sign*coefficients[node][0]
                vals=[(v[mapping[2]]-alpha*v[mapping[3]])/v[mapping[0]] for v in vertices]
                lo,hi=min(vals),max(vals)
                for den in range(1,15):
                    if gcd(den,r)>1:
                        continue
                    first=(den*lo).numerator//(den*lo).denominator-1
                    last=(den*hi).numerator//(den*hi).denominator+2
                    for num in range(first,last+1):
                        if not lo<F(num,den)<hi or gcd(num,den)!=1 or not num:
                            continue
                        if r==2 and num%2 != int(node in {'A','D'}):
                            continue
                        if ((code==119772 and node in {'A','D'}) or
                                (code==606897 and node in {'C','Q'})) and num%r==0:
                            continue
                        expected.add((code,r,node,sign,num,den))
    assert actual==expected,{'missing':sorted(expected-actual),'extra':sorted(actual-expected)}

    checked=0
    for row in all_rows:
        for plane in row['planes']:
            assert not plane['degenerate'] and plane['coordinate_cutoff'] is None
            mapping=mappings[plane['node']]
            al,be,ga,de=map(F,plane['coefficients'])
            k,h=plane['k'],plane['h']
            for core in plane['high_candidates']:
                a,c,d,q=map(F,[core[i] for i in mapping])
                assert h*d==al*h*q+k*a
                r1=de*de*h*h*(d*d-be*be*q*q)-k*k*c*c
                r2=k*(c*c-de*de*a*a)+al*h*(ga*ga-de*de)*a*q
                jj=plane['z1']*r1/(c*q)
                kk=(row['r']-1)*plane['z2']*r2/(d*q)
                assert jj.denominator==kk.denominator==1
                assert plane['level_bounds']['J'][0]<=jj<=plane['level_bounds']['J'][1]
                assert plane['level_bounds']['K'][0]<=kk<=plane['level_bounds']['K'][1]
                checked+=1
    assert sum(p['level_pairs'] for row in strata for p in row['planes'])==156195248
    assert sum(p['level_pairs'] for row in pure for p in row['planes'])==2008
    return {'status':'PASS','chamber_vertices':'three halfspace enumerations match the encoded tetrahedra',
            'symbolic_level_cancellation':'PASS','complete_signed_planes':len(actual),
            'reported_raw_candidates_rechecked':checked,
            'nonzero_J_level_pairs':156195248,'h1_nonzero_J_level_pairs':2008,
            'zero_level_cases':'handled separately by the enumerator; not included in these pair counters',
            'scope':'Coverage of h<=14, not a uniform cofactor bound'}


def run():
    started=datetime.now(timezone.utc).isoformat()
    before=inputs()
    manifest={'schema':'rgphi-integrated-arithmetic-run-v2',
              'run':{'started_utc':started,'status':'running'},
              'software':{'python':sys.version,'platform':platform.platform(),
                          'sympy':sp.__version__},
              'input_hashes_before':before,'commands':[],
              'assertion_tested':__doc__,'review':'sequential self-review, not independent peer review'}
    mp=RESULTS/'NESTED_INTEGRATION_RUN.json'
    mp.write_text(json.dumps(manifest,indent=2)+'\n')
    jobs=[(NEST,['run_all.py'],'integrated_nested'),
          (NEST,['joint_fiber_attack.py'],'integrated_joint'),
          (NEST,['truth_preserving_nesting.py'],'integrated_truth_preservation'),
          (PACK,['prime_power_packing.py'],'integrated_prime_packing')]
    for cwd,args,name in jobs:
        log=RESULTS/(name+'.log');start=time.monotonic()
        with log.open('w') as f:
            proc=subprocess.run([sys.executable,'-B',*args],cwd=cwd,stdout=f,stderr=subprocess.STDOUT)
        manifest['commands'].append({'argv':[sys.executable,'-B',*args],
                                     'cwd':str(cwd.relative_to(ROOT)),
                                     'returncode':proc.returncode,'seconds':time.monotonic()-start,
                                     'log':str(log.relative_to(ROOT)),'log_sha256':sha(log)})
        mp.write_text(json.dumps(manifest,indent=2)+'\n')
        print(name,'PASS' if proc.returncode==0 else 'FAIL',flush=True)
        if proc.returncode:
            manifest['run']['status']='failed'
            mp.write_text(json.dumps(manifest,indent=2)+'\n')
            raise SystemExit(proc.returncode)
    cov=coverage_and_algebra()
    (RESULTS/'NESTED_COVERAGE_CHECKS.json').write_text(json.dumps(cov,indent=2)+'\n')
    packing=json.loads((PACK/'RESULTS.json').read_text())
    assert packing['counts']['new_union_pass']==5246
    after=inputs();assert before==after
    manifest['input_hashes_after']=after
    manifest['run'].update({'status':'completed','finished_utc':datetime.now(timezone.utc).isoformat()})
    manifest['coverage_checks']=cov
    manifest['prime_packing_scope']='necessary-filter survivors, not realizations; known carrier retained separately'
    manifest['output_hashes']={str(p.relative_to(ROOT)):sha(p)
                               for base in [NEST,PACK] for p in sorted(base.glob('*.json'))}
    mp.write_text(json.dumps(manifest,indent=2)+'\n')
    print('PASS: complete integrated arithmetic replay, signed-plane coverage and exact cancellation',flush=True)


if __name__=='__main__':
    run()
