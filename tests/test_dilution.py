"""Tests for the Phase 0 feasibility gate math (src/feasibility/dilution.py).

Pure-function tests on the dilution/MDE/RR_needed algebra, plus the gate's
decision logic. The real-data run is exercised by an integration test.
"""
import numpy as np
import pytest

from src.feasibility import dilution as D


# --------------------------------------------------------------------------- #
# algebra                                                                      #
# --------------------------------------------------------------------------- #
def test_back_out_population():
    # 60,628 users at 183 per 100k -> ~33.1M denominator
    pop = D.back_out_population([60628], [183])[0]
    assert pop == pytest.approx(60628 / 183 * 1e5)
    assert 30e6 < pop < 36e6


def test_dilution_fraction_scales_linearly():
    assert D.dilution_fraction(1000, 1e6, kappa=1) == pytest.approx(1e-3)
    # doubling exposed or kappa doubles f
    assert D.dilution_fraction(2000, 1e6, 1) == pytest.approx(2e-3)
    assert D.dilution_fraction(1000, 1e6, 5) == pytest.approx(5e-3)


def test_induced_delta_zero_when_rr_one():
    assert D.induced_delta(1e-3, 0.10, 1.0) == 0.0
    assert D.induced_delta(1e-3, 0.10, 1.42) == pytest.approx(1e-3 * 0.10 * 0.42)


def test_mde_decreases_with_n():
    m1 = D.mde_proportion(0.10, 1_000)
    m2 = D.mde_proportion(0.10, 100_000)
    assert m2 < m1
    # 100x the isolates -> 10x tighter MDE (sqrt law)
    assert m1 / m2 == pytest.approx(10.0, rel=1e-6)


def test_rr_needed_inverts_induced_delta():
    """If RR == rr_needed(mde,...), the induced shift equals exactly the MDE."""
    f, r0, mde = 1e-3, 0.10, 0.02
    rr = D.rr_needed(mde, f, r0)
    assert D.induced_delta(f, r0, rr) == pytest.approx(mde)


def test_rr_needed_grows_as_dilution_worsens():
    # smaller f (more diluted) -> larger required RR
    assert D.rr_needed(0.02, 1e-4, 0.10) > D.rr_needed(0.02, 1e-2, 0.10)


# --------------------------------------------------------------------------- #
# gate decision logic                                                         #
# --------------------------------------------------------------------------- #
def test_gate_fails_when_rr_needed_exceeds_soge():
    import pandas as pd
    table = pd.DataFrame([
        {"RR_needed": 50.0, "detectable": False},
        {"RR_needed": 12.5, "detectable": False},
    ])
    g = D.evaluate_gate(table)
    assert not g.passed
    assert g.verdict().startswith("FAIL")
    assert g.best_case_rr_needed == 12.5


def test_gate_passes_only_within_soge_and_detectable():
    import pandas as pd
    table = pd.DataFrame([
        {"RR_needed": 1.30, "detectable": True},
        {"RR_needed": 9.0, "detectable": False},
    ])
    g = D.evaluate_gate(table)
    assert g.passed
    assert g.verdict().startswith("PASS")


# --------------------------------------------------------------------------- #
# integration on the real panel                                               #
# --------------------------------------------------------------------------- #
@pytest.mark.skipif(
    not (D.Path(__file__).resolve().parents[1] / "data/raw/aidsvu").exists(),
    reason="raw AIDSVu data not present")
def test_real_state_gate_fails_decisively():
    """Documented expectation: the state-level design is infeasible. Even the
    best-case required RR should dwarf Soge's 1.42."""
    root = D.Path(__file__).resolve().parents[1]
    df = D.load_aidsvu(root / "data/raw/aidsvu")
    table = D.sensitivity_table(df, 2022)
    gate = D.evaluate_gate(table)
    assert not gate.passed
    assert gate.n_detectable == 0
    # even the most generous cell exceeds Soge's optimistic ceiling...
    assert gate.best_case_rr_needed > D.RR_SOGE
    # ...and the typical cell fails by a wide margin
    assert table["RR_needed"].median() > D.RR_SOGE * 3
