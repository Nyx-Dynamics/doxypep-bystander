"""THE AIDSVu loader — one implementation, used by everything downstream.

Parses the AIDSVu state-level PrEP and PrEP-to-Need (PnR) workbooks into one
tidy state-year frame:

    state, state_abbrev, year,
    prep_users, prep_rate, male_prep_rate,
    prep_rate_stability, male_prep_rate_stability,
    pnr, male_pnr

File quirks handled (see CLAUDE.md and tests/test_aidsvu_loader.py):
  * header junk in rows 1-3; the real header is row 4, data start row 5.
  * column names carry embedded newlines, e.g. 'State\\nPrEP\\nRate'.
  * suppressed / unavailable values are negative sentinels. AIDSVu uses several
    (-1, -2, -8, -9 all observed). Rates, counts and ratios are never
    legitimately negative, so ANY negative in a measure column is treated as
    suppressed and becomes NaN. Never zero -- zero would be a real, wrong value.

Do not re-parse these files ad hoc anywhere else. Import from here.
"""
from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import pandas as pd

# real header lives on the 4th row (0-indexed 3); rows above are title/blurb/blank
_HEADER_ROW = 3
_YEAR_RE = re.compile(r"_(\d{4})[_-]")


def _year_from_name(path: Path) -> int:
    m = _YEAR_RE.search(path.name)
    if not m:
        raise ValueError(f"cannot parse year from filename: {path.name}")
    return int(m.group(1))


def _clean_text(value) -> str:
    """Collapse embedded newlines and runs of whitespace to single spaces.

    Used for both column headers and text cells: the PrEP workbooks carry
    embedded newlines inside *data values* too (e.g. 'New\\nHampshire',
    'Washington,\\nD.C.'), which the PnR workbooks do not. Without this the
    two sources fail to join on state and rows split.
    """
    return re.sub(r"\s+", " ", str(value).replace("\n", " ")).strip()


def _normalise_cols(cols) -> list[str]:
    """Collapse embedded newlines and surrounding whitespace to single spaces."""
    return [_clean_text(c) for c in cols]


def _suppress_negatives(s: pd.Series) -> pd.Series:
    """Coerce to numeric; any negative sentinel -> NaN (never 0)."""
    s = pd.to_numeric(s, errors="coerce")
    return s.mask(s < 0, np.nan)


def _read_raw(path: Path) -> pd.DataFrame:
    df = pd.read_excel(path, header=_HEADER_ROW, engine="openpyxl")
    df.columns = _normalise_cols(df.columns)
    # drop rows with no state name (trailing notes / blanks)
    df = df[df["State"].notna()].copy()
    return df


def load_prep_file(path: Path | str) -> pd.DataFrame:
    """Load one AIDSVu_State_PrEP_YYYY_*.xlsx into a tidy frame."""
    path = Path(path)
    raw = _read_raw(path)
    out = pd.DataFrame({
        "state": raw["State"].map(_clean_text),
        "state_abbrev": raw["State Abbreviation"].map(_clean_text),
        "year": _year_from_name(path),
        "prep_users": _suppress_negatives(raw["State PrEP Users"]),
        "prep_rate": _suppress_negatives(raw["State PrEP Rate"]),
        "male_prep_rate": _suppress_negatives(raw["Male PrEP Rate"]),
        "prep_rate_stability": raw.get("State PrEP Rate Stability"),
        "male_prep_rate_stability": raw.get("Male PrEP Rate Stability"),
    })
    return out.reset_index(drop=True)


def load_pnr_file(path: Path | str) -> pd.DataFrame:
    """Load one AIDSVu_State_PnR_YYYY_*.xlsx into a tidy frame."""
    path = Path(path)
    raw = _read_raw(path)
    out = pd.DataFrame({
        "state": raw["State"].map(_clean_text),
        "state_abbrev": raw["State Abbreviation"].map(_clean_text),
        "year": _year_from_name(path),
        "pnr": _suppress_negatives(raw["State PrEP-to-Need Ratio"]),
        "male_pnr": _suppress_negatives(raw["Male PrEP-to-Need Ratio"]),
    })
    return out.reset_index(drop=True)


def load_aidsvu(raw_dir: Path | str) -> pd.DataFrame:
    """Load and merge every state PrEP and PnR file under ``raw_dir``.

    Returns one row per (state, year) with PrEP and PnR measures joined.
    """
    raw_dir = Path(raw_dir)
    prep_files = sorted(raw_dir.glob("AIDSVu_State_PrEP_*.xlsx"))
    pnr_files = sorted(raw_dir.glob("AIDSVu_State_PnR_*.xlsx"))
    if not prep_files:
        raise FileNotFoundError(f"no AIDSVu_State_PrEP_*.xlsx under {raw_dir}")

    prep = pd.concat([load_prep_file(p) for p in prep_files], ignore_index=True)
    key = ["state", "state_abbrev", "year"]

    if pnr_files:
        pnr = pd.concat([load_pnr_file(p) for p in pnr_files], ignore_index=True)
        df = prep.merge(pnr, on=key, how="outer")
    else:
        df = prep.assign(pnr=np.nan, male_pnr=np.nan)

    df = df.sort_values(["state", "year"]).reset_index(drop=True)
    return df


if __name__ == "__main__":  # quick manual smoke check
    here = Path(__file__).resolve().parents[2]
    panel = load_aidsvu(here / "data" / "raw" / "aidsvu")
    print(f"panel shape: {panel.shape}")
    print(f"year coverage: {int(panel.year.min())}-{int(panel.year.max())}")
    print(panel.head())
