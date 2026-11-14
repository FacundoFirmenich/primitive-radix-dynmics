PYTHON ?= python
PYTHONPATH ?= src
.PHONY: verify test trace graph figures reproduce seal integrity clean
verify:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m rmr.verify --report outputs/reports/verification_report.json

test:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m pytest -q

trace:
	$(PYTHON) src/ledger/export_claim_traceability.py

graph:
	$(PYTHON) src/graph/build_epistemic_graph.py

figures:
	$(PYTHON) src/figures/generate_figures.py

seal:
	$(PYTHON) src/integrity/seal_outputs.py

integrity:
	$(PYTHON) src/integrity/validate_outputs.py

reproduce: verify test trace graph figures seal integrity
	@echo "REPRODUCE PASS"

clean:
	rm -rf outputs/figures/* outputs/interactive/* outputs/reports/* outputs/checksums/*
