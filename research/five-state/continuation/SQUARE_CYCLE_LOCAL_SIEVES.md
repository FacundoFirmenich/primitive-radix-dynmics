# Finite local sieves for the residual square-cycle systems

For each of the two linear shifts of 119772 at each factor,
and for the shift of 606897, the exact fibre equations and the
open real chamber are compatible with the localized edge
congruences and exact gcd conditions at every finite set of
primes. Here an edge congruence localized at \(p\) uses the
\(p\)-part of its entire source modulus, and reducedness
means that \(p\) cannot divide both coordinates of a state.
The result does not impose primitiveness or the edge equations
at primes outside the chosen set.

For 119772 take the independent coordinates \(A,C,Q,E\) with
\(D=rE-jA\). At any odd \(p\) other than \(r\), choose all
independent coordinates to be \(p\)-units and choose \(E/A\)
away from the single forbidden residue \(j/r\). Then \(D\)
is also a unit and all the required defect conditions hold
at \(p\), for example with \(B\equiv1\bmod p\). At \(p=r\)
all independent coordinates can again be units. Then \(D\)
is a unit since \(j\) is prime to \(r\). Only the strict
source modulus \(rA\) is divisible by \(r\), to valuation one.
The raw edge congruence is automatic on that part when
\(B\equiv0\bmod r\), as its right side is a multiple of \(r\).
For factor two this covers \(p=2\). At \(p=2\) for factor three,
take \(A,C,Q\) odd. For \(j=1\) take \(E=2\bmod4\), so \(D\)
is odd. The only even source modulus is \(E\), at a fixed
\(T\) edge, where \(B\equiv1\bmod2\) is sufficient. For \(j=2\)
take \(E\) odd, making all moduli odd.

For 606897 take independent \(A,D,E,Q\) and set \(C=3E-Q\).
At odd \(p\ne3\) choose all four to be units and choose \(E/Q\)
away from \(1/3\), making \(C\) a unit. At \(p=3\) the four
can be units and then \(C\equiv-Q\) is a unit. Only the strict
source modulus \(3Q\) has positive 3-adic valuation, namely one,
and \(3\mid B\) gives both the correct defect and the corresponding
part of the edge congruence. At \(p=2\), choose \(A,D,Q\) odd
and \(E=2\bmod4\); then \(C\) is odd. The only even modulus
is \(E\) at the fixed \(S\) edge, so odd \(B\) suffices.

The CRT combines the local prescriptions into a full-rank
translated rectangular lattice in the independent integer
coordinates. Every nonempty open homogeneous real chamber
contains points of that lattice: take any interior ray, scale it
and round the independent coordinates to the nearest lattice
points. The error is bounded while the distance from the
boundary grows. In \((A,C,D,Q,E)\) coordinates, interior points
for 119772 are respectively
\((100,170,330,180,115)\) and \((100,145,250,170,175)\) at
\(r=2,\ j=-1,1\) after choosing \(E=(D+jA)/2\).
For \(r=3,\ j=1,2\), use
\((100,170,320,180,140)\) and \((100,170,320,180,520/3)\).
For 606897 use \((96,176,185,100,92)\).
These are real chamber directions and do not assert primitive
integer realizations. The required congruence class of \(B\)
is chosen separately by CRT and contains arbitrarily large bases.

Thus the direct edge equations, reductions and height chamber
alone cannot give a contradiction on any fixed finite prime list.
A global argument can still exploit interactions between primes
actually dividing the unknown moduli, and a new necessary
Diophantine invariant can have its own local obstruction.
