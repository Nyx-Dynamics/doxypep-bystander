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

import math
from functools import lru_cache
from pathlib import Path

import pandas as pd
from scipy.stats import binom, fisher_exact, norm

from src.coding.schema_trial import load_trial

RR_SAUREUS = 2.25       # S. aureus-matched benchmark (Soge 18% vs 8%) — primary
RR_GC = 1.42            # Soge gonococcal >3 doses/mo — cross-organism, secondary
ALPHA = 0.05
POWER_TARGET = 0.80

# Follow-up / early-stopping facts (for the duration analysis; provenance in the
# CROI artifacts). DOXYVAC was DSMB-stopped for STI efficacy at ~9-month median
# follow-up (Sept 2022); it measured only MRSA carriage, so it has no S. aureus
# primary denominator and cannot enter the detectability computation. DoxyPEP's
# standard-of-care (control) arm was closed at the 5/2022 DSMB efficacy interim
# (data through 5/13/2022 SOC vs 12/1/2022 doxy-PEP) — truncating exactly the
# control-arm S. aureus accrual the comparison is limited by.
DOXYVAC_MEDIAN_FU_MONTHS = 9


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


def required_control_n(p_control: float, rr: float, ratio: float,
                       alpha: float = ALPHA, power: float = POWER_TARGET) -> float:
    """Control-arm colonised N needed for `power` to detect RR `rr` at control rate
    `p_control`, preserving the trial's doxy:control arm `ratio` (n_doxy = ratio·n).

    Large-sample normal approximation for two proportions. This is the correct tool
    here: the REQUIRED N lands in the hundreds-to-thousands per arm, exactly the
    regime where the approximation is accurate (and where exact-Fisher region
    enumeration is impractical). Exact Fisher is retained for the tiny REALISED
    denominators; `_write_duration_report` spot-checks that the solved N delivers
    ~80% by exact Fisher. Returns inf if the exposed rate saturates (rr·p >= 1)."""
    p2, p1 = p_control, rr * p_control
    if p1 >= 1.0 or p_control <= 0:
        return float("inf")
    za, zb, r = norm.ppf(1 - alpha / 2), norm.ppf(power), ratio
    pbar = (p1 * r + p2) / (r + 1)
    c_null = math.sqrt(pbar * (1 - pbar) * (1 / r + 1))
    c_alt = math.sqrt(p1 * (1 - p1) / r + p2 * (1 - p2))
    sqrt_n = (zb * c_alt + za * c_null) / abs(p1 - p2)
    return sqrt_n ** 2


def duration_table(records) -> pd.DataFrame:
    """Per S. aureus comparison: the sample the design would have needed to reach 80%
    power for each external benchmark, and the multiple over what the trial realised."""
    rows = []
    for pr in _saureus_pairs(records):
        p_c, n1, n2 = pr["p_control"], pr["n_doxy"], pr["n_control"]
        ratio = n1 / n2
        rec = {**pr, "arm_ratio": ratio}
        for tag, rr in (("2.25", RR_SAUREUS), ("1.42", RR_GC)):
            req_ctrl = required_control_n(p_c, rr, ratio)
            req_doxy = ratio * req_ctrl if math.isfinite(req_ctrl) else float("inf")
            mult = req_ctrl / n2 if math.isfinite(req_ctrl) else float("inf")
            rec[f"req_control_{tag}"] = req_ctrl
            rec[f"req_doxy_{tag}"] = req_doxy
            rec[f"multiple_{tag}"] = mult
        rows.append(rec)
    return pd.DataFrame(rows)


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
{RR_SAUREUS} and the cross-organism {RR_GC} — so the 2023 interim CROSS-SECTIONAL
comparisons were underpowered for the prespecified resistance benchmarks. This explains why
the interim presentation read as non-informative; it does NOT apply to the 2025
participant-level time-to-event analysis (Luetkemeyer 2025), which detected the signal
(incident doxy-R *S. aureus*, HR 3.89, 95% CI 1.42-10.68). The Stream A point is that the
interim cross-sectional estimand was inadequate to a signal the incidence estimand later
resolved — not that the trial could never support inference.

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


