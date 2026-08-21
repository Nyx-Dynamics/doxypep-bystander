"""Tests for the restructured Stream-A pair:
- src/analysis/selection_ratchet.py  — S. aureus-scoped within-US-DoxyPEP selection
- src/analysis/dejong_sigma.py        — MRSA-scoped between-cohort overdispersion σ̂
"""
from pathlib import Path

import numpy as np
import pytest

from src.analysis import selection_ratchet as R
from src.analysis import dejong_sigma as D

ROOT = Path(__file__).resolve().parents[1]
HAVE_DEJONG = (ROOT / "data/raw/coding/dejong_mrsa_cohorts.yaml").exists()


# --------------------------------------------------------------------------- #
# selection_ratchet (S. aureus unit)                                          #
# --------------------------------------------------------------------------- #
def test_susceptible_carriage_is_colonization_minus_resistant():
    s = R._series(R.DOXY)
    # susceptible carriage prevalence = colonization − all-swabbed resistant (identity)
    np.testing.assert_allclose(
        s["susceptible_prev"], s["colonization_prev"] - s["resistant_prev"], atol=1e-9)
    # and equals colonization × (1 − per-carrier resistant)
    np.testing.assert_allclose(
        s["susceptible_prev"],
        s["colonization_prev"] * (1 - s["per_carrier_R"]), atol=1e-9)


def test_doxy_arm_shows_the_ratchet():
    res = R.analyze()
    d = res["doxy"]
    # susceptible carriage depletes (one-sided decline) and per-carrier resistance rises
    assert d["susceptible_decline_p"] < 0.01
    assert d["per_carrier"]["p"] < 0.01
    assert d["per_carrier"]["month12"][2] > d["per_carrier"]["baseline"][2]
    # resistant carriage exceeds the neutral-suppression expectation (selection)
    assert d["neutral"]["observed"] > d["neutral"]["expected"]
    assert d["neutral"]["p"] < 0.01


def test_soc_arm_is_uninformative():
    res = R.analyze()
    sc = res["soc"]
    # not a contrasting shape — simply non-significant on every directional test
    assert sc["susceptible_decline_p"] > 0.05
    assert sc["per_carrier"]["p"] > 0.05        # per-carrier resistance did not rise


def test_ratchet_directional_tests_are_one_sided():
    # a flat series must NOT trip the one-sided decline test
    flat_counts = [50, 50, 50]
    denoms = [200, 200, 200]
    p = R.one_sided_decline_p(flat_counts, denoms)
    assert 0.3 < p < 0.7                          # ~0.5 for no trend


@pytest.mark.skipif(not (ROOT / "data/raw/papers/croi2023_luetkemeyer_OA3.md").exists(),
                    reason="CROI artifact not present")
def test_selection_ratchet_run_writes_report():
    R.run(ROOT)
    assert (ROOT / "outputs/selection_ratchet_result.md").exists()


# --------------------------------------------------------------------------- #
# dejong_sigma (MRSA unit)                                                     #
# --------------------------------------------------------------------------- #
@pytest.mark.skipif(not HAVE_DEJONG, reason="de Jong cohort data not present")
def test_sigma_large_and_lower_ci_above_one():
    cohorts = D.load_cohorts(ROOT)
    assert len(cohorts) >= 10                     # ~10 clean-denominator cohorts required
    fit = D.estimate_sigma(cohorts)
    # overdispersion is not small: point estimate large, lower CI above the degraded-regime threshold
    assert fit["sigma"] > 1.5
    assert fit["ci"][0] > 1.0                      # even the lower bound is in the degraded regime
    assert fit["ci"][0] < fit["sigma"] < fit["ci"][1]


@pytest.mark.skipif(not HAVE_DEJONG, reason="de Jong cohort data not present")
def test_sigma_robust_to_dropping_the_54pct_outlier():
    full = D.estimate_sigma(D.load_cohorts(ROOT))
    no_cond = D.estimate_sigma(D.load_cohorts(ROOT, include_conditional=False))
    # dropping the conditional-on-infection 54% cohort does not collapse the estimate
    assert abs(full["sigma"] - no_cond["sigma"]) < 1.0


def test_logit_normal_recovers_known_sigma():
    # synthetic cohorts drawn with a known between-cohort sigma -> recovered within tolerance
    rng = np.random.default_rng(0)
    true_mu, true_sigma = -2.0, 1.2
    ns = rng.integers(150, 800, size=40)
    z = rng.normal(0, 1, size=40)
    p = 1 / (1 + np.exp(-(true_mu + true_sigma * z)))
    k = rng.binomial(ns, p)
    cohorts = [{"count": int(ki), "n": int(ni)} for ki, ni in zip(k, ns)]
    fit = D.estimate_sigma(cohorts)
    assert abs(fit["sigma"] - true_sigma) < 0.4
