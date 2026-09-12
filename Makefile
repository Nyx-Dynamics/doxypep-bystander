# make all regenerates every figure and table from raw data (one manual prerequisite:
# download the AIDSVu inputs and run scripts/verify_aidsvu.py — see THIRD_PARTY_DATA.md).
# Phases are gated: a target must not run before its predecessor passes (see DECISIONS.md).

PY := python3

.PHONY: all test loader feasibility guidelines trials reliability literature pdf tex texpdf supp docx bundle deposit deposit-zip clean

all: test feasibility guidelines trials literature
	$(PY) -m src.analysis.streamc_linkage
	$(PY) -m src.analysis.summary_figure
	$(PY) -m src.analysis.linkage_figure
	$(PY) -m src.analysis.architecture_figure
	$(PY) -m src.feasibility.plots_plwh
	@echo "Stream C (feasibility incl. combined PrEP+PLWH) + Stream B (guidelines) + Stream A (trials) + literature-gap regenerated."

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
	$(PY) -m src.feasibility.dilution_plwh

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

# Manuscript PDF. The canonical source is the hand-maintained PLoS LaTeX (paper/manuscript.tex),
# NOT the superseded Markdown; `make pdf` therefore builds it via `texpdf` (pdflatex + bibtex).
# (The old pandoc-from-Markdown recipe is retired; `make docx` still uses the Markdown.)
pdf: texpdf

# paper/manuscript.tex is the HAND-MAINTAINED canonical submission source (2026-08-22):
# it carries editorial edits + Figure 3 that are NOT in manuscript.md. `make tex` therefore
# no longer overwrites it — it emits a scratch copy for diffing only. Compile the canonical
# with `make texpdf`. (manuscript.md is now a secondary convenience source; pdf/docx below
# still render from it, but the .tex is authoritative for submission.)
tex:
	pandoc paper/manuscript.md --standalone --natbib \
	  --bibliography=paper/references.bib --resource-path=paper:. \
	  -o paper/manuscript.generated.tex
	@echo "wrote paper/manuscript.generated.tex (SCRATCH — diff against the canonical paper/manuscript.tex)"
	@echo "NOTE: canonical paper/manuscript.tex is hand-maintained and was NOT overwritten. Compile it with 'make texpdf'."

# Compile the canonical hand-maintained LaTeX -> paper/manuscript.pdf (pdflatex + bibtex).
# TEXINPUTS resolves the figures' bare filenames from outputs/figures/; bibtex uses references.bib.
texpdf:
	cd paper && TEXINPUTS="../outputs/figures:$$TEXINPUTS" pdflatex -interaction=nonstopmode -halt-on-error manuscript.tex >/dev/null
	cd paper && bibtex manuscript >/dev/null
	cd paper && TEXINPUTS="../outputs/figures:$$TEXINPUTS" pdflatex -interaction=nonstopmode -halt-on-error manuscript.tex >/dev/null
	cd paper && TEXINPUTS="../outputs/figures:$$TEXINPUTS" pdflatex -interaction=nonstopmode -halt-on-error manuscript.tex >/dev/null
	@rm -f paper/manuscript.aux paper/manuscript.bbl paper/manuscript.blg paper/manuscript.out
	@echo "wrote paper/manuscript.pdf (from canonical paper/manuscript.tex)"

# Compile the standalone supporting-information supplement -> paper/supplementary.pdf.
supp:
	cd paper && TEXINPUTS="../outputs/figures:$$TEXINPUTS" pdflatex -interaction=nonstopmode -halt-on-error supplementary.tex >/dev/null
	cd paper && TEXINPUTS="../outputs/figures:$$TEXINPUTS" pdflatex -interaction=nonstopmode -halt-on-error supplementary.tex >/dev/null
	@rm -f paper/supplementary.aux paper/supplementary.log paper/supplementary.out
	@echo "wrote paper/supplementary.pdf (from paper/supplementary.tex)"

# Editable Word source (PLoS also accepts .docx). PLoS numbered references baked in via
# citeproc + plos.csl; figures embedded. Most reviewer-portable editable format.
docx:
	pandoc paper/manuscript.md --citeproc --csl=paper/plos.csl \
	  --bibliography=paper/references.bib --resource-path=paper:. \
	  -o paper/manuscript.docx
	@echo "wrote paper/manuscript.docx (editable; PLoS numbered refs baked in, figures embedded)"

# --- Deposit archives -------------------------------------------------------- #
# Two artifacts:
#   bundle  -> journal submission package (manuscript + submission-facing aids)
#   deposit -> clean research compendium for Zenodo (reproducibility artifacts only)
# Both set COPYFILE_DISABLE=1, --no-mac-metadata, and exclude AppleDouble (._*/.DS_Store) so
# macOS extended attributes (AppleDouble files AND com.apple.* xattr PAX headers) do not
# pollute the archive, and NEVER place the tarball's own checksum inside the tarball — the
# .sha256 is computed AFTER the archive is closed and lives beside it.

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
	COPYFILE_DISABLE=1 tar --no-mac-metadata --exclude='._*' --exclude='.DS_Store' \
	  -czf submission/doxypep-bystander-submission.tar.gz $$files; \
	shasum -a 256 submission/doxypep-bystander-submission.tar.gz \
	  > submission/doxypep-bystander-submission.tar.gz.sha256; \
	echo "wrote submission/doxypep-bystander-submission.tar.gz (+ .sha256, computed after)"

