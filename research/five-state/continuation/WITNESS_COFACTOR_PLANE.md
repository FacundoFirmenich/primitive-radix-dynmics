# Uniqueness in the cofactor plane of the realized factor-three core

For 119772 with factor three, the only realization satisfying
\(7D=21Q-16A\) is \((406,712,1265,731,557)\), with base residue
88011536665779 and period 223336848698040. The plane is defined by
the reduced ratio \((D-3Q)/A=-16/7\).

Put \(c=C/A\), \(y=Q/A\), and \(d=D/A=3y-16/7\). The chamber gives
\(3/2<c<y<2\) and \(3<d<2c\), hence \(y>37/21\). Define
\[
R=32(C^2-A^2)+84AQ-49Q^2,\qquad
L=4(C^2-A^2)-42AQ .
\]
The moduli \(C,Q\) divide \(8R\). At \(Q\) this follows from
\(Q\mid C^2-A^2\), and at \(C\) use
\(8R=256C^2-49(D^2-Q^2)\). The moduli \(D,Q\) divide \(L\).
At \(D\) use \(21Q\equiv16A\pmod D\) and
\(D\mid C^2-9A^2\). The overlap bounds and \(\gcd(C,Q)=1\)
give integral levels
\[
J=8R/(CQ),\qquad K=2L/(DQ).
\]
They satisfy \(0<J<291\) and \(-28<K<0\). For the first bound,
the numerator of \(J\) is eight times
\(32(c^2-1)+84y-49y^2\). This expression before the factor of eight
is greater than \(56+148-196=8\), and less than 96 because
\(y>37/21>12/7\). Also \(cy>37/14\). For \(K\), the expression
\([8(c^2-1)-84y]/(dy)\) is negative and greater than \(-84/d>-28\).

The equality \(8L-R=(-420A+49Q)Q\) eliminates \(c^2\):
\[
Jc=32Kd+3360-392y .
\]
After substitution in \(8(c^2-1)-84y=Kdy\), the equation is
quadratic in \(y\). For each of the 7830 bounded integer pairs,
the checker uses exact rational discriminants and verifies the
open chamber. It yields two primitive rational representatives,
\[
(406,712,1265,731),\qquad (76223441,143229744,281410822,151878610)
\]
in the order \((A,C,D,Q)\). The latter is excluded already because
\(C\) is divisible by three. At the former, the two strict shifts are
checked with the ten edge congruences and direct dynamics. A
primitive rational representative can have only one scale in a
full realization because \(\gcd(A,Q)=1\).

This exhaustion holds at all heights on the specified plane.
Global uniqueness requires controlling cores at other cofactor ratios.

    PYTHONPATH=src python -B research/five-state/continuation/verify_witness_cofactor_plane.py
