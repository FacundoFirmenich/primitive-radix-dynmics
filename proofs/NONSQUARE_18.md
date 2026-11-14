# Eighteen-case modular nonsquare proof

**2026-11-11 · PROVED_SYMBOLIC · Claim C010**

In the exceptional r=3, m=7, gcd(C,P)=19 branch, write C=19c, P=19p and 2P-W=jc. The high inequalities give W>(3P-A)/2 and C=A+W, hence 0<2P-W<C=19c, proving 1 <= j <= 18.

For Q(j)=403j^2+15314j+190969:
- odd j: Q(j) = 2 mod 4, not a square;
- j=4,8,14,18: nonsquare mod 5;
- j=2,12,16: nonsquare mod 11;
- j=6,10: nonsquare mod 17.

These exhaust the required range. The older 37-row certificate is retained only as a redundant regression check.

Run: `python src/rmr/check_nonsquare_18.py`.
