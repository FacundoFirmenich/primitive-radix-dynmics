# Four-state all-high rigidity — revised proof authority

**2026-11-11 · PROVED_SYMBOLIC_PLUS_CERTIFICATE · Claim C009**

The cycle budget reduces any nonpermutation four-state candidate to a Hamiltonian cycle with two T- and two S-edges and a unique strict factor 2 or 3. The two words up to cyclic rotation are TTSS and TSTS. No interchange symmetry of T and S is assumed.

For strict T in TSTS, write x0=C/(rQ), x1=A/Q, x2=A/D, x3=C/D. Closure forces S:x0<->x3, x1<->x2 and T:x1 fixed, x2<->x3. The high inequalities force r=3, Q=A+u, C=2A-u, D=2A-t, s=u-t, A>5u. From the S two-cycle in numerator fibre A: Bu = -t (mod A), B(-t)=u (mod A), hence A | u²-t². From the T two-cycle in denominator fibre D: BA=C and BC=A (mod D), hence D | A²-C² = A²-s² (mod D). The resulting integer quotient argument gives A<4u, contradiction.

For strict S, write x0=rA/D, x1=A/Q, x2=C/Q, x3=C/D with Q=A+P, D=A+rP, C=A+W. The T two-cycles yield Q | C²-A²=W(2A+W) and D | (rA)²-C²; the S two-cycle yields C | (rP-W)²-(P-W)² = (r-1)P((r+1)P-2W). Eliminating the integer quotients yields the two exact rational functions m(p,w) in the private manuscript, with uniform boundary inequalities. The exceptional branch is reduced to 1<=j<=18 and closed by the elementary modular argument in NONSQUARE_18.md.

**Remaining adversarial review gate:** an independent reviewer must still check every forced-closure subcase, the conic gcd eliminations and all cancellation steps from the full proof. Internal verification is not external peer review.
