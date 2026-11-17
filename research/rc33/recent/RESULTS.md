# Recent integrated results · RC3.3 · 17 November 2026

This public evidence register documents the added value of five recent research modules. It is a concise code-and-certificate guide, not a publication of the embargoed manuscripts. The private main, supplementary and companion documents are synchronized by the provenance hashes in `metadata/CANONICAL_ALIGNMENT.json`.

Run `make recent-verify` for the current replay and `make reproduce` for the full public pipeline. Mathematical statements retain their hypotheses; a finite test is not promoted to an all-height proof.

## R17T

**Transitive-generator rigidity and both CRT families at every cardinality.** If one generator is a transitive permutation on a finite high component, both generators are permutations. The separate numerator/denominator monotonicity proves this before any enumeration. Both transitive CRT constructions exist at every cardinality n ≥ 2, using m = 3^n − 1 and coordinates m − 3^j or 2m − 3^j. The hypothesis of transitivity is essential. See [the public proof](../../../proofs/TRANSITIVE_GENERATOR_RIGIDITY.md).

Scope: All-high sector; transitivity is an explicit hypothesis.

Evidence: [`synergies/`](synergies/), [current execution receipt](../../../outputs/reports/recent/RUN_MANIFEST.json), [immutable source manifest](SOURCE_MANIFEST.json). Status: `PROVED_SYMBOLIC`.

## R17I

**Connected cycle-incidence description in the permutation sector.** For two permutations, form the bipartite incidence graph between their cycles, one edge per state. Its connectedness is equivalent to strong connectivity of the generated action: inverse permutation steps can be replaced by positive powers. Arithmetic realization remains an additional constraint.

Scope: Both generators are permutations; arithmetic consistency is retained.

Evidence: [`synergies/`](synergies/), [current execution receipt](../../../outputs/reports/recent/RUN_MANIFEST.json), [immutable source manifest](SOURCE_MANIFEST.json). Status: `PROVED_SYMBOLIC`.

## R17O

**Bounded opposite cofactor pairs give effective finite height.** Write the four square conditions as A | D² − α²Q², C | D² − β²Q², D | C² − γ²A², Q | C² − δ²A². The coefficient tuples are (r,1,r,1) for 119772 and (1,3,1,3) for 606897. For signed cofactor ratios k_A/h_A = (D−α'Q)/A and k_C/h_C = (D−β'Q)/C, put N_D = (β'k_Ah_C)²−(γ'α'k_Ch_A)² and N_Q = (k_Ah_C)²−(δ'k_Ch_A)². Then D | 4N_D and Q | 4N_Q; at least one constant is nonzero and H ≤ 16 max(|N_D|,|N_Q|). The opposite pair gives the analogous A,C bound. Opposite-coordinate gcd bounds by two justify the factor four. Bounding either opposite pair of denominators therefore makes the problem finite, but no uniform bound is supplied. Four algebraic cancellations are replayed in `replay.py`.

Scope: Either signed pair bounded; no uniform pair bound is asserted.

Evidence: [`sine/`](sine/), [current execution receipt](../../../outputs/reports/recent/RUN_MANIFEST.json), [immutable source manifest](SOURCE_MANIFEST.json). Status: `PROVED_SYMBOLIC`.

## R17R

**Factor-three reflection preserves height and permutes cofactors.** In the factor-three completion D = 3E − A, reflection transports the common arithmetic locus, height and cofactor data between the stated chambers. The conversion is state-side arithmetic; it does not identify the oriented dynamics. Common coordinates (A_c,C_c,D_c,Q_c,E) = (Q_native,D_native,C_native,A_native,E) are retained explicitly.

Scope: Completion D=3E-A; native/common coordinates explicitly transported.

Evidence: [`sine/`](sine/), [current execution receipt](../../../outputs/reports/recent/RUN_MANIFEST.json), [immutable source manifest](SOURCE_MANIFEST.json). Status: `PROVED_SYMBOLIC`.

## R17Q

**Degree-four ideal intersection is Q ACDQ for every integer r>=2.** For every integer r ≥ 2, the degree-four simultaneous cycle-ideal construction gives only scalar multiples of ACDQ. The final compatibility determinant is 1 − r⁴, which never vanishes in that range. Its quotient is constant, so this particular invariant cannot separate the remaining cores. Checks at selected higher degrees are finite diagnostics, not a proof for all degrees. See `chamber/ALGEBRA_RESULTS.json`.

Scope: Only the stated homogeneous degree-four ansatz; higher ideal powers are finite checks.

Evidence: [`chamber/`](chamber/), [current execution receipt](../../../outputs/reports/recent/RUN_MANIFEST.json), [immutable source manifest](SOURCE_MANIFEST.json). Status: `PROVED_SYMBOLIC`.

## R17B

