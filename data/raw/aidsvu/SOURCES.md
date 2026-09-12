# AIDSVu inputs — provenance (files NOT redistributed)

The AIDSVu State-level datasets used by Stream C are **not** included in this repository or
its Zenodo deposit (IQVIA-sourced; "All Rights Reserved" — see `THIRD_PARTY_DATA.md`). Their
provenance travels here so anyone can reproduce the exact inputs.

- **Source:** AIDSVu datasets portal, https://aidsvu.org/resources/#/datasets → **State**
  level → **PrEP**, **PrEP-to-Need Ratio (PnR)**, and **Prevalence** (people living with HIV)
  datasets.
- **Retrieved:** PrEP/PnR 2026-05-25 (`_20260525` suffix); State Prevalence 2024 on
  2026-08-06 (`-20260806` suffix), added for the combined PrEP+PLWH Stream C analysis.
- **Files required:** 29 (State PrEP 2012–2025, State PnR 2012–2025, and State Prevalence
  2024); exact names, byte sizes, and SHA-256 hashes are frozen in `CHECKSUMS.md` beside this
  file.
- **Download + verify:** download the files from the portal, then `python3 scripts/verify_aidsvu.py` (downloads are portal-based, so
  place the files here keeping their exact names; the script verifies them against the frozen
  hashes). `make all` requires these files to be present and verified.
- **Terms:** AIDSVu permits downloading its datasets for analyses and publications; it does
  not grant rehosting of the original files, which is why they are excluded here rather than
  redistributed.
