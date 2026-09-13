"""Tests for the combined PrEP+PLWH primary dilution model
(src/feasibility/dilution_plwh.py) — the manuscript's primary Stream C
specification. Real-data cells are guarded on the (not-redistributed) AIDSVu XLSX.
"""
from pathlib import Path

import pytest

from src.feasibility import dilution as D
from src.feasibility import dilution_plwh as P

_AIDSVU = Path(__file__).resolve().parents[1] / "data/raw/aidsvu"
HAVE_AIDSVU = _AIDSVU.exists() and any(_AIDSVU.glob("*.xlsx"))
pytestmark = pytest.mark.skipif(not HAVE_AIDSVU, reason="AIDSVu XLSX not present")

YEAR = 2024


@pytest.fixture(scope="module")
def data():
    from src.loaders.aidsvu import load_aidsvu, load_prevalence
    return load_aidsvu(_AIDSVU), load_prevalence(_AIDSVU)


def test_msm_frac_zero_reproduces_preponly(data):
    """msm_frac=0 must reproduce the PrEP-only construction (dilution.state_dilution)."""
    prep, prev = data
    fb_plwh, _ = P._best_f(prep, prev, YEAR, 0.35, D.REALISTIC_KAPPA, 0.0)
    sd = D.state_dilution(prep, YEAR, 0.35, D.REALISTIC_KAPPA)
    assert fb_plwh == pytest.approx(sd["f"].max())


def test_plwh_increases_f(data):
    """Adding PLWH (msm_frac>0) raises the exposed fraction."""
    prep, prev = data
    f0, _ = P._best_f(prep, prev, YEAR, 0.35, D.REALISTIC_KAPPA, 0.0)
    f1, _ = P._best_f(prep, prev, YEAR, 0.35, D.REALISTIC_KAPPA, 1.0)
    assert f1 > f0


def test_plwh_lowers_rr_needed(data):
    """A larger exposed fraction lowers the RR a system would need to detect."""
    prep, prev = data
    r0 = P.realistic_rr(prep, prev, YEAR, 0.0)["rr_panel_deff1"]
    r1 = P.realistic_rr(prep, prev, YEAR, 1.0)["rr_panel_deff1"]
    assert r1 < r0


def test_frozen_primary_values(data):
    """The frozen primary (msm_frac=1.0) realistic-cell and best-cell values."""
    prep, prev = data
    ds = P.dose_sensitivity(prep, prev, YEAR, 1.00)
    row = ds[ds["d"] == 0.50].iloc[0]
    assert row["realistic_panel_deff1"] == pytest.approx(6.31, rel=1e-2)
    assert row["realistic_panel_deff25"] == pytest.approx(27.5, rel=1e-2)
    assert row["best_single_comp"] == pytest.approx(1.79, rel=1e-2)
    assert row["best_panel_deff1"] == pytest.approx(1.03, rel=1e-2)


def test_dose_sensitivity_monotone_and_limit(data):
    """RR_needed-1 scales as 1/d, so RR_needed decreases as d rises; d=1.0 gives
    the ~3.65 realistic lower bound flagged in the manuscript/supplement."""
    prep, prev = data
    ds = P.dose_sensitivity(prep, prev, YEAR, 1.00).set_index("d")
    col = "realistic_panel_deff1"
    assert ds.loc[0.50, col] > ds.loc[0.75, col] > ds.loc[1.00, col]
    assert ds.loc[1.00, col] == pytest.approx(3.65, rel=1e-2)


def test_no_soge_label_in_shipped_figure_writer():
    """The production figure writer must not carry the obsolete 'Soge' label."""
    src = (Path(__file__).resolve().parents[1]
           / "src/feasibility/plots_plwh.py").read_text()
    assert "Soge" not in src
