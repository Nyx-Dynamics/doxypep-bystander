"""Combined-denominator sensitivity: PrEP + PLWH exposed population.

The published dilution gate (dilution.py) indexed the exposed doxy-PEP population
on AIDSVu *male PrEP users* alone. But the DoxyPEP trial enrolled two populations
-- HIV-negative people on PrEP AND people living with HIV (PLWH) -- both offered
doxy-PEP. Indexing f on PrEP users alone therefore UNDERCOUNTS the exposed and
biases RR_needed UPWARD (toward "undetectable"), i.e. in favour of the paper's own
conclusion. This module corrects that, honestly, and reports the shift.

    exposed = ( male_prep_users + msm_frac * male_plwh_cases ) * uptake * dose
    f       = exposed * kappa / population

Data: AIDSVu state PrEP and Prevalence, year 2024 (the only year both series
coexist on AIDSVu; also nearer doxy-PEP scale-up). male_plwh_cases is a PREVALENCE
STOCK (correct), not new-diagnosis flow. State prevalence carries no transmission
split, so msm_frac (fraction of male PLWH attributable to MSM) is an EXTERNAL
parameter, gridded {0.50, 0.66, 0.80} with 1.00 as an explicit upper bound.

All core math is imported from dilution.py unchanged; this file only rebuilds the
exposed numerator and re-runs the same grid, so the published PrEP-only result is
preserved and this is an additive sensitivity.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from src.feasibility import dilution as D
from src.loaders.aidsvu import load_aidsvu, load_prevalence

MSM_FRAC_GRID = (0.50, 0.66, 0.80, 1.00)
MSM_FRAC_CENTRAL = 0.66
DEFF_OPTIMISTIC = 1.0   # panel best case, matches the manuscript's optimistic bound


# --------------------------------------------------------------------------- #
# per-state dilution fraction under a chosen exposed construction              #
# --------------------------------------------------------------------------- #
def _f_by_state(prep_df, prev_df, year, uptake, kappa, msm_frac):
    """Return per-state f for exposed = (male PrEP + msm_frac*male PLWH)*uptake*dose.
    msm_frac=0 reproduces the PrEP-only construction exactly."""
    p = prep_df[prep_df.year == year].copy()
    pop = D.back_out_population(p["prep_users"], p["prep_rate"])
    plwh = np.zeros(len(p))
    if msm_frac > 0 and prev_df is not None:
        v = (prev_df[prev_df.year == year][["state_abbrev", "male_plwh_cases"]]
             .set_index("state_abbrev")["male_plwh_cases"])
        plwh = p["state_abbrev"].map(v).to_numpy(dtype=float)
        plwh = np.nan_to_num(plwh, nan=0.0)
    exposed = (p["male_prep_users"].to_numpy(dtype=float)
               + msm_frac * plwh) * uptake * D.DOSE_ABOVE_THRESHOLD
    f = exposed * kappa / pop
    p = p.assign(f=f)
    return p.dropna(subset=["f"])


def _best_f(prep_df, prev_df, year, uptake, kappa, msm_frac):
    sd = _f_by_state(prep_df, prev_df, year, uptake, kappa, msm_frac)
    row = sd.loc[sd["f"].idxmax()]
    return float(row["f"]), row["state"]


def realistic_rr(prep_df, prev_df, year, msm_frac,
                 uptake=0.35, kappa=D.REALISTIC_KAPPA, r0=D.R0_BASELINE, n=min(D.N_GRID)):
    """RR_needed for the realistic cell, single-comparison and optimistic-panel."""
    f, best_state = _best_f(prep_df, prev_df, year, uptake, kappa, msm_frac)
    rr_single = D.rr_needed(D.mde_proportion(r0, n), f, r0)
    rr_panel = D.rr_needed(D.panel_mde(r0, n, deff=DEFF_OPTIMISTIC), f, r0)
    return {"f": f, "best_state": best_state,
            "rr_single": rr_single, "rr_panel_deff1": rr_panel}


def best_cell_rr(prep_df, prev_df, year, msm_frac):
    """Minimum single-comparison RR_needed over the full grid (the disowned best)."""
    best = np.inf
    for uptake in D.UPTAKE_GRID:
        for kappa in D.KAPPA_GRID:
            f, _ = _best_f(prep_df, prev_df, year, uptake, kappa, msm_frac)
            for r0 in D.R0_GRID:
                for n in D.N_GRID:
                    best = min(best, D.rr_needed(D.mde_proportion(r0, n), f, r0))
    return float(best)


def dose_sensitivity(prep_df, prev_df, year=2024, msm_frac=1.00,
                     dose_grid=(0.50, 0.75, 1.00)):
    """RR_needed for the realistic cell (panel DEFF 1 and 25) and the disowned best
    cell (single-comparison and panel DEFF 1) across the dose-above-threshold share
    d. f is linear in d, so RR_needed-1 scales as 1/d; d=1.0 is the limiting case in
    which every user exceeds three doses/month. Reproduces the supplement d-table."""
    # f at the module-default dose (D.DOSE_ABOVE_THRESHOLD); scale by d/default.
    f_real = _best_f(prep_df, prev_df, year, 0.35, D.REALISTIC_KAPPA, msm_frac)[0]
    # best cell over the grid maxes uptake/kappa/R0/N; recover its f and R0
    best_f = 0.0
    for uptake in D.UPTAKE_GRID:
        for kappa in D.KAPPA_GRID:
            best_f = max(best_f, _best_f(prep_df, prev_df, year, uptake, kappa, msm_frac)[0])
    rows = []
    for d in dose_grid:
        s = d / D.DOSE_ABOVE_THRESHOLD
        fr, fb = f_real * s, best_f * s
        rows.append({
            "d": d,
            "realistic_panel_deff1": D.rr_needed(D.panel_mde(D.R0_BASELINE, min(D.N_GRID), deff=1.0), fr, D.R0_BASELINE),
            "realistic_panel_deff25": D.rr_needed(D.panel_mde(D.R0_BASELINE, min(D.N_GRID), deff=25.0), fr, D.R0_BASELINE),
            "best_single_comp": D.rr_needed(D.mde_proportion(max(D.R0_GRID), max(D.N_GRID)), fb, max(D.R0_GRID)),
            "best_panel_deff1": D.rr_needed(D.panel_mde(max(D.R0_GRID), max(D.N_GRID), deff=1.0), fb, max(D.R0_GRID)),
        })
    return pd.DataFrame(rows)


def run(root: Path | str = None):
    root = Path(root) if root else Path(__file__).resolve().parents[2]
    prep = load_aidsvu(root / "data" / "raw" / "aidsvu")
    prev = load_prevalence(root / "data" / "raw" / "aidsvu")
    assert prev is not None, "no AIDSVu_State_Prev_*.xlsx found"

    scenarios = [
        ("PrEP-only 2022 (published)", 2022, 0.0),
        ("PrEP-only 2024 (year effect)", 2024, 0.0),
        (f"PrEP+PLWH 2024 (msm_frac={MSM_FRAC_CENTRAL})", 2024, MSM_FRAC_CENTRAL),
    ]
    print(f"{'scenario':<42} {'best f':>10} {'RR_single':>10} {'RR_panelD1':>11} {'RR_bestcell':>12}  best_state")
    for label, yr, mf in scenarios:
        r = realistic_rr(prep, prev, yr, mf)
        bc = best_cell_rr(prep, prev, yr, mf)
        print(f"{label:<42} {r['f']:>10.2e} {r['rr_single']:>10.1f} "
              f"{r['rr_panel_deff1']:>11.2f} {bc:>12.2f}  {r['best_state']}")

    print(f"\nmsm_frac sensitivity (PrEP+PLWH 2024, realistic cell):")
    print(f"{'msm_frac':>9} {'best f':>10} {'RR_single':>10} {'RR_panelD1':>11} {'RR_bestcell':>12}")
    for mf in MSM_FRAC_GRID:
        r = realistic_rr(prep, prev, 2024, mf)
        bc = best_cell_rr(prep, prev, 2024, mf)
        print(f"{mf:>9.2f} {r['f']:>10.2e} {r['rr_single']:>10.1f} "
              f"{r['rr_panel_deff1']:>11.2f} {bc:>12.2f}")
    print(f"\nCross-organism benchmark RR = {D.RR_SOGE}; realistic-cell verdict clears it iff RR > {D.RR_SOGE}.")


if __name__ == "__main__":
    run()
