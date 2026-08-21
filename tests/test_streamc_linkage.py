"""Tests for the re-anchored Stream C linkage decomposition
(src/analysis/streamc_linkage.py) — the principled systems denominator, the three-way
decomposition, and the Contract guards."""
from pathlib import Path

import pytest

from src.analysis import streamc_linkage as L

ROOT = Path(__file__).resolve().parents[1]
HAVE = (ROOT / "data/raw/coding/streamc_surveillance_systems.yaml").exists()

pytestmark = pytest.mark.skipif(not HAVE, reason="Stream C systems denominator not present")


def _systems():
    return L.load_systems(ROOT)


def test_denominator_is_a_closed_universe_with_a_stated_rule():
    s = _systems()
    assert "selection_rule" in s and s["selection_rule"].strip()
    # phenotype unit is stated as S. aureus tetracycline (Contract 2), not MRSA
    assert "tetracycline" in s["phenotype_unit"].lower()
    assert "aureus" in s["phenotype_unit"].lower()


def test_every_included_system_is_coded_on_three_capabilities():
    rows, _ = L.classify(_systems())
    assert len(rows) >= 10
    for r in rows:
        assert isinstance(r["exposure_pop"], bool)
        assert isinstance(r["phenotype_pop"], bool)
        assert isinstance(r["links"], bool)


def test_decomposition_no_phenotype_and_no_link():
    _, dec = L.classify(_systems())
    # exposure exists (PrEP proxy); the S. aureus tetR phenotype does not exist at a
    # population denominator anywhere; nothing links
    assert dec["exposure_only"] >= 2
    assert dec["phenotype_only"] == 0
    assert dec["both_unlinked"] == 0
    assert dec["linked"] == 0


def test_failure_mode_is_missing_phenotype_side():
    _, dec = L.classify(_systems())
    fm = L.failure_mode(dec)
    assert "phenotype" in fm.lower()
    assert "no phenotype-side" in fm.lower()


def test_mrsa_systems_flagged_wrong_unit_not_counted_as_phenotype():
    rows, dec = L.classify(_systems())
    # ABCs/EIP and NHSN MRSA are the population/facility MRSA near-misses
    assert dec["mrsa_wrong_unit"]                      # at least one flagged
    for r in rows:
        if r["unit_flag"] == "mrsa":
            assert r["phenotype_pop"] is False         # MRSA never counts as the tetR unit


def test_no_deployed_system_links_the_two():
    rows, _ = L.classify(_systems())
    assert not any(r["links"] for r in rows)           # Contract 3: none deployed


def test_exclusions_carry_a_reason():
    s = _systems()
    excluded = [x for x in s["systems"] if not x.get("included", False)]
    assert excluded                                     # commercial / directory / research
    for x in excluded:
        assert x.get("exclusion_reason", "").strip()


def test_run_writes_report_with_scope_bound_and_licenses():
    L.run(ROOT)
    txt = (ROOT / "outputs/streamc_linkage_result.md").read_text()
    assert "Licenses / not" in txt
    assert "deployed" in txt.lower()          # scope bound present
    assert "0/135" in txt                      # dilution leg corrected, not 0/81
    assert "impossible" in txt.lower()         # states it is NOT impossible-in-principle
