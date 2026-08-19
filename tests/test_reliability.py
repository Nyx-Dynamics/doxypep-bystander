"""Tests for the reliability module (src/analysis/reliability.py)."""
import math

import pandas as pd

from src.analysis import reliability as R


def test_cohen_kappa_perfect_and_chance():
    assert R.cohen_kappa(["a", "b", "a"], ["a", "b", "a"]) == 1.0
    # total disagreement across two categories -> kappa < 0
    assert R.cohen_kappa(["a", "a", "b"], ["b", "b", "a"]) < 0
    # no variation (all same label both sides) -> perfect -> 1.0
    assert R.cohen_kappa(["a", "a"], ["a", "a"]) == 1.0


def test_kappa_known_value():
    # 4 agree of 5; simple 2-category case
    a = ["yes", "yes", "yes", "no", "no"]
    b = ["yes", "yes", "no", "no", "no"]
    k = R.cohen_kappa(a, b)
    assert 0.0 < k < 1.0


def test_run_on_real_corpus():
    import src.analysis.reliability as R
    root = R.Path(__file__).resolve().parents[1]
    if not (root / "data/raw/coding/reliability/second_pass.json").exists():
        import pytest
        pytest.skip("second-pass coding not present")
    df, fa, dis, overall = R.run(root)
    # every second-pass unit paired with a first-pass record
    assert df["unit"].nunique() >= 5
    assert set(df["field"]) == set(R.FIELDS)
    # first-pass vs blind second-pass should agree strongly (sanity, not a target)
    assert overall >= 0.8