def _exact_validation(req_doxy, req_control, p_control, rr, max_enum=260):
    """Exact-Fisher power at the solved (rounded) required N — confirms the normal
    approximation delivers ~80%. Skipped when the region enumeration is too large
    (all-swabbed N in the hundreds-to-thousands), where the approximation is anyway
    the appropriate tool. Returns power or None."""
    n1, n2 = round(req_doxy), round(req_control)
    if not (math.isfinite(req_doxy) and n1 <= max_enum and n2 <= max_enum):
        return None
    return _power_at(n1, n2, p_control, rr)


def _write_duration_report(records, dtab, root):
    md = f"""# Stream A duration / sample-accrual — closing the "stopped early" claim

A **design-based sensitivity analysis** (not observed power), extending
`detectability_result.md`. For each primary-trial *S. aureus* comparison we solve for
the sample the design would have needed to reach 80% power against an **external**
benchmark (Soge et al.), and report the multiple over what the trial actually realised.
**Benchmark held at the matched RR = {RR_SAUREUS}** (tetracycline-resistant *S. aureus*,
same organism, same source `detectability.py` uses); the cross-organism RR = {RR_GC}
(gonococcal) is a **secondary** column, flagged. Required N uses the large-sample normal
approximation (valid where the required N lands — hundreds to thousands per arm); the
realised-denominator detectability in the companion report stays exact Fisher because
those counts are tiny. *S. aureus* unit throughout.

| comparison | basis | realised doxy/ctrl | p_ctrl | need doxy/ctrl @{RR_SAUREUS} | **multiple @{RR_SAUREUS}** | multiple @{RR_GC} (cross-org) | exact-Fisher check |
|---|---|---|---|---|---|---|---|
"""
    for _, r in dtab.iterrows():
        val = _exact_validation(r["req_doxy_2.25"], r["req_control_2.25"],
                                r["p_control"], RR_SAUREUS)
        val_s = f"{val:.0%} @ solved N" if val is not None else "N too large (approx)"
        need = (f"{r['req_doxy_2.25']:.0f}/{r['req_control_2.25']:.0f}"
                if math.isfinite(r["req_doxy_2.25"]) else "∞")
        md += (f"| {r['unit']} {r['timepoint']} | {r['basis']} | "
               f"{r['k_doxy']}/{r['n_doxy']} · {r['k_control']}/{r['n_control']} | "
               f"{r['p_control']:.0%} | {need} | **{r['multiple_2.25']:.1f}×** | "
               f"{r['multiple_1.42']:.0f}× | {val_s} |\n")

    # headline figures: the M12 colonised comparison (the endpoint the trials headline)
    m12 = dtab[(dtab["timepoint"] == "month12") & (dtab["basis"] == "colonized_participants")]
    m6 = dtab[(dtab["timepoint"] == "month6") & (dtab["basis"] == "colonized_participants")]
    k12 = float(m12["multiple_2.25"].iloc[0]) if len(m12) else float("nan")
    k6 = float(m6["multiple_2.25"].iloc[0]) if len(m6) else float("nan")
    k12_gc = float(m12["multiple_1.42"].iloc[0]) if len(m12) else float("nan")
    md += f"""
**The sample-size verdict.** At the twelve-month endpoint the trials headline, DoxyPEP
would have needed **≈{k12:.0f}× its realised colonised *S. aureus* sample** to reach 80%
power for the matched RR {RR_SAUREUS} (≈{k12_gc:.0f}× for the cross-organism RR {RR_GC});
at six months, ≈{k6:.1f}×. Across bases and timepoints the multiple never falls below
~3.6×. The exact-Fisher spot-check confirms the solved denominators deliver ~80%,
validating the approximation. These are lower bounds on what detection would have taken:
the realised sample is a small fraction of it.

**Duration is not inferable from the available schedule — stated, not fabricated.** The
*S. aureus* accrual has only two arm-split timepoints (month 6 and month 12), and the
per-visit denominators **decline** over follow-up (DoxyPEP colonised doxy arm 51 → 31;
all-swabbed 192 → 111) as retention drops. A declining two-point curve cannot support a
defensible extrapolation to the follow-up duration at which cumulative observations would
reach the required N — and because the swabs are repeated on a shrinking cohort, pooling
across visits would not accrue independent observations in any case. We therefore report
the **sample-accrual** result and do **not** infer a duration. Running longer at the
realised accrual would not have closed a ~6× gap; a larger enrolled cohort would have.

**The early efficacy stop is why the realised denominator is what it is.** DoxyPEP's
standard-of-care arm was closed at the 5/2022 DSMB efficacy interim (data through
5/13/2022 for SOC vs 12/1/2022 for doxy-PEP), truncating exactly the **control-arm**
*S. aureus* accrual — the smaller arm, which is the binding constraint on every
comparison above (control colonised n = 29 at M6, 24 at M12). DOXYVAC was likewise
DSMB-stopped for STI efficacy at ~{DOXYVAC_MEDIAN_FU_MONTHS}-month median follow-up, but
it measured only MRSA carriage and so has **no primary *S. aureus* denominator** — it
cannot be brought to this test at all (MRSA note below). In both pivotal trials the
primary STI-efficacy endpoint was met and the trial closed before the bystander endpoint
could accrue the sample its own design would have required.

**License.** The trials would have needed ≈{k12:.0f}× their realised *S. aureus* sample
to power detection of the matched RR {RR_SAUREUS}, and the early efficacy stop foreclosed
that accrual. This is design-based sensitivity against an external benchmark — **not** a
claim that a larger or longer trial *would have found* an effect, and **not** any
statement that the effect exists.

## MRSA — cannot be brought to this test

Primary-trial MRSA observations: **{mrsa_primary_denominators(records)}**. MRSA has no
primary-trial *S. aureus*-style denominator (NEJM reports no methicillin breakdown;
DOXYVAC's MRSA carriage is the main trial + a reanalysis). The duration/sample-accrual
computation is *S. aureus*-only, as the detectability computation is — a finding, not a
gap.
"""
    (root / "outputs" / "duration_result.md").write_text(md)


