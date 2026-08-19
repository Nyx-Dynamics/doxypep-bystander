"""Tests for Stream B schema v2 (src/coding/schema_guideline.py).

Contract first: a coded finding without a locator raises. The handoff's guards
(explicitly_none needs a quote; null local-literature needs search provenance;
reference_title_only needs a citation; silent needs a full-review note) are
pinned, with fixtures modelled on the PI's verified exemplars.
"""
import pytest

from src.coding.schema_guideline import GuidelineRecord, load_guideline


def rec(**kw):
    base = dict(
        unit="nyc_dohmh_2023", jurisdiction_level="city",
        issuing_body="NYC DOHMH", document_title="Dear Colleague: Doxy-PEP",
        document_type="dear_colleague", version="2023-11-09",
        effective_date="2023-11-09",
        source_file="guideline_nyc_dohmh_dearcolleague_2023.pdf",
        coder="test", code_date="2026-08-19",
        bystander_treatment="organism_named", bystander_treatment_locator="p. 2",
        s_aureus_named=True, s_aureus_location="patient_counselling_script",
        s_aureus_location_locator="p. 2",
        in_category_monitoring="GC/CT/syphilis/HIV at initiation and q3mo",
        in_category_monitoring_locator="p. 3",
        s_aureus_monitoring="explicitly_none", s_aureus_monitoring_locator="p. 3",
        s_aureus_monitoring_quote="No laboratory monitoring is needed with doxy-PEP.",
        host_toxicity_labs="silent", host_toxicity_labs_locator="p. 3",
        local_mrsa_msm_literature="Galindo 2012 J Community Health (DOHMH co-authors)",
        same_institution_authored_both="yes",
    )
    base.update(kw)
    return GuidelineRecord(**base)


# --------------------------------------------------------------------------- #
# locator-or-raise                                                            #
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("loc_field", [
    "bystander_treatment_locator", "s_aureus_location_locator",
    "in_category_monitoring_locator", "s_aureus_monitoring_locator",
    "host_toxicity_labs_locator",
])
def test_every_finding_needs_a_locator(loc_field):
    with pytest.raises(Exception):
        rec(**{loc_field: "  "})


# --------------------------------------------------------------------------- #
# the thesis guards                                                           #
# --------------------------------------------------------------------------- #
def test_explicitly_none_requires_a_verbatim_quote():
    with pytest.raises(Exception):
        rec(s_aureus_monitoring="explicitly_none", s_aureus_monitoring_quote=None)
    ok = rec(s_aureus_monitoring="explicitly_none",
             s_aureus_monitoring_quote="No laboratory monitoring is needed.")
    assert ok.s_aureus_monitoring == "explicitly_none"


def test_null_local_literature_requires_search_provenance():
    # Philadelphia: none found -> must record the search, not just leave null
    with pytest.raises(Exception):
        rec(local_mrsa_msm_literature=None, literature_search_provenance=None,
            same_institution_authored_both="no")
    ok = rec(local_mrsa_msm_literature=None,
             literature_search_provenance="PubMed 'MRSA MSM Philadelphia' 2026-08-19; none",
             same_institution_authored_both="no")
    assert ok.local_mrsa_msm_literature is None


def test_reference_title_only_requires_full_citation():
    # Philadelphia: S. aureus appears only inside a cited abstract title
    with pytest.raises(Exception):
        rec(s_aureus_named=True, s_aureus_location="reference_title_only",
            s_aureus_location_citation=None)
    ok = rec(s_aureus_named=True, s_aureus_location="reference_title_only",
             s_aureus_location_citation="Luetkemeyer et al., CROI 2023 abstract, "
             "'Doxy PEP and antimicrobial resistance in N. gonorrhoeae, commensal "
             "Neisseria and S. aureus'")
    assert ok.s_aureus_location == "reference_title_only"


def test_silent_requires_full_review_note():
    # Chicago: silent on AMR anywhere -> must confirm the whole doc was read
    with pytest.raises(Exception):
        rec(bystander_treatment="silent", s_aureus_named=False,
            s_aureus_location="absent", bystander_treatment_note=None)
    ok = rec(bystander_treatment="silent", s_aureus_named=False,
             s_aureus_location="absent",
             bystander_treatment_note="All 7 pages reviewed; no AMR mention anywhere.")
    assert ok.bystander_treatment == "silent"


def test_named_location_consistency():
    with pytest.raises(Exception):                       # named but absent
        rec(s_aureus_named=True, s_aureus_location="absent")
    with pytest.raises(Exception):                       # not named but located
        rec(s_aureus_named=False, s_aureus_location="body_text")


# --------------------------------------------------------------------------- #
# the thesis in one property                                                  #
# --------------------------------------------------------------------------- #
def test_within_artifact_asymmetry_and_lab_infrastructure():
    # NYC: S. aureus explicitly not monitored, in-category screening mandated ->
    # asymmetry True even though NYC orders no host labs either.
    nyc = rec()
    assert nyc.within_artifact_asymmetry
    assert not nyc.lab_infrastructure_shown          # NYC: no labs at all
    # San Diego / Chicago: host-toxicity labs present -> lab infrastructure shown
    san_diego = rec(unit="san_diego", s_aureus_monitoring="silent",
                    s_aureus_monitoring_quote=None, host_toxicity_labs="suggested")
    assert san_diego.within_artifact_asymmetry
    assert san_diego.lab_infrastructure_shown
    monitored = rec(s_aureus_monitoring="required", host_toxicity_labs="required")
    assert not monitored.within_artifact_asymmetry
