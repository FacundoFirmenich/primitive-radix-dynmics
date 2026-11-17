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

## Exact chamber filtering through cofactor 14

Before enumerating divisors, bound each signed quotient by the extrema
at vertices of the projectivized closed chamber. In 119772 the slice
\(A=1\) is the simplex \(rle Dle 2Cle 2Qle 4\). In 606897
the slice \(Q=1\) is the simplex \(3/2le Cle Dle 2Ale 2\).
For a ratio of linear forms with positive denominator, its value
at an interior point is a positive weighted average of the vertex
values. The strict bounds used by the checker therefore discard
only unattainable values. All ratios used here are nonconstant.
The count below is after this exact filter and after the cofactor
coprimality tests.

| Code | Factor | Side | Quotient pairs | High candidates | Realizations |
| --- | ---: | --- | ---: | ---: | ---: |
| 119772 | 2 | AC | 22320 | 8 | 0 |
| 119772 | 2 | DQ | 2790 | 2 | 0 |
| 119772 | 3 | AC | 9880 | 1 | 1 |
| 119772 | 3 | DQ | 863 | 0 | 0 |
| 606897 | 3 | AC | 3230 | 0 | 0 |
| 606897 | 3 | DQ | 2486 | 1 | 0 |

The single realization is again \((406,712,1265,731,557)\), with the
same base residue and period. Reproduce all six searches with
`--bound 14` and no code or side filter. There is no search limit
on a state coordinate. The scan uses signed reduced denominators
from 2 through 14, leaving cofactors 1 to the pure-sign exclusions
in [the sign proof](SQUARE_CYCLE_PURE_SIGNS.md).
