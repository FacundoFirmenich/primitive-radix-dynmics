# Finiteness on every fixed algebraic curve

In each of the three residual square-cycle systems, every fixed
algebraic curve in core space contains only finitely many primitive
high cores. A fixed rational parametrization admits an explicit
parameter-height bound. The result applies to 119772 at factors two
and three and to 606897 at factor three. It uses only four core
divisibilities, adjacent coprimality and the high-chamber bounds,
so the full edge and shared-base conditions only shrink the set.

## A criterion for four-coordinate cycles

Let \(X\) be a smooth projective geometrically integral curve over
\(\mathbb Q\) with a nonconstant morphism to \(\mathbb P^3\). Denote
the pullbacks of the four coordinate sections by \(s_0,\ldots,s_3\)
and the pullback of \(\mathcal O(1)\) by \(L\), of degree \(m>0\).
For a rational point under consideration, let \(x=(x_0,\ldots,x_3)\)
be the primitive integral coordinates of its image. Suppose for
some fixed \(\kappa\) that

\[
  0<\max_i |x_i|\le\kappa\min_i |x_i|,\qquad
  \gcd(x_i,x_{i+1})=1,\qquad
  x_i\mid a_i^2 x_{i+1}^2-b_i^2 x_{i-1}^2 .
\]

Indices are read modulo four, and the \(a_i,b_i\) are fixed
nonzero integers. If \(\left|\prod_i a_i\right|\ne
\left|\prod_i b_i\right|\), only finitely many rational points
satisfy these conditions.

To pass from integer coordinates to geometry, consider a
basepoint-free list of sections of one line bundle \(M\) defining
a morphism \(\Phi\) to a projective space. For any selected sublist
that is not identically zero, let \(B\) be its common zero
divisor, with multiplicity at a point equal to the minimum
vanishing order. Divide the sublist by the canonical section of
\(B\) to define a morphism \(\Psi\) using \(M(-B)\).
At a rational point away from \(B\) with primitive integer
\(\Phi\)-coordinates \(y\), let \(g\) be the gcd of the selected
coordinates. The height formula gives

\[
 h_B(P)=h_{\mathbb P}(\Phi(P))-h_{\mathbb P}(\Psi(P))+O(1)
       =\log g+\log\frac{\max |y|}{\max_{\mathrm{sel}} |y|}+O(1).
\]

