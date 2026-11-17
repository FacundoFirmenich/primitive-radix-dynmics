# RGΦ-I evidence and revision map

| Result | Authority | Auxiliary check | Would require revision if… |
|---|---|---|---|
| cycle identity / budget | `proofs/EXACT_CYCLE_IDENTITY.md`, `CYCLE_REDUCTION_BUDGET.md` | algebraic replay | an admissible high cycle violates the identity/bound |
| transitive-generator rigidity | `proofs/TRANSITIVE_GENERATOR_RIGIDITY.md` | none required | one generator is transitive but either generator fails to be a permutation |
| four-state rigidity | `proofs/FOUR_STATE_RIGIDITY.md`, `NONSQUARE_18.md` | exact modular checker | an omitted branch, invalid cancellation or square discriminant appears |
| five-state realization | `proofs/FIVE_STATE_COUNTERFAMILY.md` + CRT/state certificates | Python/C++ replay | a transition/gcd/congruence fails already at (t=0) |
| sharp threshold | `proofs/SHARP_THRESHOLD.md` | dependency graph | either lower or upper bound fails |
| fixed-(B,n) decidability | `proofs/FIXED_BASE_DECIDABILITY.md` | bounded census | a closed state lies outside the divisor universe |
| priority boundary | `literature/LITERATURE_AUDIT_2026-11-13.md` | specialist chaining | a prior equivalent theorem is identified |

The graph/ledger are navigation and provenance, not additional mathematical evidence.

The eighteen-discriminant table is retained as a historical regression certificate. It is not a claim that those eighteen cases are the current open frontier. The current oriented classification and the recent module evidence are indexed in `RESEARCH_STATUS.md` and `research/rc33/recent/RESULTS.md`.
