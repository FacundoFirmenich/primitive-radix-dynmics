# Five further factor-three exclusions

These arguments apply to the specified strict-\(T\) orientations.
Set the strict source to \(C/(3Q)\). Its target is the \(T\)-fixed
point \(A/Q\) in 0006, 0008, 0016 and 0018, and the ordinary
predecessor of the target is \(A/Q\) in 0017. The latter statement
uses the ordering of the archived graph, where the target is \(E/Q\).
In all instances \(C=3A-Q\) by the predecessor lemma and \(C<D<2A\).
Consequently
\[
 A<Q<6A/5,\qquad 9A/5<C<D<2A.
\]

## DF015-0006/T and DF015-0016/T

The ordinary \(S\) two-cycle on \(A\) gives \(A\mid D^2-Q^2\);
the ordinary \(T\) two-cycle on \(D\) gives \(D\mid C^2-A^2\).
Since \(Q\equiv-C\pmod A\) and \(\gcd(A,D)=1\),
\[
  I=\frac{A^2-C^2+D^2}{AD}\in\mathbb Z.
\]
In the high chamber \(I>0\). Moreover
\[
 I<\frac{5-81/25}{9/5}=\frac{44}{45}<1.
\]
This proves both exclusions directly and supplies a proof of
the previously archived 0016/T status.

## DF015-0008/T and DF015-0018/T

Both graphs have square cycle divisibilities \(A\mid D^2-Q^2\),
\(C\mid D^2-9Q^2\), and the cubic divisibility
\(D\mid C^3-A^3\). These are necessary regardless of the direction
around the cubic cycle, since the numerators on that cycle are
units modulo \(D\). The pairs \(A,C\), \(A,D\) and \(C,D\) are coprime:
for the first pair use \(C=3A-Q\) and reducedness of \(A/Q\),
and for the others use the states \(A/D,C/D\).
Using the three cycle divisibilities and \(Q=3A-C\) gives
\[
  K=\frac{81A^2+C^2-D^2}{AC},\qquad
  Y=\frac{81A^3-AD^2-81C^3+81CD^2}{ACD}\quad\in\mathbb Z .
\]
The checker verifies each polynomial restriction symbolically.
With \(c=C/A\), \(d=D/A\), one has \(9/5<c<d<2\).
Therefore \(K<45\) and \(K>(81+81/25-4)/2>40\).
Eliminating \(d^2\) from the second relation gives
\[
 d^2=81+c^2-Kc,\qquad
 Yd=6561+K-(81K+1)c.
\]
For each \(K\in\{41,42,43,44\}\), bounds at the four corners of
the rectangle \([9/5,2]^2\) enclose all integral values of \(Y\).
When \(Y\ne0\) substitute the linear expression for \(d\) in the
quadratic. When \(Y=0\), its linear equation determines \(c\),
and then solve for \(d\). Both branches use integer discriminants
and a final exact substitution. All 1538 quotient pairs give
zero rational points in the open high chamber.

## DF015-0017/T

In calculation variables the states in canonical order are \(U/Q,A/Q,A/D,C/D,C/(3Q)\).
The strict source is the final state; \(A/Q\) is the
ordinary predecessor of its target. The same quadratic
quotient as 0005/T applies, with \(\ell=2\) on the \(A\)-cycle:
\[
 k=\frac{D^2+72C^2-18CQ-9Q^2}{CD},\qquad
 x^2+kx+81\equiv x^2-1\equiv0\pmod A,\quad x=D/Q\bmod A .
\]
The open chamber gives \(44<k<62\); the replay includes 44 as well.
Every possible \(A\) divides the nonzero corresponding resultant.
For each divisor, enumerate \(A<Q<6A/5\) and solve the
quadratic in \(D\). There are four rational roots tested before
the integer, chamber, and coprimality conditions, and no core passes.

Run `python research/five-state/continuation/verify_remaining_resultants.py`
with `PYTHONPATH=src`.