**Positive boundary coordinates and level height bound for 606897/3.** For 606897/3 in common coordinates, t=A−E, u=A−Q, v=2Q−C, z=C−D. The high chamber is t,u,v,z>0, 2u+v+z=3t and A>6t. Reduction of the first square condition gives A | t²−u², and u=t repeats states. Thus 6t<A≤|t²−u²|<5t²/4: each t-level is finite. The native gap is Q_native−E, not A_native−E. Code: `chamber/boundary_census.py`.

Scope: Common coordinates; native gap equals Q-E.

Evidence: [`chamber/`](chamber/), [current execution receipt](../../../outputs/reports/recent/RUN_MANIFEST.json), [immutable source manifest](SOURCE_MANIFEST.json). Status: `PROVED_SYMBOLIC`.

## R17C

**No 606897/3 realization with boundary gap at most 5000.** The saved complete run through t = 5000 reports 24,470,981 primitive candidates, 157 satisfying three square conditions, and zero satisfying all four. Its exclusion is uniform over bases within this stratum. The current replay checks its code hash, an independent finite prefix, modular roots through 2500 and all 157 terminal cores. It does not claim a new complete T5000 execution. `make recent-full-census` repeats that expensive run separately.

Scope: All bases in 1<=t<=5000; prior completed exhaustive run pinned, current terminal/direct controls separate.

Evidence: [`chamber/`](chamber/), [current execution receipt](../../../outputs/reports/recent/RUN_MANIFEST.json), [immutable source manifest](SOURCE_MANIFEST.json). Status: `EXACT_CERTIFICATE`.

## R17A

**Finite-abelian record components and periods classified by K and N.** For the specified five-state automaton and finite abelian group G, assign input increments u,v to T,S. Its binary quotient obeys c(Ti)=c(i), c(Si)=1−c(i), and a common anchor has a T-loop and an S²-loop. Let K=⟨u,2v⟩ and N=⟨2(v−u)⟩. There are |G|/|K| strong components, each with |F||K| states and period |K|/|N|. The component label is r−vc(i)+K; the phase r−(v−u)c(i)+N advances by u for either action.

Scope: Strongly connected finite automaton, binary quotient, common T/SS anchor.

Evidence: [`triadic/`](triadic/), [current execution receipt](../../../outputs/reports/recent/RUN_MANIFEST.json), [immutable source manifest](SOURCE_MANIFEST.json). Status: `PROVED_SYMBOLIC_PLUS_CERTIFICATE`.

## R17S

**Scalar all-integer weights and counter-marginal classification.** For arbitrary integer weights u,v modulo m, set h=gcd(m,u,2v), g=gcd(m,2(v−u)). The full automaton cover has h components, each of period g/h. The counter process alone has h₀=gcd(m,u,v) components and period gcd(m,v−u)/h₀. These are different observation contracts; coprime weights are not assumed.

Scope: Negative, equal and zero weights included; variables observed are specified.

Evidence: [`weighted/`](weighted/), [current execution receipt](../../../outputs/reports/recent/RUN_MANIFEST.json), [immutable source manifest](SOURCE_MANIFEST.json). Status: `PROVED_SYMBOLIC`.

## R17F

**Exact character criterion and peripheral spectrum for abelian records.** For 0<a<1 and a character χ of G, the twisted transition matrix is aχ(u)T+(1−a)χ(v)S. Its spectral radius is one precisely when χ(2(v−u))=1. A diagonal gauge using χ(−(v−u)c(i)) exhibits the peripheral phase. The condition connects the period subgroup with the Fourier obstruction; it is not a universal mixing assertion for every record.

Scope: Independent letters with 0<a<1; fixed finite group.

Evidence: [`triadic/`](triadic/), [current execution receipt](../../../outputs/reports/recent/RUN_MANIFEST.json), [immutable source manifest](SOURCE_MANIFEST.json). Status: `PROVED_SYMBOLIC`.

## R17J

**Coupled covers and the least modulus eleven for the stated mixing contrast.** For u=(4777,4777), v=(6444,7444) modulo m in both coordinates, the number of components is I(m)=gcd(m,9554000); each has period m·gcd(m,2)/I(m). At m=11 each scalar automaton cover has 55 states and period one; their joint 605-state cover is irreducible with period eleven. Its phase is θ=2(r₁+r₂) mod 11. Eleven is the least modulus for the specified contrast. Both channels share the same input letters and are not statistically independent. Counter-only component and period formulas differ.

Scope: Channels share random input letters; phase already visible in joint counters.

Evidence: [`triadic/`](triadic/), [current execution receipt](../../../outputs/reports/recent/RUN_MANIFEST.json), [immutable source manifest](SOURCE_MANIFEST.json). Status: `PROVED_SYMBOLIC_PLUS_CERTIFICATE`.

## R17N

