# Reproduction log — clean run in the locked reference environment

This release (git tag `v1.0.0`) was regenerated end-to-end in a fresh virtual environment
built from `requirements-lock.txt`, on 2026-08-23 (UTC), Darwin arm64. The manuscript is the
canonical PLoS Biology (Meta-Research) LaTeX source (`paper/manuscript.tex`), whose
19-reference bibliography is compiled with `plos2015.bst`; `paper/manuscript.md` is a
superseded draft and is no longer in the deposit.

## Environment

```
Python 3.12.12
matplotlib==3.10.7 numpy==2.3.5 openpyxl==3.1.5 pandas==2.3.3 pydantic==2.12.4 pytest==9.1.1 PyYAML==6.0.3 scipy==1.16.3 statsmodels==0.14.6
```

External tools: `make pdf` builds the canonical LaTeX (`paper/manuscript.tex`) with TeX Live
**pdflatex + bibtex** (`plos2015.bst`); `make docx` uses **pandoc**.

## Sequence and result

```
python3 -m venv .venv-lock && .venv-lock/bin/pip install -r requirements-lock.txt
python3 scripts/verify_aidsvu.py         # 28/28 AIDSVu inputs verified against frozen SHA-256
make all PY=.venv-lock/bin/python         # 111 passed in ~168s; all outputs/figures regenerated
make pdf                                  # paper/manuscript.pdf rebuilt from paper/manuscript.tex (pdflatex + bibtex)
make supp                                 # paper/supplementary.pdf (S1 Text) rebuilt
git status --short                        # (empty — working tree clean at release)
```

- Full test suite: **111 passed** (92 fast + 19 `@pytest.mark.slow`; run `pytest -m "not slow"` for the fast subset).
- Reconfirmed on 2026-08-23 immediately before the final build: `pytest -m "not slow"` →
  **92 passed, 19 slow-deselected** in ~4 s (AIDSVu inputs present; when absent, the 7
  AIDSVu-dependent tests skip rather than fail, i.e. 85 passed / 7 skipped).
- The Monte-Carlo modules (`coverage_null`, `three_outbreak_fit`) are fixed-seed and
  **deterministic** — regeneration is byte-identical in this environment.
- The commit this release corresponds to is the one `git tag v1.0.0` points at; that SHA is
  recorded in the Zenodo record's description.

Anyone can reproduce: install `requirements-lock.txt`, download the AIDSVu inputs (see
`THIRD_PARTY_DATA.md`), run `scripts/verify_aidsvu.py`, then `make all` / `make pdf`.
