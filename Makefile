# make all regenerates every figure and table from raw data with no manual steps.
# Phases are gated (SCAFFOLD.md): a target must not run before its predecessor passes.

PY := python3

.PHONY: all test loader feasibility guidelines trials reliability literature clean

all: test feasibility guidelines trials literature
	@echo "Stream C (feasibility) + Stream B (guidelines) + Stream A (trials) + literature-gap regenerated."

test:
	$(PY) -m pytest -q

loader:
	$(PY) -m src.loaders.aidsvu

# Stream C — surveillance dilution (state + metro, panel-power)
feasibility:
	$(PY) -m src.feasibility.dilution
	$(PY) -m src.feasibility.dilution_metro

# Stream B — guideline coding + gate
guidelines:
	$(PY) -m src.coding.build_guidelines

# Stream B — inter-coder reliability
reliability:
	$(PY) -m src.analysis.reliability

# Stream A — trial coding + reporting analyses
trials:
	$(PY) -m src.coding.build_trials
	$(PY) -m src.analysis.detectability

# Cross-stream — the measurement gap in the doxy-PEP literature itself.
# Reads the frozen snapshot; pass ARGS=--refresh to re-query PubMed E-utilities.
literature:
	$(PY) -m src.analysis.literature_search $(ARGS)

clean:
	rm -rf data/interim/* .pytest_cache
	find . -name __pycache__ -type d -prune -exec rm -rf {} +
