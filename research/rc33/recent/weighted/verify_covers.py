"""Independent exact cover/period checks and local arithmetic controls."""
from collections import Counter,deque
from fractions import Fraction as F
from itertools import product
from math import gcd,lcm
from pathlib import Path
import hashlib,json,platform,time

ROOT=Path(__file__).resolve().parent
T=(1,0,3,2,4)
S=(4,2,1,0,0)
C=(0,0,1,1,1)
PACKET_MODULI=(2,3,4,5,6,7,8,9,10,11,12,17,29,100,1667,3334)
BASES=[('witness',T,S,C,4),
       ('binary',(0,1),(1,0),(0,1),0),
       ('three_state',(0,2,1),(1,0,0),(0,1,1),0),
       ('six_state',(1,2,0,4,3,5),(3,4,5,0,1,2),(0,0,0,1,1,1),5)]


def components_periods(adj):
    """Kosaraju SCCs, followed by exact BFS distance-difference gcds."""
    n=len(adj);rev=[[] for _ in adj]
    for i,js in enumerate(adj):
        for j in js:rev[j].append(i)
    seen=[False]*n;order=[]
    for start in range(n):
        if seen[start]:continue
        seen[start]=True;stack=[(start,0)]
        while stack:
            i,k=stack.pop()
            if k==len(adj[i]):order.append(i);continue
            stack.append((i,k+1));j=adj[i][k]
            if not seen[j]:seen[j]=True;stack.append((j,0))
    ids=[-1]*n;classes=[]
    for start in reversed(order):
        if ids[start]>=0:continue
        ci=len(classes);nodes=[];stack=[start];ids[start]=ci
        while stack:
            i=stack.pop();nodes.append(i)
            for j in rev[i]:
                if ids[j]<0:ids[j]=ci;stack.append(j)
        classes.append(nodes)
    periods=[]
    for ci,nodes in enumerate(classes):
        dist={nodes[0]:0};queue=deque([nodes[0]])
        while queue:
            i=queue.popleft()
            for j in adj[i]:
                if ids[j]==ci and j not in dist:dist[j]=dist[i]+1;queue.append(j)
        d=0
        for i in nodes:
            for j in adj[i]:
                if ids[j]==ci:d=gcd(d,abs(dist[i]+1-dist[j]))
        assert d>0
        periods.append(d)
    return classes,periods,ids


def adj_cover(t,s,m,u,v,strict=False):
    return [[t[i]*m+(r+u)%m,
             s[i]*m+(r+(int(i==3) if strict else v))%m]
            for i in range(len(t)) for r in range(m)]


