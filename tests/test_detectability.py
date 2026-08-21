"""Tests for exact-Fisher detectability (src/analysis/detectability.py) and the
cross-trial mechanism-blindness view."""
import pytest

from src.analysis import detectability as D
from src.analysis import observations as O
from src.coding.schema_trial import load_trial


def test_fisher_power_monotone_in_effect():
    # bigger true difference -> more power, at fixed arm sizes (small n: exact test
    # is O(n^2) enumeration, so keep test arms small)
    lo = D.fisher_power(50, 50, 0.20, 0.10)
    hi = D.fisher_power(50, 50, 0.55, 0.10)
    assert 0.0 <= lo <= hi <= 1.0
    assert hi > 0.5           # a large effect at n=50 has real power


def test_min_detectable_rr_shrinks_with_sample_size():
    # tiny arms need a bigger RR than modest ones (both small enough to be fast)
    small = D.min_detectable_rr(20, 20, 0.15)
    bigger = D.min_detectable_rr(70, 70, 0.15)
    assert small > bigger > 1.0


@pytest.mark.skipif(
    not (D.Path(__file__).resolve().parents[1] / "data/raw/coding/trial_doxypep.yaml").exists(),
    reason="coded trials not present")
def test_real_trials_underpowered_for_soge():
    root = D.Path(__file__).resolve().parents[1]
    _, tab, _ = D.run(root)
    assert len(tab) >= 4
    # not one primary S. aureus comparison can detect either external benchmark
    assert tab["detect_matched_2.25"].sum() == 0
    assert tab["detect_crossorg_1.42"].sum() == 0
    # every minimum detectable RR is above BOTH benchmarks
    finite = tab[tab["min_detectable_RR"] != float("inf")]
    assert (finite["min_detectable_RR"] > D.RR_SAUREUS).all()
    assert (finite["min_detectable_RR"] > D.RR_GC).all()


def test_required_control_n_matches_exact_fisher():
    # the normal-approx solved N should deliver ~80% by EXACT Fisher (validates the
    # method switch: approx for the large required N, exact for tiny realised N)
    p_c, ratio, rr = 0.10, 1.75, D.RR_SAUREUS
    n_ctrl = D.required_control_n(p_c, rr, ratio)
    n_doxy = ratio * n_ctrl
    pw = D.fisher_power(round(n_doxy), round(n_ctrl), rr * p_c, p_c)
    assert 0.76 <= pw <= 0.84          # ~80%, allowing approximation slack


def test_required_n_grows_as_benchmark_shrinks():
    # a smaller effect (cross-organism 1.42) needs MORE sample than the matched 2.25
    p_c, ratio = 0.10, 1.5
    n_matched = D.required_control_n(p_c, D.RR_SAUREUS, ratio)
    n_cross = D.required_control_n(p_c, D.RR_GC, ratio)
    assert n_cross > n_matched > 0


def test_required_control_n_infinite_when_saturated():
    # rr*p >= 1 cannot be detected at any N
    assert D.required_control_n(0.60, D.RR_SAUREUS, 1.0) == float("inf")


@pytest.mark.skipif(
    not (D.Path(__file__).resolve().parents[1] / "data/raw/coding/trial_doxypep.yaml").exists(),
    reason="coded trials not present")
def test_duration_table_multiples_exceed_one():
    root = D.Path(__file__).resolve().parents[1]
    _, _, dtab = D.run(root)
    assert len(dtab) >= 4
    # every comparison needed strictly more sample than realised, for BOTH benchmarks;
    # the matched-2.25 multiple never drops below ~3.5x, and cross-org is larger still
    assert (dtab["multiple_2.25"] > 1).all()
    assert (dtab["multiple_2.25"] >= 3.5).all()
    assert (dtab["multiple_1.42"] > dtab["multiple_2.25"]).all()
    # M12 colonised — the headline endpoint — needs ~6x
    m12 = dtab[(dtab["timepoint"] == "month12") &
               (dtab["basis"] == "colonized_participants")]
    assert 5.0 <= float(m12["multiple_2.25"].iloc[0]) <= 7.5
    assert (root / "outputs/duration_result.md").exists()


@pytest.mark.skipif(
    not (D.Path(__file__).resolve().parents[1] / "data/raw/coding/trial_doxyvac.yaml").exists(),
    reason="coded trials not present")
def test_cross_trial_mechanism_asymmetry():
    root = D.Path(__file__).resolve().parents[1]
    recs = [load_trial(p) for p in sorted((root / "data/raw/coding").glob("trial_*.yaml"))]
    ct = O.cross_trial_blindness(recs).set_index("category")
    # in-category organisms have a discriminating assay somewhere; bystander all blind
    assert ct.loc["in_category", "any_discriminating"]
    assert ct.loc["bystander", "all_blind"]
