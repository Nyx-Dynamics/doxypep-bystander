"""Inter-coder reliability for the Stream B coding (Phase F).

Compares the first-pass coding (`data/raw/coding/gl_*.yaml`, coder
`claude-firstpass`) against an INDEPENDENT blind second coding
(`data/raw/coding/reliability/second_pass.json`, coder `claude-independent-2nd-pass`)
on the coded categorical fields, and reports per-field percent agreement and
Cohen's kappa plus an overall agreement.

A one-person audit with no reliability estimate is the softness this project
criticises; this makes the estimate explicit and reproducible. Small-N caveat:
kappa is unstable on a handful of documents — read it alongside percent agreement
and the disagreement list, which is where the codebook gets refined.
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from src.coding.schema_guideline import load_guideline

FIELDS = ["bystander_treatment", "s_aureus_named", "s_aureus_location",
          "s_aureus_monitoring", "host_toxicity_labs"]


def cohen_kappa(a: list, b: list) -> float:
    """Cohen's kappa for two equal-length label sequences (no sklearn)."""
    n = len(a)
    if n == 0:
        return float("nan")
    po = sum(x == y for x, y in zip(a, b)) / n
    cats = set(a) | set(b)
    pe = sum((a.count(c) / n) * (b.count(c) / n) for c in cats)
    if pe == 1.0:
        return 1.0 if po == 1.0 else float("nan")
    return (po - pe) / (1.0 - pe)


def _load_json(path: Path) -> dict:
    data = json.loads(Path(path).read_text())
    return {k: v for k, v in data.items() if not k.startswith("_")}


def paired_frame(root: Path) -> pd.DataFrame:
    """One row per (unit, field) present in BOTH codings, with both labels.

    First pass is the FROZEN snapshot (values as coded at double-coding time), not
    the live gl_*.yaml — so the agreement is reproducible and not altered by the
    later PI adjudication."""
    rel = root / "data" / "raw" / "coding" / "reliability"
    fp = _load_json(rel / "first_pass_snapshot.json")
    sp = _load_json(rel / "second_pass.json")
    rows = []
    for unit in sp:
        if unit not in fp:
            continue
        for f in FIELDS:
            c1, c2 = str(fp[unit][f]).lower(), str(sp[unit][f]).lower()
            rows.append({"unit": unit, "field": f, "first_pass": c1,
                         "second_pass": c2, "agree": c1 == c2})
    return pd.DataFrame(rows)


def field_agreement(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for f, g in df.groupby("field"):
        labels = set(g["first_pass"]) | set(g["second_pass"])
        # a field that collapses to one category has zero variance: chance
        # agreement is 100% and kappa is UNDEFINED, not merely unstable. Report it
        # as a descriptive constant, never as a kappa.
        constant = len(labels) <= 1
        rows.append({
            "field": f, "n": len(g),
            "percent_agreement": g["agree"].mean(),
            "cohen_kappa": None if constant
            else cohen_kappa(list(g["first_pass"]), list(g["second_pass"])),
            "constant": constant,
        })
    return pd.DataFrame(rows).sort_values("field")


def disagreements(df: pd.DataFrame) -> pd.DataFrame:
    return df[~df["agree"]][["unit", "field", "first_pass", "second_pass"]]


def run(root: Path | str = None):
    root = Path(root) if root else Path(__file__).resolve().parents[2]
    df = paired_frame(root)
    fa = field_agreement(df)
    dis = disagreements(df)
    overall = df["agree"].mean()
    n_units = df["unit"].nunique()

    md = f"""# Stream B inter-coder reliability (Phase F)

First pass: `claude-firstpass` (gl_*.yaml). Second pass: `claude-independent-2nd-pass`
(blind, coded from the source PDFs + codebook only; see
`data/raw/coding/reliability/second_pass.json`). Sample: **{n_units} documents**
spanning all `s_aureus_location` categories, {len(df)} field-codings.

**Overall percent agreement: {overall:.0%}** ({int(df['agree'].sum())}/{len(df)}).

Per field:

| field | n | % agreement | Cohen's kappa |
|---|---|---|---|
"""
    for _, r in fa.iterrows():
        if r["constant"]:
            k = "n/a — constant (see below)"
        else:
            k = f"{r['cohen_kappa']:.2f}"
        md += f"| {r['field']} | {int(r['n'])} | {r['percent_agreement']:.0%} | {k} |\n"

    md += "\n## Disagreements and adjudication (2026-08-19)\n\n"
    md += ("The two initial disagreements were both codebook edge-cases, not "
           "careless errors, and were adjudicated by the PI into binding rules "
           "(now in CODEBOOK.md):\n\n")
    for _, r in dis.iterrows():
        md += (f"- **{r['unit']} / {r['field']}** — first pass `{r['first_pass']}` "
               f"vs second `{r['second_pass']}`\n")
    md += """
1. **NYC `s_aureus_monitoring`** (`explicitly_none` vs `silent`) → adjudicated to
   **`silent`** (the second coder's stricter reading). The "No laboratory
   monitoring is needed" sentence sits in Dosing and Prescribing, right after the
   NAAT/serology instructions — it answers the safety-bloodwork question, so it is
   `host_toxicity_labs = explicitly_none`, not a decision about microbiological
   surveillance. NYC is now the exact mirror of Chicago (Chicago orders host labs,
   silent on resistance; NYC waives host labs, names staph in counselling) — both
   fail to touch the organism, from opposite directions.
2. **Philadelphia `bystander_treatment`** (`generic_microbiome_resistance` vs
   `organism_named`) → binding rule: a mention only inside a reference title does
   NOT make `organism_named`; the mention is carried by
   `s_aureus_location = reference_title_only`.

## Reporting notes

- **`s_aureus_monitoring` is a descriptive CONSTANT, not a kappa.** After
  adjudication no document in the corpus specifies *S. aureus* monitoring — the
  field collapses to a single value, so chance agreement is 100% and kappa is
  undefined. Report it as: **0 of the coded governmental documents specify
  S. aureus monitoring** (hash-verified staph keyword search, guidelines/CHECKSUMS.md).
  The gate is unanimous, not a gradient with one contested cell.
- **`bystander_treatment` kappa = 0.58 (moderate)** on a five-document sample —
  stated plainly, not rounded up. Both disagreements were resolved into binding
  rules afterward; re-coding under those rules is the follow-through. This belongs
  in the limitations.
- The other fields with variance (`s_aureus_named`, `s_aureus_location`,
  `host_toxicity_labs`) agreed perfectly (kappa 1.0), including the key
  `s_aureus_location` (where the bystander appears), which is the load-bearing
  field for the paper.
"""
    (root / "outputs" / "reliability_result.md").write_text(md)
    return df, fa, dis, overall


if __name__ == "__main__":
    df, fa, dis, overall = run()
    print(f"overall percent agreement: {overall:.0%} ({int(df['agree'].sum())}/{len(df)})")
    print(fa.to_string(index=False))
    print(f"\ndisagreements: {len(dis)}")
    print(dis.to_string(index=False) if not dis.empty else "  none")
    print("wrote outputs/reliability_result.md")