def check_one(t,s,c,m,u,v):
    adj=adj_cover(t,s,m,u,v)
    classes,periods,ids=components_periods(adj)
    h=gcd(m,u,2*v);g=gcd(m,2*(v-u));d=g//h
    assert len(classes)==h and all(len(x)==len(t)*m//h for x in classes)
    assert all(x==d for x in periods)
    labels=set()
    for nodes in classes:
        vals={(r-v*c[i])%h for i,r in (divmod(x,m) for x in nodes)}
        assert len(vals)==1;labels|=vals
    assert labels==set(range(h))
    inv=pow(u//h,-1,d) if d>1 else 0
    def phase(node):
        i,r=divmod(node,m);k=(r-v*c[i])%h
        return (inv*((r-v*c[i]-k)//h)+c[i])%d
    for i,js in enumerate(adj):
        for j in js:
            assert ids[i]==ids[j]
            assert (phase(j)-phase(i))%d==1%d
    return {'m':m,'u':u,'v':v,'components':h,'period_each':d,'vertices':len(adj)}


def stationary_checks():
    import sympy as sp
    a=F(2,5);b=1-a
    p=sp.zeros(5)
    for i in range(5):p[i,T[i]]+=sp.Rational(a.numerator,a.denominator);p[i,S[i]]+=sp.Rational(b.numerator,b.denominator)
    system=p.T-sp.eye(5);system[4,:]=sp.ones(1,5);rhs=sp.zeros(5,1);rhs[4]=1
    pi=list(system.inv()*rhs);assert sum(pi)==1 and all(x>0 for x in pi)
    tested=[]
    for m,u,v in [(6,2,2),(8,2,1),(9,3,6),(6,0,0),(12,-2,3),(7,4777,6444)]:
        adj=adj_cover(T,S,m,u,v);h=gcd(m,u,2*v)
        for k in range(h):
            mu=[(sp.Rational(h,m)*pi[i] if (r-v*C[i])%h==k else 0)
                for i in range(5) for r in range(m)]
            image=[0]*len(adj)
            for i,(j0,j1) in enumerate(adj):image[j0]+=a*mu[i];image[j1]+=b*mu[i]
            assert image==mu and sum(mu)==1
        tested.append({'m':m,'u':u,'v':v,'stationary_classes':h})
    # A symbolic Fourier eigenpair, valid for every 0<a<1.
    aa=sp.symbols('a');Q=sp.zeros(5)
    for i in range(5):Q[i,T[i]]-=aa;Q[i,S[i]]+=1-aa
    f=sp.Matrix([1,1,-1,-1,-1]);assert sp.simplify(Q*f+f)==sp.zeros(5,1)
    marginal=sp.Matrix([[1-aa,aa],[aa,1-aa]])
    assert marginal*sp.ones(2,1)==sp.ones(2,1)
    assert sp.simplify(marginal*sp.Matrix([1,-1])-(1-2*aa)*sp.Matrix([1,-1]))==sp.zeros(2,1)
    uu,vv,mm=sp.symbols('u v m',integer=True)
    lattice=sp.Matrix([[1,2,0],[uu,2*vv,mm]])
    minor_values=[sp.expand(lattice[:,i:i+1].row_join(lattice[:,j:j+1]).det())
                  for i,j in [(0,1),(0,2),(1,2)]]
    assert minor_values==[2*(vv-uu),mm,2*mm]
    # Left-null certificate for d_e=letter+potential(target)-potential(source).
    cohom=sp.zeros(10,7);mark=sp.zeros(10,1)
    for li,mapping in enumerate([T,S]):
        for i,j in enumerate(mapping):
            row=5*li+i;cohom[row,li]=1
            cohom[row,2+j]+=1;cohom[row,2+i]-=1
            mark[row]=int(li==1 and i==3)
    cert=sp.Matrix([1,0,1,0,-2,-1,1,0,1,-1])
    assert cert.T*cohom==sp.zeros(1,7) and cert.T*mark==sp.ones(1,1)
    return {'a':'2/5','pi':list(map(str,pi)),'class_stationary_tests':tested,
            'symbolic_minus_one_mode_for_packet_weights':True,
            'counter_modulo_two_symbolic_eigenpairs_verified':True,
            'joint_return_lattice_minors':list(map(str,minor_values)),
            'strict_mark_noncohomology':{'edge_order':'T0..T4,S0..S4','left_null_vector':list(map(int,cert)),
                'equation_matrix':[[int(x) for x in row] for row in cohom.tolist()],
                'marked_sum':1,'scope':'all moduli m>=2; group-valued human proof uses three cycles'}}


def arithmetic_controls():
    import sympy as sp
    X,Y=4777,6444;x=F(X,Y)
    assert gcd(X,Y)==1 and F(1,2)<x<1
    def tt(q,b):return b*q-(b*q).numerator//(b*q).denominator
    def ss(q,b):return 1/(1+tt(1/q-1,b))
    assert tt(x,4)==F(1555,1611) and ss(x,4)==F(4777,6668)
    y=x
    for _ in range(3):y=tt(y,4)
    assert y==F(715,1611)<F(1,2)
    assert tt(x,102)==F(659,1074) and ss(x,102)==F(281,448)
    y=x
    for _ in range(5):y=tt(y,102)
    assert y<F(1,2)
    U=sp.Matrix([[X,917],[Y,1237]]);UT=sp.Matrix([[1555,-361],[1611,-374]])
    US=sp.Matrix([[4777,-965],[6668,-1347]])
    MT=sp.Matrix([[4,-2],[0,1]]);MS=sp.Matrix([[1,0],[-4,4]])
    assert U.det()==UT.det()==US.det()==1
    assert UT.inv()*MT*U==sp.Matrix([[4,1],[0,1]])
    assert US.inv()*MS*U==sp.Matrix([[1,1],[0,4]])
    B=88011536665779;states=[F(406,731),F(712,731),F(712,1265),F(1218,1265),F(406,557)]
    for action,mapping in [(tt,T),(ss,S)]:
        for i,q in enumerate(states):assert action(q,B)==states[mapping[i]]
    P=sp.eye(2);i=0
    for letter in 'TSTS':
        q=states[i];p0,q0=q.numerator,q.denominator
        if letter=='T':
            branch=B*p0//q0;M=sp.Matrix([[B,-branch],[0,1]]);i=T[i]
        else:
            branch=B*(q0-p0)//p0;M=sp.Matrix([[1,0],[1-B-branch,B]]);i=S[i]
        P=M*P
    assert i==0 and P*sp.Matrix([406,731])==3*sp.Matrix([406,731])
    assert P.det()==B**4 and sp.trace(P)==3+B**4//3
    transformations={tuple(range(5))};todo=list(transformations)
    while todo:
        f=todo.pop()
        for mapping in [T,S]:
            new=tuple(mapping[x] for x in f)
            if new not in transformations:transformations.add(new);todo.append(new)
    ranks=Counter(len(set(x)) for x in transformations)
    assert len(transformations)==36 and ranks=={2:8,3:18,4:8,5:2}
    recorder_tests=0
    for n in range(11):
        for word in product('TS',repeat=n):
            observations=set()
            for origin in range(5):
                i=origin;r=0
                for letter in word:
                    mark=int(letter=='S' and i==3);r=(-r+mark)%3
                    i=(T if letter=='T' else S)[i]
                assert (i,r) not in observations;observations.add((i,r));recorder_tests+=1
    assert recorder_tests==10235
    anchor=4;strict_gain=0
    for letter in 'STSTSS':
        strict_gain+=int(letter=='S' and anchor==3)
        anchor=(T if letter=='T' else S)[anchor]
    assert anchor==4 and strict_gain==1 and T[4]==4
    return {'X':X,'Y':Y,'product':X*Y,'singleton_first_base':X*Y+1,
            'T4_escape':str(F(715,1611)),'T102_escape':str(y),
            'local_triangular_matrices_verified':True,'witness_edges':10,
            'cycle_trace':str(sp.trace(P)),'semigroup_size':36,
            'ranks':dict(ranks),'recorder_cases':recorder_tests,
            'strict_counter_anchor_signatures':[[1,0],[6,1]],'strict_return_word':'STSTSS'}


if __name__=='__main__':
    config={'python':platform.python_version(),'arithmetic':'exact integer/rational',
            'units':'dimensionless modular counters and rational states',
            'witness_weights':[4777,6444],'witness_base':88011536665779,
            'small_weights_inclusive':[-4,4],'small_moduli_inclusive':[1,24],
            'base_automata':[{'name':n,'T':t,'S':s,'c':c,'loop_vertex':o} for n,t,s,c,o in BASES],
            'packet_moduli':PACKET_MODULI,'strict_edge_moduli':[2,3,4,7,12,1667],
            'probability_for_stationary_controls':'2/5','recorder_max_word_length':10,
            'local_bases':[4,102],
            'local_matrices':{'U0':[[4777,917],[6444,1237]],'UT':[[1555,-361],[1611,-374]],
              'US':[[4777,-965],[6668,-1347]],'MT':[[4,-2],[0,1]],'MS':[[1,0],[-4,4]]},
            'witness_states':[[406,731],[712,731],[712,1265],[1218,1265],[406,557]],
            'cycle_word':'TSTS',
            'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    print(json.dumps(config),flush=True);start=time.monotonic();cases=0;states_visited=0
    for name,t,s,c,o in BASES:
        assert t[o]==o and s[s[o]]==o
        assert all(c[t[i]]==c[i] and c[s[i]]==1-c[i] for i in range(len(t)))
        assert len(components_periods([[t[i],s[i]] for i in range(len(t))])[0])==1
        for u in range(-4,5):
            for v in range(-4,5):
                for m in range(1,25):
                    row=check_one(t,s,c,m,u,v);cases+=1;states_visited+=row['vertices']
    packet=[check_one(T,S,C,m,4777,6444) for m in PACKET_MODULI]
    marginal_cases=0
    for u in range(-4,5):
        for v in range(-4,5):
            for m in range(1,25):
                classes,periods,_=components_periods([[(r+u)%m,(r+v)%m] for r in range(m)])
                h0=gcd(m,u,v);d0=gcd(m,v-u)//h0
                assert len(classes)==h0 and all(x==d0 for x in periods)
                marginal_cases+=1
    marginal_packet=[]
    for m in PACKET_MODULI:
        classes,periods,_=components_periods([[(r+4777)%m,(r+6444)%m] for r in range(m)])
        assert len(classes)==1 and periods==[gcd(m,1667)]
        marginal_packet.append({'m':m,'components':1,'period':periods[0]})
    swapped=[]
    for m in [2,3,100,1667,3334]:
        # Physical letters swapped, while +4777 stays attached to T.
        classes,periods,_=components_periods(adj_cover(S,T,m,4777,6444))
        h=gcd(m,6444,2*4777);d=gcd(m,2*(6444-4777))//h
        assert len(classes)==h and all(x==d for x in periods)
        swapped.append({'m':m,'components':h,'period_each':d})
    original=[]
    for m in [2,3,4,7,12,1667]:
        classes,periods,_=components_periods(adj_cover(T,S,m,0,0,strict=True))
        assert len(classes)==1 and periods==[1]
        original.append({'m':m,'components':1,'period':1})
    result={'config':config,'generalization_finite_checks':{'cases':cases,'vertices_visited':states_visited,
             'all_SCC_period_phase_predictions_pass':True},'packet_covers':packet,
             'large_packet_modulus_without_enumeration':{'m':4777*6444,'h':gcd(4777*6444,4777,2*6444),
              'period':gcd(4777*6444,2*(6444-4777))},'strict_edge_controls':original,
             'stationary_and_fourier':stationary_checks(),'arithmetic_and_recorder':arithmetic_controls(),
             'swapped_physical_letters':swapped,'counter_marginals':{'small_cases':marginal_cases,
              'packet_moduli':marginal_packet,'modulo_two_exact_eigenvalues':['1','1-2*a']},
             'seconds':time.monotonic()-start}
    (ROOT/'EXACT_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2),flush=True)
