# Exact exclusion of eight oriented five-state rows

The shared strict-S systems I and II have no realizations for either factor
2 or factor 3. This covers the four ordered graphs 575722, 575898, 575738
and 576298 at both factors.

## Proof and finite coverage

Combine the three necessary cycle divisibilities as in BOUNDED_QUOTIENTS.md.
Two bounded integral quotients force equations F=0 and G=0 in the normalized
variables a=A/D and c=C/D. The chamber lies in
1/2 < c < r/(2r-1) and (r-(r-1)c)/2 < a < 1.
Rational interval evaluation covers the closed enclosing box, including
its boundary. With 64 subdivisions per coordinate, the integer boxes are:

| System | Factor | X | Y | Pairs | Chamber points | Primitive candidates |
| --- | --- | --- | --- | ---: | ---: | ---: |
| I | 2 | 41–47 | 39–72 | 238 | 1 | 1 |
| I | 3 | 1272–1354 | 1819–2210 | 32536 | 22 | 1 |
| II | 2 | 40–69 | 11–18 | 240 | 0 | 0 |
| II | 3 | 1989–2772 | 103–124 | 17248 | 2 | 0 |

For each of the 50,262 pairs, take the resultant in a. Its fixed factors
have zeros 1, 2, 3 for factor two, or 1, 3/2, 2 for factor three. All are
outside the chamber. The remaining factor specializes to a polynomial of
degree at most two in c. The verifier rejects an identically zero
specialization as unresolved, solves all rational roots of the linear or
quadratic equation, and recovers a from the exact polynomial gcd of F and
G. A second run with 80 subdivisions gives the same chamber counts and
primitive candidates.

The surviving primitive candidates of system I are as follows. Each fails
the necessary divisibility A | Q²−D².

| Factor | A | C | D | Q | Nonzero residue modulo A |
| --- | ---: | ---: | ---: | ---: | ---: |
| 2 | 1536 | 879 | 1679 | 2479 | 960 |
| 3 | 7805403 | 4587023 | 8104466 | 15139352 | 5653296 |

For system II at factor three, the projective chamber points have integral
coordinates (A,C,D,Q) equal to (32589,16517,32718,65120) and
(153,87,154,288). The first has gcd(A,D)=3. The second has gcd(A,Q)=9.
Both violate primitive-state requirements.

Run the two proof checkers locally:

    python research/five-state/continuation/verify_shared_quotients.py
    python research/five-state/continuation/verify_shared_chambers.py
    python research/five-state/continuation/verify_shared_chambers.py --subdivisions 80

## Scope

The result includes the strict-S direction over DF015-0015. The previous
DF015-0015-B1 certificate applies to its strict-T direction. In the 11-row
oriented continuation, the known realization is 119772 at factor three.
The unresolved rows are 119772 at factor two and 606897 at factor three.
The Round 015 archive contains further orientations and forms outside
this 11-row catalogue. The complete five-state classification remains open.
