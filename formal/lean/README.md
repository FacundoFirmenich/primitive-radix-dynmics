# Lean verification · primitive radix–Möbius dynamics · RC3.3

Author: **Facundo Firmenich**. [Alcance en castellano](README_ES.md).

This project proves selected statements of the main paper, supplement and
companion in Lean 4.19.0, with Mathlib pinned to
`c44e0c8ee63ca166450922a373c7409c5d26b00b`. It is a partial formalization.
The full four-state exclusion is a remaining obligation.

After installing the toolchain named in `lean-toolchain`:

```sh
lake build
python3 scripts/audit.py
```

The first invocation needs network access for the pinned dependencies.
`lake exe cache get` may accelerate a build when the official Mathlib cache is
accessible; otherwise Lake can compile the dependencies from source. This
project was compiled from the pinned sources. No compiler or downloaded cache
is included in the source package. `--lake /absolute/path/to/lake` selects an
existing toolchain without changing global configuration.

The audit prints its complete input configuration, rebuilds the library,
checks every named theorem with `#print axioms` under `--trust=0`, records all
types, and runs seven negative/positive mutation pairs. Intentionally false
mutation files belong only to the audit folder and are expected to fail;
they are not imported by the library. No `sorry`, `admit`, custom axiom or
`native_decide` is allowed in project sources. The reported dependencies are
only Lean's standard `propext`, `Classical.choice` and `Quot.sound`.

Read [COVERAGE.json](COVERAGE.json) and [RESULTS.md](RESULTS.md) for exact scopes.
The two infinite five-state families, their reduction factors, the36-action
monoid with minimum rank2, cycle balance, integral-lift identities and the
conic square filter are included. A square-filter theorem does not certify
the coverage of an external search. This project does not prove the37-case
classification, the large enumeration certificates, global uniqueness,
global minimum bases or the remaining606897 existence question.

Formal checking certifies the stated proposition relative to Lean's logic and
kernel. The correspondence between the formal definitions and manuscript is
separately documented in `SEMANTIC_AUDIT_ES.md`; this is an explicitly labelled
self-review, not external peer review or an independent implementation of Lean.
The versioned source and proof terms, rather than a screenshot or a PASS label,
are the certificate. No claim of new mathematical priority is made by counting
lemmas used in the formalization.
