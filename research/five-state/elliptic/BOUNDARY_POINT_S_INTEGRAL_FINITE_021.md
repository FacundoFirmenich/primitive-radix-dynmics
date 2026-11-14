# RGΦ Round 021-B — common boundary point and relative-integral finiteness

Let
\[
C=2A-z,
\qquad
D=2A-w,
\]
and let \([A:z:w]\) be a primitive integral projective point on one of the smooth cubics \(F_n=0\).

## Universal boundary point

The projective point
\[
\boxed{R=[1:2:2]}
\]
lies on every curve \(F_n=0\), because every term cancels after substituting \((A,z,w)=(1,2,2)\).

## Theorem 021-B — coprimality as avoidance of \(R\)

For every prime \(p\),
\[
\boxed{p\mid\gcd(C,D)
\iff
[A:z:w]\bmod p=R.}
\]

### Proof

If \(p\mid C,D\), then
\[
z\equiv2A,\qquad w\equiv2A\pmod p.
\]
Primitivity excludes \(A\equiv0\pmod p\), so the reduction is exactly \([1:2:2]\).

Conversely, reduction to \([1:2:2]\) immediately gives \(C\equiv D\equiv0\pmod p\).

Thus
\[
\boxed{\gcd(C,D)=1}
\]
is precisely the condition that the rational point avoid \(R\) in every finite reduction.

## Corollary 021-B1 — finiteness

For each fixed \(n\), the primitive rational points on \(F_n=0\) satisfying
\[
\gcd(2A-z,2A-w)=1
\]
form a finite set.

Indeed, after adjoining the finitely many bad primes to a set \(S_n\), these points are \(S_n\)-integral relative to the nonempty divisor \([R]\) on the elliptic curve \(F_n\).  Siegel's theorem gives finiteness of such relative-integral points.

## Scientific meaning

Round 020 showed that \(F_{17}\) has positive rank and infinitely many rational chamber points.  Round 021 shows that only finitely many of those rational points can satisfy the coprimality required by RGΦ.

The remaining problem is therefore not geometric density but an **effective relative-integral-point computation**.

## Boundary

Siegel's theorem supplies finiteness but not, by itself, the explicit list.  No effective enumeration is claimed in this round.