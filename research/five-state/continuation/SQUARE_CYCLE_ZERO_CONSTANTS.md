# The complementary constants cannot vanish

For each of the three residual systems, all four complementary
constants of the signed cofactor identities are nonzero on every
primitive realization, for every choice of signs. This assertion
has no state-height cutoff. It applies only to the vanishing
subcases, and leaves the three orientation statuses unchanged.

Use the cyclic order \(x=(A,Q,C,D)\) and write
\(L_j=a_jx_{j+1}+\sigma_j b_jx_{j-1}\), with
\(x_j\mid a_j^2 x_{j+1}^2-b_j^2x_{j-1}^2\).
The coefficients are those of the
[curve theorem](SQUARE_CYCLE_CURVE_FINITE.md).
At index \(i\), write \(X=x_i,\ W=x_{i+2},\
Y=x_{i+1},\ Z=x_{i-1}\). For the two neighboring factors
there are choices
\[
 L_{i+1}=pX+qW,\qquad L_{i-1}=sX+tW
\]
with all four coefficients nonzero. A zero complementary constant at
\(i\) means that substituting the two signed ratios into the squared
cycle numerator formally at \(X=0\) gives zero. Since the linear
factors are nonzero in the high chamber, this is equivalent to
\[
 (a_i qY/L_{i+1})^2=(b_i tZ/L_{i-1})^2 .
\]
The two square roots give one of the equations
\[
 qt(a_iY+\sigma b_iZ)W=-(a_iqsY+\sigma b_itpZ)X .
\]
The strict factor is a unit modulo \(X\); the coefficients divide
that factor or equal one, and \(X\) is coprime to both neighbors.
Thus \(\gcd(X,qt)=1\). The opposite overlap satisfies
\(\gcd(X,W)\mid2\), so \(X\mid 2(a_iY+\sigma b_iZ)\).
Consequently
\[
 k=\frac{2(a_iY+\sigma b_iZ)}{X}\in\mathbb Z,\qquad
 -8\max(a_i,b_i)<k<8(a_i+b_i).
\]
Here \(k\ne0\): the eight linear factors are nonzero in the high
chambers. The bounds use \(\max x_j<4\min x_j\), positivity,
and the fact that a difference of two positive quantities has
absolute value bounded by their maximum. The remaining coordinates
are the two linear forms
\[
 X=\frac{2(a_iY+\sigma b_iZ)}{k},\qquad
 W=-\frac{2(a_iqsY+\sigma b_itpZ)}{kqt}.
\]
These formulas give the finite list of projective line
parametrizations used by the verifier.

## Exact exhaustion of each line

Clear denominators and divide the resulting coefficient array by
its content. At primitive positive parameters \((u,v)\) the four
evaluated forms \(F_j\) include \(K u,K v\) in positions \(Y,Z\),
so the normalization gcd divides \(K\). Use one of these two
integer obstructions on each line:

- If the primitive part \(f_j\) of \(F_j\) is proportional to an
  adjacent form, its value divides the adjacent gcd of the
  evaluated coordinates, hence divides \(K\) by reducedness.
- Put \(M=(a_j\det(f_j,F_{j+1}))^2-
  (b_j\det(f_j,F_{j-1}))^2\). If \(M\ne0\), then \(f_j(u,v)\)
  divides \(M\). To see this, the cycle divisibility holds
  before normalization because the modulus scales linearly and its
  numerator quadratically. Multiply the numerator congruence by
  the square of each coefficient of \(f_j\) in turn. Modulo its
  value this yields \(M v^2\) and \(M u^2\), respectively, up to
  the same signs after squaring. Since \(\gcd(u,v)=1\), the
  divisibility follows even if one coefficient is zero.

In the catalogue every line has at least one of the declared
obstructions. If the chosen obstruction is \(f_j(u,v)\mid m\)
and \(F_j=c f_j\) with positive content \(c\), comparability gives
\(\max(u,v)<4cm/K\). Enumerate the positive divisors of \(m\).
For each divisor the equation for \(f_j\) is linear in \(u,v\);
substitution restricts its single integer parameter by the exact
high-chamber inequalities. Then check the four cycle congruences
and all four adjacent gcds on the normalized tuple.

| System | Line parametrizations | Largest derived parameter bound | Primitive square cores |
| --- | ---: | ---: | ---: |
| 119772 factor 2 | 960 | 2760 | 0 |
| 119772 factor 3 | 1216 | 59520 | 0 |
| 606897 factor 3 | 1216 | 59520 | 0 |

Some parametrizations can describe the same geometric line.
The parameter bounds follow from the divisibilities for each
parametrization. They are not an assumption about state height.
No core reaches the fifth-state or full ten-edge tests.

From the repository root with PYTHONPATH=src:

    python -B research/five-state/continuation/verify_opposite_zero_constants.py

The output can be compared to
[the certificate](SQUARE_CYCLE_ZERO_CONSTANTS_CERTIFICATE.json).
