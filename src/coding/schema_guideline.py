"""Stream B schema — governmental doxy-PEP guidelines (see METHODS_streamB.md).

Supersedes the v1 5-field GuidelineRecord. The thesis is an asymmetry WITHIN a
single artifact: S. aureus is discussed / counselled / unmeasured while
in-category organisms (GC/CT/syphilis) are resolved with laboratory precision in
the same document, and host-toxicity labs (LFTs/CMP/CBC) show the lab
infrastructure exists.

Same locator-or-raise contract as Stream A: every coded finding carries a
non-empty locator or the record raises. Guards encode the thesis:
  * s_aureus_monitoring == 'explicitly_none' needs a verbatim quote + locator.
  * local_mrsa_msm_literature is None needs literature_search_provenance
    (a null cell means "none found under stated terms", never "none exists").
  * s_aureus_location == 'reference_title_only' needs the full citation.
  * bystander_treatment == 'silent' needs a note confirming the full document was
    reviewed, not just the summary.
"""
from __future__ import annotations

from pathlib import Path
from typing import ClassVar, Literal, Optional

import yaml
from pydantic import BaseModel, ConfigDict, model_validator

JurisdictionLevel = Literal["city", "county", "state", "national", "global"]
DocumentType = Literal["clinical_protocol", "health_advisory", "guideline",
                       "dear_colleague", "patient_factsheet"]
BystanderTreatment = Literal["silent", "generic_microbiome_resistance",
                             "organism_named"]
SAureusLocation = Literal["body_text", "patient_counselling_script",
                          "still_learning_list", "reference_title_only", "absent"]
SAureusMonitoring = Literal["required", "suggested", "silent", "explicitly_none"]
HostToxicityLabs = Literal["required", "suggested", "silent", "explicitly_none"]
SameInstitution = Literal["yes", "no", "same_city_different_institution"]


def _need(cond: bool, msg: str):
    if not cond:
        raise ValueError(msg)


class GuidelineRecord(BaseModel):
    """One coded governmental doxy-PEP guideline (Stream B v2)."""
    model_config = ConfigDict(extra="forbid")

    # provenance
    unit: str
    jurisdiction_level: JurisdictionLevel
    issuing_body: str
    document_title: str
    document_type: DocumentType
    version: str
    effective_date: str
    source_file: str
    coder: str
    code_date: str

    # --- how the bystander is treated (each finding carries a locator) ---
    bystander_treatment: BystanderTreatment
    bystander_treatment_locator: str
    bystander_treatment_note: Optional[str] = None      # required if 'silent'

    s_aureus_named: bool
    s_aureus_location: SAureusLocation
    s_aureus_location_locator: str
    s_aureus_location_citation: Optional[str] = None     # required if reference_title_only

    # --- the within-artifact contrast ---
    in_category_monitoring: str                          # verbatim, mandated everywhere
    in_category_monitoring_locator: str
    s_aureus_monitoring: SAureusMonitoring
    s_aureus_monitoring_locator: str
    s_aureus_monitoring_quote: Optional[str] = None      # required if explicitly_none
    host_toxicity_labs: HostToxicityLabs                 # labs exist, for the host
    host_toxicity_labs_locator: str
    host_toxicity_labs_quote: Optional[str] = None       # required if explicitly_none

    counselling_language_verbatim: Optional[str] = None
    counselling_language_locator: Optional[str] = None

    # --- lineage + institutional memory (no locator; provenance fields) ---
    derived_from: Optional[str] = None
    local_mrsa_msm_literature: Optional[str] = None
    literature_search_provenance: Optional[str] = None   # required if the above is null
    same_institution_authored_both: SameInstitution

    note: Optional[str] = None                            # record-level annotation

    #: the coded findings that must each carry a locator
    LOCATED_FIELDS: ClassVar[tuple] = (
        "bystander_treatment", "s_aureus_location", "in_category_monitoring",
        "s_aureus_monitoring", "host_toxicity_labs",
    )

    @model_validator(mode="after")
    def _checks(self) -> "GuidelineRecord":
        # locator-or-raise for every coded finding
        for f in self.LOCATED_FIELDS:
            loc = getattr(self, f + "_locator", None)
            _need(bool(loc and str(loc).strip()),
                  f"{f} requires a non-empty locator (no locator, no value)")

        _need(self.s_aureus_monitoring != "explicitly_none"
              or bool((self.s_aureus_monitoring_quote or "").strip()),
              "s_aureus_monitoring 'explicitly_none' requires a verbatim quote")

        _need(self.host_toxicity_labs != "explicitly_none"
              or bool((self.host_toxicity_labs_quote or "").strip()),
              "host_toxicity_labs 'explicitly_none' requires a verbatim quote")

        _need(self.local_mrsa_msm_literature is not None
              or bool((self.literature_search_provenance or "").strip()),
              "local_mrsa_msm_literature is null -> literature_search_provenance "
              "is required (terms + date). 'null' means 'none found under stated "
              "terms', never 'none exists'.")

        _need(self.s_aureus_location != "reference_title_only"
              or bool((self.s_aureus_location_citation or "").strip()),
              "s_aureus_location 'reference_title_only' requires the full citation")

        _need(self.bystander_treatment != "silent"
              or bool((self.bystander_treatment_note or "").strip()),
              "bystander_treatment 'silent' requires a note confirming the full "
              "document was reviewed, not just the summary section")

        # internal consistency: named<->location
        if self.s_aureus_location == "absent":
            _need(not self.s_aureus_named,
                  "s_aureus_location 'absent' but s_aureus_named is true")
        else:
            _need(self.s_aureus_named,
                  f"s_aureus_location '{self.s_aureus_location}' but "
                  "s_aureus_named is false")
        return self

    @property
    def within_artifact_asymmetry(self) -> bool:
        """The core thesis in one boolean: in-category organisms are monitored,
        the bystander is not (silent or explicitly none) — same document."""
        return (self.s_aureus_monitoring in ("silent", "explicitly_none")
                and bool(self.in_category_monitoring.strip()))

    @property
    def lab_infrastructure_shown(self) -> bool:
        """Host-toxicity labs (LFT/CMP/CBC) ordered — proof the lab apparatus
        exists in the same document that measures no organism for the bystander."""
        return self.host_toxicity_labs in ("required", "suggested")


def load_guideline(path: Path | str) -> GuidelineRecord:
    path = Path(path)
    with open(path) as fh:
        data = yaml.safe_load(fh)
    try:
        return GuidelineRecord(**data)
    except Exception as e:
        raise ValueError(f"{path.name}: {e}") from e
