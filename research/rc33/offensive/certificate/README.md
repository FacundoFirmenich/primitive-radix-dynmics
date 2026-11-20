# Opposite-coordinate completion and half inversion

Author: Facundo Firmenich. RGΦ RC3.3, 20 November 2026.

All quantities are dimensionless integers or exact rational numbers. The common
coordinate order is `(A,C,D,Q)`; the normal factor-two and factor-three chambers
and reflected factor-three chamber are distinct declared regimes.

`paired_fibres.py` completes every divisor choice in a fixed opposite-coordinate
fibre. The two remainder labels enforce the two remaining quadratic conditions.
It retains chamber and gcd conditions, then checks the fifth coordinate, CRT,
all ten actual rational transitions and their exact defects.

`half_duality.py` implements `Psi(x)=1/(2x)` and its admissibility bit
`floor(B/x) mod 2`. The proofs explain why a normal factor-three carrier with
five odd coordinates would yield a reflected 606897 carrier. No such new carrier
is asserted here. The known factor-three carrier fails this parity gate.

Run `python3 code/check_offensive.py` from the canonical project root. It first
checks the manifest and prints equations, exact input domains and software
versions. It replays in a separate build directory:

1. 1,536 small fixed contexts against direct integer enumeration, plus both
   hidden opposite pairs of each of the two known carriers.
2. 8,400 first half-inversion identities and 4,095 high-image second identities,
   with positive and negative closed-component controls.
3. A checkpoint/resume control on static seeds. The reachable context set closes
   after 112 contexts; 160 is the requested budget, not a claim of 160 processed.
4. All 128,058 contexts in `PAIR_CONTEXTS_SNAPSHOT.jsonl`, whose explicit domain
   has no completed quadratic core. The prior generation of those contexts is
   not independently replayed and supplies no global completeness claim.

SymPy proposes factorizations; every factor is separately proved by exact trial
division or a recursive full Lucas criterion. Unresolved arithmetic is deferred,
never used as a rejection certificate. Dependencies: Python 3 and SymPy.

`opposite_worker.py` is also archived as the persistent discovery engine. Use
`--no-live` for a portable run. Its optional live feeds refer to the original
workspace; live databases and mutable logs are deliberately outside this fixed
certificate. Discovery reachability does not enumerate every possible carrier.

The finite replay, structural proofs and ongoing discovery runs have separate
contracts. Global 606897 existence, carrier uniqueness and global minimum-base
questions are not settled by this package.
