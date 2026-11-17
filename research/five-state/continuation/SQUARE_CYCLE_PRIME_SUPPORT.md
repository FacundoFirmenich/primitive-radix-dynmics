# Prime support and the fifth-state direction

Write \(H=\max(A,Q,C,D)\) and use the core order
\(x=(A,Q,C,D)\). The following results concern full primitive
realizations in the three residual systems.

Put \([n]_{\mathcal P}=\prod_{p\in\mathcal P}p^{v_p(n)}\).
For every fixed finite prime set \(\mathcal P\) and every
\(\eta>0\), only finitely many cores satisfy
\[
 [ACDQ]_{\mathcal P}^{\,2}[E]_{\mathcal P}\ge H^{4+\eta}.
\]
In particular this proves finiteness for cores supported on a
fixed set of primes, and for those with
\([ACDQ]_{\mathcal P}\ge H^{2+\eta}\) or
\([ACDQE]_{\mathcal P}\ge H^{5/2+\eta}\).

## Local rank including the fifth coordinate

The four core forms are \(x_i\), and the fifth-state form \(e\)
is \(D+jA\) for 119772 and \(C+Q\) for 606897. Thus
\(e=rE\), with \(r=2\) or \(3\). In each system
\(\gcd(r,ACDQE)=1\).

At an odd prime dividing \(x_i\), the full \(p\)-power of \(x_i\)
divides one of
\(L_{i,\pm}=a_i x_{i+1}\pm b_i x_{i-1}\), since both neighbors
are units at \(p\), and the coefficients are also units at the
primes in question. At \(p=2\) the strict-factor-two case has
no even coordinate. In the other cases, when \(x_i\) is even
both neighbors and both coefficients are odd. Both signs have
valuation at least one and one of them has valuation exactly one.
The larger is at least \(v_2(x_i)-1\). This accounts for at most
a factor two in the local bound per even core coordinate. At the
known core, for example, \(8\mid C\) and the two linear values
at \(C\) have 2-adic valuations one and two.

If \(p\) divides just one core coordinate, use \(x_i,L_{i,\pm}\)
among a basis of four rational linear forms at \(p\), selecting
the sign with larger valuation. If it also divides \(E\), add
\(e\) to this list. These three forms are independent for each
possible overlap and either sign. In 119772, \(E\) is coprime
to \(A\). For overlaps with \(Q,C\), the form \(D+jA\) has a
nonzero coefficient in the variable missing from the other
two forms, namely \(D\) or \(A\) respectively. A possible
overlap with \(D\) divides \(j\), so it occurs only at 2
for \(r=3,j=2\). For that overlap the three forms are
\(D,rC\pm A,D+2A\), which are independent.
In 606897, \(E\) is coprime to \(Q,C\); at \(A\) the fifth-state
form has a nonzero \(C\)-coefficient and at \(D\) it has a
nonzero \(Q\)-coefficient. If \(p\) divides no core coordinate,
include \(e\) when \(p\mid E\). Complete each list with coordinate
forms to obtain a basis over \(\mathbb Q\).

Two core coordinates can share a prime only at \(p=2\), in
opposite positions with minimum valuation one. Keep the one
with larger valuation and discard the other in this procedure.
The discarded contribution to \([ACDQE]_{\{2\}}\) is at most
two, and the additional discarded core contribution to the
local bound below is at most four. The form \(e\) remains
independent at any permitted overlap with the retained coordinate.
At \(p=r\) every coordinate is a unit and one may use the
coordinate basis. In every case, only finitely many bases of
linear forms are used, selected from a fixed finite list.

## Height bound for the fixed part of the support

For an odd \(p\) the product of the four chosen local absolute
values is at most
\[
 [ACDQ]_{\{p\}}^{-2}[E]_{\{p\}}^{-1}.
\]
At 2 this remains true with a factor at most eight, by the sign
loss and the discarded smaller overlap above. At the infinite
place choose the coordinate forms, whose product is at most
\(H^4\). For a fixed finite set \(\mathcal P\) the total product
is therefore bounded by
\[
 \frac{8H^4}{[ACDQ]_{\mathcal P}^{\,2}[E]_{\mathcal P}}
 \le \frac{16H^5}{[ACDQE]_{\mathcal P}^{\,2}}.
\]
The second inequality uses \(E<2H\). In particular the product
is bounded by a negative power of \(H\) whenever
\([ACDQE]_{\mathcal P}\ge H^{5/2+\eta}\) and \(H\) is sufficiently
large, for any fixed \(\eta>0\). If one drops \(E\) from the
local bases, the core-only threshold is \(H^{2+\eta}\).
The separate thresholds, rather than \(H^{2+\eta}\) for the
combined product, are the conclusions of this estimate.

For each of the finitely many choices of bases, the \(p\)-adic
Subspace Theorem places such cores in finitely many proper
rational linear subspaces of \(\mathbb Q^4\). Their
projectivizations are points, lines or planes. The
[plane theorem](SQUARE_CYCLE_SURFACE_FINITE.md) gives finitely
many cores in each one. For the precise linear-forms version
see [Evertse, *The p-adic Subspace Theorem*, Thm. 9.2](https://pub.math.leidenuniv.nl/~evertsejh/dio17-9.pdf).
This use is ineffective. Its finite set of places must be fixed
independently of the height.

## Effective exhaustion when the whole core is supported

Suppose \(ACDQ\) is supported on \(\mathcal P\). Enlarge this
set by the primes dividing \(2r\). For 119772, the relation
\(D+jA=rE\) gives an \(S\)-unit equation if \(E\) is also
supported: \(D/(rE)+jA/(rE)=1\). As \(\gcd(A,D)=1\),
each solution fixes \(A,D\) and then \(E\). The chamber
bounds \(Q,C\) in terms of \(A\). For 606897 use
\(C/(3E)+Q/(3E)=1\), with \(\gcd(C,Q)=1\). The chamber
then bounds \(A,D\) in terms of \(Q\).
This is a separate effective procedure for supported
\(ACDQE\), using the complete rational \(S\)-unit algorithm
of [Evertse and Győry, Chapter 5](https://doi.org/10.1017/CBO9781316160749.006)
or [de Weger, Chapter 6](https://math.deweger.net/proefschrift/).
Each candidate is checked with the ten-edge CRT.
The weighted support inequality above is broader and
requires no smoothness of the complementary linear forms.
A global bound on the support of the cores remains open.
