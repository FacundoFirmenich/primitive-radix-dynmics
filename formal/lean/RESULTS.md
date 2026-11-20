# Formal verification results · RC3.3

Author: Facundo Firmenich. This is a partial formalization; it adds no new global arithmetic closure.

The reproducible evidence is `records/current/AUDIT.json`, with every theorem type in `statements.log` and every axiom dependency in `axioms.log`.

## LEAN1

Exact rational maps, primitive coordinates and local reduction factors.

All natural bases; stated positivity and primitive-coordinate hypotheses; open high interval.

Declarations: `RadixMobius.radix_fraction`, `RadixMobius.pairS_value`, `RadixMobius.canonical_step`, `RadixMobius.every_high_rational_has_primitive_coordinates`, `RadixMobius.radix_gcd`, `RadixMobius.mobius_gcd`.

## LEAN2

Integral content, chronological lifts and cycle spectrum.

Integral 2x2 matrices with the stated primitive/nonzero hypotheses; actual high closed paths of any finite length.

Declarations: `RadixMobius.content_dvd_det`, `RadixMobius.unimodular_content`, `RadixMobius.actual_branch_lift`, `RadixMobius.actual_cycle_spectrum`.

## LEAN3

Two-chart cycle balance and partial strict-cycle exclusions.

Every high rational cycle; letter-count bound; no strict cycle of length <=3 or of the displayed T^a S^b form. General four-state exclusion is not formalized.

Declarations: `RadixMobius.rational_cycle_balance`, `RadixMobius.actual_cycle_letter_budget`, `RadixMobius.rational_no_strict_short_cycle`, `RadixMobius.no_strict_one_block_cycle`.

## LEAN4

Two nonpermutation five-state families and their exact defects.

Both displayed carriers and every base B0+t*M with t a natural number; five distinct high rational states, ten edges, strong connectivity, S noninjective, single strict factor r. No minimality or complete-CRT necessity claim.

Declarations: `RadixMobius.old_infinite_family`, `RadixMobius.new_infinite_family`, `RadixMobius.old_family_defects`, `RadixMobius.new_family_defects`.

## LEAN5

Exactly36 induced actions and minimum rank2.

Arbitrary finite words on both entire realized base families. Closure plus generation, not a word-length cutoff.

Declarations: `RadixMobius.reachable_action_iff`, `RadixMobius.actionCodes_cardinality`, `RadixMobius.no_rank_one_word`, `RadixMobius.rank_two_word_exists`, `RadixMobius.old_family_action_classification`, `RadixMobius.new_family_action_classification`.

## LEAN6

Sound square and modular filters from the original two conics.

Integer coefficients, rational q,s with q !=0, any positive modulus; W=0 and U=0 branches included. No coverage proof for an external enumerator or execution.

Declarations: `RadixMobius.conic_discriminant_factorization`, `RadixMobius.conic_square_filter_sound`, `RadixMobius.two_conics_require_square`, `RadixMobius.two_conics_modular_rejection`.

## Remaining formalization

- General four-state exclusion and therefore the complete sharp-threshold theorem

- Full necessity and minimal period of the CRT base fibres

- Thirty-seven oriented exclusions and completeness of the40-row classification

- External C++/Python enumeration and the1..12 completion-index exhaustion

- The all-cardinality base2..53 census and lower bound54

- Uniform global uniqueness and either global least base

- 606897/r3 nonexistence or existence

- Period lattices, modular equidistribution, CLT and passive infinite Markov order
