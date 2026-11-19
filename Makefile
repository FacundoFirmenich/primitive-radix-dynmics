PYTHON ?= python
PYTHONPATH ?= src
.NOTPARALLEL: reproduce
.PHONY: verify test trace graph figures reproduce seal integrity clean recent-verify recent-full-census sync-check rc33-seal
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
	$(PYTHON) src/figures/generate_recent.py

seal:
	$(PYTHON) src/integrity/seal_outputs.py

integrity:
	$(PYTHON) src/integrity/validate_outputs.py

reproduce: verify test rc33-verify recent-verify fst11-verify t007-verify fst1213-verify fst14-verify sine-assault-verify causal-trace-verify fst16-verify tarasutra-verify trace graph figures rc33-seal sync-check seal integrity
	@echo "REPRODUCE PASS"

recent-verify:
	$(PYTHON) research/rc33/recent/replay.py

recent-full-census:
	mkdir -p build/recent-full-census outputs/reports/recent-full-census
	cp research/rc33/recent/chamber/boundary_census.py build/recent-full-census/
	$(PYTHON) build/recent-full-census/boundary_census.py --max-t 5000
	cp build/recent-full-census/BOUNDARY_CENSUS_T5000.json outputs/reports/recent-full-census/

clean:
	rm -rf outputs/figures/* outputs/interactive/* outputs/reports/* outputs/checksums/*

.PHONY: rc33-verify
rc33-verify:
	$(MAKE) -C research/rc33 verify

rc33-seal:
	$(PYTHON) src/integrity/seal_rc33.py

sync-check:
	$(PYTHON) src/integrity/check_sync.py

.PHONY: fst11-verify
fst11-verify:
	$(PYTHON) research/rc33/fst11/replay.py

.PHONY: t007-verify t007-full-hexagon
t007-verify:
	$(PYTHON) research/rc33/t007/replay.py
t007-full-hexagon:
	$(PYTHON) research/rc33/t007/replay.py --full-hexagon

.PHONY: fst1213-verify
fst1213-verify:
	$(PYTHON) research/rc33/fst1213/replay.py --output outputs/reports/fst1213

.PHONY: fst14-verify
fst14-verify:
	$(PYTHON) research/rc33/fst14/replay.py --output outputs/reports/fst14

.PHONY: sine-assault-verify
sine-assault-verify:
	$(PYTHON) research/rc33/sine-assault/replay.py --output outputs/reports/sine-assault

.PHONY: causal-trace-verify
causal-trace-verify:
	mkdir -p outputs/reports/causal-traces
	node research/rc33/causal-traces/verify.cjs outputs/reports/causal-traces/RESULTS.json

.PHONY: fst16-verify
fst16-verify:
	$(PYTHON) research/rc33/fst16/replay.py --output outputs/reports/fst16

.PHONY: tarasutra-verify
tarasutra-verify:
	$(PYTHON) research/rc33/tarasutra/code/check_tarasutra_realization.py --write
