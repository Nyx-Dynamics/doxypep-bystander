"""Regenerate the four Stream C figures under the combined PrEP+PLWH denominator.

Primary specification: msm_frac = 1.00, AIDSVu 2024 state PrEP + prevalence
(see dilution_plwh.py / outputs/feasibility_plwh_result.md). Reuses the exact
plot styling of summary_figure.py, dilution.py and dilution_metro.py but feeds the
combined exposed density. Writes PNGs to outputs/figures/ and paper/jac/figures/.

    python3 -m src.feasibility.plots_plwh
"""
from __future__ import annotations

from pathlib import Path

import numpy as np

from src.loaders.aidsvu import load_aidsvu, load_prevalence
from src.feasibility import dilution as D
from src.feasibility import dilution_metro as M
from src.feasibility.dilution_plwh import _f_by_state
from src.analysis.summary_figure import HR_SAUREUS_FINAL, HR_SAUREUS_CI

YEAR = 2024
MSM = 1.00                      # primary
DEST = ("outputs/figures", "paper/jac/figures")


def _save(fig, name, root):
    for d in DEST:
        p = root / d / name
        p.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(p, dpi=300)


def _combined_density_dc(prep, prev):
    p = prep[prep.year == YEAR]
    dc = p.loc[p["male_prep_rate"].idxmax()]
    plwh_rate = float(prev[prev.year == YEAR].set_index("state_abbrev")
                      ["male_plwh_rate"].get(dc["state_abbrev"]))
    return dc["state"], float(dc["male_prep_rate"]) + MSM * plwh_rate


def _panel_realistic_range(prep, prev):
    """Combined realistic-cell RR_needed across DEFF 1..25 (three_streams C bar)."""
    f = _f_by_state(prep, prev, YEAR, 0.35, D.REALISTIC_KAPPA, MSM)
    fmax = f["f"].max()
    lo = D.rr_needed(D.panel_mde(D.R0_BASELINE, min(D.N_GRID), deff=1.0), fmax, D.R0_BASELINE)
    hi = D.rr_needed(D.panel_mde(D.R0_BASELINE, min(D.N_GRID), deff=25.0), fmax, D.R0_BASELINE)
    return lo, hi


