# make all regenerates every figure and table from raw data with no manual steps.
# Phases are gated (SCAFFOLD.md): a target must not run before its predecessor passes.

PY := python3

.PHONY: all test loader feasibility guidelines trials reliability literature pdf bundle deposit clean

all: test feasibility guidelines trials literature
	$(PY) -m src.analysis.streamc_linkage
	$(PY) -m src.analysis.summary_figure
	$(PY) -m src.analysis.linkage_figure
	@echo "Stream C (feasibility) + Stream B (guidelines) + Stream A (trials) + literature-gap regenerated."

test:
	$(PY) -m pytest -q

loader:
	$(PY) -m src.loaders.aidsvu

# Stream C — the linkage decomposition (systems denominator) + the dilution leg.
# streamc_linkage: does any deployed system link exposure to S. aureus phenotype?
# dilution/dilution_metro: even a linked system would face a dilute exposed subgroup.
feasibility:
	$(PY) -m src.analysis.streamc_linkage
	$(PY) -m src.feasibility.dilution
	$(PY) -m src.feasibility.dilution_metro

# Stream B — guideline coding + gate
guidelines:
	$(PY) -m src.coding.build_guidelines

# Stream B — inter-coder reliability
reliability:
	$(PY) -m src.analysis.reliability

# Stream A — trial coding + reporting analyses
# detectability: min-detectable RR (between-arm power) for the interim cross-sectional
#   contrasts — now explanatory (why the interim read null; §3.1), not a claim of
#   non-detectability. The final trial's randomised incidence analysis detected the
#   signal (Luetkemeyer 2025, HR 3.89); the S. aureus selection ratchet is retired.
# dejong_sigma: empirical between-cohort MRSA overdispersion σ̂ (feeds coverage_null).
# coverage_null + three_outbreak_fit: MRSA-scoped clustering-detectability pair —
# a mean-based endpoint cannot resolve clustering, and the trial series cannot
# identify the clustering shape either way. (dejong_sigma must run before coverage_null.)
trials:
	$(PY) -m src.coding.build_trials
	$(PY) -m src.analysis.detectability
	$(PY) -m src.analysis.dejong_sigma
	$(PY) -m src.analysis.coverage_null
	$(PY) -m src.analysis.three_outbreak_fit

# Cross-stream — the measurement gap in the doxy-PEP literature itself.
# Reads the frozen snapshot; pass ARGS=--refresh to re-query PubMed E-utilities.
literature:
	$(PY) -m src.analysis.literature_search $(ARGS)

# Manuscript PDF — pandoc + citeproc + pdflatex, house preamble (paper/preamble.tex).
# Figures are read from outputs/figures/ (regenerate them with `make feasibility`).
# --resource-path lets the manuscript's ../outputs/figures/ paths resolve from root.
# --csl paper/plos.csl → PLoS Biology numbered (Vancouver) reference style.
pdf:
	pandoc paper/manuscript.md --citeproc --bibliography=paper/references.bib \
	  --csl=paper/plos.csl \
	  --resource-path=paper:. -H paper/preamble.tex --pdf-engine=pdflatex \
	  -o paper/manuscript.pdf
	@echo "wrote paper/manuscript.pdf"

# Deposit bundle — assemble the submission package and checksum it.
# Depends on a current PDF and figures (run `make pdf` / `make all` first).
# Writes submission/CHECKSUMS.sha256 and a portable tarball under submission/.
bundle:
	@mkdir -p submission
	@files="paper/manuscript.pdf paper/manuscript.md paper/references.bib \
	  paper/preamble.tex \
	  submission/COVER_LETTER.md submission/REVIEWER_GUIDE.md \
	  submission/RESPONSE_TO_ANTICIPATED_REVIEWS.md submission/VENUE_MATRIX.md \
	  submission/PANEL_SYNTHESIS.md submission/MANIFEST.md \
	  submission/REPO_DEPOSIT_README.md \
	  DECISIONS.md outputs/gap_register.md outputs/citation_verification.md \
	  $$(ls outputs/*_result.md) $$(ls outputs/figures/*.png)"; \
	shasum -a 256 $$files > submission/CHECKSUMS.sha256; \
	tar -czf submission/doxypep-bystander-deposit.tar.gz $$files \
	  submission/CHECKSUMS.sha256; \
	echo "wrote submission/CHECKSUMS.sha256 ($$(wc -l < submission/CHECKSUMS.sha256) files)"; \
	echo "wrote submission/doxypep-bystander-deposit.tar.gz"

# Full-repository deposit for Zenodo — code + coded/derived data + manuscript.
# Enumerates only verified-safe paths: NO copyrighted publisher PDFs/DOCX or verbatim
# transcriptions (their SHA-256 provenance pins in data/raw/**/CHECKSUMS.md + SOURCES.md
# travel instead). An extracted copy runs `make all` from the coded YAML, AIDSVu public
# data, and the literature snapshot — the PDFs are source references, not runtime inputs.
deposit: bundle
	@mkdir -p submission
	tar --exclude='__pycache__' --exclude='*.pyc' --exclude='*.tar.gz' \
	  -czf submission/doxypep-bystander-repo.tar.gz \
	  src tests paper outputs submission \
	  data/processed data/raw/aidsvu data/raw/coding \
	  data/raw/literature data/raw/literature_search \
	  data/raw/papers/CHECKSUMS.md data/raw/papers/SOURCES.md \
	  data/raw/guidelines/CHECKSUMS.md data/raw/guidelines/SOURCES.md \
	  Makefile requirements.txt README.md CLAUDE.md DECISIONS.md \
	  CODEBOOK.md CODEBOOK_streamA.md METHODS_streamB.md SCAFFOLD.md \
	  PREREGISTRATION.md STREAM_B_HANDOFF.md
	@shasum -a 256 submission/doxypep-bystander-repo.tar.gz \
	  > submission/doxypep-bystander-repo.tar.gz.sha256
	@echo "wrote submission/doxypep-bystander-repo.tar.gz ($$(du -h submission/doxypep-bystander-repo.tar.gz | cut -f1))"

clean:
	rm -rf data/interim/* .pytest_cache
	find . -name __pycache__ -type d -prune -exec rm -rf {} +
