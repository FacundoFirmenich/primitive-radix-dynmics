# Bounded cofactor-pair replay

The complementary constants in SQUARE_CYCLE_COFACTOR_BOUND.md
give an exact search by divisors with the height cutoff removed.
The cutoff is on the two specified reduced ratio denominators.
Both possible signs in each modulus are tried. The other two
coordinates divide the corresponding constants. If one
constant vanishes, the other bounds the missing coordinate by
the ratio inequality. Exact fibre and shared-base CRT checks
adjudicate every resulting primitive tuple.

The replay for 119772 exhausted both pairs with each cofactor
at most eight. For factor two neither pair contains a
realization. For factor three the AC pair recovers
((406,712,1265,731,557)) and exactly its CRT class. The DQ pair
has no realization within this cofactor bound.

For 606897 both pairs with each cofactor at most eight have no
realization. A replay at bound five checked 46,400 pairs of
linear quotients per side, and the replay at bound eight
checked 321,600 per side. The bound-eight run for 119772
checked 140,800 per side at factor two and 321,600 per side
at factor three. These are pre-chamber counts.

Reproduce from PowerShell with PYTHONPATH=src:

    python research/five-state/continuation/search_square_cofactor_pairs.py --bound 8 --code 119772
    python research/five-state/continuation/search_square_cofactor_pairs.py --bound 8 --code 606897

A realization outside those cofactor ranges remains possible.
