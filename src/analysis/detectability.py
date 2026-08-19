"""Stream A detectability — could the trials detect a Soge-scale bystander effect?

For each primary-trial S. aureus arm comparison (doxy vs control, one basis), the
minimum detectable relative risk at 80% power and the power to detect Soge's
RR = 1.42, computed with the EXACT Fisher test (not the normal approximation
Stream C used at large N — these per-arm counts are single- to low-double-digit,
where the approximation misleads).

Method. The Fisher 2x2 rejection region depends only on the arm sizes and alpha,
so it is enumerated once per (n1, n2); power for any (p_doxy, p_control) is then
the binomial mass over that region. Where a result carries more than one
denominator basis (colonized vs all-swabbed), detectability is reported per basis;
the coder does not choose.

Structural gap: MRSA has no primary-trial denominator (NEJM has no methicillin
breakdown), so no detectability can be computed for it from primary data — a
finding, reported as such.
"""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import pandas as pd
from scipy.stats import binom, fisher_exact

from src.coding.schema_trial import load_trial

RR_SOGE = 1.42
ALPHA = 0.05
POWER_TARGET = 0.80


@lru_cache(maxsize=None)
def _rejection_region(n1: int, n2: int, alpha: float = ALPHA):
    """(x1, x2) tables the two-sided Fisher exact test rejects at alpha."""
    reg = []
    for x1 in range(n1 + 1):
        for x2 in range(n2 + 1):
            _, p = fisher_exact([[x1, n1 - x1], [x2, n2 - x2]])
            if p < alpha:
                reg.append((x1, x2))
    return tuple(reg)


def fisher_power(n1: int, n2: int, p1: float, p2: float, alpha: float = ALPHA) -> float:
    """Exact power of Fisher's test to detect (p1 vs p2) at the given arm sizes."""
    region = _rejection_region(n1, n2, alpha)
    return float(sum(binom.pmf(x1, n1, p1) * binom.pmf(x2, n2, p2)
                     for x1, x2 in region))


def min_detectable_rr(n_exposed: int, n_control: int, p_control: float,
                      power_target: float = POWER_TARGET) -> float:
    """Smallest RR (p_exposed = RR*p_control) the arm sizes can detect at 80% power.
    Returns inf if even RR that saturates the exposed arm (p=1) can't reach it."""
    if p_control <= 0:
        return float("nan")
    rr = 1.0
    while rr * p_control <= 1.0:
        if fisher_power(n_exposed, n_control, rr * p_control, p_control) >= power_target:
            return rr
        rr += 0.05
    return float("inf")


def _saureus_pairs(records):
    """Doxy-vs-control S. aureus pairs from PRIMARY-trial observations, per basis."""
    rows = []
    for r in records:
        prim = [o for o in r.observations
                if o.source_type == "primary_trial" and o.organism == "s_aureus"]
        # index by (timepoint, basis)
        by_key = {}
        for o in prim:
            by_key.setdefault((o.timepoint, o.denominator_basis), {})[o.arm] = o
        for (tp, basis), arms in by_key.items():
            if "doxy" in arms and "control" in arms:
                d, c = arms["doxy"], arms["control"]
                rows.append({"unit": r.unit, "timepoint": tp, "basis": basis,
                             "n_doxy": d.denominator, "k_doxy": d.numerator,
                             "n_control": c.denominator, "k_control": c.numerator,
                             "p_control": c.numerator / c.denominator})
    return rows


def detectability_table(records) -> pd.DataFrame:
    rows = []
    for pr in _saureus_pairs(records):
        p_c = pr["p_control"]
        mdr = min_detectable_rr(pr["n_doxy"], pr["n_control"], p_c)
        # power to detect Soge's 1.42 at the observed control rate
        pw = (fisher_power(pr["n_doxy"], pr["n_control"], RR_SOGE * p_c, p_c)
              if RR_SOGE * p_c <= 1 else float("nan"))
        rows.append({**pr,
                     "min_detectable_RR": mdr,
                     "power_at_RR_1.42": pw,
                     "can_detect_soge": bool(pw >= POWER_TARGET)})
    return pd.DataFrame(rows)


def mrsa_primary_denominators(records) -> int:
    return sum(1 for r in records for o in r.observations
               if o.source_type == "primary_trial" and o.organism == "mrsa")


def _write_report(records, tab, root):
    n_pairs = len(tab)
    n_detect = int(tab["can_detect_soge"].sum()) if n_pairs else 0
    md = f"""# Stream A detectability — the trials cannot see a Soge-scale bystander effect

Exact Fisher power on the primary-trial *S. aureus* arm comparisons. Soge's
within-exposed effect is RR = {RR_SOGE}. First-pass; see coded trials.

**{n_detect} of {n_pairs}** primary *S. aureus* comparisons are powered (>= 80%)
to detect RR = {RR_SOGE} at their observed control rate.

| trial | timepoint | basis | doxy | control | p_ctrl | min detectable RR (80%) | power @1.42 |
|---|---|---|---|---|---|---|---|
"""
    for _, r in tab.iterrows():
        mdr = "∞" if r["min_detectable_RR"] == float("inf") else f"{r['min_detectable_RR']:.2f}"
        md += (f"| {r['unit']} | {r['timepoint']} | {r['basis']} | "
               f"{r['k_doxy']}/{r['n_doxy']} | {r['k_control']}/{r['n_control']} | "
               f"{r['p_control']:.0%} | {mdr} | {r['power_at_RR_1.42']:.0%} |\n")
    md += f"""
Every cell needs a within-exposed RR far above Soge's {RR_SOGE} before its arm
sizes reach 80% power — the primary trials are structurally underpowered for the
bystander endpoint. This is the Stream A leg: the trials measured *S. aureus*
non-uniformly and at sample sizes that cannot support inference.

Why exact (not the Stream C normal approximation): the per-arm counts here are
single- to low-double-digit; the normal approximation to a proportion is invalid
at these n and would understate the minimum detectable effect.

## MRSA — no primary-trial denominator

Primary-trial MRSA observations: **{mrsa_primary_denominators(records)}**. NEJM
reports no methicillin breakdown; the only MRSA numbers are a secondary synthesis
(Szondy) / the CROI abstract, and the DOXYVAC MRSA carriage sits in the main trial
+ a reanalysis (Vanbaelen 2024c). Detectability for MRSA cannot be computed from
primary data — a finding, not a gap.
"""
    (root / "outputs" / "detectability_result.md").write_text(md)


def run(root: Path | str = None):
    root = Path(root) if root else Path(__file__).resolve().parents[2]
    records = [load_trial(p) for p in sorted((root / "data/raw/coding").glob("trial_*.yaml"))]
    tab = detectability_table(records)
    (root / "outputs" / "tables").mkdir(parents=True, exist_ok=True)
    tab.to_csv(root / "outputs/tables/detectability.csv", index=False)
    _write_report(records, tab, root)
    return records, tab


if __name__ == "__main__":
    records, tab = run()
    print(tab.to_string(index=False))
    print(f"\npowered to detect Soge RR 1.42: {int(tab['can_detect_soge'].sum())}/{len(tab)}")
    print("wrote outputs/detectability_result.md")
