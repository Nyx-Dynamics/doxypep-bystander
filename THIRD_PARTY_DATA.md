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

## Redistributed with a rights caveat — CONFIRM BEFORE PUBLIC FREEZE

- **AIDSVu PrEP / PnR datasets** (`data/raw/aidsvu/*.xlsx`). AIDSVu makes state/county
  PrEP/PnR datasets publicly downloadable and its published protocol permits users to
  download datasets for analyses and publications. However, AIDSVu identifies the PrEP source
  as **IQVIA data supplied under a data-sharing agreement** and the site carries an
  **"All Rights Reserved"** notice, so *rehosting the original files* is a distinct question
  from *downloading them for analysis*. These files are therefore **NOT** sublicensed under
  CC BY 4.0.

  **Decision needed before the Zenodo/public freeze — two defensible options:**
  1. Confirm with AIDSVu that redistribution/rehosting of the downloaded files is permitted,
     and note that confirmation here; or
  2. **Exclude** the original XLSX from the public archive and instead ship exact source
     URLs, retrieval dates, SHA-256 hashes (already in `data/raw/aidsvu/CHECKSUMS.md`), and a
     retrieval script — mirroring how the publisher PDFs are handled. This is the safer
     default and is fully reproducible for anyone who downloads AIDSVu themselves.

  Until (1) is confirmed, treat the XLSX as retained for convenience only, under AIDSVu's
  own terms, not under this repository's licenses.

## Authored here (covered by the repository licenses)

- All coded YAML (`data/raw/coding/`), which contains **transcribed values with locators**,
  not the source documents; the coding is our own work.
- All generated outputs (`outputs/`), figures, and processed tables.
