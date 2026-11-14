# RGΦ Round 020-A — coprime-completion theorem on the elliptic cubics

For `DF015-0015`, put

\[
C=2A-z,
\qquad
D=2A-w,
\]

\[
f=(2z-3w)(2z-w),
\qquad
g=(7z+2w)(11z-2w).
\]

Round 019 introduced, for \(n=1,\ldots,19\), the plane cubic

\[
\begin{aligned}
F_n(A,z,w)={}&4nA^3-2nA^2(w+z)+nAwz\\
&-20A^2w-340A^2z+24Aw^2+148Awz+24Az^2\\
&-4(z^3+w^3).
\end{aligned}
\]

## Exact identity

Direct expansion gives

\[
\boxed{
 gD-fC+(5w+85z-nA)CD=-F_n(A,z,w).
}
\]

Hence, on \(F_n=0\),

\[
 gD-fC+(5w+85z-nA)CD=0.
\]

## Theorem 020-A

Assume

\[
F_n(A,z,w)=0
\]

and

\[
\gcd(C,D)=1.
\]

Then

\[
\boxed{C\mid g}
\qquad\text{and}\qquad
\boxed{D\mid f}.
\]

### Proof

Modulo \(C\), the identity reduces to

\[
gD\equiv0\pmod C.
\]

Since \(\gcd(C,D)=1\), \(D\) is invertible modulo \(C\), so \(C\mid g\).

Modulo \(D\), the identity reduces to

\[
-fC\equiv0\pmod D.
\]

Again \(C\) is invertible modulo \(D\), hence \(D\mid f\). ∎

## Consequence

Inside the chamber

\[
A>5z>w>0,
\]

a primitive integral point on one of the nineteen cubics satisfies the first two cycle divisibilities automatically once the single coprimality condition

\[
\gcd(2A-z,2A-w)=1
\]

is imposed.

The global `DF015-0015` problem therefore reduces further to rational/integral points satisfying:

1. \(F_n(A,z,w)=0\) for some \(1\le n\le19\);
2. \(A\mid z^3+w^3\);
3. \(\gcd(2A-z,2A-w)=1\);
4. the remaining primitive-state conditions.

This is a symbolic theorem. It does not establish existence or impossibility.