#!/usr/bin/env python3
"""Auditoría exacta de tres unidades irreducibles {4777}, {6444}, {7444}.

Opera sobre valores completos y trazas de tokens externos. No indexa, ordena,
segmenta ni transforma las cifras internas de ninguna fuente.
Sólo Python estándar; demostraciones generales en INFORME_TERNARIO.md.
"""
from __future__ import annotations
from collections import deque, defaultdict
from fractions import Fraction
from itertools import product
from math import gcd, lcm
from pathlib import Path
import json, hashlib

X,Y,Z=4777,6444,7444
FIVE_T=(1,0,3,2,4)
FIVE_S=(4,2,1,0,0)
C=(0,0,1,1,1)


def chk(ok,msg):
    if not ok: raise AssertionError(msg)


def det3(M):
    a,b,c=M[0];d,e,f=M[1];g,h,i=M[2]
    return a*(e*i-f*h)-b*(d*i-f*g)+c*(d*h-e*g)


def extended_gcd(a,b):
    r0,r1=a,b; s0,s1=1,0;t0,t1=0,1
    while r1:
        q=r0//r1
        r0,r1=r1,r0-q*r1
        s0,s1=s1,s0-q*s1
        t0,t1=t1,t0-q*t1
    return r0,s0,t0


def crt_general(a,b,c):
    """CRT for residues modulo X,Y,Z with gcd(Y,Z)=4; no splitting sources."""
    chk((b-c)%4==0,'incompatible CRT residues on shared gcd 4')
    g,k,t=extended_gcd(Y,Z)
    chk(g==4,'pair gcd =4')
    n2=Z//4
    b2=((c-b)//4 * pow(Y//4,-1,n2)) % n2
    yz=b+Y*b2
    mod_yz=lcm(Y,Z)
    chk(yz%Y==b%Y and yz%Z==c%Z,'Y/Z CRT merge')
    L=lcm(X,Y,Z)
    u=((a-yz)*pow(mod_yz,-1,X))%X
    answer=(yz+mod_yz*u)%L
    chk((answer%X,answer%Y,answer%Z)==(a%X,b%Y,c%Z),'CRT3 check')
    return answer


def frac_step(pair,B,which):
    q=Fraction(*pair)
    if which=='T':
        w=B*q
        out=w-(w.numerator//w.denominator)
        delta=gcd(B,q.denominator)
    else:
        w=Fraction(1,1)/q-1
        t=B*w
        out=Fraction(1,1)/(1+(t-(t.numerator//t.denominator)))
        delta=gcd(B,q.numerator)
    return {'result':str(out),'defect':delta,'in_H':bool(Fraction(1,2)<out<1)}


def matmul(A,B):
    n=len(A)
    return [[sum(A[i][k]*B[k][j] for k in range(n)) for j in range(n)] for i in range(n)]


def inverse_unipotent(A):
    I=[[int(i==j) for j in range(len(A))] for i in range(len(A))]
    N=[[A[i][j]-I[i][j] for j in range(len(A))] for i in range(len(A))]
    E=[row[:] for row in I]
    power=[row[:] for row in I]
    for k in range(1,len(A)):
        power=matmul(power,N)
        for i in range(len(A)):
            for j in range(len(A)):
                E[i][j]+=(-1)**k*power[i][j]
    return E


def comm(A,B):
    return matmul(matmul(matmul(A,B),inverse_unipotent(A)),inverse_unipotent(B))


def make_UT4(weight, index):
    E=[[int(i==j) for j in range(4)] for i in range(4)]
    E[index][index+1]=weight
    return E


def ordered_signatures(word):
    freq={k:0 for k in 'XYZ'}
    pairs={(a,b):0 for a in 'XYZ' for b in 'XYZ' if a!=b}
    count_XY=0
    count_XYZ=0
    for c in word:
        if c=='Z': count_XYZ+=count_XY
        for a in 'XYZ':
            if a!=c: pairs[(a,c)]+=freq[a]
        if c=='Y': count_XY+=freq['X']
        freq[c]+=1
    return {'counts':freq,'pairs':{''.join(k):v for k,v in pairs.items()},'XYZ':count_XYZ}


def cover_adjacency(m,weights):
    """Five-state automaton: 1 coordinate of Z_m or 2 parallel coordinates."""
    t_weight,s_weight=weights
    dim=len(t_weight)
    size=5*m**dim
    def encode(i,vec):
        r=0
        for a in vec:r=r*m+a
        return i*m**dim+r
    def decode(a):
        i,v=divmod(a,m**dim)
        vec=[]
        for _ in range(dim):
            v,r=divmod(v,m);vec.append(r)
        return i,tuple(reversed(vec))
    adj=[None]*size
    for a in range(size):
        i,r=decode(a)
        adj[a]=(encode(FIVE_T[i],tuple((v+d)%m for v,d in zip(r,t_weight))),
                encode(FIVE_S[i],tuple((v+d)%m for v,d in zip(r,s_weight))))
    return adj,encode,decode


def graph_scc_period(adj):
    """Tarjan SCC + gcd of distance defects on each SCC; all exact."""
    N=len(adj)
    index=0;S=[];on=[False]*N;idx=[-1]*N;low=[0]*N;comps=[]
    # Iterative Kosaraju avoids recursion limits, reproducible for thousands of states.
    visited=bytearray(N);order=[]
    for root in range(N):
        if visited[root]:continue
        visited[root]=1
        stack=[(root,0)]
        while stack:
            u,nxt=stack[-1]
            if nxt>=2:
                order.append(u);stack.pop();continue
            stack[-1]=(u,nxt+1)
            v=adj[u][nxt]
            if not visited[v]:
                visited[v]=1;stack.append((v,0))
    rev=[[] for _ in range(N)]
    for a,vs in enumerate(adj):
        for b in vs: rev[b].append(a)
    component_id=[-1]*N
    for root in reversed(order):
        if component_id[root]>=0:continue
        label=len(comps); component_id[root]=label; comp=[root];todo=[root]
        for u in todo:
            for v in rev[u]:
                if component_id[v]<0:
                    component_id[v]=label;comp.append(v);todo.append(v)
        comps.append(comp)
    records=[]
    for n,comp in enumerate(comps):
        dist={comp[0]:0};todo=deque([comp[0]])
        while todo:
            u=todo.popleft()
            for v in adj[u]:
                chk(component_id[v]==n,'SCC must be closed for the lifted automaton')
                if v not in dist:
                    dist[v]=dist[u]+1;todo.append(v)
        chk(len(dist)==len(comp),'component distances')
        period=0
        for u in comp:
            for v in adj[u]:period=gcd(period,dist[u]+1-dist[v])
        records.append({'size':len(comp),'period':period})
    return records


def solo_cover_theory(u,v,m):
    # The additive subgroup generated by T-loop (u) and S^2-loop (2v).
    ncomp=gcd(m,u,2*v)
    a=gcd(m,2*(v-u))
    period=a//gcd(a,u)
    return {'components':ncomp,'size_each':5*m//ncomp,'period':period}


def joint_cover_theory(m):
    # Group subgroup K=< (x,x),(2y,2z) > in Z_m^2: index via 2x2 minors.
    det=2*X*(Z-Y)
    index=gcd(m*m,m*X,2*m*Y,2*m*Z,det)
    h=gcd(m,2*(Z-Y))
    p=m//h
    g=gcd(m,2*p*(Y-X))
    period=g//gcd(g,X)
    return {'components':index,'size_each':5*m*m//index,'period':period}


def phase(a,b,m):
    chk(gcd(m,X*(Z-Y))==1,'phase requires u and difference units')
    # Recover S-count, then length n mod m.
    ns=((b-a)*pow(Z-Y,-1,m))%m
    time=((a-(Y-X)*ns)*pow(X,-1,m))%m
    return ns,time


def audit():
    data={'sources':{'X':'{4777}','Y':'{6444}','Z':'{7444}',
                     'internal_access':'denied by mathematical contract'},
          'pairs':{},'triplet':{},'fourier':{},'covers':{},'tests':{}}
    values=(X,Y,Z)
    chk((-3*X+8*Y-5*Z)==1,'ternary affine Bezout')
    # Minimax L1 certificate over all integer affine relations to +01.
    affine_solutions=[]
    for a in range(-16,17):
        for b in range(-16,17):
            c=-a-b
            if abs(a)+abs(b)+abs(c)<=16 and a*X+b*Y+c*Z==1:
                affine_solutions.append((a,b,c))
    chk(affine_solutions==[(-3,8,-5)],'unique minimal L1 affine +01 certificate')
    chk(gcd(Y-X,Z-Y)==1,'difference Bezout')
    chk(gcd(X,Y,Z)==1,'global primitive triple')
    entries=[]
    for name,a,b in (('XY',X,Y),('XZ',X,Z),('YZ',Y,Z)):
        g,aa,bb=extended_gcd(a,b)
        frac=Fraction(a,b)
        chk(Fraction(1,2)<frac<1,'all three ratios in high interval')
        data['pairs'][name]={'values':[a,b],'gcd':g,'lcm':lcm(a,b),
                             'difference':b-a,'sum':a+b,'product':a*b,
                             'bezout':[aa,bb,g],'primitive_ratio':str(frac),
                             'maps':{str(B):{'T':frac_step((a,b),B,'T'),
                                              'S':frac_step((a,b),B,'S')}
                                     for B in (2,3,4,10,11,17,102)}}
        entries.append(frac)
    chk(entries[0]*entries[2]==entries[1],'projective triangle cocycle')
    # Independent application of the radix maps does NOT preserve multiplicative
    # projective triangle consistency, even if all six images stay high.
    triangle_defects={}
    for base in (4,17):
        def f(q,which):
            if which=='T':
                t=base*q
                return t-t.numerator//t.denominator
            h=base*(1-q)/q
            return 1/(1+(h-h.numerator//h.denominator))
        triangle_defects[str(base)]={}
        for which in ('T','S'):
            a,b,c=(f(q,which) for q in entries)
            defect=(a*c)/b
            triangle_defects[str(base)][which]=str(defect)
            chk(defect!=1,'separate pairwise maps fail triangle coherence')
    chk(all(frac_step((a,b),17,letter)['in_H'] for a,b in ((X,Y),(X,Z),(Y,Z)) for letter in ('T','S')),
        'base17 all six local high branches')
    chk(triangle_defects['17']=={'T':'5173373/10904859','S':'225003/477659'},
        'exact projective map coherence defects base17')
    chk(len(set(q.denominator for q in entries))==3,'denominators all distinct')
    chk(len(set(q.numerator for q in entries))==2,'two share numerator')
    # Exact three-channel generalized CRT.
    L=lcm(*values)
    chk(L==57287140668,'triple lcm')
    chk(X*Y*Z//L==4,'CRT compatibility index')
    for a,b,c in ((2,3,7),(1,1,1),(X-1,Y-1,Z-1),(100,100,100),(2667,1667,1000)):
        if (b-c)%4==0:
            r=crt_general(a,b,c)
            chk((r%X,r%Y,r%Z)==(a%X,b%Y,c%Z),'CRT assembled')
    chk(crt_general(1,2,2)%X==1,'positive CRT test')
    # Compute short GL_3(Z) equivalent coordinates (X,1,333).
    M=((1,0,0),(-3,8,-5),(1,-3,2))
    Minv=((1,0,0),(1,2,5),(1,3,8))
    u=tuple(sum(row[j]*values[j] for j in range(3)) for row in M)
    chk(u==(4777,1,333) and det3(M)==det3(Minv)==1,'unimodular ternary normalization')
    chk(tuple(sum(row[j]*u[j] for j in range(3)) for row in Minv)==values,'unimodular recovery')
    P=X*Y*Z;E1=sum(values);E2=X*Y+X*Z+Y*Z
    moments=[sum(v**n for v in values) for n in range(12)]
    chk(E1==18665 and E2==114312112 and P==229148562672,'symmetric invariants')
    chk((moments[1]**2-moments[2])//2==E2,'power sums P2 recovery')
    chk((moments[3]-E1*moments[2]+E2*moments[1])//3==P,'power sums P3 recovery')
    chk(all(moments[n+3]==E1*moments[n+2]-E2*moments[n+1]+P*moments[n]
            for n in range(9)),'cubic recurrence')
    H=[[moments[i+j] for j in range(3)] for i in range(3)]
    discr=(Y-X)**2*(Z-X)**2*(Z-Y)**2
    chk(det3(H)==discr and discr>0,'rank3 Hankel discriminant')
    data['triplet']={'triangle_defects_of_independent_radix_maps':triangle_defects,
                     'unique_minimal_affine_Bezout':[-3,8,-5],
                     'sum':E1,'pairwise_product_sum':E2,'triple_product':P,
                     'gcd':gcd(*values),'lcm':L,'CRT_image_index':4,
                     'CRT_condition':'rY ≡ rZ (mod 4)',
                     'affine_unit_relation':'-3*X+8*Y-5*Z=1',
                     'unit_coeff_norm_l1':16,
                     'unimodular_matrix':[list(r) for r in M],
                     'unimodular_inverse':[list(r) for r in Minv],
                     'unimodular_coordinates':list(u),
                     'cubic_polynomial_coefficients':[1,-E1,E2,-P],
                     'power_sums_first_8':moments[:8],
                     'hankel_3x3':H,'hankel_determinant':discr,
                     'common_singleton_base_min':1+L,
                     'high_fraction_triangle':[str(q) for q in entries]}
    # Third-order path memory in a UT_4 nilpotent group.
    A,B,C=make_UT4(X,0),make_UT4(Y,1),make_UT4(Z,2)
    I=[[int(i==j) for j in range(4)] for i in range(4)]
    nested=comm(comm(A,B),C)
    chk(nested[0][3]==P,'third-order commutator')
    chk(all(nested[i][j]==I[i][j] for i in range(4) for j in range(4) if (i,j)!=(0,3)),
        'central third-order only')
    w1,w2='XYZYX','YXZXY'
    sig1,sig2=ordered_signatures(w1),ordered_signatures(w2)
    chk(sig1['counts']==sig2['counts'] and sig1['pairs']==sig2['pairs'],'pair-signature collision')
    chk(sig1['XYZ']==1 and sig2['XYZ']==0,'triple-order distinguishes')
    def word_matrix(w):
        out=[row[:] for row in I]
        for c in w:out=matmul(out,{'X':A,'Y':B,'Z':C}[c])
        return out
    H1,H2=word_matrix(w1),word_matrix(w2)
    chk(H1[0][3]-H2[0][3]==P,'triple-order matrix separates')
    chk(all(H1[i][j]==H2[i][j] for i in range(4) for j in range(4) if (i,j)!=(0,3)),
        'all lower-order matrix coords identical')
    data['third_order_memory']={'UT4_nested_commutator_E14':P,
                                'histories':[w1,w2],
                                'histories_signatures':[sig1,sig2],
                                'E14_outputs':[H1[0][3],H2[0][3]],
                                'same_first_second_order':True}
    # The five-state automaton, original letters remain T,S; Z appears only as the
    # second S-channel weight (three sources in a TWO-component output).
    cover_tests=[]
    for m in (2,3,4,5,6,7,8,9,10,11,12,13,16,17,19,25,29,31):
        for label,u0,v0 in (('XY',X,Y),('XZ',X,Z),('YZ',Y,Z)):
            th=solo_cover_theory(u0,v0,m)
            adj,_,_=cover_adjacency(m,((u0,),(v0,)))
            records=graph_scc_period(adj)
            chk(len(records)==th['components'],'solo cover SCC count '+label+str(m))
            chk(all(r['size']==th['size_each'] and r['period']==th['period'] for r in records),
                'solo cover exact components and period '+label+str(m))
            cover_tests.append({'m':m,'weights':label,**th})
        th=joint_cover_theory(m)
        adj,enc,dec=cover_adjacency(m,((X,X),(Y,Z)))
        records=graph_scc_period(adj)
        chk(len(records)==th['components'],'joint SCC count m '+str(m))
        chk(all(r['size']==th['size_each'] and r['period']==th['period'] for r in records),
            'joint period m '+str(m))
        if m==11:
            chk(all(phase(r,s,11)[1]==(2*(r+s))%11 for r in range(11) for s in range(11)),
                'phase m11 simplifies to 2*(r+s)')
        if gcd(m,2*X*(Z-Y))==1:
            chk(th['components']==1 and th['period']==m,'coprime joint period=m')
            for i in range(5):
                for r in range(m):
                    for s in range(m):
                        a=enc(i,(r,s)); before=phase(r,s,m)[1]
                        for v in adj[a]:
                            _,(rr,ss)=dec(v)
                            chk((phase(rr,ss,m)[1]-before)%m==1,'deterministic joint clock')
        cover_tests.append({'m':m,'weights':'JOINT_XY_XZ',**th})
    # Sample where each coordinate alone is aperiodic, but joint has period m.
    for m in (11,13,19):
        chk(solo_cover_theory(X,Y,m)['period']==solo_cover_theory(X,Z,m)['period']==1,
            'two mixing individual covers')
        chk(joint_cover_theory(m)['components']==1 and joint_cover_theory(m)['period']==m,
            'joint cover has full period')
    data['covers']={'base_map_T':list(FIVE_T),'base_map_S':list(FIVE_S),
                    'tested_moduli':sorted({r['m'] for r in cover_tests}),
                    'full_independent_graph_tests':cover_tests,
                    'single_formula':'d=gcd(m,u,2v) SCCs; period=gcd(m,2(v-u))/gcd(m,2(v-u),u)',
                    'joint_SCC_index_formula':
                    'gcd(m*m,m*X,2*m*Y,2*m*Z,2*X*(Z-Y))',
                    'joint_period_formula':
                    'h=gcd(m,2*(Z-Y)), g=gcd(m,2*(m/h)*(Y-X)), period=g/gcd(g,X)',
                    'joint_period_full_m_if':'gcd(m,2*X*(Z-Y))=1',
                    'individual_aperiodic_joint_periodic':[11,13,19],
                    'deterministic_phase_example_mod_11':
                    {'phase':'X^{-1}(rXY-(Y-X)*(Z-Y)^{-1}(rXZ-rXY)) mod 11',
                     'T_increment':1,'S_increment':1}}
    data['tests']={'status':'PASS','pairwise_cases':54,'joint_graph_cases':18,
                   'individual_graph_cases':54,'total_graph_cases':72,
                   'exhaustive_joint_phase_moduli':[m for m in data['covers']['tested_moduli']
                       if gcd(m,2*X*(Z-Y))==1],
                   'limits':'Universal proofs separate from brute finite graph tests.'}
    return data


def main():
    data=audit(); root=Path(__file__).resolve().parent
    (root/'RESULTADOS_TRINARIOS.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print('PASS -- pairwise ratios, triple CRT, GL3 normalization, rank-3 Hankel, UT4 third-order memory,')
    print('72 exact SCC+period graph tests; deterministic phase on all eligible joint states.')
    print('Triple product:',data['triplet']['triple_product'],'GL3:',data['triplet']['unimodular_coordinates'])
    print('Solo vs joint m=11:',[r for r in data['covers']['full_independent_graph_tests'] if r['m']==11])

if __name__=='__main__':main()
