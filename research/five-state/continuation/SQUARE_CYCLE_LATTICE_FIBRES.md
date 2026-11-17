# Reconstructing primitive numerator slopes from a fixed denominator pair

In each residual system fix \(D,Q\). Put \(L=\operatorname{lcm}(D,Q)\).
For any primitive high core, \(A\) is a unit modulo \(L\), and
\[
 z=CA^{-1}\pmod L,\qquad
 z^2\equiv\gamma^2\pmod D,\qquad z^2\equiv\delta^2\pmod Q.
\]
Thus the fourth- and second-position moduli are no longer part
of a divisor-product search. They define a finite list of
index-\(L\) lattices
\[
 \Lambda_z=\{(a,c)\in\mathbb Z^2:c\equiv za\bmod L\}.
\]
The ratios, rather than any choice of individual prime labels,
index the lattices, including the full possibilities at 2.

**Each lattice contains at most one primitive slope \(C/A\)
in the chamber.** For pairs \((A,C),(A',C')\) of that lattice,
\(L\mid AC'-A'C\). For 119772 use \(Q/2<A<D/r\) and
\(D/2<C<Q\), giving
\[
 |AC'-A'C|< DQ(1/r-1/4) \le DQ/4.
\]
For 606897 use \(3Q/4<A<Q\) and \(3Q/2<C<D\), giving
\[
 |AC'-A'C|< DQ-9Q^2/8 < 7DQ/16 ,
\]
where \(D<2Q\). Since \(L\ge DQ/2\), the determinant must be zero.
Primitive slopes determine the pair up to the common content
\(\gcd(A,C)\mid r-1\) for 119772 and \(\gcd(A,C)\mid2\)
for 606897. A fixed slope therefore gives at most two pairs.
If \(D,Q\) are even, adjacent reducedness forces content one.

In particular the fibre over \(D,Q\) has at most
\(g\,|\mathcal Z|\) cores, where \(\mathcal Z\) is the set of
simultaneous square roots above and \(g\) is 1 for factor two
or for even \(D,Q\), and 2 otherwise. This coarser bound does
not require factoring the two quadratic numerators in \(D,Q\).
The proof gives an injective label after including the content.
It does not put a bound on \(D,Q\). A descent fixing \(D,Q\)
would have to move to a different square-root class or remove
a content of two, since it cannot change a slope within the
same lattice.

## Exact witness computation

For the known 119772 factor-three denominators use
\((D,Q)=(1265,731)\). Under the reflection to 606897 the
pair is \((D',Q')=(712,406)\). The checker constructs the
simultaneous residues using the generalized CRT, enumerates
the integer points of each lattice in the exact chamber
and applies the other two square congruences. It also checks
the direct divisor-product search on these two pairs, and
on the two complementary fixed-numerator fibres. Finally it
checks the original ten edges and records the CRT progression.

    python -B research/five-state/continuation/verify_square_lattice_fibres.py

Set PYTHONPATH=src when running from the repository root.
The comparison is specific to the four witness fibres.
