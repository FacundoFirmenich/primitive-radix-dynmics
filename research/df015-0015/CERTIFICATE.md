# DF015-0015 exact exclusion certificate

Scope: strict T, factor 3, in the chamber 9A < 5C < 5D < 10A.
Necessary reduction: the 19 cubics and gcd(C,D)=1 in
be27764cafe86b47c53c6434a993e8480e02082a, research/five-state/elliptic.

Set H=C+81D, d=81(n+148), L=4(81^3-1). Reduction modulo H gives
D^2(dA+LD)=0 mod H. Since gcd(D,H)=1, X=(dA+LD)/H is integral.
The chamber bounds give (L+d/2)/82 < X < (L+5d/9)/(819/10).
On H=1 substitute (A,C,D)=((X-Lv)/d,1-81v,v). The resulting
quadratics yield 772 fibres, six rational roots and zero chamber points.
This excludes DF015-0015 in the stated orientation. It leaves the
other arithmetic forms and the least base open.

From this directory run:

    python verify_rgphi_df015_0015.py
    python verify_rgphi_df015_0015_sympy.py

The second route uses SymPy factorization over QQ.
