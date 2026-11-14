# Claim-to-evidence traceability

| ID | Status | Claim | Primary evidence | Dependencies |
|---|---|---|---|---|
| C001 | `DEFINITION` | Primitive projective radix–Möbius system is defined by T_B, its Möbius-conjugate S_B, branch matrices and primitive normalization. | `certificates/ARITHMETIC_PROGRESSION.json` | — |
| C002 | `PROVED_SYMBOLIC` | The rational dynamics and primitive projective lift are exactly conjugate under p/q <- (p,q). | `src/rmr/core.py` | depends_on:C001 |
| C003 | `PROVED_SYMBOLIC` | Local content defects are δ_T=gcd(q,B) and δ_S=gcd(p,B) for a reduced state p/q. | `src/rmr/core.py` | depends_on:C002 |
| C004 | `PROVED_SYMBOLIC` | For an admissible word, the branch-matrix product equals the product of local defects times the terminal primitive vector. | `src/rmr/verify.py` | depends_on:C002<br>depends_on:C003 |
| C005 | `PROVED_SYMBOLIC` | Every rational periodic branch word satisfies the cycle spectral identity and square-discriminant condition. | `certificates/COUNTERFAMILY_CYCLE_CERTIFICATE.json` | depends_on:C004 |
| C006 | `PROVED_SYMBOLIC` | The high-cycle reduction budget bounds the product of defects by the numerical spread of the cycle. | `proofs/CYCLE_REDUCTION_BUDGET.md` | depends_on:C003<br>special_case:C021 |
| C007 | `PROVED_SYMBOLIC` | Every finite high closed SCC of directed diameter at most two is permutational under both generators. | `proofs/DIAMETER_TWO_RIGIDITY.md` | depends_on:C006 |
| C008 | `PROVED_SYMBOLIC` | All-high permutation rigidity holds for cardinalities 2 and 3. | `proofs/DIAMETER_TWO_RIGIDITY.md` | special_case:C007 |
| C009 | `PROVED_SYMBOLIC_PLUS_CERTIFICATE` | All-high permutation rigidity holds for cardinality 4. | `proofs/FOUR_STATE_RIGIDITY.md` | depends_on:C006<br>verified_by:C010 |
| C010 | `PROVED_SYMBOLIC` | The strict-S exceptional branch reduces to 18 necessary nonsquare discriminants excluded modulo 4 5 11 17. | `proofs/NONSQUARE_18.md` | — |
| C011 | `PROVED_SYMBOLIC_PLUS_CRT` | An exact five-state closed strongly connected nonpermutation counterfamily exists on an infinite arithmetic progression of bases. | `proofs/FIVE_STATE_COUNTERFAMILY.md` | depends_on:C003 |
| C012 | `PROVED_SHARP` | The least cardinality of an all-high finite nonpermutation closed SCC is exactly five. | `proofs/SHARP_THRESHOLD.md` | lower_bound_from:C009<br>upper_bound_from:C011 |
| C013 | `PROVED_SYMBOLIC` | For every fixed cardinality there are finitely many abstract defect-decorated RGΦ types. | `proofs/FINITE_TYPES.md` | depends_on:C006 |
| C014 | `PROVED_SYMBOLIC` | For a fixed primitive state tuple with prescribed transitions/defects, realizing bases are empty or one complete arithmetic progression. | `proofs/CRT_FIBRE.md` | depends_on:C002 |
| C015 | `PROVED_SYMBOLIC` | Every high closed rational set of size at most n at fixed base B lies in an explicit divisor universe and is decidable. | `proofs/FIXED_BASE_DECIDABILITY.md` | depends_on:C002 |
| C016 | `PROVED_SYMBOLIC` | The content defect product of a directed cycle equals each complementary product of state ratios. | `proofs/EXACT_CYCLE_IDENTITY.md` | refines:C006 |
| C017 | `PROVED_SYMBOLIC` | If one restricted generator is a single n-cycle on a finite all-high component, the other generator is the identity; in either transitive architecture n<=tau(B-1). | `proofs/TRANSITIVE_GENERATOR_RIGIDITY.md` | depends_on:C003<br>extends_beyond_small_diameter:C007 |
| B001 | `NOT_CLAIMED` | Complete arithmetic classification of all five-state realizations. | `` | — |
| B002 | `NOT_CLAIMED` | Complete six-state classification. | `` | — |
| B003 | `NOT_CLAIMED` | A physical law or physical interpretation follows from RGΦ I. | `` | — |
| B004 | `NOT_CLAIMED` | Absolute historical priority or a first-ever claim beyond the audited novelty boundary. | `literature/LITERATURE_AUDIT_2026-11-13.md` | — |
| C018 | `PROVED_COMPUTER_ASSISTED_PLUS_SYMBOLIC` | Every five-state nonpermutation finite high component has exactly one strict edge globally. | `proofs/FIVE_STATE_STRICT_EDGE_UNIQUENESS.md` | depends_on:C006 |
| C019 | `PROVED_SYMBOLIC` | Eight active S-strict oriented branches reduce state-side to two T-cycle templates with Q=rD-(r-1)C and explicit quadratic/cubic divisibilities. | `proofs/FIVE_STATE_COMMON_S_STRICT_TEMPLATES.md` | depends_on:C018<br>depends_on:C003 |
| C020 | `PROVED_SYMBOLIC_PLUS_EXACT_CAS` | For DF015-0015 every primitive realization lies on one of nineteen smooth elliptic cubics and the RGΦ coprime locus is finite on each curve by Siegel. | `proofs/DF015_0015_ELLIPTIC_FRONTIER.md` | depends_on:C018 |
| C021 | `PROVED_SYMBOLIC` | For any unimodular projective conjugacy, cycle content is controlled by the Hilbert width between the two primitive coordinate charts; the original high-cycle budget is the special H-chart case. | `proofs/TWO_CHART_PROJECTIVE_WIDTH.md` | depends_on:C003 |
| R001 | `PROVED_SYMBOLIC_PLUS_CERTIFICATE` | The strict-T factor-three form DF015-0015-B1 has no realization in its high chamber. | `research/df015-0015/CERTIFICATE.md` | uses_necessary_cubic_reduction:C020 |
| R002 | `PROVED_SYMBOLIC_PLUS_CERTIFICATE` | The eight oriented S-strict rows in the two shared systems have no realization. | `research/five-state/continuation/SHARED_SYSTEMS_EXCLUSION.md` | uses_necessary_cycle_divisibilities:C019 |
| R003 | `PROVED_SYMBOLIC` | An all-high finite closed component cannot have exactly one strict T edge of factor two. | `research/five-state/continuation/PREDECESSOR_AND_SPARSE_EXCLUSIONS.md` | uses_exact_reduction:C002 |
| R004 | `PROVED_SYMBOLIC_PLUS_CERTIFICATE` | The strict-S orientations of DF015-0004, DF015-0008, DF015-0012 and DF015-0018 have no primitive realization. | `research/five-state/continuation/PREDECESSOR_AND_SPARSE_EXCLUSIONS.md` | uses_predecessor_lemma:R003 |
| R005 | `PROVED_SYMBOLIC_PLUS_CERTIFICATE` | The strict-S orientations of DF015-0011 and DF015-0017, and the strict-T orientation of DF015-0005, have no primitive realization. | `research/five-state/continuation/ADDITIONAL_RESULTANT_EXCLUSIONS.md` | uses_predecessor_lemma:R003 |
| R006 | `PROVED_SYMBOLIC_PLUS_CERTIFICATE` | The strict-T orientations of DF015-0006, DF015-0008, DF015-0016, DF015-0017 and DF015-0018 have no primitive realization. | `research/five-state/continuation/REMAINING_RESULTANT_EXCLUSIONS.md` | uses_rectangle_quotient:R005 |
| R007 | `PROVED_SYMBOLIC` | The square-cycle systems of 119772 (factors two and three) and 606897 (factor three) admit no varying integer-polynomial primitive-state family. | `research/five-state/continuation/SQUARE_CYCLE_PARAMETER_OBSTRUCTION.md` | uses_exact_state_and_base_conditions:C014 |
| R008 | `PROVED_SYMBOLIC_PLUS_CERTIFICATE` | For 606897 every root of unity on the four ordinary cycle moduli differs from both uniform signs. | `research/five-state/continuation/SQUARE_CYCLE_PURE_SIGNS.md` | uses_exact_state_and_base_conditions:C014 |
| R009 | `PROVED_SYMBOLIC` | Each signed square-cycle cofactor system has at most one primitive core per choice of quotients; bounded cofactors give an explicit coordinate bound. | `research/five-state/continuation/SQUARE_CYCLE_COFACTOR_BOUND.md` | uses_exact_state_and_base_conditions:C014 |
| R010 | `PROVED_SYMBOLIC_PLUS_CERTIFICATE` | The least base with a five-state nonpermutation high component is at least 9185770249. | `research/five-state/continuation/FIVE_STATE_BASE_LOWER_BOUND.md` | uses_global_oriented_exclusions:R006<br>uses_known_tuple_and_base_class:C011 |
| R011 | `PROVED_SYMBOLIC` | Each remaining square-cycle shift has open-chamber representatives satisfying direct localized edge and defect conditions at every prescribed finite prime list. | `research/five-state/continuation/SQUARE_CYCLE_LOCAL_SIEVES.md` | uses_exact_reduction:C002 |
| R012 | `PROVED_SYMBOLIC` | Every fixed algebraic curve contains finitely many primitive high cores of each residual square-cycle system. Each rational parametrization has a computable parameter-height bound. | `research/five-state/continuation/SQUARE_CYCLE_CURVE_FINITE.md` | uses_exact_state_and_base_conditions:C014<br>generalizes_polynomial_obstruction:R007 |
| R013 | `PROVED_SYMBOLIC` | Each plane and each surface avoiding the eight cycle lines contains finitely many primitive high cores. A single fixed signed cofactor denominator gives an effective finite search. | `research/five-state/continuation/SQUARE_CYCLE_SURFACE_FINITE.md` | uses_curve_finiteness_and_rational_parameter_bound:R012<br>uses_signed_cofactor_planes:R009 |
| R014 | `PROVED_SYMBOLIC` | The degree-four-t intersection of the four t-th powers of the cycle ideals is spanned by the t-th power of the coordinate product in all three residual systems. | `research/five-state/continuation/SQUARE_CYCLE_POWERED_QUOTIENT_OBSTRUCTION.md` | uses_four_cycle_ideals:R013 |
| R015 | `PROVED_SYMBOLIC` | For any fixed prime set and positive eta, each residual system has finitely many realizations with weighted prime part [ACDQ]^2[E] at least H^(4+eta). | `research/five-state/continuation/SQUARE_CYCLE_PRIME_SUPPORT.md` | uses_plane_finiteness:R013<br>uses_exact_fifth_state_and_overlap_conditions:C014 |
| R016 | `PROVED_SYMBOLIC_PLUS_CERTIFICATE` | All four complementary cofactor constants are nonzero for every signed choice on any residual square-cycle realization. | `research/five-state/continuation/SQUARE_CYCLE_ZERO_CONSTANTS.md` | adjudicates_complementary_cofactor_degeneracies:R009 |
| R017 | `PROVED_SYMBOLIC` | The factor-three square systems are reflections of each other. For the shift D=3E-A their full arithmetic CRT fibres agree in shared coordinates before chamber selection. | `research/five-state/continuation/FACTOR_THREE_COMMON_ARITHMETIC.md` | identifies_exact_arithmetic_conditions:C014 |
| R018 | `PROVED_SYMBOLIC_PLUS_CERTIFICATE` | The known factor-three tuple is the sole oriented five-state nonpermutation realization at base 88011536665779. | `research/five-state/continuation/FACTOR_THREE_COMMON_ARITHMETIC.md` | uses_oriented_exclusions:R006<br>uses_exhaustive_oriented_status:R010<br>uses_known_realization:C011 |
| R019 | `PROVED_SYMBOLIC_PLUS_CERTIFICATE` | Ordinary opposite-pair divisor complements never preserve the primitive square-cycle constraints on residual high cores. Fixed rational relative weights force bounded source height. | `research/five-state/continuation/SQUARE_CYCLE_COMPLEMENT_DESCENT.md` | uses_opposite_square_cycles:R009<br>uses_primitive_states_and_overlap_conditions:C014 |
| R020 | `PROVED_SYMBOLIC` | For every fixed denominator pair in any residual square-cycle system each simultaneous CRT root supports at most one primitive numerator slope in the high chamber. | `research/five-state/continuation/SQUARE_CYCLE_LATTICE_FIBRES.md` | uses_exact_adjacent_coprimality:C014<br>uses_reflected_witness_for_replay:R017 |
| R021 | `PROVED_SYMBOLIC_PLUS_CERTIFICATE` | The least base of a five-state nonpermutation realization is at least 18371540497. The two open orientations individually have base lower bounds of 31820229419 and 66963421866. | `research/five-state/continuation/FIVE_STATE_BASE_LOWER_BOUND_PARALLEL.md` | extends_verified_coordinate_ranges:R010 |
| R022 | `PROVED_SYMBOLIC_PLUS_CERTIFICATE` | For each of the five strict shifts and each prime p>3 the state projection has p^4-4p^3+14p^2-22p+11 locally admissible classes. The residue counts lift with an explicit common p-adic Haar density. | `research/five-state/continuation/SQUARE_CYCLE_PRIME_PATTERNS.md` | uses_ten_edge_conditions_and_overlaps:C014 |
| R023 | `PROVED_SYMBOLIC` | Fix A and C in a residual square cycle. Each simultaneous root class refined by the strict shift and Q modulo three when needed supports at most one primitive D/Q slope in the high chamber. | `research/five-state/continuation/SQUARE_CYCLE_REVERSE_LATTICES.md` | extends_chamber_lattice_rigidity:R020<br>uses_high_chamber_and_overlaps:C014 |
| R024 | `PROVED_SYMBOLIC_PLUS_CERTIFICATE` | The known factor-three realization is the unique realization on the cofactor plane 7D=21Q-16A, with no height bound. | `research/five-state/continuation/WITNESS_COFACTOR_PLANE.md` | specializes_plane_quotient_method:R013<br>certifies_uniqueness_in_known_witness_plane:C011 |
| R025 | `PROVED_SYMBOLIC` | Polynomial quotients built from independent powers of the four core ideals and the principal fifth-modulus ideal are constant in matching homogeneous degree. | `research/five-state/continuation/SQUARE_CYCLE_WEIGHTED_QUOTIENT_OBSTRUCTION.md` | uses_square_cycles_and_coefficient_mismatch:R009 |

