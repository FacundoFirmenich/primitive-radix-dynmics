"""Exact checks of the supplied transfers and their actual pi-phase labels."""
from fractions import Fraction as F
from math import factorial,gcd,lcm
from pathlib import Path
import hashlib,json,platform

R=Path(__file__).resolve().parent
ANGLES=(F(1,100),F(9,500),F(1,50),F(3,125),F(3,100))
SHIFTS=(7,7,7,7,6)

def T(x,b):
    y=b*x
    return y-y.numerator//y.denominator

def S(x,b):
    return 1/(1+T(1/x-1,b))

def families(n):
    p=3**n-1
    numerators=[p-3**j for j in range(n)]
    denominators=[2*p-3**j for j in range(n)]
    out=[]
    for mode,values in [('T',numerators),('S',denominators)]:
        mod=lcm(*values)
        assert gcd(mod,p)==1
        b=1+mod*((2*pow(mod,-1,p))%p)
        states=[F(v,p) if mode=='T' else F(p,v) for v in values]
        assert all(F(1,2)<x<1 for x in states) and len(set(states))==n
        for j,x in enumerate(states):
            assert T(x,b)==(states[(j+1)%n] if mode=='T' else x)
            assert S(x,b)==(x if mode=='T' else states[(j+1)%n])
            assert gcd(b,x.numerator)==gcd(b,x.denominator)==1
        out.append({'cyclic_generator':mode,'n':n,'base':b,'core_modulus':p,'other_coordinates':values})
    return out

def atan_bounds(q,k=80):
    x=F(1,q)
    lower=sum(((-1)**j*x**(2*j+1)/F(2*j+1) for j in range(k)),F(0))
    upper=lower+x**(2*k+1)/F(2*k+1)
    assert k%2==0
    return lower,upper

def pi_bounds():
    lo5,hi5=atan_bounds(5);lo239,hi239=atan_bounds(239)
    return 16*lo5-4*hi239,16*hi5-4*lo239

def err_series(pi,m,k):
    return sum(((-1)**(j+1)*pi**(2*j+1)/(factorial(2*j+1)*m**(2*j))
                for j in range(1,k+1)),F(0))

def unique_floor(lo,hi):
    a=lo.numerator//lo.denominator;b=hi.numerator//hi.denominator
    assert a==b,('uncertified floor',a,b)
    return a

def exact_pi_labels():
    lo,hi=pi_bounds();rows=[];depths=[[] for _ in ANGLES]
    for n in range(9):
        bits=[];ds=[]
        for i,(a,s) in enumerate(zip(ANGLES,SHIFTS)):
            m=180/a*10**n
            assert F(0)<hi/m<1
            # E increases with pi: derivative 1-cos(pi/m)>0.
            el=err_series(lo,m,8);eu=err_series(hi,m,9)
            assert 0<el<eu
            scale=10**(2*n+s)
            ll,lu=scale*el,scale*eu
            assert 0<ll<lu<1
            top=unique_floor(scale*lo,scale*hi)
            theta_lo,theta_hi=scale*lo-top,scale*hi-top
            bottom=unique_floor(scale*(lo-eu),scale*(hi-el))
            borrow=top-bottom
            assert borrow in [0,1]
            if borrow:
                assert theta_hi<ll
            else:
                assert theta_lo>lu
            bits.append(borrow)
            for d in range(1,2*n+16):
                q=10**d
                if unique_floor(q*lo,q*hi)!=unique_floor(q*(lo-eu),q*(hi-el)):
                    break
            else:
                raise AssertionError('first difference not found within the test limit')
            depths[i].append(d);ds.append(d)
        assert bits[:4]==sorted(bits[:4])
        rows.append({'n':n,'borrow_bits_common_pi_normalization':bits,'first_difference_positions':ds})
    telescopes=0
    for i in range(5):
        for j in range(i+1,5):
            J=lambda k,n:2*n+SHIFTS[k]-depths[k][n]
            for u in range(8):
                for v in range(u+1,9):
                    lhs=sum((depths[i][n]-depths[i][n-1])-(depths[j][n]-depths[j][n-1])
                            for n in range(u+1,v+1))
                    rhs=(J(i,u)-J(j,u))-(J(i,v)-J(j,v))
                    assert lhs==rhs;telescopes+=1
    return {'pi_interval_width':str(hi-lo),'phase_rows':rows,
            'independently_certified_floor_comparisons':45,
            'cross_family_coboundary_checks':telescopes,
            'empirical_equidistribution_assumed':False}

