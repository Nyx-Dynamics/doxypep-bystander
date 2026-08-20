"""Tests for the Stream A schema and reporting analyses.

Contract tests first: a coded value without a locator must RAISE. The DoxyPEP
findings (three denominators, phenotype relabeling, mechanism blindness) are
pinned as regression fixtures.
"""
import pytest
from pydantic import ValidationError

from src.coding.schema import CodedField
from src.coding.schema_trial import ResistanceObservation, TrialRecord
from src.analysis import observations as O


def obs(**kw):
    base = dict(source_type="primary_trial", source_citation="Luetkemeyer 2023",
                arm="doxy", timepoint="month12", organism="s_aureus",
                phenotype_measured="doxycycline",
                phenotype_as_labeled="doxycycline",
                mechanism_discriminating="no",
                discrimination_method="standard_breakpoint",
                numerator=5, denominator=31,
                denominator_basis="colonized_participants",
                locator="Fig 4B")
    base.update(kw)
    return ResistanceObservation(**base)


def field(value="yes", **kw):
    return CodedField(value=value, locator="p. 1", **kw)


# --------------------------------------------------------------------------- #
# locator-or-raise contract                                                    #
# --------------------------------------------------------------------------- #
def test_observation_without_locator_raises():
    with pytest.raises((ValidationError, ValueError)):
        obs(locator="   ")


def test_impossible_pair_raises_rather_than_coercing():
    with pytest.raises((ValidationError, ValueError)):
        obs(numerator=80, denominator=31)


@pytest.mark.parametrize("kw", [
    dict(denominator_basis="unclear"),
    dict(description_denominator_mismatch="yes"),
    dict(denominator_intervention_affected="yes"),
    dict(mechanism_discriminating="unclear"),
    dict(phenotype_as_labeled="tetracycline"),   # relabeling
])
def test_judgment_calls_require_a_note(kw):
    with pytest.raises((ValidationError, ValueError)):
        obs(**kw)
    obs(note="reasoning recorded", **kw)


# --------------------------------------------------------------------------- #
# mechanism discrimination — Grossman 2016 Table 1 is the justification        #
# --------------------------------------------------------------------------- #
def test_standard_breakpoint_cannot_claim_discrimination():
    """A standard breakpoint cannot separate tet(K) from tet(M)."""
    with pytest.raises((ValidationError, ValueError)):
        obs(mechanism_discriminating="yes",
            discrimination_method="standard_breakpoint")


@pytest.mark.parametrize("method", ["high_level_breakpoint", "tetM_pcr", "wgs"])
def test_discriminating_methods_accepted(method):
    o = obs(mechanism_discriminating="yes", discrimination_method=method)
    assert o.mechanism_discriminating == "yes"


@pytest.mark.parametrize("method", ["high_level_breakpoint", "tetM_pcr", "wgs"])
def test_discriminating_method_cannot_be_coded_blind(method):
    with pytest.raises((ValidationError, ValueError)):
        obs(mechanism_discriminating="no", discrimination_method=method)


# --------------------------------------------------------------------------- #
# trial-level invariants                                                       #
# --------------------------------------------------------------------------- #
def _trial(**kw):
    base = dict(
        unit="doxypep_us", trial_name="DoxyPEP", citation="Luetkemeyer 2023",
        source_file="NEJMoa2211934.pdf", coder="test", code_date="2026-08-18",
        s_aureus_measured=field("yes"),
        powered_for_resistance_endpoint=field("no"),
        authors_concede_underpowering=field("no"),
        conclusion_contested=field("no"),
        selection_level_tested="individual",
        selection_level_locator="§Methods",
        observations=[obs()],
    )
    base.update(kw)
    return TrialRecord(**base)


def test_measured_yes_without_observations_raises():
    """The denominators ARE the Stream A input; 'measured' with none is a bug."""
    with pytest.raises((ValidationError, ValueError)):
        _trial(observations=[])


def test_contested_conclusion_requires_citing_the_contester():
    with pytest.raises((ValidationError, ValueError)):
        _trial(conclusion_contested=field("yes"))
    _trial(conclusion_contested=field(
        "yes", note="Vanbaelen 2024c: MRSA carriage 2%->12% in doxy-PEP arm"))


