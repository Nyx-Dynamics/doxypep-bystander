"""The unifying figure — three streams, one reference line, nothing clears it.

For each stream we place the within-exposed relative risk it would NEED to detect the
bystander signal against the largest effect anyone has actually observed (Soge: RR 2.25
for tetracycline-resistant S. aureus colonisation, 1.42 for the cross-organism gonococcal
figure). Where a threshold is computable it lies beyond that plausible effect; where it is
not (guidelines), no threshold exists at all — which is the stronger version of the same
finding. Regenerable: numbers are pulled live from the analysis modules.
"""
from __future__ import annotations

from pathlib import Path


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
        "A_lo": float(mdr.min()), "A_hi": float(mdr.max()),
        "A_n_detect": int(tab["detect_matched_2.25"].sum()), "A_n": len(tab),
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

    # Clean panel: only structural elements (bars, band, arrow, axes). All explanatory
    # text lives in the manuscript figure caption, not on the figure.
    fig, ax = plt.subplots(figsize=(7.2, 3.4))
    XMAX = 120

    # the Soge reference: plausible within-exposed effect band 1.42-2.25
    ax.axvspan(n["RR_gc"], n["RR_saureus"], color="0.85", zorder=0)
    ax.axvline(n["RR_saureus"], color="0.35", ls="--", lw=1.2, zorder=1)
    ax.axvline(n["RR_gc"], color="0.55", ls=":", lw=1.0, zorder=1)

    bar = dict(lw=7, solid_capstyle="round", color="#1f4e79", zorder=3)
    mk = dict(marker="D", ms=7, color="#1f4e79", zorder=4)

    # Stream A — trials: minimum detectable RR (a computable threshold, beyond the band)
    ax.plot([n["A_lo"], n["A_hi"]], [2, 2], **bar)
    ax.plot([n["A_hi"]], [2], **mk)

    # Stream B — guidelines: no measurement, so no threshold exists (off-scale arrow)
    ax.annotate("", xy=(XMAX, 1), xytext=(n["RR_saureus"] * 1.1, 1),
                arrowprops=dict(arrowstyle="-|>", color="#7a7a7a", lw=1.8))

    # Stream C — surveillance: RR needed to move a population rate, realistic cell
    # under the controlled panel across the design-effect range (dilution leg)
    ax.plot([n["C_lo"], n["C_hi"]], [0, 0], **bar)
    ax.plot([n["C_hi"]], [0], **mk)

    ax.set_xscale("log")
    ax.set_xlim(1, XMAX)
    ax.set_ylim(-0.6, 2.6)
    ax.set_yticks([2, 1, 0])
    ax.set_yticklabels(["Stream A\n(trials)", "Stream B\n(guidelines)",
                        "Stream C\n(surveillance)"], fontsize=10)
    ax.set_xlabel("within-exposed relative risk  (log scale)", fontsize=10)
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
    print(f"Stream A min-det RR {n['A_lo']:.1f}-{n['A_hi']:.1f} ({n['A_n_detect']}/{n['A_n']})")
    print(f"Stream C realistic-cell RR_needed {n['C_lo']:.0f}-{n['C_hi']:.0f} "
          f"(panel, {n['C_n_detect']}/{n['C_n']} detectable at DEFF=1)")
    print(f"Soge reference: {n['RR_gc']} (GC) - {n['RR_saureus']} (S. aureus)")
    print(f"wrote {out}")
