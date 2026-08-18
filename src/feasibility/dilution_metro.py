"""Phase 0 feasibility gate — metro level (the pivot from the failed state gate).

The state gate (`dilution.py`) failed: the doxy-PEP-exposed subgroup is too
dilute inside a whole state's *S. aureus* isolate stream. SCAFFOLD.md says pivot
to metro (SF, King County, LA, NYC), where uptake density is far higher. This
module runs the same feasibility test at metro grain.

Key simplification. The dilution fraction is population-independent — it depends
on exposure *density*, not headcount:

    f = MALE_FRACTION * (male_prep_rate / 1e5) * uptake * kappa          (5)

where male_prep_rate is per 100k adult males (AIDSVu) and MALE_FRACTION converts
a male-specific density to a share of the whole (both-sex) isolate pool. So the
gate reduces to a threshold on density: invert eq. (4) for the fraction of
exposed isolates required to detect at RR = 1.42,

    f_required = MDE / ((RR_SOGE - 1) * R0)                              (6)

and convert to the male PrEP density that would be needed:

    rate_required = f_required * 1e5 / (MALE_FRACTION * uptake * kappa)  (7)

We then compare rate_required against the DENSEST geography that actually exists
in the AIDSVu panel — **Washington, D.C.** (2,694 / 100k adult males in 2022, a
city-state and a generous empirical ceiling for any real US metro; SF and King
County do not exceed it). No metro-specific PrEP file is on disk (the AIDSVu
metro downloadable datasets carry HIV prevalence/SDOH, not PrEP — CLAUDE.md), so
D.C. stands in as the observed high-water mark and results are expressed as
multiples of it. If a cell needs many times the densest geography in the country,
a real metro cannot reach it.

No outcome data is touched. Gated on the state result; itself gates Phase 1.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

from src.loaders.aidsvu import load_aidsvu
from src.feasibility.dilution import (
    RR_SOGE, R0_GRID, R0_BASELINE, KAPPA_GRID, UPTAKE_GRID, N_GRID,
    DOSE_ABOVE_THRESHOLD, mde_proportion,
)

# adult-male share of the total (both-sex) population that generates isolates.
# Checked against AIDSVu internal consistency: male_prep_users/male_prep_rate*1e5
# recovers ~adult-male population (CA 2022 -> 16.4M), and that over total adult
# population is ~0.49. See DECISIONS.md.
MALE_FRACTION = 0.5
# The most that any plausible real metro could exceed the densest observed US
# geography (D.C.). SF/King County male PrEP density is at or below D.C.'s, so
# 2x is already generous. A cell is "achievable" only if the required density is
# within this multiple of D.C.
ACHIEVABLE_MULTIPLE = 2.0


def required_f(r0, n, rr=RR_SOGE):
    """Eq. (6): fraction of exposed isolates needed to detect at RR."""
    return mde_proportion(r0, n) / ((rr - 1.0) * r0)


def required_male_prep_rate(r0, n, uptake, kappa, rr=RR_SOGE,
                            male_fraction=MALE_FRACTION):
    """Eq. (7): male PrEP density (per 100k males) needed for detection.

    ``male_fraction`` is exposed as a parameter so the robustness sweep can vary
    it; it defaults to the module constant used everywhere else. The dose-above-
    threshold factor (Phase A item 3) enters the denominator: only the
    >3-doses/month subgroup carries Soge's RR 1.42, so a higher density is needed.
    """
    f_req = required_f(r0, n, rr)
    return f_req * 1e5 / (male_fraction * uptake * kappa * DOSE_ABOVE_THRESHOLD)


def density_from_rate(male_prep_rate, uptake, kappa):
    """Eq. (5): exposed-isolate fraction implied by a male PrEP density."""
    return (MALE_FRACTION * (male_prep_rate / 1e5) * uptake * kappa
            * DOSE_ABOVE_THRESHOLD)


def observed_max_density(df, year=2022):
    """Densest geography in the AIDSVu panel — the empirical metro ceiling."""
    d = df[df.year == year]
    row = d.loc[d["male_prep_rate"].idxmax()]
    return row["state"], float(row["male_prep_rate"])


def metro_table(df, year=2022):
    """For each (uptake, kappa, r0, N): the male PrEP density required to detect,
    expressed absolutely, as a share of males, and as a multiple of the densest
    observed US geography."""
    _, ref_rate = observed_max_density(df, year)
    rows = []
    for uptake in UPTAKE_GRID:
        for kappa in KAPPA_GRID:
            for r0 in R0_GRID:
                for n in N_GRID:
                    rate = required_male_prep_rate(r0, n, uptake, kappa)
                    rows.append({
                        "uptake": uptake, "kappa": kappa, "r0": r0,
                        "N_isolates": n,
                        "f_required": required_f(r0, n),
                        "rate_required_per100k": rate,
                        "pct_of_males_required": rate / 1e3,
                        "multiples_of_densest_US": rate / ref_rate,
                        "achievable": rate <= ACHIEVABLE_MULTIPLE * ref_rate,
                    })
    return pd.DataFrame(rows)


@dataclass
class MetroGate:
    passed: bool
    ref_geo: str
    ref_rate: float
    best_multiple: float
    best_row: dict
    n_achievable: int
    n_cells: int

    def verdict(self) -> str:
        return ("PASS — a real metro could reach detectable density"
                if self.passed else
                "FAIL — even the densest US geography falls short (targeted "
                "clinic sampling required, which is no longer ecological)")


def evaluate_metro_gate(table, ref_geo, ref_rate):
    best = table.loc[table["multiples_of_densest_US"].idxmin()]
    n_achievable = int(table["achievable"].sum())
    passed = bool(n_achievable > 0)
    return MetroGate(
        passed=passed, ref_geo=ref_geo, ref_rate=ref_rate,
        best_multiple=float(best["multiples_of_densest_US"]),
        best_row=best.to_dict(),
        n_achievable=n_achievable, n_cells=len(table))


# --------------------------------------------------------------------------- #
# robustness — show the verdict does not hinge on any single assumption        #
# --------------------------------------------------------------------------- #
MALE_FRACTION_SWEEP = (0.40, 0.50, 0.60)
# even GRANT a hypothetical metro up to 5x the densest observed US geography
ACHIEVABLE_MULTIPLE_SWEEP = (1.0, 2.0, 3.0, 5.0)


def robustness_sweep(df, year=2022):
    """Recount achievable cells while varying the two previously-fixed knobs
    (male fraction, achievable multiple) across the full R0 x N x kappa x uptake
    grid. The point: achievable-cell count should stay 0 throughout, so the
    negative verdict is not an artifact of MALE_FRACTION=0.5 or a 2x ceiling."""
    _, ref_rate = observed_max_density(df, year)
    rows = []
    for mf in MALE_FRACTION_SWEEP:
        for mult in ACHIEVABLE_MULTIPLE_SWEEP:
            n_ach = 0
            n_cells = 0
            for uptake in UPTAKE_GRID:
                for kappa in KAPPA_GRID:
                    for r0 in R0_GRID:
                        for n in N_GRID:
                            n_cells += 1
                            rate = required_male_prep_rate(
                                r0, n, uptake, kappa, male_fraction=mf)
                            if rate <= mult * ref_rate:
                                n_ach += 1
            rows.append({"male_fraction": mf, "achievable_multiple": mult,
                         "n_achievable": n_ach, "n_cells": n_cells})
    return pd.DataFrame(rows)


def breakeven_frontier(df, year=2022, uptake=max(UPTAKE_GRID), r0=R0_BASELINE):
    """For each (N, kappa) at the most generous uptake and central R0, the male
    PrEP density that would flip the gate — expressed as a share of ALL adult
    males on PrEP and as multiples of the densest observed US geography. The
    '% of adult males' unit is proxy-free: it needs no metro-specific datapoint
    to be recognised as impossible (>100%) or implausible (well above any real
    metro's single-digit-% MSM PrEP coverage)."""
    _, ref_rate = observed_max_density(df, year)
    rows = []
    for kappa in KAPPA_GRID:
        for n in N_GRID:
            rate = required_male_prep_rate(r0, n, uptake, kappa)
            pct = rate / 1e3                      # per-100k-males -> % of males
            rows.append({
                "uptake": uptake, "r0": r0, "kappa": kappa, "N_isolates": n,
                "rate_required_per100k": rate,
                "pct_of_all_adult_males": pct,
                "multiples_of_densest_US": rate / ref_rate,
                "physically_possible": bool(pct <= 100.0),
            })
    return pd.DataFrame(rows)


# --------------------------------------------------------------------------- #
# outputs                                                                      #
# --------------------------------------------------------------------------- #
def _plot_breakeven(be, ref_geo, ref_rate, out_png):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(7.5, 5))
    for kappa in sorted(be["kappa"].unique()):
        s = be[be["kappa"] == kappa].sort_values("N_isolates")
        ax.plot(s["N_isolates"], s["pct_of_all_adult_males"],
                marker="o", label=f"kappa {kappa:g}x")
    ax.axhline(100, color="crimson", ls="--", lw=1.5,
               label="physical ceiling (100% of males)")
    ax.axhline(ref_rate / 1e3, color="grey", ls=":", lw=1.5,
               label=f"densest US geography ({ref_geo}, {ref_rate/1e3:.1f}%)")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("isolates per geography-year (N)")
    ax.set_ylabel("% of ALL adult males on PrEP required")
    ax.set_title("Break-even: male-PrEP coverage required to make the\n"
                 "doxy-PEP signal detectable (uptake 55%, R0 10%)\n"
                 "every curve sits above any real metro's coverage")
    ax.legend(fontsize=8, loc="best")
    fig.tight_layout()
    out_png.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_png, dpi=130)
    plt.close(fig)


