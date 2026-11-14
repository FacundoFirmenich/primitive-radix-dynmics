# Resultant obstruction for regular polynomial families

Suppose the coordinates \(A,C,D,Q\) in one of the remaining
square-cycle systems are integer polynomials in \(t\), all of degree
\(m>0\). Assume that their four adjacent pairs
\((A,Q),(Q,C),(C,D),(D,A)\) are coprime over \(\mathbb Q[t]\).
This coprimality follows if the four corresponding integer pairs
are reduced for infinitely many positive integer values of \(t\)
tending to infinity. If two coordinates shared a nonconstant
primitive integer polynomial factor, that factor would divide
both integer evaluations and grow in absolute value.

Under these hypotheses the four square-cycle divisibilities
cannot hold on such an unbounded set of integers \(t\).
In fact, an integer-polynomial divisibility on that set implies
divisibility in \(\mathbb Q[t]\). To see this, divide \(F\) by the
modulus polynomial \(G\) and multiply by a fixed integer clearing
the coefficients of the quotient and remainder. Then \(G(t)\)
divides the integer remainder for infinitely many \(t\), while
the remainder has lower degree. It is identically zero.

Write \(R(U,V)\) for the resultant of two degree-\(m\) coordinate
polynomials. For a cycle condition
\(U\mid V^2-\lambda^2W^2\), evaluate \(V^2=\lambda^2W^2\) at the
roots of \(U\) with multiplicities. The equal degrees make the
powers of the leading coefficient of \(U\) cancel, giving
\[
  R(U,V)^2=\lambda^{2m} R(U,W)^2 .
\]
In the 119772 shape at factor \(r=2\) or \(3\), the core congruences
are
\[
 A\mid r^2Q^2-D^2,\quad
 D\mid C^2-r^2 A^2,\quad
 C\mid D^2-Q^2,\quad
 Q\mid C^2-A^2 .
\]
The first two scale the squared resultants by \(r^{2m}\) each.
The other two preserve the squared resultants. Because the
squared resultant is symmetric, circulating around the four
adjacent pairs forces a nonzero squared resultant to equal
\(r^{4m}\) times itself, a contradiction. For 606897 the
congruences are
\[
 A\mid Q^2-D^2,\quad
 D\mid C^2-A^2,\quad
 C\mid D^2-9Q^2,\quad
 Q\mid C^2-9A^2 .
\]
Here the last two scale the resultants by \(3^{2m}\) each,
again giving a contradiction around the cycle.
Every coordinate has comparable height in the stated chambers.
Thus any polynomial parametrization along unbounded integers
in a chamber must have common degree. Constant coordinates
give a single core.

The resultant argument has a rational-function formulation.
Represent the four core coordinates by a coprime tuple of
homogeneous binary forms of the same degree \(m>0\) with rational
coefficients, and clear the coefficient denominators once.
At a reduced parameter \((u:v)\), the common gcd of the four
evaluated forms divides a fixed nonzero integer. Indeed their
homogeneous ideal contains powers of both parameter variables
over \(\mathbb Q\), since the forms have no common projective
zero. Clearing the two identities gives the gcd bound because
\(\gcd(u,v)=1\). The gcd here is taken over the core coordinates.
In each system \(rE\) is an integer-linear combination of core
coordinates, so passing from the primitive five-coordinate
representative to this evaluated core costs only a bounded factor.

If the four adjacent pairs of forms are coprime pairwise over
\(\mathbb Q\), then a varying rational parametrization is also
impossible for an entire rational parameter interval. An interval
contains a rational endpoint \(\alpha\) and infinitely many
distinct parameters \(\alpha+1/n\) in its interior. Substituting
this projective linear transformation into the binary forms
gives integer polynomials in \(n\) after a fixed clearing of
denominators. Choose \(\alpha\) away from roots so that all four
degrees are the same. Their bounded common normalization factor
does not obstruct the polynomial divisibility implication:
the evaluated modulus divides the quadratic numerator even
before removal of any common factor. The resultant argument then
applies. The claim does not cover sparse sets of rational
parameters near a common root of an adjacent pair of forms.

The argument excludes ordinary one-parameter polynomial
families of varying primitive states. It leaves open an
infinite discrete set and general rational parametrizations
with unbounded normalization factors. It places no height
bound on isolated solutions.
