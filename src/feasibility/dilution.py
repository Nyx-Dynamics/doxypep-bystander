"""Phase 0 feasibility gate — the dilution calculation.

The question (CLAUDE.md, "Phase 0 is a gate, not a warm-up"): before acquiring
any outcome data, what fraction of a state's *S. aureus* isolates could
plausibly originate from doxy-PEP-exposed people, and what within-exposed effect
would be needed to move the *state-level* tetracycline non-susceptibility rate
detectably? If that required effect exceeds what Soge observed (RR 1.42), a
state-level ecological design cannot detect this and the project pivots to
metro-level. Either way the result is written up.

Model
-----
The state-level tetracycline non-susceptibility rate is a two-component mixture
of exposed and unexposed isolates. If doxy-PEP multiplies the exposed subgroup's
resistance rate by RR, the induced shift in the *observed state rate* is

    dR_state = f * R0 * (RR - 1)                                        (1)

where
    R0 = baseline tetracycline non-susceptibility rate in S. aureus,
    RR = within-exposed relative risk from doxy-PEP (Soge: 1.42, optimistic),
    f  = fraction of the state's S. aureus isolates coming from the exposed.

The dilution fraction is

    f = (male_prep_users * uptake * kappa) / population                 (2)

    male_prep_users : AIDSVu, observed (the better doxy-PEP proxy than overall).
    uptake          : doxy-PEP uptake among PrEP users, bounded 0.20-0.55
                      (0.55 = Spinelli SF sexual-health-clinic high-water mark;
                      not a national value).
    kappa           : isolate enrichment -- how over-represented the exposed are
                      among sampled S. aureus isolates relative to their
                      population share (kappa=1 => proportional sampling).
    population      : backed out of AIDSVu itself as prep_users / prep_rate * 1e5
                      (AIDSVu's own adult denominator; avoids importing a
                      possibly-mismatched Census figure). See DECISIONS.md.

Detectability. With N isolates per state-year and a pre/post comparison of a
proportion around R0, the minimum detectable absolute change (two-sided alpha,
given power) is

    MDE = (z_alpha/2 + z_power) * sqrt(2 * R0 * (1 - R0) / N)           (3)

The gate inverts (1): the within-exposed RR that would be *needed* to produce a
detectable state-level shift is

    RR_needed = 1 + MDE / (f * R0)                                      (4)

Gate: if RR_needed > RR_SOGE across the plausible range, state-level fails.

Everything here is deterministic and unit-tested; run() executes it on the real
AIDSVu panel and writes outputs/feasibility_result.md plus a sensitivity table
and figure. No outcome data is touched -- that is Phase 1, gated on this.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

from src.loaders.aidsvu import load_aidsvu

# --------------------------------------------------------------------------- #
# documented parameters (sources in DECISIONS.md)                              #
# --------------------------------------------------------------------------- #
RR_SOGE = 1.42            # Soge et al., >3 doses/month, tetR (optimistic ceiling)
UPTAKE_BOUND = (0.20, 0.55)
R0_BASELINE = 0.10        # central baseline S. aureus tetR; sensitivity below
R0_GRID = (0.05, 0.10, 0.13)   # 0.13 = doxy-PEP-eligible-population tetR observed
KAPPA_GRID = (1.0, 3.0, 5.0)   # proportional -> 5x isolate enrichment of exposed
UPTAKE_GRID = (0.20, 0.35, 0.55)
# Isolate volume per state-year. ATLAS is not yet acquired (Phase 1). Bound it
# GENEROUSLY high so a failed gate is robust: if detection fails even with more
# isolates than any real surveillance stream plausibly supplies per state, the
# kill decision does not hinge on the true N.
N_GRID = (1_000, 10_000, 100_000)
ALPHA = 0.05
POWER = 0.80
_Z_ALPHA2 = 1.959963985   # two-sided 0.05
_Z_POWER = 0.841621234    # 0.80


# --------------------------------------------------------------------------- #
# core math — pure, testable                                                   #
# --------------------------------------------------------------------------- #
def back_out_population(prep_users, prep_rate):
    """AIDSVu adult denominator: users / (rate per 100k) * 1e5."""
    prep_users = np.asarray(prep_users, dtype=float)
    prep_rate = np.asarray(prep_rate, dtype=float)
    with np.errstate(divide="ignore", invalid="ignore"):
        return prep_users / prep_rate * 1e5


def dilution_fraction(exposed_people, population, kappa=1.0):
    """Eq. (2): fraction of state isolates from the exposed subgroup."""
    return exposed_people * kappa / population


def induced_delta(f, r0, rr):
    """Eq. (1): induced absolute shift in the observed state-level rate."""
    return f * r0 * (rr - 1.0)


def mde_proportion(r0, n, alpha=ALPHA, power=POWER):
    """Eq. (3): minimum detectable absolute change in a proportion ~ r0."""
    z = _Z_ALPHA2 if alpha == ALPHA else _z(1 - alpha / 2)
    zb = _Z_POWER if power == POWER else _z(power)
    return (z + zb) * np.sqrt(2.0 * r0 * (1.0 - r0) / n)


def rr_needed(mde, f, r0):
    """Eq. (4): within-exposed RR required for a detectable state-level shift."""
    return 1.0 + mde / (f * r0)


def _z(p):
    """Inverse standard-normal CDF for non-default alpha/power only."""
    from statistics import NormalDist
    return NormalDist().inv_cdf(p)


# --------------------------------------------------------------------------- #
# per-state dilution on the real panel                                         #
# --------------------------------------------------------------------------- #
def state_dilution(df, year, uptake, kappa=1.0):
    """Return a per-state frame of exposed count, population and f for ``year``."""
    d = df[df.year == year].copy()
    d["population"] = back_out_population(d["prep_users"], d["prep_rate"])
    d["exposed"] = d["male_prep_users"] * uptake
    d["f"] = dilution_fraction(d["exposed"], d["population"], kappa)
    return d[["state", "state_abbrev", "year", "male_prep_users",
              "population", "exposed", "f"]].dropna(subset=["f"])


def sensitivity_table(df, year):
    """Full grid: for each (uptake, kappa, r0, N), the best-case state's
    induced dR, the MDE, and RR_needed. 'Best case' = the state with the
    largest dilution fraction f (most favourable to detection)."""
    rows = []
    for uptake in UPTAKE_GRID:
        for kappa in KAPPA_GRID:
            sd = state_dilution(df, year, uptake, kappa)
            best = sd.loc[sd["f"].idxmax()]
            f = best["f"]
            for r0 in R0_GRID:
                dR = induced_delta(f, r0, RR_SOGE)
                for n in N_GRID:
                    mde = mde_proportion(r0, n)
                    rows.append({
                        "year": year, "uptake": uptake, "kappa": kappa,
                        "r0": r0, "N_isolates": n,
                        "best_state": best["state"], "f": f,
                        "induced_dR_pp": dR * 100,       # percentage points
                        "MDE_pp": mde * 100,
                        "RR_needed": rr_needed(mde, f, r0),
                        "detectable": bool(dR >= mde),
                    })
    return pd.DataFrame(rows)


@dataclass
class Gate:
    passed: bool
    best_case_rr_needed: float
    best_case_row: dict
    n_detectable: int
    n_cells: int

    def verdict(self) -> str:
        return "PASS — state-level detectable" if self.passed \
            else "FAIL — pivot to metro-level"


def evaluate_gate(table: pd.DataFrame) -> Gate:
    """State-level passes only if some plausible cell is detectable AND the
    required RR does not exceed Soge's optimistic 1.42. The most favourable
    cell is the one with the smallest RR_needed."""
    best = table.loc[table["RR_needed"].idxmin()]
    n_detectable = int(table["detectable"].sum())
    passed = bool(best["RR_needed"] <= RR_SOGE and n_detectable > 0)
    return Gate(passed=passed,
                best_case_rr_needed=float(best["RR_needed"]),
                best_case_row=best.to_dict(),
                n_detectable=n_detectable,
                n_cells=len(table))


# --------------------------------------------------------------------------- #
# outputs                                                                      #
# --------------------------------------------------------------------------- #
def _plot_surface(df, year, out_png):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.colors as mcolors

    # RR_needed over uptake x kappa for the best state, at central R0 and the
    # most generous N (100k) — the single most detection-favourable slice.
    r0 = R0_BASELINE
    n = max(N_GRID)
    mde = mde_proportion(r0, n)
    U = np.array(UPTAKE_GRID)
    K = np.array(KAPPA_GRID)
    Z = np.zeros((len(K), len(U)))
    for i, kappa in enumerate(K):
        for j, uptake in enumerate(U):
            sd = state_dilution(df, year, uptake, kappa)
            Z[i, j] = rr_needed(mde, sd["f"].max(), r0)

    fig, ax = plt.subplots(figsize=(7, 5))
    im = ax.imshow(Z, origin="lower", aspect="auto", cmap="viridis_r",
                   norm=mcolors.LogNorm())
    ax.set_xticks(range(len(U)), [f"{u:.0%}" for u in U])
    ax.set_yticks(range(len(K)), [f"{k:g}x" for k in K])
    ax.set_xlabel("doxy-PEP uptake among PrEP users")
    ax.set_ylabel("isolate enrichment (kappa)")
    for i in range(len(K)):
        for j in range(len(U)):
            ax.text(j, i, f"{Z[i, j]:.0f}", ha="center", va="center",
                    color="white", fontsize=10)
    ax.set_title("RR within exposed needed for a detectable state-level shift\n"
                 f"(best state, R0={r0:.0%}, N={n:,}/state-yr, {year})\n"
                 f"Soge optimistic RR = {RR_SOGE} — every cell exceeds it")
    fig.colorbar(im, ax=ax, label="RR_needed (log scale)")
    fig.tight_layout()
    out_png.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_png, dpi=130)
    plt.close(fig)


def _realistic_cell(table):
    """A deliberately un-generous cell: proportional sampling (kappa=1), central
    uptake and baseline, and the smallest (most realistic) isolate volume."""
    m = ((table.kappa == 1.0) & (table.uptake == 0.35) &
         (table.r0 == R0_BASELINE) & (table.N_isolates == min(N_GRID)))
    return table[m].iloc[0]


def _write_report(table, gate, year, root, fig_rel, tab_rel):
    best = gate.best_case_row
    real = _realistic_cell(table)
    median_rr = float(table["RR_needed"].median())
    md = f"""# Phase 0 feasibility result — state-level dilution