def test_label_mismatch_requires_a_note():
    """A phenotype label/assay mismatch is a finding; asserting it with no note
    (quoting the conflicting labels) is rejected."""
    with pytest.raises((ValidationError, ValueError)):
        _trial(saureus_endpoint_label_mismatch=field("yes"))  # field() has no note
    # with a note it is accepted
    _trial(saureus_endpoint_label_mismatch=CodedField(
        value="yes", locator="NEJM End Points p.1298; Trial Procedures p.1298",
        note="assay: doxycycline E-test; End Points sentence label: tetracycline"))


def test_new_optional_fields_default_absent():
    """DuDHS/DOXYVAC carry neither field; they must remain optional."""
    r = _trial()
    assert r.data_availability is None
    assert r.saureus_endpoint_label_mismatch is None


def test_real_doxypep_records_data_withheld_and_label_mismatch():
    from pathlib import Path

    from src.coding.schema_trial import load_trial
    p = Path(__file__).resolve().parents[1] / "data/raw/coding/trial_doxypep.yaml"
    if not p.exists():
        pytest.skip("coded trial not present")
    rec = load_trial(p)
    assert rec.data_availability.value == "no"
    assert rec.saureus_endpoint_label_mismatch.value == "yes"
    assert rec.saureus_endpoint_label_mismatch.note  # required, non-empty


def test_selection_level_needs_locator():
    with pytest.raises((ValidationError, ValueError)):
        _trial(selection_level_locator="")


# --------------------------------------------------------------------------- #
# DoxyPEP fixtures                                                             #
# --------------------------------------------------------------------------- #
@pytest.fixture
def doxypep():
    """S. aureus month-12 doxy arm, as reported by three sources."""
    return [_trial(observations=[
        obs(numerator=5, denominator=31,
            denominator_basis="colonized_participants", locator="Fig 4B"),
        obs(numerator=5, denominator=111,
            denominator_basis="all_participants_swabbed",
            denominator_intervention_affected="yes", locator="Fig 4B",
            note="carriage fell 47%->28% in the doxy arm (P=.03), so the "
                 "intervention moved the denominator itself"),
        obs(source_type="guideline", source_citation="CDC MMWR 2024",
            numerator=28, denominator=222,
            denominator_basis="all_participants_swabbed",
            phenotype_as_labeled="tetracycline",
            description_denominator_mismatch="yes", locator="p. 4",
            note="CDC describes 'those with S. aureus in their nares' but prints "
                 "428/222, the totals swabbed; and labels the endpoint "
                 "tetracycline where NEJM Methods state doxycycline ETEST"),
    ])]


@pytest.fixture
def two_organism_trial():
    """Same trial, gonococcus resolved by mechanism, S. aureus not."""
    return [_trial(observations=[
        obs(organism="s_aureus", mechanism_discriminating="no",
            discrimination_method="standard_breakpoint"),
        obs(organism="n_gonorrhoeae", phenotype_measured="tetracycline",
            phenotype_as_labeled="tetracycline",
            mechanism_discriminating="yes",
            discrimination_method="high_level_breakpoint",
            numerator=5, denominator=13,
            denominator_basis="isolates_cultured", locator="Fig 4A"),
    ])]


def test_discordance_flags_the_denominator_split(doxypep):
    d = O.discordance(doxypep)
    row = d.iloc[0]
    assert row["discordant"]
    assert row["n_bases"] == 2
    assert row["any_description_mismatch"]
    assert row["any_intervention_affected_denominator"]
    # 5/31 = 16% vs 5/111 = 4.5%: basis choice alone moves it >3x
    assert row["proportion_ratio"] > 3.0


def test_relabeling_is_surfaced(doxypep):
    r = O.phenotype_relabeling(doxypep)
    assert len(r) == 1
    assert r.iloc[0]["phenotype_measured"] == "doxycycline"
    assert r.iloc[0]["phenotype_as_labeled"] == "tetracycline"
    assert r.iloc[0]["source_citation"] == "CDC MMWR 2024"


