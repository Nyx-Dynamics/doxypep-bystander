"""Evidence-to-argument architecture (Figure 3) — the measurement-inheritance chain.

A conceptual schematic of the paper's construct, not a data plot. Two coupled parts:

  (top) the measurement vector M = {U, E, P, D, T, L, R} carried stage-by-stage down the
        chain — Stream A (the trial that generated the signal) inherits every dimension at
        the resolution its question needs; Stream B (guidance) and Stream C (surveillance)
        inherit the architecture but not the dimensions the downstream estimand requires.
        The two load-bearing gaps are marked: no measurement responsibility is assigned
        (Stream B, R) and no deployed system links exposure to phenotype (Stream C, L).

  (bottom) the distributive fork B != H — the benefit accrues to an observed recipient
        population, the potential externality to an unobserved third-party population;
        one side of the ledger is measurable and the other is not (distributive observability).

Cell states are documented constants tied to the Results/Methods coding, not free choices;
the single live number (systems that link exposure to phenotype, 0 of 12) is pulled from
the Stream C decomposition where available. All prose lives in the manuscript caption.

`make` target: `python -m src.analysis.architecture_figure`.
"""
from __future__ import annotations

from pathlib import Path

# palette shared with linkage_figure.py (Figure 2) for cross-figure consistency
GREEN_F, RED_F, AMBER_F = "#d7ead9", "#f6d9d9", "#f9e6c7"
EDGE, EDGE_LB = "0.6", "#c1121f"  # load-bearing gaps carry the signal-red border

# The seven measurement dimensions (Methods: the measurement-inheritance schema).
DIMS = ["U", "E", "P", "D", "T", "L", "R"]

# Per-stage inheritance of each dimension AT THE RESOLUTION THE DOWNSTREAM QUESTION NEEDS.
#   "ok"    present and adequate (green)
#   "amber" present but wrong unit/resolution — inherited from the upstream question (amber)
#   "gap"   absent (red);  "gap_lb" = the load-bearing gap for that stream
# Stream A (trial): the upstream instrument — every dimension of its own estimand is present.
# Stream B (guidance): counsels about the phenotype but assigns no one to measure it (R).
# Stream C (surveillance): exposure and phenotype exist in different systems; nothing links them (L).
STATES = {
    "Stream A · trial":        ["ok",    "ok",    "ok",  "ok",    "ok", "ok",     "ok"],
    "Stream B · guidance":     ["gap",   "amber", "gap", "gap",   "gap", "gap",   "gap_lb"],
    "Stream C · surveillance": ["amber", "amber", "gap", "amber", "ok", "gap_lb", "gap"],
}

FACE = {"ok": GREEN_F, "amber": AMBER_F, "gap": RED_F, "gap_lb": RED_F}
GLYPH = {"ok": "✓", "amber": "~", "gap": "", "gap_lb": ""}


def linked_count(root: Path):
    """Live headline for the Stream C linkage gap (n_linked of n_systems); (None, None) if
    the Stream C inputs are absent, in which case the caption's documented 0/12 stands."""
    try:
        from src.analysis.streamc_linkage import classify, load_systems
        _, dec = classify(load_systems(root))
        return dec["linked"], dec["n_systems"]
    except Exception:
        return None, None


def run(root: Path | str = None):
    root = Path(root) if root else Path(__file__).resolve().parents[2]
    n_link, n_sys = linked_count(root)
    if n_link is None:
        n_link, n_sys = 0, 12  # documented constant (Stream C decomposition)

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle, FancyArrowPatch, Patch

    fig, ax = plt.subplots(figsize=(7.6, 5.8))

    ncol = len(DIMS)
    stages = list(STATES.keys())
    row_y = {stages[0]: 4.0, stages[1]: 3.0, stages[2]: 2.0}  # A top, C bottom
    cw, ch, gap = 0.9, 0.9, 0.1

    # column headers (the dimension letters)
    for i, d in enumerate(DIMS):
        ax.text(i + cw / 2, 5.15, d, ha="center", va="center",
                fontsize=13, weight="bold", color="0.2")

    # the inheritance matrix
    for stage in stages:
        y = row_y[stage]
        ax.text(-0.18, y + ch / 2, stage, ha="right", va="center",
                fontsize=10.5, weight="bold", color="0.15")
        for i, st in enumerate(STATES[stage]):
            lb = st.endswith("_lb")
            ax.add_patch(Rectangle((i, y), cw, ch, facecolor=FACE[st],
                                   edgecolor=(EDGE_LB if lb else EDGE),
                                   lw=(2.4 if lb else 1.1), zorder=2))
            if GLYPH[st]:
                ax.text(i + cw / 2, y + ch / 2, GLYPH[st], ha="center", va="center",
                        fontsize=12, color="0.35", zorder=3)

    # downstream-flow arrow: the question moves down the chain; the architecture does not
    ax.add_patch(FancyArrowPatch((ncol + 0.35, 4.75), (ncol + 0.35, 2.05),
                                 arrowstyle="-|>", mutation_scale=16,
                                 color="0.45", lw=1.6, zorder=1))
    ax.text(ncol + 0.62, 3.4, "responsibility passes downstream;\n"
            "the inherited dimensions do not",
            rotation=90, ha="center", va="center", fontsize=8.2, color="0.4")

    # The two load-bearing gaps (Stream B · R = no measurement responsibility assigned;
    # Stream C · L = nothing links exposure to phenotype, n_link of n_sys systems) carry the
    # red border and the legend entry; the caption names them. Kept off-figure by design.

    # ---- the distributive fork: B != H ----
    fork_y, bh, bw = 0.85, 0.66, 2.7
    ax.add_patch(Rectangle((0.0, fork_y), bw, bh, facecolor=GREEN_F,
                           edgecolor=EDGE, lw=1.1, zorder=2))
    ax.text(bw / 2, fork_y + bh / 2, "benefit → recipients (B)\nobserved",
            ha="center", va="center", fontsize=8.3, weight="bold", color="0.2")
    ax.add_patch(Rectangle((ncol - bw, fork_y), bw, bh, facecolor=RED_F,
                           edgecolor=EDGE_LB, lw=1.6, zorder=2))
    ax.text(ncol - bw / 2, fork_y + bh / 2, "externality → third parties (H)\nunobserved",
            ha="center", va="center", fontsize=8.3, weight="bold", color="0.2")
    ax.text(ncol / 2, fork_y + bh / 2, "B ≠ H", ha="center", va="center",
            fontsize=13, weight="bold", color="0.15")
    ax.text(ncol / 2, fork_y - 0.16, "distributive observability", ha="center", va="top",
            fontsize=8.5, style="italic", color="0.4")

    legend = [
        Patch(facecolor=GREEN_F, edgecolor=EDGE, label="present at needed resolution"),
        Patch(facecolor=AMBER_F, edgecolor=EDGE, label="present, wrong unit/resolution"),
        Patch(facecolor=RED_F, edgecolor=EDGE, label="absent"),
        Patch(facecolor=RED_F, edgecolor=EDGE_LB, label="load-bearing gap"),
    ]
    ax.legend(handles=legend, loc="upper center", bbox_to_anchor=(0.5, 1.045),
              ncol=4, frameon=False, fontsize=8, handlelength=1.3, columnspacing=1.1)

    ax.set_xlim(-1.7, ncol + 1.5)
    ax.set_ylim(0.5, 5.75)
    ax.axis("off")
    fig.tight_layout()

    out = root / "outputs/figures/measurement_inheritance.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return out


if __name__ == "__main__":
    print(f"wrote {run()}")
