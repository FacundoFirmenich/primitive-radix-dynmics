#!/usr/bin/env python3
"""Stage VII: exact lifting of k-decks by one alternation probe, and commutator obstruction.

Only complete opaque source packets {4777} and {6444} are used.
X/Y below are EXTERNAL labels of interventions, never extracted packet digits.
No third-party dependencies; exhaustive up to n=20, constructive checks at higher n.
"""
import argparse
import json
from array import array
from itertools import product
from time import perf_counter

FIRST = 'XYYXXXXXYYYXXXXY'
SECOND = FIRST[::-1]
SELECTED_PROBE = 'XXXXXY'
ALPHABET = 'XY'
MAX_OBSERVER_ORDER = 5


def signatures(words, order):
    """Exact k-decks for a short list of EXTERNAL sequences (independent DP)."""
    patterns = ['']
    for size in range(1, order + 1):
        patterns.extend(''.join(w) for w in product(ALPHABET, repeat=size))
    idx = {pat: k for k, pat in enumerate(patterns)}
    ops = {char: sorted(((idx[p], idx[p[:-1]], len(p)) for p in patterns[1:]
                         if p[-1] == char), key=lambda x: -x[2]) for char in ALPHABET}
    out = []
    for word in words:
        state = [0]*len(patterns)
        state[0] = 1
        for char in word:
            for dest, src, _ in ops[char]:
                state[dest] += state[src]
        out.append(tuple(state[1:]))
    return out


def scan_lift(n):
    """Exhaustive exact enumeration; uint16 safe for n<=20: C(20,6)<65536."""
    if not 1 <= n <= 20:
        raise ValueError('This exhaustive packing is proved safe only for 1<=n<=20')
    pats = [()]
    for length in range(1, MAX_OBSERVER_ORDER + 1):
        pats.extend(product((0, 1), repeat=length))
    idx = {p:i for i,p in enumerate(pats)}
    ops = {bit: sorted(((idx[p], idx[p[:-1]], len(p)) for p in pats[1:]
                        if p[-1] == bit),key=lambda x:-x[2]) for bit in (0, 1)}
    objective = tuple(0 if c=='X' else 1 for c in SELECTED_PROBE)
    deck = [0]*len(pats)
    deck[0] = 1
    extra = [0]*(len(objective)+1)
    deck_classes = set()
    lifted = set()
    count = 0
    first_counterexample = None
    started = perf_counter()

    def rec(depth, history):
        nonlocal count, first_counterexample
        if depth == n:
            counts = array('H', deck[1:]).tobytes()
            augmented = counts + array('H', [extra[-1]]).tobytes()
            deck_classes.add(counts)
            if augmented in lifted and first_counterexample is None:
                first_counterexample = history
            lifted.add(augmented)
            count += 1
            return
        for bit in (0,1):
            for dest, src, _ in ops[bit]:
                deck[dest] += deck[src]
            for length in range(len(objective),0,-1):
                if objective[length-1] == bit:
                    extra[length] += 1 if length==1 else extra[length-1]
            rec(depth+1, (history<<1)|bit)
            for length in range(1,len(objective)+1):
                if objective[length-1] == bit:
                    extra[length] -= 1 if length==1 else extra[length-1]
            for dest,src,_ in reversed(ops[bit]):
                deck[dest] -= deck[src]

    rec(0,0)
    assert count == 1 << n
    return {
        'n':n,'histories':count,
        'O5_classes':len(deck_classes),
        'O5_plus_single_sixth_order_count_classes':len(lifted),
        'O5_missing_classes':count-len(deck_classes),
        'augmented_missing_classes':count-len(lifted),
        'first_duplicate_augmented_history_binary_code':first_counterexample,
        'elapsed_seconds_diagnostic_only':round(perf_counter()-started,3),
    }


def commutator_tower(levels=5):
    assert FIRST != SECOND
    base, other = FIRST, SECOND
    results=[]
    for stage in range(levels):
        k = 5+stage
        deck_k = signatures((base,other),k)
        deck_next = signatures((base,other),k+1)
        assert deck_k[0] == deck_k[1]
        assert deck_next[0] != deck_next[1]
        results.append({
            'stage':stage,
            'length_each':len(base),
            'indistinguishable_through_order':k,
            'distinguished_at_order':k+1,
            'distinct_histories':base != other,
        })
        base, other = base+other, other+base
    return results


def sixth_order_certificate():
    a, b = signatures((FIRST,SECOND),6)
    patterns = [''.join(p) for p in product(ALPHABET,repeat=6)]
    differences = [(w,x,y) for w,x,y in zip(patterns,a[62:],b[62:]) if x!=y]
    assert len(differences)==52
    assert ('XXXXXY',270,252) in differences
    # The independent second exceptional pair has a different but nonzero difference.
    pair2=('XYYYYXXXYYYYYXXY','YXXYYYYYXXXYYYYX')
    c,d=signatures(pair2,6)
    diff2=[(w,x,y) for w,x,y in zip(patterns,c[62:],d[62:]) if x!=y]
    assert len(diff2)==52
    assert ('XXXXXY',6,4) in diff2
    assert {x[0] for x in differences}=={x[0] for x in diff2}
    return {'sixth_order_patterns_total':64,
            'patterns_that_split_both_initial_ambiguous_pairs':52,
            'selected_pattern':SELECTED_PROBE,
            'first_pair_count':[270,252],
            'second_pair_count':[6,4]}


def run():
    scans=[]
    expected={16:65534,17:131064,18:262120,19:524212,20:1048360}
    for n in range(16,21):
        row=scan_lift(n)
        assert row['O5_classes']==expected[n]
        assert row['augmented_missing_classes']==0
        scans.append(row)
    tower=commutator_tower()
    assert tower[0]['length_each']==16
    assert tower[1]['length_each']==32
    return {
        'protocol':'Two irreducible full source packets; histories are EXTERNAL interactions',
        'sixth_order_probe_certificate':sixth_order_certificate(),
        'exhaustive_scans':scans,
        'commutator_tower':tower,
        'proof_scope':'Universal commutator/order-lifting theorem plus exhaustive length<=20; no physical ascensional transition',
    }


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--check',action='store_true')
    parser.add_argument('--output',default='')
    args=parser.parse_args()
    report=run()
    out=json.dumps(report,indent=2,ensure_ascii=False)+'\n'
    if args.output:
        with open(args.output,'w',encoding='utf-8') as f:
            f.write(out)
    if args.check:
        print('PASS: n=16..20 exhaustive lifted observers; tower 16,32,64,128,256')
    else:
        print(out,end='')
