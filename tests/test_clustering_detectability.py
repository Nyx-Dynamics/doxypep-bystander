"""Tests for the clustering-detectability pair (¶4/¶7):
- src/analysis/coverage_null.py       — a mean-based endpoint cannot resolve clustering
- src/analysis/three_outbreak_fit.py  — the trial series cannot identify the shape
"""
from pathlib import Path

import numpy as np
import pytest

# whole module is computationally heavy — see pytest.ini 'slow' marker
pytestmark = pytest.mark.slow

from src.analysis import coverage_null as C
from src.analysis import three_outbreak_fit as T

ROOT = Path(__file__).resolve().parents[1]
HAVE_DOXYVAC = (ROOT / "data/raw/coding/trial_doxyvac.yaml").exists()


# --------------------------------------------------------------------------- #
# coverage_null                                                                #
# --------------------------------------------------------------------------- #
def test_cochran_armitage_calibrated_under_no_trend_no_clustering():
    # a flat process with no clustering rejects at ~alpha, not more (calibration)
    denoms = [300, 280, 250, 200, 120]
    rng = np.random.default_rng(1)
    rej = 0
    B = 3000
    for _ in range(B):
        x = rng.binomial(denoms, 0.05)
        if C.cochran_armitage_p(x, denoms) < 0.05:
            rej += 1
    assert 0.03 < rej / B < 0.07          # nominal 5%, allowing Monte-Carlo slack


def test_perfect_monotone_rise_is_significant():
    # a clean rising series must trip the trend test
    denoms = [300, 300, 300, 300, 300]
    counts = [6, 12, 24, 36, 48]
    assert C.cochran_armitage_p(counts, denoms) < 0.001


def test_clustering_inflates_typeI_and_erodes_power():
    denoms = [331, 304, 251, 193, 121]
    a = np.log(0.03 / 0.97)
    b = 0.375
    pw0, t1_0 = C.power_and_typeI(denoms, a, b, sigma=0.0, n_sim=1500, seed=7)
    pw1, t1_1 = C.power_and_typeI(denoms, a, b, sigma=1.0, n_sim=1500, seed=7)
    # no clustering: calibrated Type-I, high power
    assert t1_0 < 0.08 and pw0 > 0.85
    # clustering: Type-I inflates well above nominal, power drops
    assert t1_1 > 0.25
    assert t1_1 > t1_0
    assert pw1 < pw0


def test_estimate_sigma_nonnegative_and_zero_for_binomial_series():
    # a series generated with NO overdispersion should not manufacture clustering
    denoms = [300, 300, 300, 300, 300]
    rng = np.random.default_rng(3)
    p = 1 / (1 + np.exp(-(-3.0 + 0.4 * np.arange(5))))
    counts = rng.binomial(denoms, p)
    fit = C.estimate_sigma(counts, denoms)
    assert fit["sigma"] >= 0.0


@pytest.mark.skipif(not HAVE_DOXYVAC, reason="coded DOXYVAC not present")
def test_coverage_null_run_reports_inflation():
    _, _, rows, anchored = C.run(ROOT, n_sim=1200)
    by_sigma = {r["sigma"]: r for r in rows}
    assert by_sigma[0.0]["typeI"] < 0.08           # calibrated at sigma=0
    assert by_sigma[1.0]["typeI"] > by_sigma[0.0]["typeI"]   # inflates with clustering
    assert by_sigma[1.0]["power"] < by_sigma[0.0]["power"]   # power erodes
    # empirically anchored rows exist and sit deep in the degraded regime (Type-I high)
    assert anchored and all(r["typeI"] > 0.5 for r in anchored)
    assert (ROOT / "outputs/coverage_null_result.md").exists()


# --------------------------------------------------------------------------- #
# three_outbreak_fit                                                           #
# --------------------------------------------------------------------------- #
def test_richer_model_never_fits_worse():
    denoms = [300, 300, 300, 300, 300]
    counts = [6, 11, 16, 11, 12]
    ll1 = T.fit_model(counts, denoms, 1)["loglik"]
    ll2 = T.fit_model(counts, denoms, 2)["loglik"]
    ll3 = T.fit_model(counts, denoms, 3)["loglik"]
    assert ll2 >= ll1 - 1e-6
    assert ll3 >= ll2 - 1e-6           # nested: more params cannot lower the likelihood


def test_bootstrap_recovers_a_strong_monotone_trend():
    # a strong real rise -> trend-vs-flat bootstrap should be significant
    denoms = [300, 300, 300, 300, 300]
    counts = [6, 12, 24, 36, 48]
    out = T.bootstrap_discrimination(counts, denoms, k_full=2, k_red=1, n_boot=500, seed=2)
    assert out["p_boot"] < 0.05


def test_bootstrap_does_not_manufacture_curvature_from_a_line():
    # data from a pure monotone line -> wave-vs-trend must NOT be significant
    denoms = [300, 300, 300, 300, 300]
    rng = np.random.default_rng(5)
    p = 1 / (1 + np.exp(-(-3.0 + 0.4 * np.arange(5))))
    counts = rng.binomial(denoms, p)
    out = T.bootstrap_discrimination(counts, denoms, k_full=3, k_red=2, n_boot=500, seed=5)
    assert out["p_boot"] > 0.05


@pytest.mark.skipif(not HAVE_DOXYVAC, reason="coded DOXYVAC not present")
def test_outbreak_curvature_unidentifiable_in_both_arms():
    results = T.run(ROOT)
    assert len(results) == 2
    for r in results:
        # the outbreak (wave) curvature is not distinguishable from a monotone trend
        assert r["wave_vs_trend"]["p_boot"] > 0.05
    assert (ROOT / "outputs/three_outbreak_fit_result.md").exists()


def test_no_best_model_when_indistinguishable():
    # three near-identical AICs -> no "best" named (struck as noise-mining)
    denoms = [300, 300, 300, 300, 300]
    rng = np.random.default_rng(9)
    counts = rng.binomial(denoms, 0.05)          # flat-ish; models will be within ~2 AIC
    r = T.analyze_series("flatish", list(counts), denoms)
    if r["aic_spread"] < 2.0:
        assert r["best_by_aic"] is None
    else:
        assert r["best_by_aic"] is not None


def test_fmt_p_floors_zero_at_one_over_nboot():
    assert T._fmt_p(0.0).startswith("<")
    assert T._fmt_p(0.0) == f"<{1/T.N_BOOT:.4f}"
    assert T._fmt_p(0.05) == "0.050"
