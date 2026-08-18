"""Tests for the AIDSVu loader — written BEFORE the implementation.

These pin the file quirks documented in CLAUDE.md and discovered on inspection:
  * header junk in rows 1-3, real header on row 4, data from row 5
  * column names carry embedded newlines, e.g. 'State\\nPrEP\\nRate'
  * suppressed / unavailable values are coded as negative sentinels
    (-1, -2, -8, -9 all observed) and MUST become NaN, never 0.

The unit tests build synthetic .xlsx fixtures that reproduce the quirks so they
run without the real data. One integration test loads the real raw/ tree if it
is present, and is skipped otherwise.
"""
from pathlib import Path

import numpy as np
import openpyxl
import pandas as pd
import pytest

from src.loaders.aidsvu import load_aidsvu, load_prep_file, load_pnr_file

RAW = Path(__file__).resolve().parents[1] / "data" / "raw" / "aidsvu"


# --------------------------------------------------------------------------- #
# fixture builders — reproduce the real file layout                            #
# --------------------------------------------------------------------------- #
def _write_sheet(path, title, header, rows):
    """Row1 title, row2 methods blurb, row3 blank, row4 header, row5+ data."""
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Data"
    ws.append([title])
    ws.append(["For additional information ... see the Data Methods ..."])
    ws.append([])
    ws.append(header)
    for r in rows:
        ws.append(r)
    wb.save(path)


PREP_HEADER = [
    "GEO\nID", "State\nAbbreviation", "State",
    "State\nPrEP\nUsers", "State\nPrEP\nRate", "State\nPrEP\nRate\nStability",
    "Male\nPrEP\nUsers", "Male\nPrEP\nRate", "Male\nPrEP\nRate\nStability",
]
PNR_HEADER = [
    "GEO ID", "State\nAbbreviation", "State",
    "State\nPrEP-to-Need\nRatio", "Male\nPrEP-to-Need\nRatio",
]


@pytest.fixture
def prep_2022(tmp_path):
    rows = [
        [1, "AL", "Alabama", 3401, 80, "Y", 3111, 151, "Y"],
        [2, "AK", "Alaska", 690, 114, "Y", 651, 203, "Y"],
        # every negative sentinel appears; none may survive as a number
        [4, "AZ", "Arizona", -1, -2, "N", -8, -9, "N"],
        # PrEP workbooks embed newlines inside the state VALUE, PnR ones do not
        [33, "NH", "New\nHampshire", 500, 90, "Y", 470, 170, "Y"],
    ]
    p = tmp_path / "AIDSVu_State_PrEP_2022_20260525.xlsx"
    _write_sheet(p, "2022 State PrEP Data - AIDSVu", PREP_HEADER, rows)
    return p


@pytest.fixture
def pnr_2022(tmp_path):
    rows = [
        [1, "AL", "Alabama", 4.94, 5.85],
        [2, "AK", "Alaska", 18.65, 19.73],
        [4, "AZ", "Arizona", -1, -8],
        [33, "NH", "New Hampshire", 6.10, 6.40],  # no embedded newline here
    ]
    p = tmp_path / "AIDSVu_State_PnR_2022_20260525.xlsx"
    _write_sheet(p, "2022 State PnR Data - AIDSVu", PNR_HEADER, rows)
    return p


# --------------------------------------------------------------------------- #
# header offset + newline column names                                         #
# --------------------------------------------------------------------------- #
def test_header_offset_finds_real_columns(prep_2022):
    df = load_prep_file(prep_2022)
    # If the loader read the wrong header row, 'Alabama' etc. would be missing.
    assert {"Alabama", "Alaska", "Arizona"} <= set(df["state"])
    assert "prep_rate" in df.columns
    assert "male_prep_rate" in df.columns
    # male PrEP users is the doxy-PEP exposure proxy used by Phase 0
    assert "male_prep_users" in df.columns
    assert df.loc[df.state == "Alabama", "male_prep_users"].iloc[0] == 3111