## Artifact registry

| ID | Type | Path | Supports |
|---|---|---|---|
| A001 | `exact_certificate` | `certificates/NONSQUARE_CERTIFICATE_J1_37.csv` | C009;C010 |
| A002 | `exact_certificate` | `certificates/STATES_AND_ACTIONS.csv` | C011;C012 |
| A003 | `exact_certificate` | `certificates/CRT_CONGRUENCES.csv` | C011;C014 |
| A004 | `exact_certificate` | `certificates/ARITHMETIC_PROGRESSION.json` | C011;C012 |
| A005 | `exact_certificate` | `certificates/COUNTERFAMILY_CYCLE_CERTIFICATE.json` | C005;C011 |
| A006 | `software` | `src/rmr/verify.py` | C002;C003;C004;C005;C009;C011;C012 |
| A007 | `software` | `src/rmr/trusted_checker.cpp` | C011 |
| A008 | `generated_report` | `outputs/reports/claim_traceability.md` | all |
| A009 | `interactive` | `outputs/interactive/epistemic_graph.html` | all |
| A010 | `generated_figure` | `outputs/figures/` | C001;C005;C011;C012 |
| A011 | `communication_map` | `interactive/supergraph/supergraph_model.json` | all |
| A012 | `governance` | `docs/EPISTEMIC_PROTOCOL.md` | all |
| A013 | `communication` | `docs/RGPHI_I_PRIMER_EPISTEMICO_ES.md` | all |
| A014 | `exact_catalogue` | `research/five-state/DIOPHANTINE_NORMAL_FORMS_20.csv` | C018;C019 |
| A015 | `exact_certificates` | `research/five-state/certificates/` | C018 |
| A016 | `proof_record` | `research/five-state/elliptic/` | C020 |
| A017 | `proof_record` | `proofs/TWO_CHART_PROJECTIVE_WIDTH.md` | C021 |
| A018 | `software` | `src/rmr/check_two_chart_projective_width.py;src/rmr/check_elliptic_frontier.py` | C020;C021 |
| A019 | `exact_certificate` | `research/df015-0015/` | R001 |
| A020 | `software` | `src/rmr/verify_rgphi_farkas_728.py` | C018 |
| A021 | `catalogue` | `research/five-state/continuation/ORIENTED_TO_ROUND015.csv` | R001;R002 |
| A022 | `software` | `research/five-state/continuation/verify_shared_chambers.py` | R002 |
| A023 | `exact_certificate` | `research/five-state/continuation/SPARSE_S_STRICT_CERTIFICATES.json` | R004 |
| A024 | `catalogue` | `research/five-state/continuation/ORIENTED_STATUS.csv` | R001;R002;R003;R004 |
| A025 | `exact_certificate` | `research/five-state/continuation/STRICT_T_RECTANGLE_CERTIFICATES.json` | R005 |
| A026 | `exact_certificate` | `research/five-state/continuation/REMAINING_RESULTANT_CERTIFICATES.json` | R006 |
| A027 | `exact_certificate` | `research/five-state/continuation/SQUARE_CYCLE_PURE_SIGN_CERTIFICATE.json` | R008 |
| A028 | `regression_certificate` | `research/five-state/continuation/SQUARE_CYCLE_COFACTOR_REPLAY.json` | R009 |
| A029 | `computation_record` | `research/five-state/continuation/SQUARE_CYCLE_SEARCH_100000.md` | R010 |
| A030 | `regression_certificate` | `research/five-state/continuation/SQUARE_CYCLE_LOCAL_SIEVES_43.json` | R011 |
| A031 | `proof_record` | `research/five-state/continuation/SQUARE_CYCLE_CURVE_FINITE.md` | R012 |
| A032 | `proof_record` | `research/five-state/continuation/SQUARE_CYCLE_SURFACE_FINITE.md` | R013 |
| A033 | `proof_record` | `research/five-state/continuation/SQUARE_CYCLE_POWERED_QUOTIENT_OBSTRUCTION.md` | R014 |
| A034 | `proof_record` | `research/five-state/continuation/SQUARE_CYCLE_PRIME_SUPPORT.md` | R015 |
| A035 | `software` | `research/five-state/continuation/verify_square_prime_support.py` | R015 |
| A036 | `exact_certificate` | `research/five-state/continuation/SQUARE_CYCLE_ZERO_CONSTANTS_CERTIFICATE.json` | R016 |
| A037 | `software` | `research/five-state/continuation/verify_opposite_zero_constants.py` | R016 |
| A038 | `proof_record` | `research/five-state/continuation/FACTOR_THREE_COMMON_ARITHMETIC.md` | R017;R018 |
| A039 | `exact_certificate` | `research/five-state/continuation/verify_residual_by_base.py;research/five-state/continuation/FACTOR_THREE_WITNESS_BASE_CERTIFICATE.json` | R018 |
| A040 | `exact_certificate` | `research/five-state/continuation/SQUARE_CYCLE_COMPLEMENT_DESCENT.md;research/five-state/continuation/verify_complement_descent.py;research/five-state/continuation/SQUARE_CYCLE_COMPLEMENT_DESCENT_CERTIFICATE.json` | R019 |
| A041 | `proof_record` | `research/five-state/continuation/SQUARE_CYCLE_LATTICE_FIBRES.md;research/five-state/continuation/verify_square_lattice_fibres.py;research/five-state/continuation/SQUARE_CYCLE_LATTICE_FIBRES_CERTIFICATE.json` | R020 |
| A042 | `computation_record` | `research/five-state/continuation/SQUARE_CYCLE_PARALLEL_CENSUS.json;research/five-state/continuation/square_cycle_search_range.cs` | R021 |
| A043 | `proof_record` | `research/five-state/continuation/SQUARE_CYCLE_PRIME_PATTERNS.md;research/five-state/continuation/verify_square_prime_patterns.py` | R022 |
| A044 | `proof_record` | `research/five-state/continuation/SQUARE_CYCLE_REVERSE_LATTICES.md` | R023 |
| A045 | `exact_certificate` | `research/five-state/continuation/WITNESS_COFACTOR_PLANE.md;research/five-state/continuation/verify_witness_cofactor_plane.py` | R024 |
| A046 | `proof_record` | `research/five-state/continuation/SQUARE_CYCLE_WEIGHTED_QUOTIENT_OBSTRUCTION.md` | R025 |
