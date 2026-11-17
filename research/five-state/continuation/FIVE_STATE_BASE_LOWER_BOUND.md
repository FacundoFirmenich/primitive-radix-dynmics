# A lower bound for the first five-state nonpermutation base

In the oriented catalogue of forty rows, thirty-seven have been
excluded. The remaining three rows are covered at coordinate
100000 by the [bounded local search](SQUARE_CYCLE_SEARCH_100000.md).
The only reported state tuple realizes bases in the known CRT class,
whose least admissible representative is \(88011536665779\).

For 119772 both factors satisfy
\[
 B^2-1\ge \operatorname{lcm}(A,C,D,Q)
 =\frac{ACDQ}{\gcd(A,C)\gcd(D,Q)}
 > \frac{r^3}{4(r-1)}A^4 .
\]
The equality uses reducedness of the four core states. The
overlap product is at most \(r-1\) by the exact CRT criterion
and reducedness of \(A/Q\). Highness gives \(C,Q>rA/2\) and
\(D>rA\). At \(r=2\), the coefficient is two. At \(r=3\), it
is \(27/8\).

For 606897 all four cycle moduli divide \(B^2-1\). The four
cross pairs are coprime by reducedness, and the two possible
same-side overlaps divide two. They cannot both be even,
again by reducedness of \(A/Q\). Consequently
\[
 B^2-1\ge \operatorname{lcm}(A,C,D,Q)
 \ge \frac{ACDQ}{2}
 > \frac{27}{32}Q^4 ,
\]
using \(A>3Q/4\), \(C,D>3Q/2\).

Any witness other than the known tuple must have \(A\) or \(Q\)
at least \(100001\) in its corresponding row. The weakest of
the three bounds gives \(32(B^2-1)>27\cdot100001^4\).
The two exact comparisons
\[
 32(9185770248^2-1)\le27\cdot100001^4
 <32(9185770249^2-1)
\]
give \(B_{\min}^{(5)}\ge9185770249\). This bound concerns the
cardinality-five question only. It does not determine the
least realizing base.