def affine_strips():
    # Common coordinates (A,Q,C,D), vertices of closure at A=1.
    # Use symbolic rational linear feasibility only; certificates below
    # are identities in the chamber's positive wall variables.
    import sympy as s
    A,t,u,v,z=s.symbols('A t u v z')
    Q=A-u;E=A-t;D=2*A-3*t;C=D+z
    # Four original square conditions yield products, not chosen signs.
    assert s.expand(D-3*Q+A-3*(u-t))==0
    assert s.expand(C+A-3*Q-(u-v)) .subs(z,3*t-2*u-v)==0
    # Exact Farkas certificates, in independent original core coordinates.
    a,q,c,d=s.symbols('A Q C D');e=(d+a)/3;xx=(a,q,c,d)
    walls=[2*d-3*a,c-d,2*q-c,a-q]
    G=s.Matrix([[s.expand(w).coeff(y) for y in xx] for w in walls])
    assert G.det()==1
    forms=[a-e+q,a+e-q,e+q-a,2*a-e-q,c-a,q-c+a,
           c+a-2*q,4*q-c-a,d-q,c-d+q,d+q-c,2*c-d-q,
           3*a-c,d-3*a+c,3*a+c-2*d,4*d-3*a-c]
    certs=[]
    for form in forms:
        coeff=s.Matrix([[s.expand(form).coeff(y) for y in xx]])*G.inv()
        assert all(x>=0 for x in coeff) and any(x>0 for x in coeff)
        assert s.expand(form-sum(k*w for k,w in zip(coeff,walls)))==0
        certs.append({'positive_form':str(form),'nonnegative_wall_coefficients':list(map(str,coeff))})
    labels=[{'modulus':'A','sign':'+','linear_form':'E-Q','consequence':'forced zero then repeated state'},
            {'modulus':'A','sign':'-','linear_form':'E+Q','strip':'A<L<2A'},
            {'modulus':'Q','sign':'+','linear_form':'C-A','strip':'0<L<Q'},
            {'modulus':'Q','sign':'-','linear_form':'C+A','consequence':'L=3Q, equivalently v=u; requires archived nontrivial pure-sign exclusion'},
            {'modulus':'C','sign':'+','linear_form':'D-Q','strip':'0<L<C'},
            {'modulus':'C','sign':'-','linear_form':'D+Q','strip':'C<L<2C'},
            {'modulus':'D','sign':'+','linear_form':'3A-C','strip':'0<L<D'},
            {'modulus':'D','sign':'-','linear_form':'3A+C','consequence':'L=3D, forcing 3|C'}]
    return {'uniform_sign_branches':labels,'branches_disposed_by_simple_strips_and_primitivity':7,
            'positive_walls':list(map(str,walls)),'wall_basis_determinant':1,
            'exact_nonnegative_combination_certificates':certs,
            'new_global_rows_excluded':0,'scope':'uniform roots only; does not discard mixed CRT roots'}

if __name__=='__main__':
    config={'python':platform.python_version(),'arithmetic':'exact integer/rational',
            'angles_degrees':[[x.numerator,x.denominator] for x in ANGLES],
            'normalization':'P=m*sin(pi/m), m=(180/a)*10**n',
            'scale_shifts':SHIFTS,'phase_indices':list(range(9)),
            'pi_certificate':'Machin: 16 atan(1/5)-4 atan(1/239), even 80-term lower sums',
            'error_certificate':'8-term lower at pi_lower; 9-term upper at pi_upper',
            'family_n_cases':list(range(2,9)),
            'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    print(json.dumps(config),flush=True)
    import sympy as s
    assert s.sin(s.pi)==0
    result={'config':config,'permutation_families':[r for n in range(2,9) for r in families(n)],
            'sine_certificates':exact_pi_labels(),'strip_transfer':affine_strips(),
            'unrestricted_angle_counterexample':{'a_degrees':180,'n':0,'m':1,'P':'sin(pi)=0'}}
    (R/'INDEPENDENT_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2),flush=True)
