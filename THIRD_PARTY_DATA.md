# Third-party data — rights and provenance

The licenses in this repository (LICENSE-CODE, MIT; LICENSE-TEXT, CC BY 4.0) cover only
material **authored for this work**. They do **not** relicense externally-sourced inputs.
This file records the provenance and rights status of every third-party input, and what is
and is not redistributed here.

## Not redistributed (provenance travels; retrieve from source)

- **Publisher journal PDFs / DOCX** (`data/raw/papers/`) — copyrighted articles
  (NEJM, Lancet ID, CID, JAC, BMC, etc.). **Excluded** from this repository and its history;
  each is retrievable by the DOI/PMID/URL listed in `data/raw/papers/SOURCES.md` and pinned
  by SHA-256 in `data/raw/papers/CHECKSUMS.md`. The analysis reads coded YAML, not the PDFs.
- **Guideline PDFs** (`data/raw/guidelines/`) — mixed copyright (some US-government works are
  public domain; others are not). **Excluded**; provenance in
  `data/raw/guidelines/SOURCES.md` + `CHECKSUMS.md`.
- **Verbatim conference transcriptions** (CROI abstract/slides) — **excluded**; source
  identifiers in `data/raw/papers/SOURCES.md`.

- **AIDSVu PrEP / PnR datasets** (`data/raw/aidsvu/*.xlsx`) — **NOT redistributed.** AIDSVu
  makes State-level PrEP/PnR datasets freely downloadable for analysis and publication, but
  identifies the PrEP source as **IQVIA data under a data-sharing agreement** and carries an
  **"All Rights Reserved"** notice, so *rehosting the original files* is a distinct question
  from *downloading them for analysis*. We therefore **exclude** the XLSX from this repository
  and its Zenodo deposit and instead ship the source portal URL, retrieval date, exact
  filenames, byte sizes, and SHA-256 hashes (`data/raw/aidsvu/SOURCES.md` + `CHECKSUMS.md`)
  with a **fetch-and-verify script** (`scripts/fetch_aidsvu.py`) — mirroring how the publisher
  PDFs are handled, and fully reproducible for anyone who downloads AIDSVu themselves.
  `make all` requires these files to be fetched and verified first.

## Authored here (covered by the repository licenses)

- All coded YAML (`data/raw/coding/`), which contains **transcribed values with locators**,
  not the source documents; the coding is our own work.
- All generated outputs (`outputs/`), figures, and processed tables.