**Strict witness content cannot be made constant by letter through vertex gauge.** The witness's strict-content record is state dependent. A positive vertex rescaling cannot turn it into a constant increment for each letter: the anchor T-loop forces T-weight one, its S²-loop forces S-weight one, while the strict TSTS cycle has content three. Cycle products are invariant under such gauges.

Scope: Positive representative scalings in main; arbitrary group labels in companion.

Evidence: [`weighted/`](weighted/), [current execution receipt](../../../outputs/reports/recent/RUN_MANIFEST.json), [immutable source manifest](SOURCE_MANIFEST.json). Status: `PROVED_SYMBOLIC`.

## R17G

**Nonabelian strict-marker gauge obstruction.** The same loop obstruction extends to a nonabelian strict-marker group record. A T-loop forces U=1 and the S²-loop forces V²=1; then the strict TSTS marker would be trivial, contradicting the prescribed nontrivial marker. This concerns vertex gauges and constant letter increments under the stated contract.

Scope: Three explicit cycles; does not rule out arbitrary postprocessing observers.

Evidence: [`triadic/`](triadic/), [current execution receipt](../../../outputs/reports/recent/RUN_MANIFEST.json), [immutable source manifest](SOURCE_MANIFEST.json). Status: `PROVED_SYMBOLIC`.

## R17P

**Exact sine-pi conjugacy and borrow threshold.** Let θ_k={10^(2k+5)π}, z_k=1/(1+θ_k), P_k=10^(k+3)sin(π10^(−k−3)), and τ_k=10^(2k+5)(π−P_k). Then z_(k+1)=S_100(z_k); the borrow decision is θ_k<τ_k, with 1/2<τ_k<π³/60<1. Rational interval certificates decide the supplied finite cases; floating-point equality is not used as proof. See `sine/input/verificar_puente.py`.

Scope: All k>=0; exact irrational phase, no normality assumption.

Evidence: [`sine/`](sine/), [current execution receipt](../../../outputs/reports/recent/RUN_MANIFEST.json), [immutable source manifest](SOURCE_MANIFEST.json). Status: `PROVED_SYMBOLIC`.

## R17D

**Nested sine thresholds, cylinder refinement and coboundary transport.** The specified sine thresholds induce nested observation fibres. The angles .01, .018, .02 and .024 use their common 2n+7 decimal scale; .03 has a different 2n+6 scale and must be transported before comparison. The stated domain is m>2. Refinement and coboundary transport do not imply π-normality or an exhaustive description of its orbit.

Scope: Declared angle domain m>2; fifth family has a different scale.

Evidence: [`synergies/`](synergies/), [current execution receipt](../../../outputs/reports/recent/RUN_MANIFEST.json), [immutable source manifest](SOURCE_MANIFEST.json). Status: `PROVED_SYMBOLIC`.

## R17H

**Base 100 has no nonpermutation high component of size at most five.** The certified size-at-most-five arithmetic catalogue excludes a nonpermutation high component in base 100: the required prime support is unavailable (99 has two distinct prime factors and 101 has one), and 3 does not divide 100. No claim is made at arbitrary cardinality.

Scope: Uses certified residual classification and prime support; not arbitrary cardinality.

Evidence: [`sine/`](sine/), [current execution receipt](../../../outputs/reports/recent/RUN_MANIFEST.json), [immutable source manifest](SOURCE_MANIFEST.json). Status: `PROVED_SYMBOLIC`.

## R17L

**FST normalization chains, exact multiplicities and maximal fibre.** In the stated finite suffix model, m=10^ℓ and K_s=8m−9s=7^aH_s with 7∤H_s. Equality of normalized H-values gives the exact finite chains s↦343s−304m within the admitted suffix interval. The maximal fibre size is 1+⌊log_343(m)⌋. Source identifiers and signed values are retained; normalization is not source identity.

Scope: Defined signed integers K=8m-9s; earlier FST07 motivation is not a proof premise.

Evidence: [`triadic/`](triadic/), [current execution receipt](../../../outputs/reports/recent/RUN_MANIFEST.json), [immutable source manifest](SOURCE_MANIFEST.json). Status: `PROVED_SYMBOLIC_PLUS_CERTIFICATE`.

## R17M

**Optimal fixed additional record j=floor(v7(K)/3) given exact H.** Given the exact normalized H, the additional integer j=⌊a/3⌋ is an optimal fixed finite record on the admitted fibre domain. H modulo nine determines a modulo three, and j resolves the remaining ambiguity. The minimum alphabet size is the maximum fibre size. Optimality is relative to this exact-H access contract.

Scope: Endpoint exact-H recovery; does not replace online automaton recorder contract.

Evidence: [`triadic/`](triadic/), [current execution receipt](../../../outputs/reports/recent/RUN_MANIFEST.json), [immutable source manifest](SOURCE_MANIFEST.json). Status: `PROVED_SYMBOLIC_PLUS_CERTIFICATE`.

