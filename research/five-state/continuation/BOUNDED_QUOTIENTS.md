# Bounded integral quotients for the shared S-strict systems

Write (Q=rD-(r-1)C), with (r=2,3), and let (P) and (m) be the
cubic and scale returned by the corresponding row of
`verify_shared_quotients.py`. The certificate checks identities over the
integer polynomial ring of the form (mP=M F+N L), where (L) is each
of (A,D,Q) and (F) is its established cycle numerator:

| System | Modulo A | Modulo D | Modulo Q | m |
| --- | --- | --- | --- | --- |
| I, factor 2 | Q² − D² | A² − C² | A³ − (2C)³ | 1 |
| I, factor 3 | Q² − D² | A² − C² | A³ − (3C)³ | 2 |
| II, factor 2 | Q² − D² | C³ − A³ | A² − (2C)² | 2 |
| II, factor 3 | Q² − D² | C³ − A³ | A² − (3C)² | 6 |

Reducedness gives (gcd(A,D)=gcd(A,Q)=gcd(C,D)=1).
Consequently (gcd(D,Q)) divides (r-1). The certificate therefore
gives the integer

    X = (r - 1) m P(A,C,D) / (A D Q).

Here (A/D) and (C/D) lie strictly between (1/2) and (1),
and (Q/D>1). Divide numerator and denominator by (D^3).
The triangle inequality gives the following strict bounds by summing
absolute coefficients of the dehomogenized cubic.

| System | Factor | Strict upper bound on abs(X) |
| --- | --- | ---: |
| I | 2 | 712 |
| I | 3 | 33104 |
| II | 2 | 548 |
| II | 3 | 26592 |

For system I, the checker also supplies a second cubic V divisible by A, D
and Q. Use Y = (r - 1) V / (A D Q). For system II it supplies a quadratic
V divisible by A and Q. Use Y = V / (A Q). The same chamber bounds apply.
Both second numerators are in the function second_numerator. These
independent quotients cut the admissible locus down to the finite exact
intersections documented in [SHARED_SYSTEMS_EXCLUSION.md](SHARED_SYSTEMS_EXCLUSION.md).

Execute the symbolic check locally after installing the development extras:

    python research/five-state/continuation/verify_shared_quotients.py
