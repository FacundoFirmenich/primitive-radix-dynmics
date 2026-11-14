# Reproducibility pattern audit — Beyond Redfield / KwanTube

The design of this repository deliberately borrows the strongest reproducibility patterns observed in the public `FacundoFirmenich/KwanTube` companion to *Beyond Redfield: Thermodynamic Bounds and Non-Perturbative Quantum Dynamics in Tubulin Networks* (bioRxiv DOI 10.64898/2026.05.10.724047), while adapting them to exact mathematics.

## Patterns retained

- one-shot reproduction entry point;
- explicit execution order and pipeline map;
- automated validation ledger;
- claim-to-evidence traceability;
- lineage/provenance audit;
- SHA-256 sealing and validation;
- paired machine-readable + human-readable reports;
- CI smoke tests;
- reproducible figures;
- interactive epistemic graph;
- Zenodo and citation metadata;
- strict distinction between expensive/discovery computation and authoritative verification.

## Mathematical adaptations

Unlike the computational-physics pipeline, this repository treats symbolic proof and exact finite certificates as the highest authority. Finite scans cannot silently become theorem evidence. The interactive graph therefore distinguishes `PROVED_SYMBOLIC`, `EXACT_CERTIFICATE`, `PROVED_SYMBOLIC_PLUS_CRT`, `NOT_CLAIMED` and literature-context nodes.
