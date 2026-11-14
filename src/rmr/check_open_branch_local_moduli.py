from itertools import product
from math import gcd
from collections import deque

CASES={
575722:([2,4,3,0,1],[4,1,2,1,0],'S',3),
575738:([3,2,4,0,1],[4,1,2,1,0],'S',3),
575898:([3,4,0,2,1],[4,1,2,1,0],'S',3),
576298:([3,4,1,0,2],[4,1,2,1,0],'S',3),
119772:([2,4,0,3,1],[3,2,1,0,0],'S',4),
606897:([2,4,0,0,1],[4,3,2,1,0],'T',3),
}
FACTORS={606897:[3],575722:[2,3],575738:[2,3],575898:[2,3],576298:[2,3],119772:[2,3]}

def vp(x,p,k):
    x%=p**k
    if x==0:return k
    v=0
    while x%p==0:x//=p;v+=1
    return v

def components(mapping,letter,strict_letter,strict_source,r):
    adj=[[] for _ in range(5)]
    for i,j in enumerate(mapping):
        e=1 if letter==strict_letter and i==strict_source else 0
        adj[i].append((j,-e)); adj[j].append((i,e))
    cid=[None]*5; ex=[None]*5; comps=[]
    for st in range(5):
        if cid[st] is not None:continue
        c=len(comps); cid[st]=c; ex[st]=0; q=deque([st]); nodes=[]
        while q:
            u=q.popleft();nodes.append(u)
            for v,d in adj[u]:
                ev=ex[u]+d
                if cid[v] is None:cid[v]=c;ex[v]=ev;q.append(v)
                else:assert ex[v]==ev
        mn=min(ex[i] for i in nodes)
        for i in nodes:ex[i]-=mn
        comps.append(nodes)
    return cid,ex,comps

def witness(T,S,sl,ss,r):
    p=r; k=3 if r==2 else 2; mod=p**k
    pc,pe,pcomps=components(S,'S',sl,ss,r)
    qc,qe,qcomps=components(T,'T',sl,ss,r)
    for vals in product(range(mod),repeat=len(pcomps)+len(qcomps)+1):
        pv=vals[:len(pcomps)]; qv=vals[len(pcomps):-1]; B=vals[-1]
        P=[pow(r,pe[i],mod)*pv[pc[i]]%mod for i in range(5)]
        Q=[pow(r,qe[i],mod)*qv[qc[i]]%mod for i in range(5)]
        if any(P[i]%p==0 and Q[i]%p==0 for i in range(5)):continue
        ok=True
        for letter,mapping in [('T',T),('S',S)]:
            for i,j in enumerate(mapping):
                d=r if letter==sl and i==ss else 1
                fibre=Q[i] if letter=='T' else P[i]
                desired=1 if d==r else 0
                if min(vp(B,p,k),vp(fibre,p,k))!=desired:ok=False;break
                if letter=='T': expr=B*P[i]-d*P[j]; need=vp(Q[i],p,k)
                else: expr=B*(Q[i]-P[i])-d*(Q[j]-P[j]); need=vp(P[i],p,k)
                if vp(expr,p,k)<need:ok=False;break
            if not ok:break
        if ok:return vals
    return None

count=0
for code,(T,S,sl,ss) in CASES.items():
    for r in FACTORS[code]:
        w=witness(T,S,sl,ss,r)
        assert w is not None,(code,r)
        print(f'{code} factor={r} local_mod={8 if r==2 else 9} SURVIVES witness={w}')
        count+=1
assert count==11
print('PASS: all 11 oriented open branches survive the natural local mod-8/mod-9 constraint test')
print('BOUNDARY: this is not a realizability result; it only rules out the blanket local shortcut')
