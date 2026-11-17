# Exact state and base constraints for the exceptional ordered rows

The archived universal CRT theorem (research monorepo, Round 019-B)
checks the exact labelled dynamics once the primitive state tuple is
fixed. This note applies it in the original orientation of each row.

## 606897, strict T, factor three

Use numerators (A,C,E,C,A) and denominators (Q,D,Q,3Q,D).
Write B=3b. Exact defects and reducedness imply that 3 divides none
of A,C,D,Q,E. The T cycle through E/Q gives B E congruent to A
modulo Q. The strict T edge gives b C congruent to A modulo Q.
Subtracting yields C congruent to 3E modulo Q. The strict high chamber
gives E<Q, 3Q/2<C and C<D<2A<2Q. Hence

    C = 3E - Q,     5Q/6 < E < Q.

The necessary and sufficient state-plus-base conditions are:

1. The five prescribed fractions are distinct, reduced and lie in
   the open interval (1/2,1), and 3 is prime to A C D Q E.
2. A divides Q²−D², C divides 9Q²−D², D divides C²−A² and
   Q divides E²−A².
3. The six congruences below admit a common integer B.

| Modulus | Residue |
| --- | --- |
| Q | E/A |
| D | A/C |
| A | D/Q |
| C | 3Q/D |
| E | 1 |
| 3 | 0 |

Fractions in this table mean modular inverses. The four divisibilities
ensure the reverse edges of the defect-one two-cycles. The fixed
S edge at E has residue 1 because Q−E is a unit modulo E. The forward
strict T congruence follows from C=3E−Q and B=3b together with
BE≡A modulo Q. Because all nonstrict moduli are units relative to
the corresponding residues, the exact defect is three only at the
declared strict edge. Conversely the edge congruences and defects
force all these conditions. For every compatible tuple the base
fibre has period lcm(A,C,D,Q,E,3).

In a bounded check, for every Q and E in the interval above, A/E
must be a square root of 1 modulo Q. Enumerating those roots yields
all possible A<Q. The square divisibility on D then makes D a
positive divisor of C²−A² in (C,2A). Every survivor is checked
against both the six-modulus criterion and all ten original edges.

## 119772, strict S, factor two

In checker order the states are A/Q, C/D, C/Q, A/E, 2A/D.
For the strict source, reduce the complementary-coordinate S
congruence modulo A and use the reverse edge between A/Q and A/E.
It follows that D≡2E modulo A. All coordinates are odd: the strict
defect forces B even and the unit edges force their moduli odd.
By highness, 2A<D<2C<4A and A<E<2A. Thus (D−2E)/A lies
strictly between −2 and 2 and is odd, giving D=2E±A.

The other T fibre gives Q dividing C²−A², with C<Q<2A.
The two-cycle modulo D gives C²≡4A², so C/(2A) must be a
square root of 1 modulo D. The local checker enumerates A, E,
both linear shifts, these exact roots and all possible positive
divisors Q. It then checks all ten original congruences and
exact defects, followed by direct execution of both maps for the
least positive base in each returned progression.

## Reproduction and boundary

The checker reproduces the archived positive control for factor
three of 119772, including its base residue and period.

    PYTHONPATH=src python research/five-state/continuation/verify_exceptional_crt.py --max-coordinate 2500

The finite bounds are on A for 119772 and Q for 606897. They cover
the entire corresponding bounded chamber given the linear shifts,
but there is no global bound on those coordinates.

## Pairwise overlaps and faster bounded replay

For 606897, under the primitive, distinct and high assumptions plus the
four cycle conditions and \(C=3E-Q\), CRT compatibility is exactly
\[
 \gcd(A,C),\gcd(Q,D)\mid2,\qquad
 \gcd(E,A)\mid D-Q,\qquad
 \gcd(E,D)\mid A-C.
\]
The four cross pairs of the core moduli are coprime by reducedness.
Also \(\gcd(E,Q)=\gcd(E,C)=1\).
On \(\gcd(A,C)\) compatibility reduces to \(D^2\equiv3Q^2\).
The cycle condition \(D^2\equiv Q^2\) and invertibility of \(Q\)
give equivalence with divisibility by two. On \(\gcd(Q,D)\)
compatibility reduces to \(EC\equiv A^2\), and
\(EC\equiv3E^2\equiv3A^2\) gives the same equivalence.
The two overlaps with \(E\) give the remaining tests.

Use roots of unity modulo \(Q,C\) for 606897, and modulo \(D,C\)
for 119772 at factor two. The latter uses \(C<Q<2A<2C\).
For 606897, \(C<D<2A<2Q<2C\), so a residue modulo \(C\)
determines \(D\) uniquely. Both loops check the full ten-edge CRT.
The 5000-bound replay agrees with the earlier test on each 2500-bound
overlap and reproduces the known factor-three positive control.
