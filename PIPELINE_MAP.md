# Pipeline map

```text
certificates/*.csv|json
        │
        ├──> src/rmr/core.py --------------------┐
        │                                         │
        ├──> src/rmr/verify.py ------------------>│ verification_report.json
        │                                         │
        ├──> data/claims.csv + dependencies.csv --┼--> claim_traceability.md
        │                                         │
        ├──> src/graph/build_epistemic_graph.py --┼--> epistemic_graph.json/html
        │                                         │
        └──> src/figures/generate_figures.py -----┴--> figures SVG/PNG/PDF

all generated artifacts --> src/integrity/seal_outputs.py --> SHA256SUMS.txt
```

No generated file is an authority for a theorem; authority flows from exact proof/certificate to generated representation.
