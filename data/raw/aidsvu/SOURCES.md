# AIDSVu inputs — provenance (files NOT redistributed)

The AIDSVu State-level datasets used by Stream C are **not** included in this repository or
its Zenodo deposit (IQVIA-sourced; "All Rights Reserved" — see `THIRD_PARTY_DATA.md`). Their
provenance travels here so anyone can reproduce the exact inputs.

- **Source:** AIDSVu datasets portal, https://aidsvu.org/resources/#/datasets → **State**
  level → **PrEP** and **PrEP-to-Need Ratio (PnR)** datasets, all available years.
- **Retrieved:** 2026-05-25 (encoded as the `_20260525` suffix in each filename).
- **Files required:** 28 (State PrEP 2012–2025 and State PnR 2012–2025); exact names, byte
  sizes, and SHA-256 hashes are frozen in `CHECKSUMS.md` beside this file.
- **Retrieve + verify:** `python3 scripts/fetch_aidsvu.py` (downloads are portal-based, so
  place the files here keeping their exact names; the script verifies them against the frozen
  hashes). `make all` requires these files to be present and verified.
- **Terms:** AIDSVu permits downloading its datasets for analyses and publications; it does
  not grant rehosting of the original files, which is why they are excluded here rather than
  redistributed.
