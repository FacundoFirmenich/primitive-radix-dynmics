# Two-chart projective balance and Hilbert-width rigidity

**Status:** PROVED_SYMBOLIC  
**Date:** 2026-11-14

Let Gamma be an element of GL_2(Z), with projective action gamma. Consider the pair

- T_B;
- S_(B,Gamma) = gamma o T_B o gamma^{-1}

on a common positive cone.

Define the primitive linear coordinates

- q_0(v) = e_2^T v;
- q_Gamma(v) = e_2^T Gamma^{-1} v;
- xi_Gamma(v) = q_Gamma(v) / q_0(v).

For every primitive state v,

delta_T(v) = gcd(q_0(v), B),

delta_Gamma(v) = gcd(q_Gamma(v), B).

For an admissible primitive path v_0 -> ... -> v_m with total content product Delta_w,

Delta_w = [q_Gamma(v_0)/q_Gamma(v_m)] * product_T xi_Gamma(v_i)/xi_Gamma(v_(i-1)),

and symmetrically

Delta_w = [q_0(v_0)/q_0(v_m)] * product_S xi_Gamma(v_(i-1))/xi_Gamma(v_i).

On a cycle C the endpoint ratios cancel. If

omega_Gamma(F) = max_{u,v in F} |log xi_Gamma(u) - log xi_Gamma(v)|,

then

log R_C <= omega_Gamma(F) * min(m_T, m_Gamma).

Consequently, if ell(B) is the least prime divisor of B, every finite strongly connected nonpermutation component of cardinality n satisfies

ell(B) <= exp(omega_Gamma(F) * floor(n/2)).

For Gamma = [[0,1],[1,1]], q_Gamma(p,q)=p and xi_Gamma=p/q. Hence a component in (1/2,1) has exp(omega_Gamma(F))<2, recovering the original high-cycle budget.
