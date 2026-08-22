#!/usr/bin/env python3
"""Fetch-and-verify the AIDSVu State PrEP / PnR inputs.

The AIDSVu State-level datasets are **not redistributed** in this repository or its Zenodo
deposit (they are IQVIA-sourced and carry an "All Rights Reserved" notice; see
THIRD_PARTY_DATA.md). They are, however, freely downloadable for analysis/publication from
AIDSVu's datasets portal. This script records the exact provenance and verifies any files you
place in ``data/raw/aidsvu/`` against the SHA-256 hashes frozen in
``data/raw/aidsvu/CHECKSUMS.md`` — so a third party can reproduce the exact inputs.

Source (portal, not a stable direct link per file):
    https://aidsvu.org/resources/#/datasets   ->  "State" -> PrEP and PrEP-to-Need (PnR)
Retrieved for this study: 2026-05-25 (encoded in each filename's _20260525 suffix).

Usage:
    python3 scripts/fetch_aidsvu.py            # verify present files against the hashes
    python3 scripts/fetch_aidsvu.py --list     # print the exact files + hashes needed

Exit 0 iff every required file is present and matches its recorded SHA-256. Otherwise it
lists what is missing/mismatched with download instructions and exits non-zero.
"""
from __future__ import annotations

import argparse
import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AIDSVU = ROOT / "data/raw/aidsvu"
CHECKSUMS = AIDSVU / "CHECKSUMS.md"
PORTAL = "https://aidsvu.org/resources/#/datasets"
RETRIEVED = "2026-05-25"

ROW = re.compile(r"^\|\s*`([^`]+\.xlsx)`\s*\|\s*(\d+)\s*\|\s*`([0-9a-f]{64})`\s*\|", re.M)


def expected() -> list[tuple[str, int, str]]:
    if not CHECKSUMS.exists():
        sys.exit(f"missing {CHECKSUMS} — cannot determine required files")
    return ROW.findall(CHECKSUMS.read_text())


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--list", action="store_true", help="print required files + hashes and exit")
    args = ap.parse_args()

    files = expected()
    if not files:
        sys.exit("no file rows parsed from CHECKSUMS.md")

    if args.list:
        print(f"# AIDSVu State PrEP/PnR — download from {PORTAL} (retrieved {RETRIEVED})")
        print(f"# place these {len(files)} files in {AIDSVU.relative_to(ROOT)}/ :")
        for name, size, digest in files:
            print(f"{digest}  {name}  ({size} bytes)")
        return 0

    AIDSVU.mkdir(parents=True, exist_ok=True)
    missing, mismatch, ok = [], [], []
    for name, size, digest in files:
        p = AIDSVU / name
        if not p.exists():
            missing.append(name)
        elif sha256(p) != digest:
            mismatch.append(name)
        else:
            ok.append(name)

    print(f"AIDSVu inputs: {len(ok)}/{len(files)} present and verified.")
    if mismatch:
        print("\nHASH MISMATCH (re-download):")
        for n in mismatch:
            print(f"  - {n}")
    if missing:
        print(f"\nMISSING {len(missing)} file(s). Download the State PrEP and PrEP-to-Need")
        print(f"(PnR) datasets, all years, from:\n  {PORTAL}\n"
              f"then place them (keeping the exact filenames) in {AIDSVU.relative_to(ROOT)}/ and re-run.")
        for n in missing:
            print(f"  - {n}")
    if missing or mismatch:
        return 1
    print("All AIDSVu inputs verified against the frozen SHA-256 hashes. `make all` can run.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
