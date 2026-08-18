"""Tests for the metro-level Phase 0 gate (src/feasibility/dilution_metro.py)."""
import pytest

from src.feasibility import dilution_metro as M
from src.feasibility import dilution as D


def test_required_f_inverts_rr_needed():
    """f_required is exactly the f at which RR_needed == RR_SOGE."""
    r0, n = 0.10, 10_000
    f_req = M.required_f(r0, n)
    assert D.rr_needed(M.mde_proportion(r0, n), f_req, r0) == pytest.approx(D.RR_SOGE)


def test_density_and_required_rate_are_consistent():
    """A geography at exactly rate_required should realise f_required."""
    r0, n, uptake, kappa = 0.10, 10_000, 0.55, 3.0
    rate = M.required_male_prep_rate(r0, n, uptake, kappa)
    f = M.density_from_rate(rate, uptake, kappa)
    assert f == pytest.approx(M.required_f(r0, n))


def test_required_rate_falls_with_enrichment_and_isolates():
    base = M.required_male_prep_rate(0.10, 1_000, 0.55, 1.0)
    assert M.required_male_prep_rate(0.10, 1_000, 0.55, 5.0) < base   # more kappa
    assert M.required_male_prep_rate(0.10, 100_000, 0.55, 1.0) < base  # more N


@pytest.mark.skipif(
    not (M.Path(__file__).resolve().parents[1] / "data/raw/aidsvu").exists(),
    reason="raw AIDSVu data not present")
def test_real_metro_gate_fails_and_dc_is_densest():
    root = M.Path(__file__).resolve().parents[1]
    df = M.load_aidsvu(root / "data/raw/aidsvu")
    geo, rate = M.observed_max_density(df, 2022)
    assert "D.C." in geo                      # city-state is the empirical ceiling
    assert rate > 2000                        # ~2694/100k
    table = M.metro_table(df, 2022)
    gate = M.evaluate_metro_gate(table, geo, rate)
    assert not gate.passed
    assert gate.n_achievable == 0
    # even the least-demanding cell needs > the densest US geography
    assert gate.best_multiple > 1.0
