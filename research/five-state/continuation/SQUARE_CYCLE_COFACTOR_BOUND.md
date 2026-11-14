# Cofactor bounds and unique primitive lift

Write the four square congruences in the form
\[
 A\mid D^2-\alpha^2Q^2,\quad C\mid D^2-\beta^2Q^2,\quad
 D\mid C^2-\gamma^2A^2,\quad Q\mid C^2-\delta^2A^2 .
\]
The tuples \((\alpha,\beta,\gamma,\delta)\) are \((r,1,r,1)\)
for 119772 and \((1,3,1,3)\) for 606897. The chamber ensures
that none of the eight linear factors is zero. For factor two of 119772, no prime divisor of the odd modulus
can divide both factors.

For any choice of signs, absorb them into the signed constants
\(\alpha',\beta',\gamma',\delta'\). On a solution define
\[
 h_A=\frac{A}{\gcd(A,D-\alpha'Q)},\quad
 h_C=\frac{C}{\gcd(C,D-\beta'Q)},\quad
 h_D=\frac{D}{\gcd(D,C-\gamma'A)},\quad
 h_Q=\frac{Q}{\gcd(Q,C-\delta'A)}.
\]
There are nonzero integers \(k_i\) such that the four linear
equations are
\[
 \begin{aligned}
 D-\alpha'Q&=(k_A/h_A)A,& D-\beta'Q&=(k_C/h_C)C,\\
 C-\gamma'A&=(k_D/h_D)D,& C-\delta'A&=(k_Q/h_Q)Q.
 \end{aligned}
\]
Thus fixing the signs and the four cofactors gives finitely many
choices for the \(k_i\). For example \(|k_i|<10h_i\) by the
chamber inequalities for both shapes and both factors.

The resulting homogeneous system always has rank at least three.
Indeed the first two rows solve for \(A,C\) in terms of \(D,Q\).
If the last two rows then vanished identically, the coefficient
of \(D\) in \(C-\delta'A\), and the coefficient of \(Q\)
in \(C-\gamma'A\), would give, with \(u=h_A/k_A,v=h_C/k_C\),
\[
 v=\delta' u,\qquad \beta'v=\gamma'\alpha' u .
\]
This requires \(\beta'\delta'=\gamma'\alpha'\), which fails by
absolute values for the three systems under consideration.
Therefore at most one rational projective point satisfies the
four linear equations. Normalizing via the reduced pair \(A,Q\)
leaves at most one primitive tuple of the four core coordinates,
and the branch relation determines the fifth state. The exact CRT
test then adjudicates that candidate.

If the tuple exists, choose three independent integral rows,
multiplying the rows above by \(h_A,h_C,h_D,h_Q\), respectively.
Their signed three-by-three minors give a nonzero integral kernel
vector. The primitive coordinate vector divides this vector in
\(\mathbb Z^4\). Every absolute coordinate is bounded by
\(6\cdot 10^3\) times the product of the three selected cofactors.
In particular, if all four cofactors are at most \(H\), every core
coordinate is at most \(6000 H^3\).

In the factor-two case of 119772 all four roots are nonuniform.
At \(D,Q\) this was already forced by high distinct numerators.
At \(C\), \(0<D-Q<C\) and \(2C<D+Q<4C\). The negative sign
would give \(D+Q=3C\), impossible by oddness. At \(A\),
\(Q,E\) are distinct in \((A,2A)\). The positive sign is excluded
by their difference and the negative sign would give \(Q+E=3A\),
again impossible by oddness. Thus both allocations are proper
and nontrivial in every modulus in this case.

This reduces a uniform cofactor bound to a finite classification.

## Two cofactors suffice on one side of the cycle

Fix the reduced quotients \(k_A/h_A,k_C/h_C\), including their
signs. Set
\[
 \begin{split}
 N_D&=(\beta' k_A h_C)^2-(\gamma'\alpha' k_C h_A)^2,\\
 N_Q&=(k_A h_C)^2-(\delta' k_C h_A)^2 .
 \end{split}
\]
At least one is nonzero because
\(\lvert\beta'\delta'\rvert\ne\lvert\gamma'\alpha'\rvert\).
Modulo \(D\), the linear equations for \(A,C\) and the square
congruence at \(D\) give \(D\mid Q^2 N_D\). Modulo \(Q\) they
give \(Q\mid D^2 N_Q\). The exact CRT criterion gives
\(\gcd(Q,D)\le2\), so \(D\mid4N_D\) and \(Q\mid4N_Q\).
Highness gives a ratio below four between any two core
coordinates. Hence all core coordinates are at most
\(16\max(|N_D|,|N_Q|)\).

The reverse calculation fixes the signed quotients at \(D,Q\).
Modulo \(A\), substitute \(k_DD\equiv h_DC\) and
\(k_QQ\equiv h_QC\). Modulo \(C\), substitute
\(k_DD\equiv-\gamma'h_DA\) and \(k_QQ\equiv-\delta'h_QA\).
The resulting constants are
\[
 \begin{split}
 N_A&=(k_Q h_D)^2-(\alpha' k_D h_Q)^2,\\
 N_C&=(\gamma' k_Q h_D)^2-(\beta'\delta' k_D h_Q)^2 .
 \end{split}
\]
At least one is nonzero. The bound \(\gcd(A,C)\le2\) gives
\(A\mid4N_A\) and \(C\mid4N_C\), leading to the same coordinate
bound. Bounded cofactors on either side suffice. On any
sequence of unbounded height, the maximum of the two smaller
sign cofactors on each side must therefore tend to infinity.
The determinant of the four-row system gives a further integer
condition. Reduce the numerator of that determinant, after
clearing the four cofactors, modulo any prime \(p\) dividing
all four cofactors. Only the term \(k_Ak_Ck_Dk_Q\) remains.
Each \(k_i\) is coprime to its own \(h_i\) by construction.
Thus no prime can divide all four cofactors. In the stated
factor-two case the moduli themselves \(A,C,D,Q\) are pairwise
coprime, so their four cofactors are pairwise coprime as well.

For an infinite family of primitive tuples, at least one of the
four smaller cofactors must grow without bound. The argument
does not bound those smaller cofactors.
