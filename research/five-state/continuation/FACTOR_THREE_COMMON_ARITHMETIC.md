# A shared arithmetic problem for the two factor-three orientations

Use the labels of 119772 and set
\[
 (A',Q',C',D')=(Q,A,D,C).
\]
For 119772 with \(r=3\), the four square congruences in the
order \(A,Q,C,D\) are
\[
 A\mid D^2-9Q^2,\quad Q\mid C^2-A^2,\quad
 C\mid D^2-Q^2,\quad D\mid C^2-9A^2 .
\]
They become exactly those of 606897 in primed coordinates,
in the order \(Q',A',D',C'\). The four adjacent gcd conditions
and the two opposite overlaps are preserved by the reflection.

There is a stronger identity on the branch \(D=3E-A\).
For 606897 the fifth coordinate satisfies \(3E'=C'+Q'\).
Under the reflection this gives \(E'=E=(D+A)/3\).
The six base congruences of 606897 then read

| Modulus in 119772 labels | Required residue |
| --- | --- |
| \(A\) | \(E/Q\) |
| \(Q\) | \(C/A\) |
| \(C\) | \(Q/D\) |
| \(D\) | \(3A/C\) |
| \(E\) | \(1\) |
| \(3\) | \(0\) |

This is the base system of 119772 at \(r=3,j=1\).
For the congruence at \(A\), use \(B(Q-A)\equiv E-A\bmod A\)
from the ordinary \(S\) edge. At \(Q,D\), the forward \(T\)
edges give the displayed residues. At \(C\), the ordinary
\(S\) edge gives \(Q/D\), which equals the reverse residue
by the square congruence. The fixed \(T\) edge gives the
residue \(1\) at \(E\). The strict \(S\) edge at numerator
\(3A\) asks for
\(B(D-3A)\equiv3(Q-A)\bmod3A\). Given \(3\mid B\), this is
equivalent to \(B D/3\equiv Q\bmod A\), where the division
means \((B/3)D\). Substitute \(D=3E-A\) and use
\(E^2\equiv Q^2\bmod A\). The latter follows from the first
square congruence since \(3\) is a unit modulo \(A\).
This verifies the remaining strict edge. At the other
orientation the exact derivation is in
[Exceptional CRT reduction](EXCEPTIONAL_CRT_REDUCTION.md).

Primitivity of the fractions in either description, once
transferred to the shared coordinates, requires adjacent core
coprimality, \(\gcd(A,E)=1\) and the unit conditions at three.
For example 606897 has the extra pair \(E'/Q'=E/A\). Both
descriptions have the same admissible base fibre on the common
arithmetic locus, before selecting their real chambers and
checking the distinct labelled states of each chart.

The \(j=1\) chamber of 119772 has \(A<Q\) in these coordinates.
The chamber transported from 606897 has \(Q<A\), since its
condition is \(A'<Q'\). More precisely the latter is
\(3A/2<D<C<2Q<2A\), with \((D+A)/3<A\).
In the former, \(D>3A\) gives \((D+A)/3>4A/3\).
The shared arithmetic problem therefore asks whether the
same arithmetic locus can meet a second separated chamber.
The known core
\((A,C,D,Q,E)=(406,712,1265,731,557)\) reproduces the same
arithmetic CRT fibre after reflection, and the reflected tuple
lies outside the 606897 chamber. No identification of the two
dynamics follows. The \(j=2\) branch of 119772 has
\(3E=D+2A\), so it shares the square system, with a distinct
completion at the fifth state.

## Independent base-first enumeration

For either system all four core moduli divide \(B^2-1\),
and \(E\mid B-1\). The program
[verify_residual_by_base.py](verify_residual_by_base.py)
generates these possible moduli from divisors of \(B-1\) and
\(B+1\), including their shared power of two. For 119772 it
determines \(C\) from \(BA\bmod Q\), enumerates \(D\) in the
high interval and determines \(E\) from the strict shift.
For 606897 it determines \(E=BA\bmod Q\), then \(C=3E-Q\),
and enumerates \(D\) in the high interval. These residues
are necessary by the original \(T\) edges. Thus every
realization at the specified base enters the candidate list.
The final ten-edge check and membership in the retrieved CRT
progression decide the candidates.

At \(B=88011536665779\), the enumeration used all 24,576
divisors of \(B^2-1\). Factor two is excluded at this odd
base. It found the known tuple in 247 pre-CRT candidates
from 119772/3 and no realization among 943 candidates from
606897/3. The other 37 oriented rows are already excluded
globally, so the known tuple in its marked orientation is
the only five-state nonpermutation realization at this base.
This result is specific to the stated base.
