"""Coding schema (pydantic) — the locator-or-raise contract.

Every coded value is a ``CodedField`` carrying a REQUIRED, non-empty locator.
A record whose field lacks a locator raises at load time; it never validates to a
null. See CODEBOOK.md for field definitions.
"""
from __future__ import annotations

from pathlib import Path
from typing import ClassVar, Literal, Optional

import yaml
from pydantic import BaseModel, ConfigDict, field_validator, model_validator

Value = Literal["yes", "no", "partial", "na"]


class CodedField(BaseModel):
    """One coded value + its provenance. Locator is mandatory and non-empty."""
    model_config = ConfigDict(extra="forbid")

    value: Value
    locator: str
    quote: Optional[str] = None
    note: Optional[str] = None

    @field_validator("locator")
    @classmethod
    def _locator_nonempty(cls, v: str) -> str:
        if v is None or not str(v).strip():
            raise ValueError("locator is required and must be non-empty "
                             "(no locator, no value — see CODEBOOK.md)")
        return str(v).strip()

    @model_validator(mode="after")
    def _partial_needs_note(self) -> "CodedField":
        if self.value == "partial" and not (self.note and self.note.strip()):
            raise ValueError("value 'partial' requires a 'note' explaining the "
                             "boundary (CODEBOOK.md)")
        return self


class GuidelineRecord(BaseModel):
    """One coded guideline document (Stream B)."""
    model_config = ConfigDict(extra="forbid")

    unit: str
    jurisdiction: str
    citation: str
    doi: Optional[str] = None
    source_file: str
    coder: str
    code_date: str

    discusses_staph_risk: CodedField
    requires_staph_monitoring: CodedField
    requires_counselling_commensal_resistance: CodedField
    harms_evidence_graded: CodedField
    efficacy_evidence_graded: CodedField

    # the five coded fields, in codebook order
    CODED_FIELDS: ClassVar[tuple] = (
        "discusses_staph_risk",
        "requires_staph_monitoring",
        "requires_counselling_commensal_resistance",
        "harms_evidence_graded",
        "efficacy_evidence_graded",
    )


def load_guideline(path: Path | str) -> GuidelineRecord:
    """Parse one guideline YAML into a validated record (raises on any missing
    locator / invalid value / unknown key)."""
    path = Path(path)
    with open(path) as fh:
        data = yaml.safe_load(fh)
    try:
        return GuidelineRecord(**data)
    except Exception as e:                       # add filename context
        raise ValueError(f"{path.name}: {e}") from e
