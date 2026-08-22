# Reproducibility

Everything in this compendium regenerates from public inputs by one command. No
participant-level trial data are used or required.

## Environment

- Python 3.11+ (validated on CPython 3.12.12; also exercised under 3.13).
- `pip install -r requirements-lock.txt` for the exact validated versions
  (`requirements.txt` keeps broad bounds for normal use).
- `make pdf` additionally needs **pandoc** and a TeX Live **pdflatex** on the PATH.

## One command

```
make all      # runs the full pytest suite, then regenerates every output, table, and figure
make pdf       # builds paper/manuscript.pdf (pandoc + citeproc + plos.csl + pdflatex)
```

`make all` is test-gated: the suite must pass before outputs regenerate. Each coded value
carries a page/table locator and the builder fails on a missing locator rather than emitting
a null. Analysis decisions were logged with dates, before results, in `DECISIONS.md`.

## Expected runtime (the honest numbers)

The full `pytest` suite is **the complete suite** (currently 111 tests) and takes roughly
**2.5–3 minutes** on a laptop. Most modules finish in seconds; two are deliberately
compute-heavy and dominate the wall-clock:

- `tests/test_detectability.py` — exact-Fisher rejection-region enumeration (no large-sample
  shortcut at these small counts). This is the single slowest module and can exceed ~150 s on
  a constrained machine.
- the clustering / parametric-bootstrap tests (`coverage_null`, `three_outbreak_fit`,
  `dejong_sigma`) — Monte-Carlo Type-I and bootstrap model-selection.

If you only want a fast structural check, run everything except those:

```
pytest -q --ignore=tests/test_detectability.py --ignore=tests/test_clustering_detectability.py
```

Then run the two heavy modules separately with a generous timeout. A full clean-extraction
`make all` completes end-to-end; budget ~5 minutes including figure regeneration.

## Third-party inputs

See `THIRD_PARTY_DATA.md`. Publisher PDFs and guideline PDFs are **not** redistributed
(provenance travels via `SOURCES.md` + `CHECKSUMS.md`); the analysis reads coded YAML and
public datasets, not the PDFs. The AIDSVu XLSX files carry a rights caveat documented there.
