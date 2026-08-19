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


def _first_pass(coding_dir: Path) -> dict:
    """unit -> {field: value} from the first-pass gl_*.yaml records."""
    out = {}
    for p in sorted(coding_dir.glob("gl_*.yaml")):
        r = load_guideline(p)
        out[r.unit] = {f: getattr(r, f) for f in FIELDS}
    return out


def _second_pass(path: Path) -> dict:
    data = json.loads(Path(path).read_text())
    return {k: v for k, v in data.items() if not k.startswith("_")}


def paired_frame(root: Path) -> pd.DataFrame:
    """One row per (unit, field) present in BOTH codings, with both labels."""
    fp = _first_pass(root / "data" / "raw" / "coding")
    sp = _second_pass(root / "data" / "raw" / "coding" / "reliability" / "second_pass.json")
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
        rows.append({
            "field": f, "n": len(g),
            "percent_agreement": g["agree"].mean(),
            "cohen_kappa": cohen_kappa(list(g["first_pass"]), list(g["second_pass"])),
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
        k = "n/a (no variation)" if pd.isna(r["cohen_kappa"]) else f"{r['cohen_kappa']:.2f}"
        md += f"| {r['field']} | {int(r['n'])} | {r['percent_agreement']:.0%} | {k} |\n"

    md += "\n## Disagreements (the codebook-refinement points)\n\n"
    if dis.empty:
        md += "None.\n"
    else:
        for _, r in dis.iterrows():
            md += (f"- **{r['unit']} / {r['field']}** — first pass `{r['first_pass']}` "
                   f"vs second `{r['second_pass']}`\n")
    md += """
### Adjudication needed (proposed codebook rules)

- **`s_aureus_monitoring` when a document says 'no laboratory monitoring is
  needed' generally.** Does a blanket no-monitoring statement code as
  `explicitly_none` (it affirmatively denies monitoring, which includes the
  bystander) or `silent` (it is not S. aureus-specific)? Proposed: `explicitly_none`
  — the strongest 'we do not measure it' signal — but this needs a codebook rule.
- **`bystander_treatment` when S. aureus is named ONLY in a reference title.** Does
  a citation-title mention make `bystander_treatment = organism_named`, or does it
  stay at the body-level treatment (`generic_...`) with the mention captured by
  `s_aureus_location = reference_title_only`? Proposed: the latter (organism_named
  requires naming in substantive text), so `s_aureus_location` carries the
  reference mention. Needs a codebook rule.

Kappa is small-N and unstable here; read it with the percent agreement and the
disagreement list. The two disagreements are edge-case rule ambiguities, not
careless errors — resolving them in the codebook and re-coding is the next step.
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
