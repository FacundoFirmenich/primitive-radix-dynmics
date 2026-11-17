# Exact FST16 continuation records

17 November2026 · RC3.3. The input is a research communication in the current chat; original FST15/16 PDF, ZIP, Python engine and atlas were not supplied. This record separates internal proofs from independent finite reconstruction, not external peer review.

## F16I

For admissible label h, C=K0 is8mod9, hence a3-adic unit. At fixed length ell, v_j=(8*10^ell-C343^j)/9 has v3(v_j-v_k)=v3(j-k): exponent lifting gives v3(343^d-1)=2+v3(d) and division by9 removes exactly two factors. Thus each residual map j mod3^t -> v_j mod3^t is a permutation. Compatible inverse limits give a bijective isometry of Z3. Its inverse is log((8*10^ell-9v)/C)/log343; the ratio belongs to1+9Z3. Word representatives retain their original bounded index window.

Value modulo3^t requires key modulo3^(t+2). For general erased prime p!=3, q=p^ord9(p), s=v3(q-1)>=2, the valuation difference is s-2+v3(j-k). Only s=2 gives an isometry onto all Z3. For larger s the image is one coset of3^(s-2)Z3. Primes109 and163 give shifts1 and2; the audit checks both as counterexamples to an unrestricted prime-generalization.

## F16C

A literal decimal prefix cuts the monotone values into one index interval[L,U), computed by exact binary search with the sign of C respected. The preserved terminal inverse yields a class a modulo T, with only2/5 prime factors. The value residue modulo3^t yields one class b modulo3^t by exactly three candidate tests per lift. Coprime CRT gives a single class a* modulo M=T3^t. Put F=L+((a*-L)mod M). Count=max(0,1+floor((U-1-F)/M)); selection gives F+kM. At width W>0, maximal multiplicity is ceil(W/M), injectivity holds exactly when M>=W, and the optimum fixed auxiliary code has ceil(log2(ceil(W/M))) bits. These are exact information bounds conditional on the declared observations, not empirical entropies or total code costs.

With declared h=C=8,ell10000,prefix/suffix88 and selected rank3000, counts are3944,986,110,2,1; the last three value moduli are9,729,2187. The final class is3000mod8748. There are21 ternary candidate tests and five separately counted suffix candidate congruences. Without the suffix,3^8=6561 resolves the prefix interval uniformly. This reconstructs every displayed source count while explicitly supplying omitted parameters.

## F16D

For a complete decimal DFA, compute some(q,d) and all(q,d) by Boolean disjunction/conjunction over all ten next digits. Their initial values are acceptance at d=0. In each prefix cylinder, intersect its contiguous index window with the joint CRT progression. Discard zero/impossible nodes; add universally accepted nodes wholesale; evaluate a singleton directly; otherwise partition into the ten disjoint children. Induction on remaining length proves correctness. An iterative stack avoids a bounded Python-recursion assumption. No universal sublinear runtime is claimed. The starts-with88 DFA at length10000 accepts3944 of3945 representatives with21 visited nodes.

The audit compares15840 valuation pairs,10920 residue values,1620 lifted inversions,324 generalized-prime pairs,1050 prefix windows,15450 joint queries,6240 direct DFA comparisons and6612 sharp-width instances. The10000-digit words are not enumerated. The current native runner records limits, input hashes and outputs; original FST15/16 suites are absent. These word-observation results do not bound the unbounded completion index of rational carriers.
