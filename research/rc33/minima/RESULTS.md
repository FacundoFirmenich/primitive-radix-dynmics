# Uniqueness and minimum-base fronts · 20 November 2026

Facundo Firmenich · RGΦ RC3.3.

## MIN1

At fixed base B put K0=(1/2,1) and
K(d+1)=H intersect T_B^-1(Kd) intersect S_B^-1(Kd). Every high closed set lies
in every Kd. These are finite unions of rational open intervals. Keep touching
endpoints excluded. Form the two possible interval-transition graphs and prune
vertices with no remaining successor under either letter.

If the graph core is empty, no high closed component exists. If one letter is
deterministic on that core, it fixes an eventually periodic digit itinerary.
Expansion in the T-chart, or the conjugate S-chart, gives at most one point per
interval. Compute those rational points, retain their common closed subset,
and extract terminal strongly connected components. This classifies every high
component at that base, without a prior cardinality or height bound.

[Proof](certificate/FINITE_TRAP_PROOF_ES.md). The criterion is sufficient; an
inconclusive resource-limited attempt provides no exclusion.

## MIN2

The fixed certificates cover every base 2 through 53. A separate checker
reconstructs each interval level from all cut points, checks endpoints, derives
the rational points anew and recomputes closure and components. It finds 23
singleton and two two-state closed strong components, all permutational. They
agree with the earlier cardinality-five census; the new proof establishes that
larger components are absent too.

Therefore any base admitting a nonpermutation high component is at least 54,
at every cardinality. This is a lower bound, not a global minimum theorem.

## MIN3

Let B*=88011536665779 and N=(B*-1)^2-1. In the five classified nonpermutation
chambers, lambda L divides B^2-1, L>H^4/32, and MIN4 gives lambda>=13.
Hence 13H^4<32N. Chamber inequalities also give E^4/L<81/16, so
16 lambda^5<81N. Exact integer roots yield

**B<B* implies H<=11750908 and13<=lambda<=523225.**

This finite necessary search window can support a five-state minimum proof
without classifying carriers at larger bases. It has not been exhausted.

## MIN4

The fixed prefix covers indices 1 through 12 at every coordinate height:
1,151 blocks and 117,093,402 integral-level pairs, with no primitive candidate
of the necessary system. Indices sharing the strict prime are impossible
because lambda divides E. Every remaining plane and level box is recorded.

The omitted kappa=lambda|j| planes have F=E, where F=Q-j(C-A).
Only the normal j=1 chambers permit this ratio. For factor two,
D=A+2Q-2C>2A yields 2A<2Q-C<3A, whereas the square condition at A
and gcd(A,4C)=1 require A to divide 2Q-C, a contradiction. For factor three,
D=2A+3Q-3C, the condition at A and gcd(A,C)|2 force
2(2Q-C)/A to be an integer. The chamber gives 3<2(2Q-C)/A<5, hence
C=2Q-2A. The condition at Q then gives Q|3, incompatible with its unit
condition at 3 and Q>4A/3. Thus no omitted plane contains an admissible carrier.

The exact discriminant factorization Delta=W^2 Z supplies a sound modular
square filter. C++/GMP checks integer square roots; Python reconstructs rational
roots and verifies the chamber, primitive coordinates, index, CRT and ten edges.
The W=0 case is retained. Tests include 44,100 signed-coefficient pairs, both
known-carrier controls, checkpoint equality, and full rational-reference
comparisons at indices 3 and 5. [Proof](certificate/INDEX_PREFIX_PROOF_ES.md).

## Reproduction and live research

Run `make minima-verify` for manifest/coverage checks and fresh controls.
`make minima-full-verify` replays all 117,093,402 pairs and all 52 cut-point
certificates from scratch in an isolated directory. Requirements: Python,
SymPy, C++17 and GMP development headers/libraries. Actual versions and compiler
flags are recorded in `certificate/BUILD_ENVIRONMENT.json`.

Ongoing index search preserves two objectives: any distinct carrier can refute
uniqueness, while a lower least CRT base can improve the five-state candidate.
The cardinality supervisor extends checked bases and fairly retries deferred
ones; resource limits are never exclusions. Live jobs and mutable databases are
separate from these fixed certificates.

The oriented classification remains 37 excluded / 2 realized-containing / 1
existence-open. Global uniqueness, the five-state minimum and the arbitrary-
cardinality minimum remain open. Full manuscripts remain private; the original
DOI/tag is unchanged.