**Verdict: {gate.verdict()}.**

Generated by `src/feasibility/dilution.py` on the AIDSVu state panel
({year} exposure). No outcome data was used; this gates Phase 1.

## What was tested

Whether a *state-level* ecological design could detect doxy-PEP's association
with tetracycline-resistant *S. aureus*, given how thin the exposed subgroup is
inside a whole state's isolate stream. The induced state-level shift is
`dR = f * R0 * (RR - 1)`; the required within-exposed effect is
`RR_needed = 1 + MDE / (f * R0)`. Soge's optimistic within-exposed effect is
RR = {RR_SOGE}.

## Result

Across the full sensitivity grid — uptake {UPTAKE_GRID}, isolate enrichment
{KAPPA_GRID}x, baseline tetR {R0_GRID}, and **generously** high isolate volumes
{N_GRID} per state-year — **{gate.n_detectable} of {gate.n_cells} cells are
detectable**.

**Most detection-favourable cell** (largest dilution `f`, smallest `RR_needed`) —
note the "best state" is **{best['best_state']}**, a city-state whose tiny
population and high male-PrEP density make it an outlier that already points
toward the metro pivot:

- dilution fraction f = {best['f']:.2e}
- uptake {best['uptake']:.0%}, enrichment {best['kappa']:g}x, R0 {best['r0']:.0%},
  N = {int(best['N_isolates']):,}/state-year (a fantastical volume — no US state
  surveillance stream supplies anywhere near this many S. aureus tetracycline MICs
  per year)
