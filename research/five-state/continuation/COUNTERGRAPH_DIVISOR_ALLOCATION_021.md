# RGΦ Round 021-D — countergraph divisor-allocation normal form

For the realized branch `DF015-0007-B2`, write
\[
Q_0=P+a,
\qquad
Q_1=P+b,
\qquad
U=P+c,
\qquad
D=3Q_0-P=2P+3a.
\]
The high-domain chamber is
\[
\boxed{\frac P3<a<\frac{2P}{3},\qquad \frac{3a}{2}<c<b<P.}
\]
The state-side system is
\[
\boxed{P\mid(b-a)(b+a)},
\]
\[
\boxed{P+b\mid c(2P+c)},
\]
\[
\boxed{P+c\mid(P+3a-b)(P+3a+b-2c)},
\]
\[
\boxed{2P+3a\mid(c-2P)(c+4P)}.
\]
In every line the overlap of the modulus with both factors divides two.  Hence every odd prime power of each modulus has a unique side allocation.

## Known solution

The Round-017 tuple corresponds to
\[
(P,a,b,c)=(406,151,325,306),
\]
so
\[
(Q_0,Q_1,U,D)=(557,731,712,1265).
\]
Its exact allocations are:

| modulus | factorization | allocation |
|---|---|---|
| \(P=406\) | \((b-a)(b+a)=174\cdot476\) | \(406=58\cdot7\), overlap \(2\) |
| \(Q_1=731\) | \(c(2P+c)=306\cdot1118\) | \(731=17\cdot43\) |
| \(U=712\) | \((D-Q_1)(D+Q_1-2U)=534\cdot572\) | \(712=178\cdot4\), overlap \(2\) |
| \(D=1265\) | \((U-3P)(U+3P)=-506\cdot1930\) | \(1265=253\cdot5\) |

## Exact finite audit extension

The independent exact enumerator was extended to
\[
Q_1\le16000,
\qquad
D\le48000.
\]
It examined
\[
496,924,929
\]
candidates and again found exactly the known tuple.

This remains a finite jurisdiction, not a global uniqueness proof.