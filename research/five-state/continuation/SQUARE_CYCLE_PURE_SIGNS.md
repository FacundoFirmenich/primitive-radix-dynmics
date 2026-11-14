# Pure signs and divisor allocations for the square-cycle frontier

For 606897/T all four square roots of unity in the core moduli
\(A,C,D,Q\) must differ from both uniform signs. Use
\[
 3Q/2<C<D<2A<2Q,\qquad 5Q/6<E<Q,\qquad C=3E-Q .
\]
At \(Q\), both \(A,E\) lie in \((Q/2,Q)\) and are distinct, ruling
out \(A\equiv\pm E\pmod Q\). At \(D\), both \(A,C\) lie in
\((D/2,D)\) and are distinct, giving the same argument.
At \(C\), \(0<3Q-D<C\), while \(2C<3Q+D<4C\).
Equality with \(3C\) would make \(D\) divisible by three.
Thus \(D\not\equiv\pm3Q\pmod C\).

At \(A\), \(0<D-Q<A\). If \(D\equiv-Q\pmod A\), then
\(5A/2<D+Q<10A/3\), so \(D=3A-Q\).
Under that relation the three remaining cycle conditions imply
\[
 k=\frac{9Q^2-D^2+C^2}{CQ}\in\mathbb Z,\qquad
 \ell=\frac{kQ-82C}{D}\in\mathbb Z .
\]
For the first use \(C\mid D^2-9Q^2\), \(Q\mid C^2-9A^2\),
\(D\equiv3A\pmod Q\) and \(\gcd(C,Q)=1\). For the second reduce
\(kCQ=9Q^2-D^2+C^2\) modulo \(D\), use \(Q\equiv3A\pmod D\)
and \(C^2\equiv A^2\pmod D\), and cancel the unit \(C\).
With \(c=C/Q\), \(d=D/Q\), the equations become
\[
 kc=9-d^2+c^2,\qquad \ell d=k-82c .
\]
Since \(3/2<c<d<2\), the first yields \(k>29/8>3\)
and \(k<6\). The replay includes \(k=3,6\) as well. For the second,
\(-110<\ell<0\). The replay uses the inclusive range from
\(-110\) to 0. On substitution of \(c=(k-\ell d)/82\)
the quadratic in \(d\) has coefficients
\[
 82^2-\ell^2,\qquad -80k\ell,\qquad 81k^2-9\cdot82^2 .
\]
The exact replay of 444 integer pairs finds only the chamber
point \((A/Q,C/Q,D/Q)=(148/153,80/51,97/51)\).
Its primitive common representative is \((148,240,291,153)\).
The gcd of \(C,D\) is three, so the state \(C/D\) is not reduced
in the prescribed coordinates. This rules out the uniform negative
sign on \(A\) and completes the four-modulus obstruction.

For 119772 at factor two, the roots in \(Q,D\) must also differ
from both uniform signs. For \(Q\) the two numerators \(A,C\)
are distinct and high over \(Q\); for \(D\) the two numerators
\(2A,C\) are distinct and high over \(D\).
A root different from both signs implies that the modulus cannot
be an odd prime power or a power of two at most four. For odd
moduli, it requires at least two distinct prime factors assigned
to opposite signs. For even moduli the elementary \(2\)-adic
options must also be retained. These restrictions leave the mixed
sign configurations open.
