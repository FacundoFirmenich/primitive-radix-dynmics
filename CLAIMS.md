# Claim policy

The authoritative claim table is `data/claims.csv`.

Evidence labels:

- `DEFINITION` — mathematical definition, not a theorem.
- `PROVED_SYMBOLIC` — closed by symbolic proof.
- `PROVED_SYMBOLIC_PLUS_CERTIFICATE` — symbolic reduction plus exact finite certificate.
- `PROVED_SYMBOLIC_PLUS_CRT` — symbolic proof plus generalized CRT construction.
- `PROVED_SHARP` — matching lower and upper constructions establish an exact threshold.
- `EXACT_CERTIFICATE` — finite exact computation in a theorem-defined jurisdiction.
- `CONDITIONAL_HISTORICAL_CENSUS_BOUND` — conditional on documented historical coordinate cutoffs.
- `NOT_CLAIMED` — explicit publication boundary.

A claim may be promoted only if its evidence artifact exists, the dependency graph is closed and all relevant checks pass. `make reproduce` covers the current RC3.3 integration; `make verify` alone is the core verifier.
