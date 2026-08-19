"""Tests for the defined literature search (src/analysis/literature_search.py).

No network: these read the frozen snapshot committed under data/raw. The E-utilities
query is exercised only when a developer runs `--refresh` by hand.
"""
import pytest

from src.analysis import literature_search as L

ROOT = L.Path(__file__).resolve().parents[1]
SNAP = ROOT / "data/raw/literature_search/snapshot.json"


@pytest.mark.skipif(not SNAP.exists(), reason="literature snapshot not present")
def test_snapshot_shape():
    snap = L.load_snapshot(ROOT)
    # numerator is a subset restriction of the denominator, so it cannot exceed it
    assert 0 < snap["numerator_count"] <= snap["denominator_count"]
    # the bystander clause is literally appended to the denominator query
    assert snap["numerator_query"].startswith(snap["denominator_query"])
    assert L.BYSTANDER_CLAUSE in snap["numerator_query"]
    # every retrieved PMID is accounted for (retmax=100 >= count, so this is all of them)
    assert len(snap["numerator_pmids"]) == snap["numerator_count"]


@pytest.mark.skipif(not SNAP.exists(), reason="literature snapshot not present")
def test_every_numerator_pmid_is_classified():
    # no silent default-to-names_only for a paper we never actually read
    snap = L.load_snapshot(ROOT)
    unclassified = [p for p in snap["numerator_pmids"] if p not in L.NUMERATOR_CLASSIFICATION]
    assert unclassified == []


@pytest.mark.skipif(not SNAP.exists(), reason="literature snapshot not present")
def test_tiers_partition_the_numerator():
    snap = L.load_snapshot(ROOT)
    tiers = L._tiers(snap["numerator_pmids"])
    total = sum(len(v) for v in tiers.values())
    assert total == snap["numerator_count"]
    # measuring is a strict subset of naming, and the contrast tier a subset of measuring
    n_meas = len(tiers["measures_with_contrast"]) + len(tiers["measures_no_contrast"])
    assert len(tiers["measures_with_contrast"]) <= n_meas <= snap["numerator_count"]
    # the load-bearing claim: at least one paper measures against a doxy-PEP contrast,
    # and strictly fewer measure than merely name
    assert len(tiers["measures_with_contrast"]) >= 1
    assert n_meas < snap["numerator_count"]


@pytest.mark.skipif(not SNAP.exists(), reason="literature snapshot not present")
def test_report_regenerates_from_snapshot(tmp_path):
    # run() with refresh=False must not touch the network and must write the report
    snap = L.run(ROOT, refresh=False)
    assert (ROOT / "outputs/literature_search_result.md").exists()
    assert snap["denominator_count"] == L.load_snapshot(ROOT)["denominator_count"]
