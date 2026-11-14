# DF015-0015-B1 and the oriented frontier

[Exact exclusion certificate](../df015-0015/CERTIFICATE.md).
It resolves the admissible locus in the chamber. Full relative-integral
enumeration outside the chamber is separate.

Round 017 uses T=[1,0,3,3,4] and S=[3,2,1,4,0], with cycle lengths
(1,1,2) and (2,3). The 606897 local-moduli checker uses
T=[2,4,0,0,1] and S=[4,3,2,1,0], with cycle lengths (2,2) and (1,2,2).
No relabeling or generator swap matches the published representatives.
Keep 606897 and aggregate counts unchanged pending a catalogue crosswalk.

The Farkas JSON in 35035e58e6dc3cb99933b637740320519d90ff0b contains 14545 bytes and is a literal prefix
of the recovered 200558-byte Round 018 object.
[Exact source](https://github.com/FacundoFirmenich/rgphi-radix-mobius-dynamics/blob/c25857e53eea8585a4f10e0a5a42295a315151ec/paper-iii/round-018/03_MULTI_STRICT/HIGH_INFEASIBILITY_FARKAS_728.json).
SHA-256: ea43ded3bda4fcc7ef74b9a01e988ffbb69f6535a52d0850d5a30b5af880d96b.

    python src/rmr/verify_rgphi_farkas_728.py research/five-state/certificates/HIGH_INFEASIBILITY_FARKAS_728.json

All 728 identities verify. The 728 Farkas, 56 collision, 50 injectivity
and 6 terminal IDs disjointly partition 840 profiles.
The three CSV ledgers have valid record separators.
