# Predecessor congruences and sparse oriented exclusions

## Predecessor lemma

Suppose a generator has exactly one strict source, of factor \(r\). The
other sources inject into the complement of that source. Indeed, an
ordinary edge preserves its modulus and cannot reach the strict source,
whose modulus has nontrivial gcd with the base. Finiteness gives a
bijection on the complement and a unique ordinary predecessor of the
strict target. Work in the radix chart for \(T\) and in the inverse Möbius
chart for \(S\). Write the strict source as \(u_s/(rq)\) and the ordinary
predecessor as \(u_o/q\) in that chart. Write \(B=rb\). The two congruences
for their common image give \(b u_s\equiv rb u_o\pmod q\).
The ordinary predecessor makes \(B\) a unit modulo \(q\). Hence
\(u_s=r u_o+jq\), with \(j\ne0\) since \(u_s/(rq)\) is reduced.

For \(T\), both chart fractions lie in \((1/2,1)\), so \(|j|<r/2\).
In particular factor two is impossible, and factor three permits only
\(j=\pm1\). The two signs cannot both fit for a fixed ordinary
predecessor. For \(S\), the inverse chart fractions lie in \((0,1)\),
so \(|j|<r\). If expressed in terms of the original denominators,
the sign is the same when the common target numerator is \(q\).

The full oriented replay uses the Round 015 graph keys, two generator
orders and integer positive linear elimination of the high constraints.
It finds eight forced collisions (four classes in both orders) and
eight further exclusions of strict \(T\) with factor two.
The 24 surviving linear systems are necessary chambers only.
The historical Round 016 ledger already excludes some of these
orientations, so these counts are not added to the archived total.

## Sparse strict-S factor two or three

For DF015-0004/0012 at factor two and DF015-0008/0018 at factor three,
use the ordered states
\[
 (A/Q,\ rA/D,\ C/Q,\ C/D,\ C/E).
\]
Here \(S=(0,0,3,4,2)\) or \(S=(0,0,4,2,3)\), strict at source 1, while
\(T=(2,3,0,1,4)\) in this state order for both forms. The two
orientations of the \(S\) three-cycle distinguish the graphs.

The predecessor is the \(S\)-fixed state at \(A/Q\). Highness gives
\(D<2C<2Q\), \(rA<D\), and \(Q<2A\).
Therefore \(D=rQ+jA\) with \(j>-r\). For \(r=2\), \(D<2Q\)
gives \(j<0\). For \(r=3\), \(D<2Q\) gives
\((D-3Q)/A<-Q/A<-1\). Thus \(j=-(r-1)\) in both cases.

The two \(T\) cycles give \(Q\mid C^2-A^2\) and
\(D\mid C^2-r^2A^2\). Reducedness gives \(\gcd(C,QD)=1\), so
\(D=rQ-(r-1)A\) and \(\gcd(A,Q)=\gcd(r,Q)=1\) give
\(\gcd(D,Q)\mid r-1\). Put
\[
 k=\frac{(r-1)(C^2-A^2-r(r+1)AQ)}{QD}.
\]
The numerator before multiplication by \(r-1\) is zero modulo
\(Q\). Modulo \(D\), use \(rQ\equiv(r-1)A\) to obtain
\(C^2-r^2A^2\). Hence \(k\) is an integer.

Let \(x=A/Q\), \(y=C/Q\) and \(d=D/Q=r-(r-1)x\).
The high chamber imposes \(1/2<x<r/(2r-1)\) and \(d/2<y<1\).
The quotient is \((r-1)(y^2-x^2-r(r+1)x)/d\).
Both endpoint functions in \(y\), at \(y=d/2\) and \(y=1\),
are decreasing in \(x\). The resulting strict bounds are
\(-3<k<-3/2\) for \(r=2\) and \(-15/2<k<-21/4\) for \(r=3\).
The only possibilities are respectively \(-2\) and \(-7,-6\).

The ordinary \(S\) three-cycle on numerator \(C\) gives \(B^3=1\bmod C\)
and \(D\equiv BQ\) or \(D\equiv B^2Q\pmod C\). Thus
\(d^3-1\equiv0\pmod C\), using the modular unit \(Q\).
The equation for \(k\) also gives
\((r-1)(x^2+r(r+1)x)+kd=0\bmod C\).
The resultant of these two polynomials in \(x\) must be divisible by
\(C\), by the integral Sylvester determinant identity. The three
resultants are respectively \(2945,3655600,3740480\).
For each divisor \(C\) of the corresponding constant, the checker
finds every simultaneous root modulo \(C\) by prime power lifting
and CRT. The interval \(C<Q<2C\) is exhaustive once \(C\) is fixed.
For every \(Q\) in that interval, \(A<C\) follows from \(rA<D<2C\).
Thus the residue \(xQ\bmod C\) is the only possible \(A\).
Exact highness, reducedness and cycle divisibilities leave no core tuple
\((A,C,D,Q)\). The fifth coordinate need not be searched.

Run `python research/five-state/continuation/verify_sparse_s_strict.py`
with `PYTHONPATH=src` and the development dependencies installed.
The replay counts 3,832, 10,632 and 911,800 residue-compatible
pairs before the primitive and cycle filters.
