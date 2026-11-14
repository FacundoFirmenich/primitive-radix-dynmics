# Project charter

## Mission

Maintain the exact, reproducible and auditable computational companion to the first mathematics publication in the Projective Radix Dynamics programme.

## Current deliverable

A public research and reproducibility companion containing exact certificates, checkers, reproducible figures, a claim/evidence ledger, a literature ledger, an interactive epistemic graph and release metadata — **but no manuscript or supplementary manuscript**.

## Definition of done for this repository phase

1. `make verify` passes from a clean Python environment.
2. `make reproduce` regenerates all figures, ledgers and the interactive graph.
3. Every promoted claim in `data/claims.csv` has explicit evidence and dependencies.
4. Every binary/generated artifact has a SHA-256 entry.
5. The repository contains no manuscript `.tex` source and no manuscript PDF.
6. Zenodo metadata validates and contains no fictional DOI.

## Exclusions

- manuscript prose and supplementary manuscript before arXiv;
- claims of complete five-state arithmetic or six-state classification;
- physical interpretations;
- unpublished novelty claims unsupported by the literature ledger.
