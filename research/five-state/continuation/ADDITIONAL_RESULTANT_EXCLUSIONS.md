# Additional resultant exclusions

## DF015-0011/S and DF015-0017/S

In checker order the states are \(A/Q,rA/D,C/Q,C/D,A/E\). The
strict source is 1, \(T=(2,3,0,1,4)\), and \(S=(4,4,3,2,0)\).
The ordinary predecessor of the strict target is still \(A/Q\).
Hence \(D=rQ-(r-1)A\), the two \(T\)-cycle congruences and the
bounds for \(k\) in the sparse strict-S proof still apply.
Now \(S\) exchanges \(C/Q\) and \(C/D\), giving
\((D/Q)^2=1\bmod C\). The same resultant argument with exponent
two gives 145, 19152 and 19840 for \((r,k)=(2,-2),(3,-7),(3,-6)\).
The finite enumerations have 176, 2068 and 2476 residue-compatible
pairs, respectively. No high primitive core survives. In the
checker the previous \(A\)-modulus condition involving \(Q,D\)
must use the actual \(A\)-cycle, which here involves \(Q,E\).
The two-cycle at \(C\) gives \(C\mid D^2-Q^2\) directly. The
certificate excludes the full chamber before requiring the
\(A\)-cycle condition on \(E\).

## DF015-0005/T

In the orientation encoded by the archived map, write the
states as \(A/Q,C/(3Q),A/E,A/D,C/D\). The only strict edge is \(T:1\to0\)
and state 0 is fixed by \(T\). Comparing the two predecessors
gives \(C=3A-Q\): the positive shift is excluded by \(C<D<2A\).
The high chamber gives
\[
  A<Q<6A/5,\qquad 3Q/2<C<D<2A<2Q .
\]
The \(S\) cycle on \(C\) contains the two denominators \(3Q,D\).
They are exchanged in a two-cycle, giving \(C\mid 9Q^2-D^2\).
The \(T\) cycle at denominator \(D\) gives \(D\mid C^2-A^2\).
Therefore
\[
 k=\frac{D^2+72C^2-18CQ-9Q^2}{CD}
\]
is integral. Indeed the numerator vanishes modulo \(C\), and
\(9(C^2-A^2)=8C^2-2CQ-Q^2\) gives the identity modulo \(D\).
The reduced state \(C/D\) gives
\(\gcd(C,D)=1\).
Put \(u=Q/C\), \(v=D/C\), so \(1/2<u<2/3\) and
\(1<v<10/9\). The quotient \(v+(72-18u-9u^2)/v\) is
decreasing in both variables on this rectangle. Hence
\(44<k<62\), and the checker uses the inclusive integer range
44 through 61.

On the cycle at \(A\), \(D/Q\bmod A\) has order dividing the
cycle length \(\ell\). Reducing the quotient equation modulo
\(A\) and using \(C\equiv-Q\) gives
\(x^2+kx+81\equiv0\), where \(x=D/Q\bmod A\).
The resultant with \(x^\ell-1\) bounds \(A\) by a finite divisor
list. For each divisor enumerate \(A<Q<6A/5\), set \(C=3A-Q\)
and solve the quadratic in \(D\) by the integer discriminant.
The exact finite replay leaves no core.

The order for this row is \(\ell=3\). In 0006 and 0016 the
\(C\) cycle has length three and must use its cubic congruence.

## Remaining cycle families

| Ordinary nontrivial cycle lengths | Open oriented rows |
| --- | --- |
| Two in both charts | 0003/S, 0007/T, 0017/T |
| Two in T, including a three-cycle in S | 0006/T |
| Three in T, two in S | 0008/T, 0018/T |

This grouping gives the degrees of the ordinary cycle equations.
The linear predecessor shifts, reducedness and CRT constraints
remain attached to the individual rows. The partial archived
exclusion of 0016/T is excluded from this open-row table.
