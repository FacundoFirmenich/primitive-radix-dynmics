# Exact decidability at fixed base and cardinality

**2026-11-11 · PROVED_SYMBOLIC · Claim C015**

For integers B >= 2 and n >= 1, set L = lcm(B^k-1 : 1 <= k <= n) and N = B^(n-1) L.

**Theorem.** If F is a nonempty finite set of reduced rational states in (1/2,1), |F| <= n, closed under both T_B(x) = {Bx} and S_B = Phi T_B Phi^{-1} with Phi(x)=1/(1+x), then each p/q in F satisfies p | N and q | N. Consequently all closed strongly connected components of size <= n are effectively enumerable by exact arithmetic.

**Proof.** The T-orbit of p/q is eventually periodic in at most n states: after r <= n-1 steps it enters a cycle of period k <= n. A periodic reduced denominator divides B^k-1. The r preceding denominator reductions multiply to a divisor of B^r, so q divides B^r(B^k-1), hence N. In the conjugate coordinate Phi^{-1}(p/q)=(q-p)/p, the reduced denominator is p and S becomes T, proving p | N. Thus all possible states lie in the finite set of reduced p/q in (1/2,1) with p,q divisors of N. Evaluate both generators on that set, remove states with outgoing edges to excluded states until stable, and extract terminal strongly connected components. A genuinely closed component cannot be removed. This is a finite exact decision procedure.

**Boundary.** The bound does not imply efficient complexity or the existence of nonpermutation components for every base. The finite-base census is computational evidence, not a proof of uniform arithmetic classification.