## R17K

**FST finite precision threshold with full valuation.** When the full valuation a is supplied and the remaining observation is the unit modulo 7^k, exact recovery holds if and only if 7^k≥10^ℓ for k≥1 in the stated model. This finite-precision contract differs from access to the entire integer H.

Scope: k>=1; units modulo 7^k and all fixed-ell suffixes.

Evidence: [`triadic/`](triadic/), [current execution receipt](../../../outputs/reports/recent/RUN_MANIFEST.json), [immutable source manifest](SOURCE_MANIFEST.json). Status: `PROVED_SYMBOLIC`.

## R17E

**FST geometric fibre law, uniform-prior entropy and ending-02 threshold.** Under the explicitly uniform prior on suffixes, fibre depths have the stated truncated geometric law; the limiting conditional entropy is approximately 0.0058373324 bits. In the stated ending-02 subfamily, the first collision occurs at ℓ=13 with P=7^12=13,841,287,201. These are properties of the declared finite family, not universal information constants. No unattached historical FST program is claimed to have been replayed.

Scope: Prior explicitly uniform; 02 collisions begin at ell=13; no physical information law.

Evidence: [`triadic/`](triadic/), [current execution receipt](../../../outputs/reports/recent/RUN_MANIFEST.json), [immutable source manifest](SOURCE_MANIFEST.json). Status: `PROVED_SYMBOLIC`.

## R17W

**Weighted Parikh representation and order-two/order-three observation collision.** The whole-input operators I+4777E₁₂, I+6444E₂₃ and I+7444E₃₄ give the UT₄ nested commutator I+229148562672E₁₄. The words XYZYX and YXZXY have identical letter and ordered-pair counts but different XYZ-subsequence counts. This is an explicit order-two/order-three observation collision in a weighted Parikh representation; it does not assume an internal dynamics inside the inputs.

Scope: Standard word-combinatorics framework; observer hierarchy is cumulative.

Evidence: [`triadic/`](triadic/), [current execution receipt](../../../outputs/reports/recent/RUN_MANIFEST.json), [immutable source manifest](SOURCE_MANIFEST.json). Status: `PROVED_SYMBOLIC`.

## R17U

**Affine Bezout optimality, unimodular recoding, CRT and rank-three moments.** For (X,Y,Z)=(4777,6444,7444), −3X+8Y−5Z=1 with coefficient sum zero and minimal ℓ¹ norm sixteen under that affine constraint. The associated integer matrix has determinant one and maps the ordered triple reversibly to (4777,1,333). Pairwise gcds are 1,1,4; compatible CRT residues number lcm(X,Y,Z)=57,287,140,668. Symmetric power moments have rank three. These are arithmetic relations and reversible recodings, not universal compression or source decomposition.

Scope: Evaluated labelled inputs; no universal compression or new arithmetic realization.

Evidence: [`triadic/`](triadic/), [current execution receipt](../../../outputs/reports/recent/RUN_MANIFEST.json), [immutable source manifest](SOURCE_MANIFEST.json). Status: `PROVED_SYMBOLIC`.

## R17Z

**The three primitive input ratios never form a three-state high component.** The primitive ratios 4777/6444, 4777/7444 and 1611/1861 all lie in the high interval, but cannot form a strongly connected closed three-state component for any base. The sharp rigidity theorem would make both maps permutations; the three distinct denominator fibres then force T to fix each, and numerator fibres isolate the third state. Separately fixed singletons remain possible at their own CRT bases.

Scope: Distinct denominator fibres and the isolated unique numerator.

Evidence: [`triadic/`](triadic/), [current execution receipt](../../../outputs/reports/recent/RUN_MANIFEST.json), [immutable source manifest](SOURCE_MANIFEST.json). Status: `PROVED_SYMBOLIC`.

## R17V

**Integrated continuation certificate contracts.** The imported 31-file code/data subset is pinned byte-for-byte by SOURCE_MANIFEST.json. New runs use temporary copies and preserve those checkpoints. RUN_MANIFEST.json records actual computations and expressly distinguishes saved exhaustive evidence, current independent implementations and same-source replay. No new global existence exclusion, independent external peer review or new DOI archival event is asserted.

Scope: Frozen source checkpoints, source and fresh replay domains separated.

Evidence: [`triadic/`](triadic/), [current execution receipt](../../../outputs/reports/recent/RUN_MANIFEST.json), [immutable source manifest](SOURCE_MANIFEST.json). Status: `EXACT_CERTIFICATE`.

## Mathematical context

Finite-group extensions and their gauges are established constructions; the specific contribution here is the exact subgroup, phase and component calculation for this action graph and these observation contracts. Weighted Parikh matrices likewise belong to established word-combinatorics frameworks. No priority over those general theories is asserted. Context references are recorded in `data/literature.csv`.
