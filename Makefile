# make all regenerates every figure and table from raw data with no manual steps.
# Phases are gated (SCAFFOLD.md): a target must not run before its predecessor passes.

PY := python3

.PHONY: all test loader feasibility guidelines trials reliability clean

all: test feasibility guidelines trials
	@echo "Stream C (feasibility) + Stream B (guidelines) + Stream A (trials) regenerated."

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

clean:
	rm -rf data/interim/* .pytest_cache
	find . -name __pycache__ -type d -prune -exec rm -rf {} +
