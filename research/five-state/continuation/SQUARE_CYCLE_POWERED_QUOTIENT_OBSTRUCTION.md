# Obstruction to global polynomial quotients built from the four cycle ideals

Let \(S=\mathbb Q[x_0,x_1,x_2,x_3]\) and use cyclic indices. Set
\[
 I_i=(x_i,N_i),\qquad N_i=a_i^2x_{i+1}^2-b_i^2x_{i-1}^2 .
\]
Assume all coefficients are nonzero and the two absolute ratios
\[
 \rho_0=|a_0a_2/(b_0b_2)|,\qquad
 \rho_1=|a_1a_3/(b_1b_3)|
\]
are either both greater than one or both less than one.
For every \(t\ge1\),
\[
  \left(\bigcap_i I_i^t\right)_{4t}
     =\mathbb Q\,(x_0x_1x_2x_3)^t.
\]
This covers all three residual systems. In particular increasing the
common power in the four-ideal quotient construction cannot yield a
nonconstant global quotient.

## The two degrees force a sharp balance

Give the variables \(x_0,x_2\) bidegree \((1,0)\) and
\(x_1,x_3\) bidegree \((0,1)\). All four ideals and their
powers are bihomogeneous. It suffices to consider one
nonzero bihomogeneous component \(P\) of degree \((n_0,n_1)\)
with \(n_0+n_1=4t\).

Let \(e_i\) be the exact exponent of \(x_i\) dividing \(P\).
The coefficient of \(x_i^{e_i}\) in \(P\) is divisible by
\(N_i^{(t-e_i)_+}\), where \(z_+=\max(z,0)\). This follows by
expanding the generators \(x_i^j N_i^{t-j}\) in \(x_i\),
which does not occur in \(N_i\). The coefficient is also
divisible by \(x_{i-1}^{e_{i-1}} x_{i+1}^{e_{i+1}}\).
The latter monomial and \(N_i\) are coprime. Comparing
degrees in the two blocks, with \(u=\min(e_0,e_2)\) and
\(v=\min(e_1,e_3)\), gives
\[
 n_1\ge e_1+e_3+2(t-u)_+,\qquad
 n_0\ge e_0+e_2+2(t-v)_+ .
\]
The sum of the two right sides is
\(4t+|e_0-e_2|+|e_1-e_3|+2(u-t)_++2(v-t)_+\).
Thus equality holds in both bounds, \(e_0=e_2=u\le t\),
and \(e_1=e_3=v\le t\).

## Boundary compatibility for the remaining polynomial

Put \(\ell_i=t-e_i\) and divide \(P\) by \(\prod_i x_i^{e_i}\)
to obtain \(R\). It has degree \((2(t-v),2(t-u))\) and its
restriction to every coordinate plane is nonzero. The coefficient
divisibilities and the exact bidegrees force
\[
 R|_{x_i=0}=h_i x_{i+2}^{2\ell_{i+1}} N_i^{\ell_i},
 \qquad h_i\in\mathbb Q^\times .
\]
On the edge \(x_i=x_{i+1}=0\), the two resulting monomials
in \(x_{i+2},x_{i-1}\) have the same powers. Equating their
coefficients gives
\[
 h_i(-b_i^2)^{\ell_i}=h_{i+1}(a_{i+1}^2)^{\ell_{i+1}} .
\]
Multiplication and absolute values yield
\(\rho_0^{2(t-u)}\rho_1^{2(t-v)}=1\). The strict
same-direction hypothesis forces \(u=v=t\). Then \(R\)
is constant, which proves the claim. Conversely the coordinate
product to power \(t\) lies in each \(I_i^t\).

In the order \((A,Q,C,D)\) both ratios equal \(r\) for
119772 with \(r=2,3\), and both equal \(1/3\) for 606897.
Independent finite-field rank calculations through power five
returned nullity one in each system. They check a bounded
range of the linear algebra. The bidegree argument proves the
result for all powers. Quotients on a fixed surface can still
exist because its defining equation changes the ideal
conditions. This obstruction concerns the direct powered
construction on the full core space.