Here \(h_{\mathbb P}\) is the logarithm of the maximum absolute
primitive coordinate. The first equality is height functoriality
and additivity. A nonzero effective \(B\) on a projective curve
has positive degree and is ample, so bounded \(h_B\) gives
finiteness by Northcott over \(\mathbb Q\). See [Silverman,
*Canonical Heights on Abelian Varieties*, lecture 1, p. 2](https://swc-math.github.io/aws/2024/2024SilvermanLecture1Slides.pdf).

If infinitely many qualifying rational points existed, select
\((s_i,s_{i+1})\) in the coordinate list for \(M=L\). Here \(g=1\)
and the real ratio is at most \(\kappa\). Thus adjacent zero
divisors \(D_i=(s_i)_0\) and \(D_{i+1}=(s_{i+1})_0\) have
disjoint support, including over \(\overline{\mathbb Q}\).

Put \(N_i=a_i^2s_{i+1}^2-b_i^2s_{i-1}^2\). In degree two use
the full list of all products \(s_js_k\), augmented by \(N_i\).
Its evaluation at \(P\) is already primitive: it includes the
four squares \(x_j^2\) with common gcd one, and \(N_i(x)\) is
integral. Select \(s_i^2\), the four products \(s_is_j\), and
\(N_i\). The products alone have gcd \(|x_i|\), and this gcd
divides \(N_i(x)\). The full list has maximum at most
\(\max(1,a_i^2+b_i^2)(\max |x|)^2\), and the selected maximum
is at least \(|x_i|\max |x|\). At any geometric point some
\(s_j\) is nonzero. Consequently the selected common zero
divisor is precisely \(\min(D_i,(N_i)_0)\), with value \(D_i\)
if \(N_i\) vanishes identically. The height formula now reads

\[
  h_{\min(D_i,(N_i)_0)}(P)=h_L(P)+O(1).
\]

Indeed both sides differ from \(\log\max|x|\) by a bounded
amount. Subtracting heights bounds the height of the effective
divisor \(D_i-\min(D_i,(N_i)_0)\). Infinitude forces it to be
zero. In particular at every point of \(D_i\), the two
neighboring sections are nonzero and their values obey

\[
  (s_{i+1}/s_{i-1})^2=(b_i/a_i)^2.
\]

Take \(f=s_0/s_2\) and \(g=s_1/s_3\). Their divisors
\(D_0-D_2\) and \(D_1-D_3\) have disjoint supports by
adjacent disjointness. The squared value of \(f\) on \(D_1\)
is \((a_1/b_1)^2\) and on \(D_3\) it is \((b_3/a_3)^2\).
Similarly \(g^2\) is \((b_0/a_0)^2\) on \(D_0\) and
\((a_2/b_2)^2\) on \(D_2\). Over \(\mathbb C\), Weil
reciprocity yields \(f((g))^2=g((f))^2\), with values taken
with divisor multiplicities. Since each \(D_i\) has degree
\(m\), this reads

\[
 \left(\frac{a_1a_3}{b_1b_3}\right)^{2m}
 =
 \left(\frac{b_0b_2}{a_0a_2}\right)^{2m}.
\]

The assumed imbalance contradicts \(m>0\). This argument
allows cancellation between opposite zero divisors. See
[Horozov, *Reciprocity Laws for the Higher Tame Symbol and the
Witt Symbol on an Algebraic Surface*, Theorem 0.1](https://www.math.wustl.edu/~matkerr/Reciprocity.pdf).

## Applications to the three systems

Take \(x=(A,Q,C,D)\). The four adjacent pairs are coprime.
The integral coefficients \((a_i,b_i)\) are:

| System | \(A\) | \(Q\) | \(C\) | \(D\) |
| --- | --- | --- | --- | --- |
| 119772, factor \(r\) | \((r,1)\) | \((1,1)\) | \((1,1)\) | \((r,1)\) |
| 606897, factor 3 | \((1,1)\) | \((1,3)\) | \((1,3)\) | \((1,1)\) |

Thus the ratios \(\prod a_i/\prod b_i\) are \(r^2\) and
\(1/9\). For 119772 the bounds \(A<C<Q<2A\),
\(rA<D<2C\) imply \(\max x_i<4\min x_i\).
For 606897 use \(3Q/2<C<D<2A<2Q\), which gives
\(3Q/4<A<Q\) and \(\max x_i< (8/3)\min x_i\).
The fifth coordinate \(E\) has at most one value per fixed
shift and core.

Normalize each curve and remove its finitely many singular
image points before applying the criterion. For a curve
over \(\mathbb Q\) that is irreducible over \(\mathbb Q\) but
not geometrically irreducible, its rational points belong
to intersections of distinct conjugate geometric components,
which are finite. The Zariski closure of a set of rational
points is defined over \(\mathbb Q\): in each degree the
equations of vanishing at those points form a linear system
over \(\mathbb Q\). Thus working over a larger field gives
the same dimension conclusion. An infinite set of cores
in any of the three systems would have Zariski closure of
dimension at least two in \(\mathbb P^3\).

## Computing a bound for a given rational parametrization

Write the morphism from \(\mathbb P^1\) as binary forms
\(F_i\in\mathbb Z[U,V]\) of one degree \(m>0\) with no common
projective zero. At primitive integral \((u,v)\) the common
gcd of their evaluations divides a fixed positive \(K\).
To compute \(K\), express powers of \(U\) and \(V\) in the
ideal generated by the forms over \(\mathbb Q\) and clear
the two denominators. One can compute both identities by
dehomogenizing in the two standard charts, running the
polynomial Euclidean algorithm, and homogenizing again.
This computation also gives an explicit rational \(c>0\)
such that

\[
 \max_i |F_i(u,v)|\ \ge\ c H^m,\qquad H=\max(|u|,|v|).
\]

For instance, normalize the two homogeneous identities to
have left sides \(U^{k}\) and \(V^{\ell}\) and take \(c\)
to be the reciprocal of the larger sum of the coefficient
norms of the multiplier polynomials, with each norm the
sum of absolute coefficients. Use the identity for the
coordinate of absolute value \(H\).

For an adjacent nonconstant common factor, choose a
primitive integer form \(J\) dividing both adjacent forms.
Its value divides their gcd, which equals the common
normalization gcd and is at most \(K\). Otherwise write
\(G_i=a_i^2F_{i+1}^2-b_i^2F_{i-1}^2\). Some \(F_i\) does
not divide \(G_i\) over \(\mathbb Q\): the opposite
assumption, with adjacent disjointness, would give the
same reciprocity contradiction. Take a primitive gcd
\(J'=\gcd(F_i,G_i)\) in \(\mathbb Z[U,V]\) up to content
and put \(J=F_i/J'\), of positive degree. At qualifying
parameters \(F_i(u,v)\) divides \(G_i(u,v)\), since the
normalized core obeys the divisibility and the square
difference scales quadratically. Cancel \(J'(u,v)\),
which is nonzero. The coprime binary forms \(J\) and
\(G_i/J'\) bound \(|J(u,v)|\) by a computed positive
constant \(K'\) using the two ideal identities again.
In either case let \(B\) be the resulting bound on
\(|J(u,v)|\).

As \(J\) divides some \(F_i\), writing \(d=\deg J\) gives
the explicit bound

\[
 H^d\ \le\ \frac{\kappa B\,\|F_i/J\|_1}{c}.
\]

This follows by comparing \(|F_i(u,v)|\ge cH^m/\kappa\)
with the product bound \(B\|F_i/J\|_1H^{m-d}\). Thus a
particular rational curve can be exhausted by a finite
parameter search followed by the exact state and CRT tests.
Finiteness on each fixed curve supplies no bound on the
total number or heights of cores in the full chamber.