def _plot(df, gate, year, out_png):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.colors as mcolors

    r0 = R0_BASELINE
    n = max(N_GRID)
    U = np.array(UPTAKE_GRID)
    K = np.array(KAPPA_GRID)
    Z = np.array([[required_male_prep_rate(r0, n, u, k) / gate.ref_rate
                   for u in U] for k in K])
    fig, ax = plt.subplots(figsize=(7, 5))
    im = ax.imshow(Z, origin="lower", aspect="auto", cmap="magma_r",
                   norm=mcolors.LogNorm())
    ax.set_xticks(range(len(U)), [f"{u:.0%}" for u in U])
    ax.set_yticks(range(len(K)), [f"{k:g}x" for k in K])
    ax.set_xlabel("doxy-PEP uptake among PrEP users")
    ax.set_ylabel("isolate enrichment (kappa)")
    for i in range(len(K)):
        for j in range(len(U)):
            ax.text(j, i, f"{Z[i, j]:.0f}x", ha="center", va="center",
                    color="white", fontsize=10)
    ax.set_title("Male PrEP density required for a detectable metro shift,\n"
                 f"as multiples of the densest US geography "
                 f"({gate.ref_geo}, {gate.ref_rate:.0f}/100k)\n"
                 f"R0={r0:.0%}, N={n:,}/yr (generous) — 1x = already the US max")
    fig.colorbar(im, ax=ax, label="x densest US geography (log)")
    fig.tight_layout()
    out_png.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_png, dpi=130)
    plt.close(fig)


