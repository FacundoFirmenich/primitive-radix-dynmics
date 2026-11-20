"""Reproducible JSON report for the Argüelles->RC3.3 instrument."""
from __future__ import annotations
import argparse
import json
from fractions import Fraction
from pathlib import Path
from .loom_bridge import full_audit,witness_modular_readings

def make_report():
    r = full_audit()
    A,C,D,Q,E = 1089859,1627375,3121631,2087631,2105745
    x = (Fraction(A,Q),Fraction(C,Q),Fraction(C,D),Fraction(2*A,D),Fraction(A,E))
    r['rgphi_witness_modular_observer'] = witness_modular_readings(x,(2,4,8,16,32,64,260))
    r['witness_source'] = 'primitive-radix-mobius-dynamics/research/rc33/tarasutra/RESULTS.md'
    r['reproducible'] = True
    return r

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--output')
    x=p.parse_args()
    r=json.dumps(make_report(),ensure_ascii=False,indent=2,sort_keys=True) + '\n'
    if x.output:
        path=Path(x.output)
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(r,encoding='utf-8')
    else:
        print(r)
if __name__=='__main__': main()