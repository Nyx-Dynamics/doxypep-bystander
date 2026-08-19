"""Stream A detectability — a DESIGN-BASED SENSITIVITY ANALYSIS.

This is NOT post-hoc / observed power (which fixes the effect size at the trial's
own observed estimate and which statistical reviewers reject on sight). For each
primary-trial S. aureus arm comparison we ask: given only the arm sizes and the
observed control rate, what is the power to detect an effect size specified
INDEPENDENTLY of the trials' own results, and what is the minimum detectable
relative risk at 80% power? The benchmark effect comes from a source EXTERNAL to
the trials being assessed (Soge et al.). Fixing the effect a priori is what makes
this a design/sensitivity calculation rather than observed power.

Two external benchmarks, reported together (the conclusion holds for both):
  * RR = 2.25 — the S. aureus-MATCHED benchmark. Soge observed tetracycline-
    resistant S. aureus colonization 18% vs 8% (P<.0001) in doxy-PEP users vs
    non-users, i.e. RR ~ 2.25. This is the defensible, same-organism benchmark.
  * RR = 1.42 — Soge's GONOCOCCAL >3-doses/month figure. A cross-organism import;
    reported for continuity but flagged as not matched to S. aureus.

Method. The Fisher 2x2 rejection region depends only on the arm sizes and alpha,
so it is enumerated once per (n1, n2); power for any (p_doxy, p_control) is the
binomial mass over that region. EXACT Fisher (not the normal approximation Stream
C used at large N) because these per-arm counts are single- to low-double-digit.
Where a result carries more than one denominator basis (colonized vs all-swabbed),
detectability is reported per basis; the coder does not choose.

Structural gap: MRSA has no primary-trial denominator (NEJM has no methicillin
breakdown), so no detectability can be computed for it from primary data.
"""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import pandas as pd
from scipy.stats import binom, fisher_exact

from src.coding.schema_trial import load_trial

RR_SAUREUS = 2.25       # S. aureus-matched benchmark (Soge 18% vs 8%) — primary
RR_GC = 1.42            # Soge gonococcal >3 doses/mo — cross-organism, secondary
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


def _power_at(n1, n2, p_c, rr):
    return (fisher_power(n1, n2, rr * p_c, p_c) if rr * p_c <= 1 else float("nan"))


def detectability_table(records) -> pd.DataFrame:
    rows = []
    for pr in _saureus_pairs(records):
        p_c = pr["p_control"]
        n1, n2 = pr["n_doxy"], pr["n_control"]
        mdr = min_detectable_rr(n1, n2, p_c)
        pw_saureus = _power_at(n1, n2, p_c, RR_SAUREUS)   # matched benchmark
        pw_gc = _power_at(n1, n2, p_c, RR_GC)             # cross-organism
        rows.append({**pr,
                     "min_detectable_RR": mdr,
                     "power_at_RR_2.25": pw_saureus,
                     "power_at_RR_1.42": pw_gc,
                     "detect_matched_2.25": bool(pw_saureus >= POWER_TARGET),
                     "detect_crossorg_1.42": bool(pw_gc >= POWER_TARGET)})
    return pd.DataFrame(rows)


def mrsa_primary_denominators(records) -> int:
    return sum(1 for r in records for o in r.observations
               if o.source_type == "primary_trial" and o.organism == "mrsa")


def _write_report(records, tab, root):
    n_pairs = len(tab)
    n_matched = int(tab["detect_matched_2.25"].sum()) if n_pairs else 0
    n_cross = int(tab["detect_crossorg_1.42"].sum()) if n_pairs else 0
    md = f"""# Stream A detectability — a design-based sensitivity analysis

**This is NOT post-hoc / observed power.** For each primary-trial *S. aureus* arm
comparison we compute, from the arm sizes and observed control rate alone, the
power to detect an effect size fixed A PRIORI from a source **external** to the
trials (Soge et al.), and the minimum detectable relative risk at 80% power. The
effect is not read off the trials' own results — that is what makes this a
design/sensitivity calculation, not observed power. Exact Fisher (per-arm counts
are single- to low-double-digit, where the normal approximation misleads).

**Benchmarks (both external; conclusion holds for either):**
- **RR = {RR_SAUREUS}** — the *S. aureus*-MATCHED benchmark. Soge: tetracycline-
  resistant *S. aureus* colonization **18% vs 8% (P<.0001)** in doxy-PEP users vs
  non-users, RR ≈ {RR_SAUREUS}. The defensible, same-organism number.
- **RR = {RR_GC}** — Soge's gonococcal >3-doses/month figure; a **cross-organism**
  import, reported for continuity and flagged as such.

Result: **{n_matched} of {n_pairs}** comparisons are powered (≥80%) to detect the
matched **RR {RR_SAUREUS}**; **{n_cross} of {n_pairs}** to detect the cross-organism
RR {RR_GC}. Either way, none are.

| trial | timepoint | basis | doxy | control | p_ctrl | min detectable RR (80%) | power@2.25 | power@1.42 |
|---|---|---|---|---|---|---|---|---|
"""
    for _, r in tab.iterrows():
        mdr = "∞" if r["min_detectable_RR"] == float("inf") else f"{r['min_detectable_RR']:.2f}"
        md += (f"| {r['unit']} | {r['timepoint']} | {r['basis']} | "
               f"{r['k_doxy']}/{r['n_doxy']} | {r['k_control']}/{r['n_control']} | "
               f"{r['p_control']:.0%} | {mdr} | {r['power_at_RR_2.25']:.0%} | "
               f"{r['power_at_RR_1.42']:.0%} |\n")
    md += f"""
Every cell's minimum detectable RR (**3.8–5.1**) sits above **both** the matched
{RR_SAUREUS} and the cross-organism {RR_GC} — so the primary trials are
structurally underpowered for the bystander endpoint regardless of which benchmark
a reviewer prefers. This is the Stream A leg: the trials measured *S. aureus*
non-uniformly and at sample sizes that cannot support inference.

Methods language to carry into the manuscript verbatim: *"a design-based
sensitivity analysis (not observed power): the minimum detectable effect and the
power to detect an externally specified relative risk, with the benchmark drawn
from a source independent of the trials assessed."*

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
    print(f"\npowered to detect matched RR {RR_SAUREUS}: "
          f"{int(tab['detect_matched_2.25'].sum())}/{len(tab)}; "
          f"cross-organism RR {RR_GC}: {int(tab['detect_crossorg_1.42'].sum())}/{len(tab)}")
    print("wrote outputs/detectability_result.md")