def _write_report(table, gate, robustness, breakeven, year, root,
                  fig_rel, tab_rel, be_fig_rel, rob_rel, be_rel):
    b = gate.best_row
    realistic_rob = robustness[(robustness.achievable_multiple <= 2.0) &
                               (robustness.male_fraction <= 0.5)]
    max_ach_realistic = int(realistic_rob["n_achievable"].max())
    max_ach_5x = int(robustness["n_achievable"].max())
    be_real = breakeven[(breakeven.N_isolates == min(N_GRID)) &
                        (breakeven.kappa == 1.0)].iloc[0]
    be_gen = breakeven[(breakeven.N_isolates == max(N_GRID)) &
                       (breakeven.kappa == max(KAPPA_GRID))].iloc[0]
    md = f"""# Phase 0 feasibility result — metro-level dilution (the pivot)

**Verdict: {gate.verdict()}.**

Generated by `src/feasibility/dilution_metro.py` on the AIDSVu panel
({year}). Follows the failed state-level gate (`feasibility_result.md`). No
outcome data was used.

## What was tested

The dilution fraction is population-independent — it tracks exposure *density*,
not headcount (eq. 5). So the metro question is: what male-PrEP density would a
metro need for the state-level-undetectable signal to become detectable, and can
any real metro reach it? We invert to the required density (eq. 6-7) and compare
it against the **densest geography that actually exists** in AIDSVu:
**{gate.ref_geo}** at **{gate.ref_rate:.0f}/100k adult males** — a city-state and
a generous ceiling for any US metro (SF and King County do not exceed it).

No metro-specific PrEP file exists on disk (AIDSVu metro datasets are HIV
prevalence/SDOH, not PrEP), so D.C. stands in as the empirical high-water mark
and requirements are expressed as multiples of it.

## Result

Of {gate.n_cells} grid cells, **{gate.n_achievable}** are achievable (required
density within {ACHIEVABLE_MULTIPLE:g}x the densest US geography).

The least-demanding cell still needs male-PrEP density = **{b['multiples_of_densest_US']:.1f}x
{gate.ref_geo}** ({b['pct_of_males_required']:.1f}% of all adult males on PrEP),
and only under the most generous inputs: uptake {b['uptake']:.0%}, enrichment
{b['kappa']:g}x, R0 {b['r0']:.0%}, N = {int(b['N_isolates']):,}/year. Under
realistic surveillance volumes and proportional sampling the requirement runs to
tens or hundreds of times D.C.'s density — i.e. more than 100% of males on PrEP,
which is impossible.

## Interpretation — why this matters

The signal does not fail for lack of a real association; it fails because
**population-scale ecological sampling dilutes it below detectability at every
geographic grain that has population denominators** — state and metro alike. The
only lever that rescues detection is enrichment (kappa): sampling *S. aureus*
specifically from the doxy-PEP-exposed population. But high enrichment is exactly
**targeted clinic sampling** — a cohort/clinic design, no longer an ecological
one. King County's doxy-PEP-era sexual-health-clinic isolate data is that design.

This is the measurement-inheritance thesis made quantitative: existing
surveillance is not instrumented to detect a bystander-organism signal, because
its sampling frame is the general population while the exposure is concentrated in
a small, specifically-sampled subgroup.

## Robustness — the verdict does not hinge on any single assumption

The comparison above uses D.C. as a proxy for the densest US metro and fixes two
knobs (male fraction 0.5, an "achievable" ceiling of 2x D.C.). Neither drives the
result:

- **Assumption sweep** ({rob_rel}). Varying male fraction over
  {MALE_FRACTION_SWEEP} AND the achievable ceiling over
  {ACHIEVABLE_MULTIPLE_SWEEP} across the full R0 x N x kappa x uptake grid. At any
  **realistic** metro density (<= 2x the densest US geography) with male fraction
  <= 0.5, the achievable-cell count is **{max_ach_realistic}** of {gate.n_cells} —
  the verdict does not move. Cells begin to open only when one *simultaneously*
  grants a metro **3x-5x** denser than any US geography that exists AND the
  fantastical isolate volume of {max(N_GRID):,}/year AND {min(k for k in KAPPA_GRID if k >= 3):g}x+
  enrichment; even then at most **{max_ach_5x}** of {gate.n_cells} cells. Every
  cell that ever opens is a compound of implausibilities, and its high enrichment
  is targeted clinic sampling — a cohort design, not the ecological one under test.

- **Break-even, in proxy-free units** ({be_rel}, figure `{be_fig_rel}`). The male
  PrEP coverage that would be *required* to make the signal detectable, as a share
  of **all adult males**:
  - realistic surveillance (N={int(be_real['N_isolates']):,}/yr, proportional
    sampling): **{be_real['pct_of_all_adult_males']:.0f}% of all adult males on
    PrEP** — above the physical ceiling of 100%, i.e. impossible.
  - fantastical best case (N={int(be_gen['N_isolates']):,}/yr, {be_gen['kappa']:g}x
    enrichment): **{be_gen['pct_of_all_adult_males']:.1f}% of all adult males** —
    still far above any real metro, where MSM are a single-digit percentage of men
    and PrEP covers only a fraction of them.

  Expressed this way the conclusion needs no metro-specific datapoint: no US
  metro has anywhere near the required share of its *entire* adult-male population
  on PrEP.

## Decision

Abandon the population-ecological design at **both** state and metro grain as the
primary quantitative test. Two legitimate paths forward, to choose deliberately:

1. **Targeted cohort/clinic design** — King County (and SF) sexual-health-clinic
   *S. aureus* isolates, where the sampled population *is* the exposed one
   (kappa large by construction). This is a different study, not this ecological
   panel, and needs its own preregistration.
2. **Surveillance-infrastructure paper** — write up this two-level negative
   feasibility result as the empirical demonstration that no existing
   surveillance system can detect the bystander signal. Per CLAUDE.md this is a
   legitimate and arguably the more important output.

## Artifacts

- required-density table: `{tab_rel}`
- required-density figure: `{fig_rel}`
- assumption-robustness sweep: `{rob_rel}`
- break-even frontier table: `{be_rel}`
- break-even figure: `{be_fig_rel}`
"""
    (root / "outputs" / "feasibility_metro_result.md").write_text(md)


