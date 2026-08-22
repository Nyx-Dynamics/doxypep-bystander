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

# --- Deposit archives -------------------------------------------------------- #
# Two artifacts:
#   bundle  -> journal submission package (manuscript + submission-facing aids)
#   deposit -> clean research compendium for Zenodo (reproducibility artifacts only)
# Both set COPYFILE_DISABLE=1 and exclude AppleDouble (._*/.DS_Store) so macOS extended
# attributes do not pollute the archive, and NEVER place the tarball's own checksum inside
# the tarball — the .sha256 is computed AFTER the archive is closed and lives beside it.

# Journal submission package (author-facing; includes the editorial aids).
bundle:
	@mkdir -p submission
	@files="paper/manuscript.pdf paper/manuscript.md paper/references.bib paper/preamble.tex \
	  paper/plos.csl \
	  submission/COVER_LETTER.md submission/REVIEWER_GUIDE.md \
	  submission/RESPONSE_TO_ANTICIPATED_REVIEWS.md submission/VENUE_MATRIX.md \
	  submission/PANEL_SYNTHESIS.md submission/MANIFEST.md submission/REPO_DEPOSIT_README.md \
	  DECISIONS.md outputs/gap_register.md outputs/citation_verification.md \
	  $$(ls outputs/*_result.md) $$(ls outputs/figures/*.png)"; \
	COPYFILE_DISABLE=1 tar --exclude='._*' --exclude='.DS_Store' \
	  -czf submission/doxypep-bystander-submission.tar.gz $$files; \
	shasum -a 256 submission/doxypep-bystander-submission.tar.gz \
	  > submission/doxypep-bystander-submission.tar.gz.sha256; \
	echo "wrote submission/doxypep-bystander-submission.tar.gz (+ .sha256, computed after)"

# Zenodo research compendium — reproducibility artifacts only. NO editorial/process layer
# (no CLAUDE.md/SCAFFOLD.md/STREAM_B_HANDOFF.md, no submission/); NO copyrighted publisher or
# guideline PDFs / transcriptions, and NO AIDSVu XLSX (IQVIA-sourced) — all excluded, with
# provenance travelling via SOURCES.md + CHECKSUMS.md. AIDSVu is retrieved+verified by
# scripts/fetch_aidsvu.py before `make all`. See THIRD_PARTY_DATA.md.
DEPOSIT_PATHS = README.md CITATION.cff LICENSE-CODE LICENSE-TEXT THIRD_PARTY_DATA.md \
  REPRODUCIBILITY.md Makefile requirements.txt requirements-lock.txt \
  CODEBOOK.md CODEBOOK_streamA.md METHODS_streamB.md PREREGISTRATION.md DECISIONS.md \
  src tests scripts outputs \
  paper/manuscript.md paper/manuscript.pdf paper/references.bib paper/preamble.tex paper/plos.csl \
  data/processed data/raw/coding data/raw/literature data/raw/literature_search \
  data/raw/aidsvu/SOURCES.md data/raw/aidsvu/CHECKSUMS.md \
  data/raw/papers/SOURCES.md data/raw/papers/CHECKSUMS.md \
  data/raw/guidelines/SOURCES.md data/raw/guidelines/CHECKSUMS.md

deposit:
	@mkdir -p submission
	@rm -f CHECKSUMS.sha256
	@COPYFILE_DISABLE=1 find $(DEPOSIT_PATHS) -type f \
	  ! -name '._*' ! -name '.DS_Store' ! -name '*.pyc' ! -path '*/__pycache__/*' \
	  | LC_ALL=C sort | xargs shasum -a 256 > CHECKSUMS.sha256
	@COPYFILE_DISABLE=1 tar --exclude='__pycache__' --exclude='*.pyc' \
	  --exclude='._*' --exclude='.DS_Store' \
	  -czf submission/doxypep-bystander-repo.tar.gz $(DEPOSIT_PATHS) CHECKSUMS.sha256
	@shasum -a 256 submission/doxypep-bystander-repo.tar.gz \
	  > submission/doxypep-bystander-repo.tar.gz.sha256
	@echo "wrote submission/doxypep-bystander-repo.tar.gz ($$(du -h submission/doxypep-bystander-repo.tar.gz | cut -f1); $$(tar tzf submission/doxypep-bystander-repo.tar.gz | grep -c .) members)"
	@echo "external checksum beside archive (NOT inside): submission/doxypep-bystander-repo.tar.gz.sha256"

clean:
	rm -rf data/interim/* .pytest_cache
	find . -name __pycache__ -type d -prune -exec rm -rf {} +
