# Reproduction log — v2.0.0 (JAC release)

Current release. The v1.0.0 (PLOS-era) log is preserved as
`REPRODUCTION_LOG_v1.0.0.md`.

- **Release version:** v2.0.0
- **Zenodo DOI:** 10.5281/zenodo.22725070 (supersedes v1.0.0, 10.5281/zenodo.22051031)
- **Date of regeneration:** 2026-09-12
- **Branch:** `main` (release commit is the child of `3d315f3` that adds this log; see `git log`)
- **Environment:** CPython **3.12.12**, macOS; `pip install -r requirements-lock.txt`

## Commands run

```
python3 -m pytest -q                 # full suite
python3 scripts/jac_wordcount.py     # JAC word count -> paper/jac/JAC_wordcount_report.md
make jac                             # compile canonical JAC manuscript + supplement (pdflatex + bibtex)
make deposit-zip                     # regenerate CHECKSUMS.sha256 + package the compendium
```

`make all` (full analysis regeneration) was **not** re-run in this hygiene pass; it
requires the manually-downloaded AIDSVu inputs (not redistributed — see
`THIRD_PARTY_DATA.md`) and regenerates the outputs already present. The analysis
code, coded data, and validated outputs are unchanged in this pass; only
documentation, canonical-file aliases, the build system, and the archive were
touched.

## Results

- **Tests:** `pytest -q` → **111 passed** (~161 s). No failures; no tests skipped in
  this run (the `@pytest.mark.slow` modules ran).
- **JAC manuscript build:** `pdflatex`+`bibtex` clean — **0 undefined references**,
  0 undefined control sequences; supplement compiles clean.
- **Word counts** (`scripts/jac_wordcount.py`): main text **3412 / 3500**
  (Introduction–Discussion); synopsis **234 / 250**.
- **Canonical aliases:** `JAC_manuscript.{tex,pdf}` / `JAC_supplement.{tex,pdf}`
  verified **byte-identical** to the `*_v3.*` sources (`cmp`).
- **Checksum verification:** `CHECKSUMS.sha256` — **157 files, 0 mismatches**.

## Data intentionally not redistributed

AIDSVu State PrEP/PnR (release 20260525) and State Prevalence 2024 (release
20260806); publisher and guideline PDFs; verbatim conference transcriptions. All
carry SHA-256 hashes + source provenance in the respective `SOURCES.md` /
`CHECKSUMS.md`, per `THIRD_PARTY_DATA.md`.

## Archive

`submission/doxy_zenodo_final.zip` — the exact final SHA-256 is recorded in
`submission/doxy_zenodo_final.zip.sha256`, computed **after** packaging and kept
**external** to the archive by design (the archive never contains its own checksum).
The internal `CHECKSUMS.sha256` lists per-file hashes for every archived file.
