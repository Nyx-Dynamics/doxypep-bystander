# Reproducibility

Everything in this compendium regenerates from public inputs by one command. No
participant-level trial data are used or required.

## Environment

- Python 3.11+ (validated on CPython 3.12.12; also exercised under 3.13).
- `pip install -r requirements-lock.txt` for the exact validated versions
  (`requirements.txt` keeps broad bounds for normal use).
- `make pdf` builds the canonical LaTeX source (`paper/manuscript.tex`) and needs a TeX Live
  **pdflatex** + **bibtex** on the PATH (`plos2015.bst` ships in `paper/`). `make docx` still uses **pandoc**.

## One command

```
python3 scripts/verify_aidsvu.py  # verify manually-downloaded AIDSVu inputs (not redistributed)
make all                          # runs the full pytest suite, then regenerates outputs/figures
make pdf                           # builds paper/manuscript.pdf from paper/manuscript.tex (pdflatex + bibtex + plos2015.bst)
```

The AIDSVu State PrEP/PnR datasets are **not** redistributed (IQVIA-sourced; see
`THIRD_PARTY_DATA.md`). `scripts/verify_aidsvu.py` records their source portal, retrieval date,
and per-file SHA-256, and verifies the files you place in `data/raw/aidsvu/`. `make all`
requires them present and verified.

`make all` is test-gated: the suite must pass before outputs regenerate. Each coded value
carries a page/table locator and the builder fails on a missing locator rather than emitting
a null. Analysis decisions were logged with dates, before results, in `DECISIONS.md`.

## Expected runtime (the honest numbers)

The complete suite is 111 tests. **92 are fast** (structural/unit checks) and finish in a few
seconds. **19 are computationally heavy** and are marked `@pytest.mark.slow` (see
`pytest.ini`): the exact-Fisher rejection-region enumeration in `tests/test_detectability.py`
(no large-sample shortcut at these small counts) and the Monte-Carlo Type-I / parametric-
bootstrap model-selection tests in `tests/test_clustering_detectability.py`.

- **Fast structural check** (seconds): `pytest -m "not slow"`
- **The heavy tests only:** `pytest -m slow`
- **Everything** (what `make all` runs): `pytest`

Wall-clock for the full suite is roughly **~3 minutes on the author's reference machine**
(CPython 3.12.12, `requirements-lock.txt`) but **considerably longer on resource-constrained
CI/containers** — the two slow modules can each take several minutes there, so budget
accordingly or run `-m "not slow"` for a quick check. A full clean-extraction `make all`
(tests + all output/figure regeneration) completes end-to-end; budget ~5–10 minutes depending
on the machine.

## Third-party inputs

See `THIRD_PARTY_DATA.md`. Publisher PDFs and guideline PDFs are **not** redistributed
(provenance travels via `SOURCES.md` + `CHECKSUMS.md`); the analysis reads coded YAML and
public datasets, not the PDFs. The AIDSVu XLSX files carry a rights caveat documented there.