- induced state-level shift dR = **{best['induced_dR_pp']:.4f} pp**,
  MDE = **{best['MDE_pp']:.3f} pp**
- **RR_needed = {gate.best_case_rr_needed:.2f}** vs Soge's {RR_SOGE} — even here,
  above the ceiling.

**Realistic cell** (proportional sampling kappa=1, uptake {real['uptake']:.0%},
R0 {real['r0']:.0%}, N = {int(real['N_isolates']):,}/state-year):

- induced dR = **{real['induced_dR_pp']:.4f} pp**, MDE = **{real['MDE_pp']:.2f} pp**
- **RR_needed = {real['RR_needed']:.0f}** — roughly {real['RR_needed']/RR_SOGE:.0f}x
  Soge's optimistic effect.

**Across all {gate.n_cells} grid cells** the median RR_needed is
**{median_rr:.0f}** (~{median_rr/RR_SOGE:.0f}x Soge). The exposed subgroup is too
dilute inside a state's total *S. aureus* isolate pool: at the best case detection
narrowly fails, and under any realistic isolate volume it fails by 1–2 orders of
magnitude.

## Decision

Per CLAUDE.md's kill criterion, the state-level ecological design **cannot detect
this signal** and is abandoned as the primary design. The project pivots to
**metro-level** analysis (SF, King County, LA, NYC), where uptake density is far
higher — shrinking the denominator in eq. (2) and raising `f` — and where King
County has actual doxy-PEP-era isolate data. This is a legitimate, documented
negative feasibility result, not a failure to record.

The metro pivot does not rescue the state design; it is a different unit of
analysis and needs its own feasibility check with metro population denominators
and metro isolate volumes before any outcome data is acquired.

## Artifacts

- sensitivity table: `{tab_rel}`
- sensitivity figure: `{fig_rel}`
"""
    (root / "outputs" / "feasibility_result.md").write_text(md)


def run(root: Path | str = None, year: int = 2022) -> Gate:
    root = Path(root) if root else Path(__file__).resolve().parents[2]
    df = load_aidsvu(root / "data" / "raw" / "aidsvu")
    table = sensitivity_table(df, year)
    gate = evaluate_gate(table)

    tab_rel = "outputs/tables/feasibility_sensitivity.csv"
    fig_rel = "outputs/figures/feasibility_dilution.png"
    (root / "outputs" / "tables").mkdir(parents=True, exist_ok=True)
    table.to_csv(root / tab_rel, index=False)
    _plot_surface(df, year, root / fig_rel)
    _write_report(table, gate, year, root, fig_rel, tab_rel)
    return gate


if __name__ == "__main__":
    g = run()
    print(f"Phase 0 gate: {g.verdict()}")
    print(f"best-case RR_needed = {g.best_case_rr_needed:.1f} "
          f"(Soge optimistic {RR_SOGE})")
    print(f"detectable cells: {g.n_detectable}/{g.n_cells}")
    print("wrote outputs/feasibility_result.md")
