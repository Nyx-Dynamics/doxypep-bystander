"""Build the Stream B v2 corpus (governmental doxy-PEP guidelines) + gate.

Loads every `gl_*.yaml` under the coding dir into validated GuidelineRecords
(each raising if any coded finding lacks a locator), evaluates the within-artifact
asymmetry, the monitoring gate, and the template-propagation lineage, and writes
`outputs/guidelines_result.md` + `data/processed/guidelines_coded.csv`.

`make` target: `python -m src.coding.build_guidelines`.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.coding.schema_guideline import GuidelineRecord, load_guideline


def build_guideline_corpus(coding_dir: Path | str):
    coding_dir = Path(coding_dir)
    paths = sorted(coding_dir.glob("gl_*.yaml"))
    if not paths:
        raise FileNotFoundError(f"no gl_*.yaml under {coding_dir}")
    return [load_guideline(p) for p in paths]


def frame(records) -> pd.DataFrame:
    rows = []
    for r in records:
        rows.append({
            "unit": r.unit, "jurisdiction_level": r.jurisdiction_level,
            "issuing_body": r.issuing_body, "document_type": r.document_type,
            "s_aureus_named": r.s_aureus_named,
            "s_aureus_location": r.s_aureus_location,
            "s_aureus_monitoring": r.s_aureus_monitoring,
            "in_category_monitoring_present": bool(r.in_category_monitoring.strip()),
            "host_toxicity_labs": r.host_toxicity_labs,
            "within_artifact_asymmetry": r.within_artifact_asymmetry,
            "lab_infrastructure_shown": r.lab_infrastructure_shown,
            "derived_from": r.derived_from,
            "local_mrsa_msm_literature": r.local_mrsa_msm_literature,
            "same_institution_authored_both": r.same_institution_authored_both,
        })
    return pd.DataFrame(rows)


def monitoring_gate(records) -> list[str]:
    """Stream B gate: units that REQUIRE S. aureus monitoring. Non-empty => the
    leg fails and the paper says so (METHODS_streamB.md falsification)."""
    return [r.unit for r in records if r.s_aureus_monitoring == "required"]


def lineage(records) -> pd.DataFrame:
    """Template propagation: which documents state adaptation from another."""
    return pd.DataFrame([
        {"unit": r.unit, "derived_from": r.derived_from}
        for r in records if r.derived_from])


def _write_report(records, df, gate, lin, root):
    n = len(records)
    n_asym = int(df["within_artifact_asymmetry"].sum())
    n_named = int(df["s_aureus_named"].sum())
    n_labs = int(df["lab_infrastructure_shown"].sum())
    loc = df["s_aureus_location"].value_counts().to_dict()
    md = f"""# Stream B result — discussed, counselled, unmeasured (governmental corpus)

**Gate: {'CLEAR' if not gate else 'TRIPPED'} — {'no' if not gate else len(gate)}
governmental guideline REQUIRES *S. aureus* monitoring.** ({n} units;
`data/processed/guidelines_coded.csv`.) Coding is double-coded (blind second pass, 20%;
92% agreement, disagreements adjudicated into CODEBOOK.md rules — `outputs/reliability_result.md`)
and PI-verified.

Scope: governmental public-health authorities only (see DECISIONS.md /
METHODS_streamB.md); FQHCs and professional societies excluded, retained in
`data/raw/guidelines/excluded/` with reasons.

## The within-artifact asymmetry

**{n_asym} of {n}** documents monitor in-category organisms (GC/CT/syphilis)
while leaving *S. aureus* silent or explicitly unmeasured — in the same document.
**{n_named} of {n}** name *S. aureus*; where it appears:
{', '.join(f'{k} ({v})' for k, v in loc.items())}.
**{n_labs} of {n}** order host-toxicity labs (LFT/CMP/CBC) — the lab apparatus
plainly exists; it is pointed at the host, not the organism.

So the bystander is discussed and, in several documents, written into the patient
counselling script — yet no governmental authority requires anyone to measure it.

## Template propagation
"""
    if not lin.empty:
        for _, r in lin.iterrows():
            md += f"\n- **{r['unit']}** states adaptation from: {r['derived_from']}"
        md += ("\n\nIf a single source (SF City Clinic 2022) seeded the counselling "
               "posture, 'no jurisdiction requires staph monitoring' is one decision "
               "replicated, not N independent assessments — a stronger, different "
               "finding. Pursue as prose + a lineage figure (separate analysis).")
    else:
        md += "\n(no derived_from lineage recorded yet)"

    md += f"""

## Gate

{'TRIPPED — a governmental guideline requires S. aureus monitoring; stop and report.' if gate else 'CLEAR — no governmental guideline requires S. aureus monitoring.'}
"""
    (root / "outputs" / "guidelines_result.md").write_text(md)


def run(root: Path | str = None):
    root = Path(root) if root else Path(__file__).resolve().parents[2]
    records = build_guideline_corpus(root / "data" / "raw" / "coding")
    df = frame(records)
    gate = monitoring_gate(records)
    lin = lineage(records)

    proc = root / "data" / "processed"
    proc.mkdir(parents=True, exist_ok=True)
    df.to_csv(proc / "guidelines_coded.csv", index=False)
    _write_report(records, df, gate, lin, root)
    return records, df, gate, lin


if __name__ == "__main__":
    records, df, gate, lin = run()
    n = len(records)
    print(f"coded {n} governmental guideline(s)")
    print(f"within-artifact asymmetry: {int(df['within_artifact_asymmetry'].sum())}/{n}")
    print(f"host-toxicity labs ordered: {int(df['lab_infrastructure_shown'].sum())}/{n}")
    print("GATE:", "TRIPPED — " + ", ".join(gate) if gate else "clear (0 require S. aureus monitoring)")
    print("wrote outputs/guidelines_result.md")
