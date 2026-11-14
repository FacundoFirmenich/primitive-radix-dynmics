from sympy import symbols, expand, groebner, QQ
from math import gcd
A,z,w,n,C,D=symbols('A z w n C D')
F=(4*n*A**3-2*n*A**2*(w+z)+n*A*w*z-20*A**2*w-340*A**2*z+24*A*w**2+148*A*w*z+24*A*z**2-4*(z**3+w**3))
F0=expand(F.subs(n,0))
assert expand(F-(F0+n*A*(2*A-z)*(2*A-w)))==0
f=(2*z-3*w)*(2*z-w); g=(7*z+2*w)*(11*z-2*w)
assert expand(g*(2*A-w)-f*(2*A-z)+(5*w+85*z-n*A)*(2*A-z)*(2*A-w)+F)==0
G=4*C**3+4*D**3+(n+148)*A*C*D-4*A**2*C-324*A**2*D
assert expand(F.subs({z:2*A-C,w:2*A-D})-G)==0
partials=[F.diff(A),F.diff(z),F.diff(w)]
for nv in range(1,20):
    poly=F.subs(n,nv); deriv=[p.subs(n,nv) for p in partials]
    for var,subs in [(A,{A:1}),(z,{z:1}),(w,{w:1})]:
        rem=[v for v in (A,z,w) if v!=var]
        gb=groebner([expand(poly.subs(subs))]+[expand(d.subs(subs)) for d in deriv],*rem,domain=QQ)
        assert any(h.as_expr()==1 for h in gb.polys),(nv,var)
AA,zz,ww=64233,11741,1138
assert int(F.subs({n:17,A:AA,z:zz,w:ww}))==0
assert AA>5*zz>ww>0
S=zz**3+ww**3
assert S%AA==0 and S//AA==25220421
CC=2*AA-zz; DD=2*AA-ww
assert (CC,DD)==(116725,127328) and gcd(CC,DD)==23
print('PASS elliptic_frontier smooth_cubics=19/19 F17_gcd_CD=23')
