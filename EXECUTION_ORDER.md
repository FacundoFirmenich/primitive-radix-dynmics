# Canonical execution order

1. `python -m rmr.verify --report outputs/reports/verification_report.json`
2. `python src/ledger/export_claim_traceability.py`
3. `python src/graph/build_epistemic_graph.py`
4. `python src/figures/generate_figures.py`
5. `python src/integrity/seal_outputs.py`
6. `python src/integrity/validate_outputs.py`

`make reproduce` executes this order.
