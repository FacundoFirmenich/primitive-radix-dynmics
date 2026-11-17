# Exact trace-observation transfer records

17 November2026 · RC3.3. Compact proof/certificate register, not the complete private manuscript. XI uses right products. Our chronological RGΦ word has N(w)=M_last ... M_first and probes tr(Q_suffix N).

## RTB

At a primitive rational v, every based loop satisfies N(w)v=Delta(w)v. A common unimodular basis with first column v gives

$$U^{-1}N(w)U=\begin{pmatrix}\Delta(w)&\beta(w)\\0&B^{|w|}/\Delta(w)\end{pmatrix}.$$

The two diagonal characters multiply, so the loop trace Hankel has rank at most2. Its pairings are blind to beta.

At x0=p/q=406/731 in the known family, TT and SS are ordinary returns:

$$N_{TT}=\begin{pmatrix}B^2&(1-B^2)p/q\\0&1\end{pmatrix},\quad
N_{SS}=\begin{pmatrix}1&0\\(1-B^2)q/p&B^2\end{pmatrix}.$$

They are distinct but have the same diagonals(1,B^2) in that common basis. Every closed suffix gives equal traces. The Hankel minor on{empty,TT} is(B^2-1)^2, proving rank exactly2. An open T probe separates them:

$$\operatorname{tr}(M_TN_{TT})-\operatorname{tr}(M_TN_{SS})=(B^2-1)(712-406)/406\ne0.$$

A lifted-matrix oracle or retained causal matrix is essential. The terminal rational alone does not supply these traces; once histories merge to one rational, future state observations still cannot recover them.

## RTP

For vertices0..3, T exchanges p/q with p'/q, p!=p'. Put u=B-1,

$$A=\begin{pmatrix}B&-k\\0&1\end{pmatrix},\ C=\begin{pmatrix}1&0\\h&B\end{pmatrix},\
D=N(TT)=\begin{pmatrix}B^2&-(Bk+\ell)\\0&1\end{pmatrix}.$$

Here k=(Bp-p')/q, ell=(Bp'-p)/q, h=1-B-b_S<0. Row-vectorizing I,A,C,D gives determinant h(B-1)(k-ell), nonzero since k-ell=(B+1)(p-p')/q. Therefore empty,T,S,TT span all2x2 matrices.

For N=(a,b;c,d), denote their traces by z,t,s,w. The inverse is

$$c=\frac{w-(B+1)t+Bz}{k-\ell},\
a=\frac{t-z+kc}{B-1},\
d=z-a,\quad b=\frac{s-a-Bd}{h}.$$

At vertex4, T fixes406/557 and S sends it to406/731. Use empty,T,S,TS; the TS lift is CA. Its basis determinant is kh(u^2+kh), where

$$k=up/q,\quad h=(731-Bq)/p,\quad u^2+kh=u(731-q)/q\ne0.$$

The inverse now is

$$d=\frac{t+Bs-Bz-w}{u^2+kh},\
a=z-d,\quad c=\frac{Ba+d-t}{k},\quad b=\frac{s-a-Bd}{h}.$$

All suffixes are admissible because the witness component is closed. The identities prove the whole CRT family; the replay also checks its first three bases. Four is minimal for linear recovery of arbitrary2x2 matrices, not necessarily for restricted histories. Four growing-precision integer registers are not four bits. An active trace oracle still requires equivalent starting preparations; causal accumulation is a distinct access model.

## RTH

Let tau_w be the transformation of the five-state witness and f(w)=#Fix(tau_w), the trace of its5x5 action matrix. The complete generated monoid has36 elements, so its finite36x36 trace table represents every row/column of the infinite word Hankel.

For basis words empty,T,S,TS,ST,SS,TST,TSS,STS,SST,STSS, the11x11 minor K has determinant-576. The certificate supplies adj(K) and checks all1296 integer identities

$$\det(K)H=H[:,I]\operatorname{adj}(K)H[I,:].$$

Consequently rank(H)=11. There are30 distinct rows: two four-element classes collapse under all future fixed-point trace queries. For example STSTS and STSTST act by(2,2,0,0,0) and(3,3,1,1,1), but their complete future trace rows agree. The action matrices themselves span dimension17. These dimensions concern distinct tasks; the source's external rank4/rank9 does not carry over by replacing the generators' names.

## Source replay and boundaries

The independent exact ECMAScript implementation checks2,097,151 binary histories through length20 and13,483 distinct traces there;265,720 ternary histories through length11, with92,475 matrices and6,636 trace-invisible words at length11; the16-state integer annihilator S(S-2I)(S-I)^4=0 and65 counts;4,777 Apéry residues, every DP point through the declared cutoff,8664 complementary double gaps and4096 generalized CRT inversions. Frobenius2445719 and genus1231524 are reproduced.

Nine source proof/code/result hashes match their published manifests. Original Python suites and browser laboratories were not rerun. The8888 experiment does not overwrite7444 data. No global existence row, uniqueness or least-base question closes: observability has not bounded the unbounded completion index. Private manuscript integration is pending while the workspace is unavailable.
