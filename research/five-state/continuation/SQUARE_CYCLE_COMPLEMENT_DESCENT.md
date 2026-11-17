# Obstruction to ordinary divisor-complement descent

Keep the notation \((\alpha,\beta,\gamma,\delta)\) of the
[cofactor theorem](SQUARE_CYCLE_COFACTOR_BOUND.md). Define
\[
 U=D^2-\alpha^2 Q^2,\quad V=D^2-\beta^2 Q^2,\quad
 W=C^2-\gamma^2 A^2,\quad Z=C^2-\delta^2 A^2.
\]
On a primitive high core all four values are nonzero. Consider
replacing the opposite pair \((A,C)\) by \((|U|/A,|V|/C)\)
in either order, or the pair \((D,Q)\) by \((|W|/D,|Z|/Q)\)
in either order. Retain the other two coordinates unchanged.
In none of the three residual systems can the replacement
satisfy even the square congruences and adjacent coprimality.
This exclusion concerns arbitrary height in the original
high chamber. The replacement itself need not be high.

## Compatibility at the retained pair

The retained pair must be coprime. Its gcd divides \(r-1\)
in 119772 and two in 606897. If both retained coordinates are
even, the original coordinates across from them are odd by
adjacent coprimality. All four coefficients are odd in the
factor-three systems. The two corresponding quadratic
numerators, and hence both replacement coordinates, would
be even. This violates adjacent coprimality.

Cancel the retained unit of each opposite pair and the two
adjacent units in the replacement congruences. The following
necessary divisibilities result. A zero right side imposes
no restriction.

| Replaced pair | Ordering | Necessary divisibilities |
| --- | --- | --- |
| \(A,C\) | original | \(D\mid\beta^4-(\alpha\gamma)^4,\ Q\mid1-\delta^4\) |
| \(A,C\) | exchanged | \(D\mid\alpha^4-\beta^4\) |
| \(D,Q\) | original | \(A\mid1-\alpha^4,\ C\mid\gamma^4-(\beta\delta)^4\) |
| \(D,Q\) | exchanged | \(C\mid\gamma^4-\delta^4\) |

For instance, for the ordinary \(A,C\) replacement, the
congruence at \(D\), after clearing \(A^2C^2\), gives
\(D\mid A^2 V^2-\gamma^2 C^2 U^2\). Reduce this using
\(C^2\equiv\gamma^2 A^2\pmod D\) and cancel \(A^2Q^4\).
At \(Q\) use \(C^2\equiv\delta^2 A^2\pmod Q\); the remaining
constant is \(1-\delta^4\). For the exchanged order at \(D\)
the corresponding expression is \(C^2U^2-\gamma^2 A^2V^2\),
which reduces to \(\alpha^4-\beta^4\) after cancellation.
For the ordinary \(D,Q\) replacement, at \(A\) and \(C\)
reduce \(Q^2 W^2-\lambda^2D^2Z^2\) with
\(\lambda=\alpha,\beta\) respectively. Use the original
square congruences to cancel the adjacent unit and the other
retained unit. At \(C\) with the exchanged order use
\(D^2Z^2-\beta^2Q^2W^2\) instead. The sign of the resulting
constant is immaterial.

At least one displayed constant is nonzero in every row.
The possible retained moduli divide integers in
\(\{15,80,255,6560\}\). The checker takes one such divisor,
uses the neighboring chart to enumerate the necessary
square roots of unity, derives the other unknown modulus
from a nonvanishing quadratic numerator, and tests the exact
source chamber, gcds and four congruences. It exhausts all
twelve system-and-order cases and finds zero source cores.
The enumeration uses divisors and the real chamber to bound
coordinates. No independent search cutoff is needed.

From the repository root with PYTHONPATH=src:

    python -B research/five-state/continuation/verify_complement_descent.py

Compare with the [exact output](SQUARE_CYCLE_COMPLEMENT_DESCENT_CERTIFICATE.json).
## Fixed rational weights also force a height bound

Multiply the first and second replacement coordinates by positive
rational weights in the ratio \(\ell:m\), where \(\ell,m\) are
coprime positive integers. Assume the resulting coordinates are
integers and satisfy the four square divisibilities. The common
scale of the two weights may vary with the source. The congruences
at the retained pair, multiplied by the common denominator squared
when needed, now give the following integers.

| Replacement | Integer at first retained modulus | Integer at second retained modulus |
| --- | --- | --- |
| \(A,C\), original | at \(D\): \(\beta^4m^2-(\alpha\gamma)^4\ell^2\) | at \(Q\): \(m^2-\delta^4\ell^2\) |
| \(A,C\), exchanged | at \(D\): \(\alpha^4m^2-\beta^4\ell^2\) | at \(Q\): \(m^2-\ell^2\) |
| \(D,Q\), original | at \(A\): \(\ell^2-\alpha^4m^2\) | at \(C\): \(\gamma^4\ell^2-(\beta\delta)^4m^2\) |
| \(D,Q\), exchanged | at \(A\): \(\ell^2-m^2\) | at \(C\): \(\delta^4\ell^2-\gamma^4m^2\) |

Each retained modulus divides 16 times its displayed integer.
To see the independence from the common scale, write the two
complements in their chosen order as \(F,G\). The positive
integer replacements are proportional to \(\ell F,mG\). The
primitive integer pair on this ray divides \((\ell F,mG)\)
and the replacement pair. If the replacement has adjacent
coprimality with the retained moduli, its integer scaling of
the primitive pair is a unit at each retained modulus.
Therefore the retained congruences hold also on \((\ell F,mG)\).
Apply the same substitutions as above. The only factors left to
cancel are units of the adjacent moduli, powers of strict-factor
units, and at most the fourth power of the *other retained
coordinate*. A retained modulus and that fourth power can share
at most a factor 16, since the retained pair has gcd at most two.

The two displayed integers in a row cannot vanish simultaneously:
the original order would require
\(\alpha\gamma=\beta\delta\), and the exchanged order would
require \(\alpha=\beta\) or \(\gamma=\delta\), respectively.
All these equalities fail in the three configurations.
The height is thus bounded in terms of the reduced weight ratio,
even if its common scale varies. More explicitly, for
\(H=\max(A,C,D,Q)\),
\[
 H<64\cdot 9^4\max(\ell,m)^2 .
\]
In particular a finite menu of relative weights cannot implement
this type of descent on an unbounded family. The argument leaves
open transformations that redistribute the two linear factors
separately with growing weight ratios, or change both pairs at once.
