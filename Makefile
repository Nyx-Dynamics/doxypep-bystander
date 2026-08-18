# make all regenerates every figure and table from raw data with no manual steps.
# Phases are gated (SCAFFOLD.md): a target must not run before its predecessor passes.

PY := python3

.PHONY: all test loader feasibility clean

all: test feasibility
	@echo "Phase 0 is the gate. Phases 1-4 wire in here only once their gate passes."

test:
	$(PY) -m pytest -q

# Phase 0 gate
loader:
	$(PY) -m src.loaders.aidsvu

feasibility:
	$(PY) -m src.feasibility.dilution
	$(PY) -m src.feasibility.dilution_metro

clean:
	rm -rf data/interim/* .pytest_cache
	find . -name __pycache__ -type d -prune -exec rm -rf {} +
