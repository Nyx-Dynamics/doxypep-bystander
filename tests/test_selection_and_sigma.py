"""Tests for the MRSA-scoped between-cohort overdispersion σ̂ (dejong_sigma.py).

The S. aureus selection ratchet (formerly selection_ratchet.py) was RETIRED once the
final DoxyPEP analysis (Luetkemeyer 2025 Lancet ID) reported the participant-level
randomised test the reconstruction was approximating — incident doxy-R S. aureus,
HR 3.89 (95% CI 1.42-10.68). The manuscript now cites that result directly (§3.1); the
aggregate reconstruction and its one-sided Fisher / Poisson neutral-suppression tests are
no longer part of the argument. See DECISIONS.md (2026-08-21, Luetkemeyer-2025 pivot).
"""
from pathlib import Path

import numpy as np
import pytest

from src.analysis import dejong_sigma as D

ROOT = Path(__file__).resolve().parents[1]
HAVE_DEJONG = (ROOT / "data/raw/coding/dejong_mrsa_cohorts.yaml").exists()


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
