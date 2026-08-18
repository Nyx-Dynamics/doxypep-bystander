"""Tests for the coding harness (src/coding/). Written before implementation.

The load-bearing contract (CODEBOOK.md, SCAFFOLD Phase B): a coded value without
a locator must RAISE, not validate to a null. Everything else builds on that.
"""
import textwrap

import pytest
import yaml

from src.coding.schema import CodedField, GuidelineRecord, load_guideline
from src.coding.build_corpus import build_guideline_corpus, staph_monitoring_gate


def _valid_record_dict():
    def f(value, loc="p. 1"):
        return {"value": value, "locator": loc, "quote": "…"}
    return {
        "unit": "test_cdc", "jurisdiction": "US",
        "citation": "MMWR 2024;73(RR-2)", "doi": "10.15585/mmwr.rr7302a1",
        "source_file": "guideline_cdc.pdf", "coder": "ACD",
        "code_date": "2026-08-18",
        "discusses_staph_risk": f("yes"),
        "requires_staph_monitoring": f("no", "p. 4, Box 2"),
        "requires_counselling_commensal_resistance": f("yes"),
        "harms_evidence_graded": f("no", "§Methods"),
        "efficacy_evidence_graded": f("yes", "§Methods"),
    }


# --------------------------------------------------------------------------- #
# the locator-or-raise contract                                               #
# --------------------------------------------------------------------------- #
def test_coded_field_requires_locator():
    with pytest.raises(Exception):
        CodedField(value="yes")                      # no locator key at all
    with pytest.raises(Exception):
        CodedField(value="yes", locator="")          # empty locator
    with pytest.raises(Exception):
        CodedField(value="yes", locator="   ")       # whitespace-only


def test_coded_field_valid():
    c = CodedField(value="no", locator="p. 4, Box 2", quote="…")
    assert c.value == "no"
    assert c.locator == "p. 4, Box 2"


def test_value_vocabulary_enforced():
    with pytest.raises(Exception):
        CodedField(value="maybe", locator="p. 1")


def test_partial_requires_note():
    with pytest.raises(Exception):
        CodedField(value="partial", locator="p. 2")   # partial without note
    ok = CodedField(value="partial", locator="p. 2", note="only 'commensals'")
    assert ok.value == "partial"


def test_record_builds_and_missing_locator_raises(tmp_path):
    good = tmp_path / "guideline_ok.yaml"
    good.write_text(yaml.safe_dump(_valid_record_dict()))
    rec = load_guideline(good)
    assert isinstance(rec, GuidelineRecord)
    assert rec.requires_staph_monitoring.value == "no"

    # strip the locator from one field -> must raise on load, not null it
    bad_dict = _valid_record_dict()
    del bad_dict["requires_staph_monitoring"]["locator"]
    bad = tmp_path / "guideline_bad.yaml"
    bad.write_text(yaml.safe_dump(bad_dict))
    with pytest.raises(Exception):
        load_guideline(bad)


# --------------------------------------------------------------------------- #
# corpus builder + gate                                                       #
# --------------------------------------------------------------------------- #
def test_build_corpus_and_gate(tmp_path):
    d = tmp_path / "coding"
    d.mkdir()
    (d / "guideline_a.yaml").write_text(yaml.safe_dump(_valid_record_dict()))
    monitors = _valid_record_dict()
    monitors["unit"] = "test_monitors"
    monitors["requires_staph_monitoring"] = {
        "value": "yes", "locator": "p. 5", "quote": "assess for SSTI"}
    (d / "guideline_b.yaml").write_text(yaml.safe_dump(monitors))

    records, df = build_guideline_corpus(d)
    assert len(records) == 2
    assert {"unit", "requires_staph_monitoring", "requires_staph_monitoring_locator"} <= set(df.columns)

    # the gate flags the unit that requires staph monitoring
    flagged = staph_monitoring_gate(records)
    assert flagged == ["test_monitors"]