# Zenodo research compendium — reproducibility artifacts only. NO editorial/process layer
# (no CLAUDE.md/SCAFFOLD.md/STREAM_B_HANDOFF.md, no submission/); NO copyrighted publisher or
# guideline PDFs / transcriptions, and NO AIDSVu XLSX (IQVIA-sourced) — all excluded, with
# provenance travelling via SOURCES.md + CHECKSUMS.md. AIDSVu is retrieved+verified by
# scripts/verify_aidsvu.py before `make all` (download AIDSVu first). See THIRD_PARTY_DATA.md.
DEPOSIT_PATHS = README.md CITATION.cff LICENSE-CODE LICENSE-TEXT THIRD_PARTY_DATA.md \
  REPRODUCIBILITY.md REPRODUCTION_LOG.md Makefile pytest.ini requirements.txt requirements-lock.txt \
  CODEBOOK.md CODEBOOK_streamA.md METHODS_streamB.md ECOLOGICAL_PREREGISTRATION_DRAFT_NOT_REGISTERED.md DECISIONS.md \
  src tests scripts outputs \
  paper/jac \
  paper/manuscript.tex paper/references.bib paper/plos2015.bst paper/preamble.tex paper/plos.csl \
  data/processed data/raw/coding data/raw/literature data/raw/literature_search \
  data/raw/aidsvu/SOURCES.md data/raw/aidsvu/CHECKSUMS.md \
  data/raw/papers/SOURCES.md data/raw/papers/CHECKSUMS.md \
  data/raw/guidelines/SOURCES.md data/raw/guidelines/CHECKSUMS.md

deposit:
	@mkdir -p submission
	@rm -f CHECKSUMS.sha256
	@COPYFILE_DISABLE=1 find $(DEPOSIT_PATHS) -type f \
	  ! -name '._*' ! -name '.DS_Store' ! -name '*.pyc' ! -path '*/__pycache__/*' \
	  ! -name '*.aux' ! -name '*.log' ! -name '*.bbl' ! -name '*.blg' ! -name '*.out' ! -name '*.toc' ! -name '.gitignore' \
	  | LC_ALL=C sort | xargs shasum -a 256 > CHECKSUMS.sha256
	@COPYFILE_DISABLE=1 tar --no-mac-metadata --no-xattrs --exclude='__pycache__' --exclude='*.pyc' \
	  --exclude='._*' --exclude='.DS_Store' \
	  -czf submission/doxy_zenodo_final.tz $(DEPOSIT_PATHS) CHECKSUMS.sha256
	@shasum -a 256 submission/doxy_zenodo_final.tz \
	  > submission/doxy_zenodo_final.tz.sha256
	@echo "wrote submission/doxy_zenodo_final.tz ($$(du -h submission/doxy_zenodo_final.tz | cut -f1); $$(tar tzf submission/doxy_zenodo_final.tz | grep -c .) members)"
	@echo "external checksum beside archive (NOT inside): submission/doxy_zenodo_final.tz.sha256"

# Same compendium as `deposit`, packaged as .zip for portals/OSes that don't open .tz
# (macOS Archive Utility). Identical file set + internal CHECKSUMS.sha256; `zip -X` drops
# extra file attributes (AppleDouble resource forks, extended attributes).
deposit-zip:
	@mkdir -p submission
	@rm -f CHECKSUMS.sha256
	@COPYFILE_DISABLE=1 find $(DEPOSIT_PATHS) -type f \
	  ! -name '._*' ! -name '.DS_Store' ! -name '*.pyc' ! -path '*/__pycache__/*' \
	  ! -name '*.aux' ! -name '*.log' ! -name '*.bbl' ! -name '*.blg' ! -name '*.out' ! -name '*.toc' ! -name '.gitignore' \
	  | LC_ALL=C sort | xargs shasum -a 256 > CHECKSUMS.sha256
	@rm -f submission/doxy_zenodo_final.zip
	@COPYFILE_DISABLE=1 zip -X -r -9 -q submission/doxy_zenodo_final.zip $(DEPOSIT_PATHS) CHECKSUMS.sha256 \
	  -x '*/__pycache__/*' '*.pyc' '*.DS_Store' '*/._*' \
	     '*.aux' '*.log' '*.bbl' '*.blg' '*.out' '*.toc' '*/.gitignore'
	@shasum -a 256 submission/doxy_zenodo_final.zip > submission/doxy_zenodo_final.zip.sha256
	@echo "wrote submission/doxy_zenodo_final.zip ($$(du -h submission/doxy_zenodo_final.zip | cut -f1); $$(unzip -Z1 submission/doxy_zenodo_final.zip | grep -c .) entries)"
	@echo "external checksum beside archive (NOT inside): submission/doxy_zenodo_final.zip.sha256"

clean:
	rm -rf data/interim/* .pytest_cache
	find . -name __pycache__ -type d -prune -exec rm -rf {} +
