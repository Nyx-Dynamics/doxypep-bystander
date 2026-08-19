"""Stream A coding schema — trials.

Append to `src/coding/schema.py` (reuses CodedField / Value from it).

Three structural points, each with a field to match (see CODEBOOK_streamA.md):

1. A phenotype scored at the standard tetracycline breakpoint cannot distinguish
   tet(K) efflux from tet(M) ribosomal protection. Grossman 2016 Table 1: tet(K)
   raises tetracycline MIC 64x but doxycycline only 2x. Doxy-PEP is predicted to
   shift composition toward tet(M) *within* the resistant fraction, which a
   mechanism-blind endpoint cannot see at all. -> `mechanism_discriminating`.
2. One result is reported many times with different denominators, and some of
   those denominators are moved by the intervention itself.
   -> `ResistanceObservation` is per *reporting*, plus
   `denominator_intervention_affected`.
3. Sources relabel the drug tested (NEJM measured doxycycline; CDC describes it as
   tetracycline). -> `phenotype_measured` vs `phenotype_as_labeled`.
"""
from __future__ import annotations

from pathlib import Path
from typing import ClassVar, Literal, Optional

import yaml
from pydantic import BaseModel, ConfigDict, model_validator

from src.coding.schema import CodedField  # noqa: F401

SourceType = Literal["primary_trial", "guideline", "meta_analysis",
                     "secondary_synthesis", "reanalysis", "registry"]
# secondary_synthesis: an extraction/re-tabulation of ANOTHER study's data (e.g. a
# systematic review's table re-printing one trial's numbers). A second reading of
# the same underlying data — reconciles to the primary by construction, NOT an
# independent observation; excluded from detectability inputs like every non-primary.
Arm = Literal["doxy", "control", "combined"]
Organism = Literal["s_aureus", "mssa", "mrsa", "n_gonorrhoeae",
                   "commensal_neisseria", "c_trachomatis", "gas", "other"]
Phenotype = Literal["doxycycline", "tetracycline", "methicillin",
                    "minocycline", "not_stated"]
DenominatorBasis = Literal["all_participants_swabbed", "colonized_participants",
                           "isolates_cultured", "unclear"]
DiscriminationMethod = Literal["standard_breakpoint", "high_level_breakpoint",
                               "tetM_pcr", "wgs", "none"]
SignificanceReported = Literal["within_arm", "between_arm", "both", "none"]
SelectionLevel = Literal["individual", "population", "both", "na"]
YesNo = Literal["yes", "no"]

#: Methods that resolve efflux (tetK) from ribosomal protection (tetM).
DISCRIMINATING_METHODS = {"high_level_breakpoint", "tetM_pcr", "wgs"}


class ResistanceObservation(BaseModel):
    """One *reported instance* of a resistance result — not one result."""
    model_config = ConfigDict(extra="forbid")

    source_type: SourceType
    source_citation: str
    arm: Arm
    timepoint: str
    organism: Organism

    phenotype_measured: Phenotype
    phenotype_as_labeled: Phenotype

    mechanism_discriminating: Literal["yes", "no", "unclear"]
    discrimination_method: DiscriminationMethod = "none"

    numerator: int
    denominator: int
    denominator_basis: DenominatorBasis
    denominator_intervention_affected: YesNo = "no"
    description_denominator_mismatch: YesNo = "no"

    significance_reported: SignificanceReported = "none"
    p_value: Optional[str] = None

    locator: str
    quote: Optional[str] = None
    note: Optional[str] = None

    @model_validator(mode="after")
    def _checks(self) -> "ResistanceObservation":
        if not self.locator or not self.locator.strip():
            raise ValueError("locator is required and must be non-empty "
                             "(no locator, no value — see CODEBOOK.md)")
        if self.denominator <= 0:
            raise ValueError("denominator must be positive")
        if not 0 <= self.numerator <= self.denominator:
            raise ValueError(
                f"numerator {self.numerator} outside [0, {self.denominator}]. "
                "If the source prints an impossible pair, that is itself a "
                "finding: record it in `note` and code basis 'unclear'.")

        note = (self.note or "").strip()

        if self.denominator_basis == "unclear" and not note:
            raise ValueError("denominator_basis 'unclear' requires a note")
        if self.description_denominator_mismatch == "yes" and not note:
            raise ValueError(
                "description_denominator_mismatch 'yes' requires a note quoting "
                "both the prose description and the printed denominator")
        if self.denominator_intervention_affected == "yes" and not note:
            raise ValueError(
                "denominator_intervention_affected 'yes' requires a note saying "
                "how the intervention moved the denominator")
        if self.phenotype_measured != self.phenotype_as_labeled and not note:
            raise ValueError(
                f"phenotype_measured '{self.phenotype_measured}' differs from "
                f"phenotype_as_labeled '{self.phenotype_as_labeled}' — a note is "
                "required quoting both. Relabeling is a finding, not a typo.")

        # mechanism discrimination must be backed by a method that can do it
        if (self.mechanism_discriminating == "yes"
                and self.discrimination_method not in DISCRIMINATING_METHODS):
            raise ValueError(
                f"mechanism_discriminating 'yes' needs a discrimination_method in "
                f"{sorted(DISCRIMINATING_METHODS)}; got "
                f"'{self.discrimination_method}'. A standard breakpoint cannot "
                "separate tet(K) from tet(M) (Grossman 2016 Table 1).")
        if (self.mechanism_discriminating == "no"
                and self.discrimination_method in DISCRIMINATING_METHODS):
            raise ValueError(
                f"discrimination_method '{self.discrimination_method}' resolves "
                "mechanism, so mechanism_discriminating should not be 'no'")
        if self.mechanism_discriminating == "unclear" and not note:
            raise ValueError("mechanism_discriminating 'unclear' requires a note")
        return self

    @property
    def proportion(self) -> float:
        return self.numerator / self.denominator

    @property
    def relabeled(self) -> bool:
        return self.phenotype_measured != self.phenotype_as_labeled

    @property
    def key(self) -> tuple:
        """Identity of the underlying result, independent of who reported it."""
        return (self.arm, self.timepoint, self.organism, self.phenotype_measured)