def run(root: Path | str = None):
    root = Path(root) if root else Path(__file__).resolve().parents[2]
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.colors as mcolors

    prep = load_aidsvu(root / "data/raw/aidsvu")
    prev = load_prevalence(root / "data/raw/aidsvu")
    ref_geo, ref_rate = _combined_density_dc(prep, prev)   # DC combined density
    U, K = np.array(D.UPTAKE_GRID), np.array(D.KAPPA_GRID)
    info = {"ref_geo": ref_geo, "ref_rate": ref_rate}

    # ---- three_streams.png : Stream C bar = combined realistic panel range ----
    from src.analysis import detectability as DET
    recs = [DET.load_trial(p) for p in sorted((root / "data/raw/coding").glob("trial_*.yaml"))]
    mdr = DET.detectability_table(recs)
    mdr = mdr[mdr["min_detectable_RR"] != float("inf")]["min_detectable_RR"]
    c_lo, c_hi = _panel_realistic_range(prep, prev)
    info["C_lo"], info["C_hi"] = c_lo, c_hi

    fig, ax = plt.subplots(figsize=(7.2, 3.4))
    XMAX = 120
    ax.axvspan(DET.RR_GC, DET.RR_SAUREUS, color="0.85", zorder=0)
    ax.axvline(DET.RR_SAUREUS, color="0.35", ls="--", lw=1.2, zorder=1)
    ax.axvline(DET.RR_GC, color="0.55", ls=":", lw=1.0, zorder=1)
    SIGNAL, THRESH = "#c1121f", "#1f4e79"
    ax.plot([mdr.min(), mdr.max()], [2.26, 2.26], lw=3, color="0.72",
            solid_capstyle="round", zorder=1)
    ax.plot([HR_SAUREUS_CI[0], HR_SAUREUS_CI[1]], [2, 2], lw=2.4, color=SIGNAL,
            solid_capstyle="round", zorder=3)
    ax.plot([HR_SAUREUS_FINAL], [2], marker="o", ms=11, color=SIGNAL,
            markeredgecolor="white", markeredgewidth=1.2, zorder=5)
    ax.annotate("observed trial HR", xy=(HR_SAUREUS_FINAL, 2),
                xytext=(HR_SAUREUS_FINAL * 1.25, 2.28), fontsize=8, color=SIGNAL)
    ax.annotate("", xy=(XMAX, 1), xytext=(DET.RR_SAUREUS * 1.1, 1),
                arrowprops=dict(arrowstyle="-|>", color="#7a7a7a", lw=1.8))
    ax.plot([c_lo, c_hi], [0, 0], lw=7, color=THRESH, solid_capstyle="round", zorder=3)
    ax.plot([c_hi], [0], marker="D", ms=7, color=THRESH, zorder=4)
    ax.annotate("modelled RR detectability threshold", xy=(c_lo, 0),
                xytext=(c_lo * 0.98, 0.42), fontsize=8, color=THRESH)
    ax.set_xscale("log"); ax.set_xlim(1, XMAX); ax.set_ylim(-0.6, 2.7)
    ax.set_yticks([2, 1, 0])
    ax.set_yticklabels(["Stream A\n(trials)", "Stream B\n(guidelines)",
                        "Stream C\n(surveillance)"], fontsize=10)
    ax.set_xlabel("within-exposed relative risk / hazard ratio  (log scale)", fontsize=10)
    ax.set_xticks([1, 2, 5, 10, 20, 50, 100])
    ax.set_xticklabels(["1", "2", "5", "10", "20", "50", "100"])
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig.tight_layout(); _save(fig, "three_streams.png", root); plt.close(fig)

    # ---- feasibility_dilution.png (Fig A): RR_needed over uptake x kappa ----
    r0, n = D.R0_BASELINE, max(D.N_GRID)
    mde = D.mde_proportion(r0, n)
    Z = np.zeros((len(K), len(U)))
    for i, k in enumerate(K):
        for j, u in enumerate(U):
            f = _f_by_state(prep, prev, YEAR, u, k, MSM)
            Z[i, j] = D.rr_needed(mde, f["f"].max(), r0)
    info["figA_min"], info["figA_max"] = float(Z.min()), float(Z.max())
    fig, ax = plt.subplots(figsize=(7, 5))
    im = ax.imshow(Z, origin="lower", aspect="auto", cmap="viridis_r", norm=mcolors.LogNorm())
    ax.set_xticks(range(len(U)), [f"{u:.0%}" for u in U])
    ax.set_yticks(range(len(K)), [f"{k:g}x" for k in K])
    ax.set_xlabel("doxy-PEP uptake"); ax.set_ylabel("isolate enrichment (kappa)")
    for i in range(len(K)):
        for j in range(len(U)):
            ax.text(j, i, f"{Z[i, j]:.1f}", ha="center", va="center", color="white", fontsize=10)
    ax.set_title("RR within exposed needed for a detectable state-level shift\n"
                 f"combined PrEP+PLWH exposed, best state, R0={r0:.0%}, N={n:,} ({YEAR})\n"
                 f"cross-organism benchmark RR = {DET.RR_GC}; "
                 f"S. aureus-matched RR = {DET.RR_SAUREUS}")
    fig.colorbar(im, ax=ax, label="RR_needed (log)")
    fig.tight_layout(); _save(fig, "feasibility_dilution.png", root); plt.close(fig)

    # ---- feasibility_metro.png (Fig B): required density / combined densest ----
    Zb = np.array([[M.required_male_prep_rate(r0, n, u, k) / ref_rate for u in U] for k in K])
    info["figB_min"] = float(Zb.min())
    fig, ax = plt.subplots(figsize=(7, 5))
    im = ax.imshow(Zb, origin="lower", aspect="auto", cmap="magma_r", norm=mcolors.LogNorm())
    ax.set_xticks(range(len(U)), [f"{u:.0%}" for u in U])
    ax.set_yticks(range(len(K)), [f"{k:g}x" for k in K])
    ax.set_xlabel("doxy-PEP uptake"); ax.set_ylabel("isolate enrichment (kappa)")
    for i in range(len(K)):
        for j in range(len(U)):
            ax.text(j, i, f"{Zb[i, j]:.0f}x", ha="center", va="center", color="white", fontsize=10)
    ax.set_title("Exposure density required for a detectable metro shift,\n"
                 f"x the densest US geography's combined PrEP+PLWH density\n"
                 f"({ref_geo}, {ref_rate:.0f}/100k, {YEAR}) - 1x = already the US max")
    fig.colorbar(im, ax=ax, label="x densest US geography (log)")
    fig.tight_layout(); _save(fig, "feasibility_metro.png", root); plt.close(fig)

    # ---- feasibility_metro_breakeven.png (Fig C) ----
    fig, ax = plt.subplots(figsize=(7.5, 5))
    for k in K:
        ys = [M.required_male_prep_rate(D.R0_BASELINE, nn, max(D.UPTAKE_GRID), k) / 1e3
              for nn in D.N_GRID]
        ax.plot(D.N_GRID, ys, marker="o", label=f"kappa {k:g}x")
    ax.axhline(100, color="crimson", ls="--", lw=1.5, label="physical ceiling (100% of males)")
    ax.axhline(ref_rate / 1e3, color="grey", ls=":", lw=1.5,
               label=f"densest US combined density ({ref_geo}, {ref_rate/1e3:.1f}%)")
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlabel("isolates per geography-year (N)")
    ax.set_ylabel("% of adult males (combined exposure) required")
    ax.set_title("Break-even: combined PrEP+PLWH exposure required to make the\n"
                 "doxy-PEP signal detectable (uptake 55%, R0 10%)")
    ax.legend(fontsize=8, loc="best")
    fig.tight_layout(); _save(fig, "feasibility_metro_breakeven.png", root); plt.close(fig)
    return info


if __name__ == "__main__":
    info = run()
    print(f"three_streams Stream C bar: RR {info['C_lo']:.1f}-{info['C_hi']:.1f}")
    print(f"Fig A dilution heatmap: RR_needed {info['figA_min']:.2f}-{info['figA_max']:.1f}")
    print(f"Fig B metro min multiple: {info['figB_min']:.2f}x the densest combined density")
    print(f"ref geography: {info['ref_geo']} @ {info['ref_rate']:.0f}/100k (combined)")
