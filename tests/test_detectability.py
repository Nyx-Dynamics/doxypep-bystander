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
    _, tab = D.run(root)
    assert len(tab) >= 4
    # not one primary S. aureus comparison can detect either external benchmark
    assert tab["detect_matched_2.25"].sum() == 0
    assert tab["detect_crossorg_1.42"].sum() == 0
    # every minimum detectable RR is above BOTH benchmarks
    finite = tab[tab["min_detectable_RR"] != float("inf")]
    assert (finite["min_detectable_RR"] > D.RR_SAUREUS).all()
    assert (finite["min_detectable_RR"] > D.RR_GC).all()


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
