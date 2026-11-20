LAKE ?= lake
PYTHON ?= python3
.PHONY: build audit
build:
	$(LAKE) build
audit:
	$(PYTHON) scripts/audit.py --lake $(LAKE)
