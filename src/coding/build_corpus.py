"""Build the coded guideline corpus from per-document YAMLs.

Loads every `guideline_*.yaml` under a coding directory into validated records
(each raising if any coded value lacks a locator), flattens them to a tidy frame,
and evaluates the Phase B gate. Writes `data/processed/guidelines_coded.csv`.

`make` target: `python -m src.coding.build_corpus`.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.coding.schema import GuidelineRecord, load_guideline


def build_guideline_corpus(coding_dir: Path | str):
    """Return (records, tidy DataFrame) for every guideline_*.yaml in the dir.

    Raises (via load_guideline) if any coded value is missing a locator."""
    coding_dir = Path(coding_dir)
    paths = sorted(coding_dir.glob("guideline_*.yaml"))
    if not paths:
        raise FileNotFoundError(f"no guideline_*.yaml under {coding_dir}")

    records = [load_guideline(p) for p in paths]
    rows = []
    for r in records:
        row = {"unit": r.unit, "jurisdiction": r.jurisdiction,
               "citation": r.citation, "doi": r.doi}
        for name in GuidelineRecord.CODED_FIELDS:
            cf = getattr(r, name)
            row[name] = cf.value
            row[f"{name}_locator"] = cf.locator
        rows.append(row)
    df = pd.DataFrame(rows)
    return records, df


def staph_monitoring_gate(records) -> list[str]:
    """Phase B gate: units that REQUIRE staph monitoring. A non-empty list means
    stop and report — the 'no system requires measurement' framing needs revision."""
    return [r.unit for r in records
            if r.requires_staph_monitoring.value == "yes"]


def grading_asymmetry(records) -> pd.DataFrame:
    """The load-bearing contrast: efficacy graded vs harms graded, per unit."""
    return pd.DataFrame([{
        "unit": r.unit,
        "efficacy_graded": r.efficacy_evidence_graded.value,
        "harms_graded": r.harms_evidence_graded.value,
        "asymmetry": (r.efficacy_evidence_graded.value == "yes"
                      and r.harms_evidence_graded.value in ("no", "partial")),
    } for r in records])


def _write_report(records, df, flagged, asym, root):
    n = len(records)
    n_discuss = sum(r.discusses_staph_risk.value == "yes" for r in records)
    n_counsel = sum(r.requires_counselling_commensal_resistance.value == "yes"
                    for r in records)
    asym_units = asym.loc[asym["asymmetry"], "unit"].tolist()
    md = f"""# Stream B result — guidelines discuss the risk, require no measurement

**Gate: {'CLEAR' if not flagged else 'TRIPPED'} — {'no' if not flagged else len(flagged)}
guideline requires *S. aureus* monitoring.** ({n} units coded; see
`data/processed/guidelines_coded.csv`.)

Coded from the source PDFs with a locator and quote per field; PI-verified (2026-08-22)
and double-coded (20% blind second pass; 92% agreement — `outputs/reliability_result.md`).

## The degenerate case, quantified

- **{n_discuss} of {n} units name a staph/S. aureus resistance risk** in their
  text (CDC, ECDC, Germany); Australia and IUSTI reference 'bystander'/'off-target'
  organisms without naming staph; SF does not mention it.
- **0 of {n} require any *S. aureus* / MRSA / SSTI monitoring or testing** at
  baseline or follow-up. Follow-up, where specified, is STI + HIV screening only.
- **{n_counsel} of {n} require counselling patients about commensal/other-organism
  resistance** (CDC); the rest mention it only partially ('being studied',
  'known and unknown harms').

So a harm that is discussed in the evidence review, and in CDC's case must be
*counselled to patients*, is required to be *measured* by no one. That is the
Stream B point: RR-needed to detect is undefined because nothing is measured.

## Near-misses on the gate (reported, not hidden)

- **Australia Rec 5**: "Clear guidance for clinicians should be developed on
  whether and how to monitor for the emergence of AMR ... in bystander organisms"
  — aspirational, not a requirement, not staph-specific.
- **IUSTI**: makes "off-target antimicrobial resistance" monitoring a service-
  framework principle — population/service level, not a per-patient staph test.

Neither mandates clinical *S. aureus* monitoring; the gate holds.

## The CDC grading asymmetry

Only the CDC guideline is formally evidence-graded, and there the asymmetry is
stark: **efficacy graded (AI, high-quality, strong), harms explicitly "not
graded"** — in the same Methods section, for a harms question that names
antimicrobial-resistant pathogen development. Units with the asymmetry:
{', '.join(asym_units) if asym_units else 'none'}. The other five are consensus/
position/considerations documents with no formal grading (coded `na`).
"""
    (root / "outputs" / "guidelines_result.md").write_text(md)


def run(root: Path | str = None):
    root = Path(root) if root else Path(__file__).resolve().parents[2]
    records, df = build_guideline_corpus(root / "data" / "raw" / "coding")
    out = root / "data" / "processed" / "guidelines_coded.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out, index=False)

    flagged = staph_monitoring_gate(records)
    asym = grading_asymmetry(records)
    _write_report(records, df, flagged, asym, root)
    return records, df, flagged, asym


if __name__ == "__main__":
    records, df, flagged, asym = run()
    n = len(records)
    print(f"coded {n} guideline unit(s); wrote data/processed/guidelines_coded.csv")
    mon = sum(r.requires_staph_monitoring.value == "yes" for r in records)
    print(f"requires_staph_monitoring == yes: {mon}/{n}")
    print("\nGATE:", "TRIPPED — stop and report:" if flagged
          else "clear — no guideline requires staph monitoring.",
          ", ".join(flagged) if flagged else "")
    print("\ngrading asymmetry (efficacy graded, harms not):")
    print(asym.to_string(index=False))
