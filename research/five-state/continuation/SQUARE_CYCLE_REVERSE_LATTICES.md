# Primitive slopes in the reverse lattices

Fix \(A,C\) in a residual square cycle. Write \(L=\operatorname{lcm}(A,C)\).
Every realization has \(Q\) invertible modulo \(L\) and gives a
class \(z=D/Q\bmod L\). The two squares of \(z\) are the prescribed
ones modulo \(A\) and \(C\). For two candidates in the same class
their determinant \(\Delta=DQ'-D'Q\) is divisible by \(L\).

For 119772, the bounds \(rA<D<2C\) and \(C<Q<2A\) give
\(|\Delta|<(4-r)AC\). At factor two the coordinates are odd and
\(\gcd(A,C)=1\). Thus \(\Delta\) is even and divisible by the odd
\(L=AC\), forcing zero.

At factor three, append the class of the strict shift \(j\in\{1,2\}\),
where \(D=3E-jA\), and the nonzero class of \(Q\) modulo three.
With those fixed, \(D,D'\equiv-jA\pmod3\) and \(Q\equiv Q'\pmod3\).
Hence \(3L\mid\Delta\), since \(3\nmid AC\). The chamber bound is
smaller than \(3L\) even when \(\gcd(A,C)=2\). This leaves at most
four refined classes for each original root at factor three.

For 606897 the bounds \(C<D<2A\) and \(A<Q<2C/3\)
give \(|\Delta|<AC/3<L\), as \(\gcd(A,C)\le2\).

A zero determinant determines the primitive slope. It leaves at
most two choices for the pair \((D,Q)\) because \(\gcd(D,Q)\le2\),
and only one for 119772 at factor two. At a fixed shift the fifth
coordinate is then determined. These statements bound fibres in
the direction opposite to the
[denominator-pair theorem](SQUARE_CYCLE_LATTICE_FIBRES.md).
They do not bound the number of root classes or fixed pairs globally.