def test_newline_columns_are_normalised(prep_2022):
    df = load_prep_file(prep_2022)
    # No surviving column may contain a raw newline from the embedded-newline header.
    assert not any("\n" in c for c in df.columns)
    assert df.loc[df.state == "Alabama", "prep_rate"].iloc[0] == 80


def test_year_parsed_from_filename(prep_2022):
    df = load_prep_file(prep_2022)
    assert (df["year"] == 2022).all()


# --------------------------------------------------------------------------- #
# the sentinel contract: suppressed -> NaN, never 0                            #
# --------------------------------------------------------------------------- #
def test_negative_sentinels_become_nan_not_zero(prep_2022):
    df = load_prep_file(prep_2022)
    az = df.loc[df.state == "Arizona"].iloc[0]
    for col in ["prep_users", "prep_rate", "male_prep_rate"]:
        assert pd.isna(az[col]), f"{col} should be NaN for suppressed AZ"
        assert az[col] != 0


def test_no_negative_values_survive_in_measures(prep_2022, pnr_2022):
    prep = load_prep_file(prep_2022)
    pnr = load_pnr_file(pnr_2022)
    for df, cols in [(prep, ["prep_users", "prep_rate", "male_prep_rate"]),
                     (pnr, ["pnr", "male_pnr"])]:
        for c in cols:
            vals = df[c].dropna()
            assert (vals >= 0).all(), f"negative sentinel leaked into {c}"


def test_valid_values_preserved(pnr_2022):
    df = load_pnr_file(pnr_2022)
    assert df.loc[df.state == "Alabama", "pnr"].iloc[0] == pytest.approx(4.94)
    assert df.loc[df.state == "Alaska", "male_pnr"].iloc[0] == pytest.approx(19.73)


# --------------------------------------------------------------------------- #
# combined tidy panel                                                          #
# --------------------------------------------------------------------------- #
def test_load_aidsvu_merges_prep_and_pnr(tmp_path, prep_2022, pnr_2022):
    # place both fixtures in one dir the combined loader can scan
    raw = tmp_path
    df = load_aidsvu(raw)
    assert {"state", "year", "prep_users", "prep_rate",
            "male_prep_rate", "pnr", "male_pnr"} <= set(df.columns)
    # one row per state-year, PrEP and PnR joined on the same key
    al = df.loc[(df.state == "Alabama") & (df.year == 2022)].iloc[0]
    assert al["prep_rate"] == 80
    assert al["pnr"] == pytest.approx(4.94)
    assert not df.duplicated(subset=["state", "year"]).any()


def test_embedded_newline_in_state_value_does_not_split_join(prep_2022, pnr_2022):
    """'New\\nHampshire' (PrEP) must join to 'New Hampshire' (PnR), not split."""
    df = load_aidsvu(prep_2022.parent)
    assert not any("\n" in s for s in df["state"])
    nh = df.loc[df.state == "New Hampshire"]
    assert len(nh) == 1  # one row, not two phantom halves
    assert nh.iloc[0]["prep_rate"] == 90
    assert nh.iloc[0]["pnr"] == pytest.approx(6.10)
    # 4 distinct states in the fixtures, not 5 (NH would double without the fix)
    assert df["state"].nunique() == 4


# --------------------------------------------------------------------------- #
# integration — real data if present                                          #
# --------------------------------------------------------------------------- #
@pytest.mark.skipif(not RAW.exists() or not any(RAW.glob("*.xlsx")),
                    reason="raw AIDSVu data not present")
def test_real_data_shape_and_coverage():
    df = load_aidsvu(RAW)
    assert df["year"].min() == 2012
    assert df["year"].max() == 2025
    # 52 geographies (50 states + DC + PR) x 14 years
    assert df.groupby("year").size().min() >= 50
    # sentinel contract holds on real data too
    for c in ["prep_users", "prep_rate", "male_prep_rate", "pnr", "male_pnr"]:
        vals = df[c].dropna()
        assert (vals >= 0).all()
