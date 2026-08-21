"""The unifying figure — the trial cleared the line; the downstream systems cannot follow.

The pivot (Luetkemeyer 2025 Lancet ID final analysis): the trial DID detect the bystander
signal — incident doxycycline-resistant S. aureus, HR 3.89 (95% CI 1.42-10.68). So Stream A
no longer shows a detection *threshold* nothing clears; it shows the *observed* effect, which
clears the Soge reference band. Streams B and C then show the inheritance failure: guidelines
measure nothing (no threshold exists), and surveillance would need an implausible within-
exposed RR (~14-64) to move a population rate. One reference line: the signal is above it,
and the systems built to follow it are not. Numbers pulled live where computed; the final-
trial HR is a published scalar (Fig 4B), carried as a documented constant.
"""
from __future__ import annotations

from pathlib import Path

# Luetkemeyer AF, et al. Lancet Infect Dis 2025;25:873-83, Figure 4B — randomised, Cox PH,
# incident doxy-R S. aureus among those free of it at baseline (SC censored at crossover).
HR_SAUREUS_FINAL = 3.89
HR_SAUREUS_CI = (1.42, 10.68)


def _numbers(root: Path):
    from src.analysis import detectability as D
    from src.feasibility import dilution as DIL
    from src.loaders.aidsvu import load_aidsvu

    recs = [D.load_trial(p) for p in sorted((root / "data/raw/coding").glob("trial_*.yaml"))]
    tab = D.detectability_table(recs)
    mdr = tab[tab["min_detectable_RR"] != float("inf")]["min_detectable_RR"]

    df = load_aidsvu(root / "data/raw/aidsvu")
    # Stream C is anchored on the realistic cell under the controlled panel (not the
    # retired single-comparison grid): RR_needed runs from the optimistic design effect
    # up to the autocorrelation-adjusted one. Both lie well beyond the Soge band.
    panel = DIL.panel_summary(df, 2022)
    c_realistic = panel["realistic_RR_needed"]
    return {
        "RR_saureus": D.RR_SAUREUS, "RR_gc": D.RR_GC,
        "A_hr": HR_SAUREUS_FINAL, "A_ci_lo": HR_SAUREUS_CI[0], "A_ci_hi": HR_SAUREUS_CI[1],
        "A_interim_lo": float(mdr.min()), "A_interim_hi": float(mdr.max()),
        "C_lo": float(c_realistic.min()), "C_hi": float(c_realistic.max()),
        "C_n_detect": int(panel.loc[panel.deff == 1.0, "n_detectable"].iloc[0]),
        "C_n": int(panel.loc[panel.deff == 1.0, "n_cells"].iloc[0]),
    }


def run(root: Path | str = None):
    root = Path(root) if root else Path(__file__).resolve().parents[2]
    n = _numbers(root)

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    # Clean panel: only structural elements. All explanatory text lives in the caption.
    fig, ax = plt.subplots(figsize=(7.2, 3.4))
    XMAX = 120

    # the Soge reference: plausible within-exposed effect band 1.42-2.25
    ax.axvspan(n["RR_gc"], n["RR_saureus"], color="0.85", zorder=0)
    ax.axvline(n["RR_saureus"], color="0.35", ls="--", lw=1.2, zorder=1)
    ax.axvline(n["RR_gc"], color="0.55", ls=":", lw=1.0, zorder=1)

    SIGNAL = "#c1121f"   # the detected effect
    THRESH = "#1f4e79"   # detection thresholds / ranges

    # Stream A — trials: the FINAL analysis DETECTED the signal. Observed hazard ratio with
    # its 95% CI whisker (filled marker = an observed effect, not a threshold); it clears the
    # band. Faint tick marks the interim's minimum-detectable RR — the threshold that kept the
    # cross-sectional interim blind to the effect the incidence estimand later resolved.
    ax.plot([n["A_interim_lo"], n["A_interim_hi"]], [2.26, 2.26], lw=3,
            color="0.72", solid_capstyle="round", zorder=1)
    ax.plot([n["A_ci_lo"], n["A_ci_hi"]], [2, 2], lw=2.4, color=SIGNAL,
            solid_capstyle="round", zorder=3)
    ax.plot([n["A_hr"]], [2], marker="o", ms=11, color=SIGNAL,
            markeredgecolor="white", markeredgewidth=1.2, zorder=5)

    # Stream B — guidelines: no measurement, so no threshold exists (off-scale arrow)
    ax.annotate("", xy=(XMAX, 1), xytext=(n["RR_saureus"] * 1.1, 1),
                arrowprops=dict(arrowstyle="-|>", color="#7a7a7a", lw=1.8))

    # Stream C — surveillance: RR needed to move a population rate, realistic cell under the
    # controlled panel across the design-effect range (dilution leg) — a threshold, unreached.
    ax.plot([n["C_lo"], n["C_hi"]], [0, 0], lw=7, color=THRESH,
            solid_capstyle="round", zorder=3)
    ax.plot([n["C_hi"]], [0], marker="D", ms=7, color=THRESH, zorder=4)

    ax.set_xscale("log")
    ax.set_xlim(1, XMAX)
    ax.set_ylim(-0.6, 2.7)
    ax.set_yticks([2, 1, 0])
    ax.set_yticklabels(["Stream A\n(trials)", "Stream B\n(guidelines)",
                        "Stream C\n(surveillance)"], fontsize=10)
    ax.set_xlabel("within-exposed relative risk / hazard ratio  (log scale)", fontsize=10)
    ax.set_xticks([1, 2, 5, 10, 20, 50, 100])
    ax.set_xticklabels(["1", "2", "5", "10", "20", "50", "100"])
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig.tight_layout()

    out = root / "outputs/figures/three_streams.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=150)
    plt.close(fig)
    return n, out


if __name__ == "__main__":
    n, out = run()
    print(f"Stream A DETECTED HR {n['A_hr']} (CI {n['A_ci_lo']}-{n['A_ci_hi']}); "
          f"interim min-detectable RR {n['A_interim_lo']:.1f}-{n['A_interim_hi']:.1f}")
    print(f"Stream C realistic-cell RR_needed {n['C_lo']:.0f}-{n['C_hi']:.0f} "
          f"(panel, {n['C_n_detect']}/{n['C_n']} detectable at DEFF=1)")
    print(f"Soge reference band: {n['RR_gc']} (GC) - {n['RR_saureus']} (S. aureus)")
    print(f"wrote {out}")
