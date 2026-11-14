# RGΦ Round 021-C — four-fibre near-coprime splitting

The four dense priority forms
\[
\texttt{DF015-0003},\quad
\texttt{DF015-0007},\quad
\texttt{DF015-0011},\quad
\texttt{DF015-0017}
\]
share the same fibre topology.  After dual normalization, write their states as
\[
\frac{P}{Q_0},\quad
\frac{P}{Q_1},\quad
\frac{U}{Q_1},\quad
\frac{rP}{D},\quad
\frac{U}{D},
\]
where \(r\in\{2,3\}\) is the strict factor and all displayed fractions are reduced and high.

Every realization satisfies the four divisibilities
\[
\boxed{P\mid(Q_1-Q_0)(Q_1+Q_0-2P)},
\]
\[
\boxed{Q_1\mid(U-P)(U+P)},
\]
\[
\boxed{U\mid(D-Q_1)(D+Q_1-2U)},
\]
\[
\boxed{D\mid(U-rP)(U+rP)}.
\]
The branch-specific predecessor-shift equation fixes \(D\) as one of the linear expressions listed in `DENSE_BRANCHES_021.csv`.

## Theorem 021-C — overlap at most two

In each of the four boxed divisibilities, the gcd of the modulus with both linear factors divides two.

For example, an odd prime dividing
\[
P,\ Q_1-Q_0,\ Q_1+Q_0-2P
\]
would imply \(Q_1\equiv Q_0\equiv P\equiv0\pmod\ell\), contradicting the reducedness of \(P/Q_0\) and \(P/Q_1\).  The other three cases are identical after using the appropriate primitive fractions.

Therefore every odd prime power dividing a modulus belongs to exactly one of the two paired linear factors.

## Consequence — divisor-allocation normal form

The dense forms are equivalent to finitely many allocations of the odd prime-power divisors of
\[
P,\ Q_1,\ U,\ D
\]
between the corresponding linear factors, with only a controlled two-adic overlap.

This is strictly sharper than a direct height scan: it turns each form into a finite divisor-splitting problem once the moduli are fixed.

## Boundary

The theorem does not yet prove that the unrealized branches are impossible.  It supplies the arithmetic normal form for Gate 022.