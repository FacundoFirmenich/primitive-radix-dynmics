# RGΦ Round 019-C — elliptic reduction of DF015-0015

The conditional strict-T factor-three form DF015-0015 has

\[
A>5z>w>0,\qquad C=2A-z,\qquad D=2A-w,
\]

and the necessary divisibilities

\[
D\mid C^2-A^2,\qquad
C\mid(A+4z)^2-(z-w)^2,\qquad
A\mid z^3+w^3.
\]

Set

\[
f=(2z-3w)(2z-w),\qquad g=(7z+2w)(11z-2w),
\]

\[
h=f/D,\qquad j=g/C.
\]

## Linear quotient theorem

Using f=h(2A-w), g=j(2A-z), and A|(z^3+w^3), one obtains

\[
\boxed{A\mid L:=j-h+5w+85z}.
\]

The interval A>5z>w>0 gives

\[
|h|<4z/9,\qquad 0<j<9z,
\]

hence

\[
0<L<100z.
\]

Therefore

\[
\boxed{L=nA\quad\text{for one }n\in\{1,\ldots,19\}.}
\]

## Nineteen plane cubics

Eliminating h and j gives the homogeneous cubic

\[
\begin{aligned}
F_n(A,z,w)={}&4nA^3-2nA^2(w+z)+nAwz\\
&-20A^2w-340A^2z+24Aw^2+148Awz+24Az^2\\
&-4(z^3+w^3)=0.
\end{aligned}
\]

Every global realization of DF015-0015 lies on one of the nineteen curves
F_n=0 and must additionally satisfy the original divisor, primitive and high
conditions.

## Smoothness and elliptic structure

For every n=1,...,19, exact Groebner elimination of

\[
\partial_A F_n=\partial_z F_n=\partial_w F_n=0
\]

in each of the three projective affine charts returns the unit ideal.  Thus
F_n=0 is a smooth projective plane cubic.  It contains the rational point

\[
[0:1:-1],
\]

so, with that point as origin, each curve is an elliptic curve over Q.

Projection from [0:1:-1] gives the binary quartic

\[
Y^2=\Delta_n(m),
\]

where

\[
\begin{aligned}
\Delta_n(m)={}&-48m^4+(8n+1952)m^3\\
&+(n^2+200n+10960)m^2\\
&-(8n^2+1328n+72000)m\\
&+16n^2+1600n+102400.
\end{aligned}
\]

Its classical invariants are

\[
I_n=n^4+592n^3+131424n^2+12967168n+482771200,
\]

\[
J_n=-2\bigl(n^6+888n^5+328560n^4+64835840n^3
+7183341312n^2+422071941120n+12095636377600\bigr).
\]

## Boundary

This is a structural reduction, not a no-go theorem.  Rational points on the
elliptic curves must still satisfy the integer quotient conditions h,j, the
three original divisibilities, reducedness and the high inequalities.
DF015-0015 remains OPEN_ELLIPTIC_REDUCED.