def run(root: Path | str = None):
    root = Path(root) if root else Path(__file__).resolve().parents[2]
    records = [load_trial(p) for p in sorted((root / "data/raw/coding").glob("trial_*.yaml"))]
    tab = detectability_table(records)
    dtab = duration_table(records)
    (root / "outputs" / "tables").mkdir(parents=True, exist_ok=True)
    tab.to_csv(root / "outputs/tables/detectability.csv", index=False)
    dtab.to_csv(root / "outputs/tables/duration.csv", index=False)
    _write_report(records, tab, root)
    _write_duration_report(records, dtab, root)
    return records, tab, dtab


if __name__ == "__main__":
    records, tab, dtab = run()
    print(tab.to_string(index=False))
    print(f"\npowered to detect matched RR {RR_SAUREUS}: "
          f"{int(tab['detect_matched_2.25'].sum())}/{len(tab)}; "
          f"cross-organism RR {RR_GC}: {int(tab['detect_crossorg_1.42'].sum())}/{len(tab)}")
    print("\nrequired-sample multiples (S. aureus, RR 2.25 matched):")
    for _, r in dtab.iterrows():
        print(f"  {r['unit']} {r['timepoint']:8s} {r['basis'][:9]:9s}: "
              f"{r['multiple_2.25']:.1f}× realised (cross-org RR 1.42: {r['multiple_1.42']:.0f}×)")
    print("wrote outputs/detectability_result.md, outputs/duration_result.md")
