# Weighted polynomial quotients, including the fifth modulus

Let \(x=(A,Q,C,D)\) in cyclic order and
\(I_i=(x_i,N_i)\), where
\(N_i=a_i^2x_{i+1}^2-b_i^2x_{i-1}^2\) is the corresponding
core square numerator. In each residual system, for all integers
\(t_i\ge0\) and \(T=\sum_i t_i\),
\[
\left(\bigcap_i I_i^{t_i}\right)_T
=\mathbb Q\prod_i x_i^{t_i}.
\]
If we additionally impose the fifth-modulus ideal to a nonnegative
power \(s\) and include its linear modulus to that power in the
denominator, the numerator space is still one-dimensional.

The fifth ideal in this construction is \((e)\), with \(e=D+jA\)
for 119772 and \(e=C+Q\) for 606897. Indeed the fixed edge at \(E\)
determines the base residue there. It gives no separate
state-side polynomial over that hyperplane. Each \(I_i^t\) is
saturated with respect to \(e\). On the reduced ring
\(\mathbb Q[x]/I_i\), neither of the two cycle lines is contained
in \(e=0\), so multiplication by \(e\) is injective. The graded
pieces \(I_i^k/I_i^{k+1}\) are free over \(\mathbb Q[x]/I_i\)
on the classes of \(x_i^lN_i^{k-l}\), for \(0\le l\le k\).
Filtering by these pieces gives injectivity on
\(\mathbb Q[x]/I_i^t\). Thus from \(P=e^sP_0\) we can cancel
\(e^s\) in each of the core ideal conditions.

For the core assertion, split by the two opposite variable blocks
\((x_0,x_2)\), \((x_1,x_3)\). Let \(P_0\) be a nonzero component
of bidegree \((n_0,n_1)\) with \(n_0+n_1=T\). Write
\(e_i=\operatorname{ord}_{x_i}(P_0)\),
\(v_i=t_i-e_i\), and \(u_i=\max(v_i,0)\).
The coefficient at the least power of \(x_i\) is divisible by
\(N_i^{u_i}\) and by the evident monomial in the neighboring
variables. The quadratic numerator and that monomial are coprime,
giving
\[
n_1\ge e_1+e_3+2\max(u_0,u_2),\qquad
n_0\ge e_0+e_2+2\max(u_1,u_3).
\]
As \(2\max(u_i,u_{i+2})\ge v_i+v_{i+2}\), adding forces equality.
Consequently \(v_i=v_{i+2}\ge0\) in each opposite block. Dividing
by the coordinate monomial leaves a polynomial whose nonzero
restriction to \(x_i=0\) has the form
\(h_i x_{i+2}^{2v_{i+1}}N_i^{v_i}\). Comparing on consecutive
coordinate planes gives
\[
h_i(-b_i^2)^{v_i}=h_{i+1}(a_{i+1}^2)^{v_{i+1}} .
\]
The product yields \(\rho_0^{2v_0}\rho_1^{2v_1}=1\), with
\(\rho_0=|a_0a_2/(b_0b_2)|\) and
\(\rho_1=|a_1a_3/(b_1b_3)|\). In the three systems these ratios
are either both greater than one or both less than one.
Thus all \(v_i\) vanish, proving the assertion.

This covers arbitrary unequal nonnegative weights and the specified
fifth ideal. It leaves open quotients using conditions that couple
the base residues on several moduli, or different denominator forms.