class TrialRecord(BaseModel):
    """One coded trial (Stream A)."""
    model_config = ConfigDict(extra="forbid")

    unit: str
    trial_name: str
    citation: str
    doi: Optional[str] = None
    registry_id: Optional[str] = None
    source_file: str
    coder: str
    code_date: str

    s_aureus_measured: CodedField
    powered_for_resistance_endpoint: CodedField
    authors_concede_underpowering: CodedField
    conclusion_contested: CodedField

    selection_level_tested: SelectionLevel
    selection_level_locator: str

    body_site: Optional[CodedField] = None
    identification_method: Optional[CodedField] = None
    susceptibility_method: Optional[CodedField] = None
    breakpoint_standard: Optional[CodedField] = None
    breakpoint_value: Optional[CodedField] = None

    #: Whether the trial's individual-level data is shared ('no' = not available).
    #: The evidentiary-adequacy floor: if the data is withheld, the bystander
    #: discrepancies below cannot be adjudicated by anyone's re-analysis.
    data_availability: Optional[CodedField] = None
    #: 'yes' when a source's LABEL for the S. aureus resistance phenotype does not
    #: match the assay actually run. The DoxyPEP S. aureus assay was doxycycline
    #: throughout (E-test MIC>=16; CROI methods table, NEJM Trial Procedures, Appendix
    #: Table 2), yet NEJM's End Points sentence and the protocol aims call it
    #: "tetracycline" and CDC/Szondy relabel it downstream. This is a labeling
    #: inconsistency, NOT a measurement switch (no tetracycline-S.-aureus assay ever
    #: existed) and NOT concealment (tetracycline is the broader surrogate; doxycycline
    #: is the more conservative measure). Note must quote the conflicting labels.
    saureus_endpoint_label_mismatch: Optional[CodedField] = None

    observations: list[ResistanceObservation] = []

    CODED_FIELDS: ClassVar[tuple] = (
        "s_aureus_measured",
        "powered_for_resistance_endpoint",
        "authors_concede_underpowering",
        "conclusion_contested",
    )

    @model_validator(mode="after")
    def _checks(self) -> "TrialRecord":
        if not self.selection_level_locator.strip():
            raise ValueError("selection_level_tested requires a locator")
        if (self.conclusion_contested.value == "yes"
                and not (self.conclusion_contested.note or "").strip()):
            raise ValueError("conclusion_contested 'yes' requires a note naming "
                             "the contesting citation")
        if self.s_aureus_measured.value == "yes" and not self.observations:
            raise ValueError(
                f"{self.unit}: s_aureus_measured is 'yes' but no observations "
                "were coded — the denominators are the Stream A input")
        if (self.saureus_endpoint_label_mismatch is not None
                and self.saureus_endpoint_label_mismatch.value == "yes"
                and not (self.saureus_endpoint_label_mismatch.note or "").strip()):
            raise ValueError(
                "saureus_endpoint_label_mismatch 'yes' requires a note quoting the "
                "conflicting labels (the assay's drug vs the label a source applies) "
                "— a mislabel is a finding, not a typo")
        return self


def load_trial(path: Path | str) -> TrialRecord:
    path = Path(path)
    with open(path) as fh:
        data = yaml.safe_load(fh)
    try:
        return TrialRecord(**data)
    except Exception as e:
        raise ValueError(f"{path.name}: {e}") from e