def test_mechanism_blindness_marks_s_aureus_blind(two_organism_trial):
    m = O.mechanism_blindness(two_organism_trial).set_index("organism")
    assert m.loc["s_aureus", "blind"]
    assert not m.loc["n_gonorrhoeae", "blind"]


def test_blindness_asymmetry_detects_two_standards_in_one_trial(two_organism_trial):
    a = O.blindness_asymmetry(two_organism_trial)
    assert len(a) == 1
    assert a.iloc[0]["asymmetric"]


def test_primary_trial_filter_excludes_guideline_restatements(doxypep):
    """Detectability must use trial denominators, not a guideline's retelling."""
    p = O.primary_trial_denominators(doxypep)
    assert (p["source_type"] == "primary_trial").all()
    assert "CDC MMWR 2024" not in set(p["source_citation"])


def test_significance_asymmetry_detects_one_sided_reporting():
    recs = [_trial(observations=[
        obs(significance_reported="within_arm", p_value="<0.05"),
        obs(source_citation="between-arm not reported",
            significance_reported="within_arm"),
    ])]
    assert O.significance_asymmetry(recs)["one_sided_only"].all()


# --------------------------------------------------------------------------- #
# S. aureus broadening: conference_abstract source + measurement heterogeneity #
# --------------------------------------------------------------------------- #
def test_conference_abstract_excluded_from_detectability_inputs():
    """The trial's own CROI abstract table is first-party but not peer-reviewed;
    detectability must run on the primary (published) denominators only."""
    recs = [_trial(observations=[
        obs(),  # primary_trial s_aureus
        obs(source_type="conference_abstract",
            source_citation="CROI abstract table",
            numerator=16, denominator=137,
            denominator_basis="all_participants_swabbed"),
    ])]
    p = O.primary_trial_denominators(recs)
    assert (p["source_type"] == "primary_trial").all()
    assert "CROI abstract table" not in set(p["source_citation"])


def test_heterogeneity_flags_non_poolability():
    """A resistance-axis trial and a carriage-axis (no-obs) trial do not share a
    measurement axis; nothing standard-breakpoint is mechanism-discriminating."""
    resistance_trial = _trial(unit="doxypep_us", trial_name="DoxyPEP",
                              observations=[obs(denominator_basis="all_participants_swabbed"),
                                            obs(denominator_basis="colonized_participants")])
    carriage_trial = _trial(unit="doxyvac", trial_name="DOXYVAC",
                            s_aureus_measured=field("partial", note="MRSA carriage only"),
                            observations=[obs(organism="n_gonorrhoeae",
                                              phenotype_measured="tetracycline",
                                              phenotype_as_labeled="tetracycline")])
    h = O.saureus_measurement_heterogeneity([resistance_trial, carriage_trial]).set_index("trial")
    assert not bool(h["shared_axis"].iloc[0])            # axes differ
    assert not bool(h["shared_denominator_basis"].iloc[0])
    assert not h["any_mechanism_discriminating"].any()   # all standard breakpoint
    assert h.loc["DOXYVAC", "phenotype_axis"] == "not coded (see trial note)"
    assert h.loc["DoxyPEP", "phenotype_axis"] == "resistance-within-S.aureus"


@pytest.mark.skipif(
    not (__import__("pathlib").Path(__file__).resolve().parents[1]
         / "data/raw/coding/trial_doxypep.yaml").exists(),
    reason="coded trials not present")
def test_real_corpus_saureus_resists_pooling():
    from pathlib import Path

    from src.coding.schema_trial import load_trial
    root = Path(__file__).resolve().parents[1]
    recs = [load_trial(p) for p in sorted((root / "data/raw/coding").glob("trial_*.yaml"))]
    h = O.saureus_measurement_heterogeneity(recs)
    assert len(h) >= 3
    assert not bool(h["shared_axis"].iloc[0])              # DOXYVAC is a different axis
    assert not bool(h["shared_denominator_basis"].iloc[0])  # all-swabbed vs colonized
    assert not h["any_mechanism_discriminating"].any()      # none resolves tetK/tetM
