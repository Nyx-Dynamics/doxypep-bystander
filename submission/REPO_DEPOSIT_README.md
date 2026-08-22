# doxypep-bystander — repository deposit

This archive is the code-and-data deposit accompanying the manuscript *"Monitoring That the
Instrument Cannot Provide: Measurement Inheritance and Tetracycline-Resistant
Staphylococcus aureus in Doxycycline Post-Exposure Prophylaxis"* (A. C. Demidont). It is the
Zenodo-citable snapshot that the manuscript's data-and-code-availability statement points to.

## Reproduce

```
pip install -r requirements.txt      # Python 3.11; pandas, statsmodels, scipy, matplotlib
make all                             # test-gated: the complete pytest suite, then regenerate every output/figure
make pdf                             # rebuild paper/manuscript.pdf (needs pandoc + pdflatex)
```

Every coded value carries a page/table locator; the builder fails on a missing locator
rather than emitting a null. Analysis decisions are logged, with dates and before results,
in `DECISIONS.md`.

## What is included

- `src/`, `tests/`, `Makefile`, `requirements.txt` — all analysis code and its test suite
- `paper/` — manuscript source (`manuscript.md`, `references.bib`, `preamble.tex`) and the
  built `manuscript.pdf`
- `outputs/` — every regenerated result doc, table, and figure; plus `gap_register.md` and
  `citation_verification.md`
- `submission/` — cover letter, reviewer guide, response-to-anticipated-reviews, manifest
- `data/processed/` — the coded corpus (generated from the coding YAML)
- `data/raw/aidsvu/` — public AIDSVu PrEP/PnR panels (the only outcome-adjacent inputs)
- `data/raw/coding/` — the coded source YAML: one file per document, each value locator-pinned
- `data/raw/literature/`, `data/raw/literature_search/` — the frozen PubMed snapshots
- documentation: `README.md`, `CLAUDE.md`, `CODEBOOK*.md`, `METHODS_streamB.md`,
  `SCAFFOLD.md`, `PREREGISTRATION.md`, `STREAM_B_HANDOFF.md`

## What is deliberately NOT included, and why

The primary-source **publisher PDFs and DOCX** (`data/raw/papers/`, `data/raw/guidelines/`)
and the verbatim conference **transcriptions** are copyrighted third-party works and are not
redistributed. Their provenance travels instead as **SHA-256 checksums and source locators**
in `data/raw/papers/CHECKSUMS.md`, `data/raw/papers/SOURCES.md`,
`data/raw/guidelines/CHECKSUMS.md`, and `data/raw/guidelines/SOURCES.md`. Each is a published
article, guideline, or public presentation retrievable by its DOI/PMID/URL as listed. The
analysis reads the coded YAML and the public datasets, not the PDFs, so reproduction does not
require them.

## License

No `LICENSE` file is present in this snapshot. Before minting the Zenodo DOI, add a license
(e.g. MIT or BSD-3-Clause for the code, CC-BY-4.0 for the text/data) so downstream reuse
terms are explicit.

## Integrity

`submission/CHECKSUMS.sha256` pins the submission-facing bundle; this archive's own
checksum is `submission/doxypep-bystander-repo.tar.gz.sha256`.
