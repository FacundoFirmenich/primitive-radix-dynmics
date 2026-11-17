"""Exact consequence checker for a future supplied critical-word/endpoint dataset.

The endpoint enclosures must be justified by the originating mathematical model.
This file does not manufacture that missing model or certify its enclosures.
"""
from fractions import Fraction
from collections import Counter
import argparse,json
import exact_inverse as E

def endpoint_profile(intervals,k):
    scale=10**k;prefix=[];interior=[];last=None
    for lo,hi in intervals:
        a,b=Fraction(lo),Fraction(hi)
        if not 0<=a<=b<=1:raise ValueError('endpoint outside the phase interval')
        if last is not None and a<=last:raise ValueError('endpoint enclosures overlap or are unsorted')
        last=b
        r=a*scale;s=b*scale
        if a==b and r.denominator==1:
            prefix.append(int(r));continue
        if int(r)!=int(s) or r.denominator==1 or s.denominator==1:
            raise ValueError('refine endpoint enclosure before assigning a decimal cylinder')
        prefix.append(int(r));interior.append(int(r))
    return {'digits':k,'max_interior_boundaries_per_cylinder':max(Counter(interior).values(),default=0),
            'all_endpoints_in_distinct_prefixes':len(prefix)==len(set(prefix))}

def verify(data):
    words=data['critical_words'];intervals=data['endpoint_intervals']
    if len(words)!=15 or len(set(words))!=15 or any(len(w)!=7 for w in words):raise ValueError('fifteen distinct seven-digit words required')
    labels=[E.primitive(E.key(w),7) for w in words]
    if len(intervals)!=1922:raise ValueError('the stated patch expects1922 endpoint enclosures')
    return {'critical_labels_distinct':len(labels)==len(set(labels)),
            'critical_fibre_sizes':[E.fibre_count(h,7) for h in labels],
            'critical_extra_bits':[E.bits(E.fibre_count(h,7)) for h in labels],
            'phase_profiles':[endpoint_profile(intervals,k) for k in [7,8,9]],
            'scope':'Consequences conditional on the supplied endpoint enclosures; their analytic provenance requires a separate source certificate.'}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('dataset');a=p.parse_args();data=json.load(open(a.dataset))
    print('CONFIG BEFORE COMPUTATION: fifteen literal seven-digit words;1922 exact rational endpoint enclosures; depths7,8,9; exact fractions; endpoint-generating model remains an external prerequisite.')
    print(json.dumps(verify(data),indent=2))