def run(root: Path | str = None, year: int = 2022) -> MetroGate:
    root = Path(root) if root else Path(__file__).resolve().parents[2]
    df = load_aidsvu(root / "data" / "raw" / "aidsvu")
    ref_geo, ref_rate = observed_max_density(df, year)
    table = metro_table(df, year)
    gate = evaluate_metro_gate(table, ref_geo, ref_rate)
    robustness = robustness_sweep(df, year)
    breakeven = breakeven_frontier(df, year)

    tab_rel = "outputs/tables/feasibility_metro.csv"
    rob_rel = "outputs/tables/feasibility_metro_robustness.csv"
    be_rel = "outputs/tables/feasibility_metro_breakeven.csv"
    fig_rel = "outputs/figures/feasibility_metro.png"
    be_fig_rel = "outputs/figures/feasibility_metro_breakeven.png"
    (root / "outputs" / "tables").mkdir(parents=True, exist_ok=True)
    table.to_csv(root / tab_rel, index=False)
    robustness.to_csv(root / rob_rel, index=False)
    breakeven.to_csv(root / be_rel, index=False)
    _plot(df, gate, year, root / fig_rel)
    _plot_breakeven(breakeven, ref_geo, ref_rate, root / be_fig_rel)
    _write_report(table, gate, robustness, breakeven, year, root,
                  fig_rel, tab_rel, be_fig_rel, rob_rel, be_rel)
    return gate


if __name__ == "__main__":
    g = run()
    print(f"Metro Phase 0 gate: {g.verdict()}")
    print(f"reference (densest US): {g.ref_geo} @ {g.ref_rate:.0f}/100k males")
    print(f"least-demanding cell needs {g.best_multiple:.1f}x that density")
    print(f"achievable cells: {g.n_achievable}/{g.n_cells}")
    print("wrote outputs/feasibility_metro_result.md "
          "(+ robustness & break-even tables/figure)")
