"""Stream C linkage/resolution schematic (Figure 2, §3.3) — shaded 2x2.

To link doxy-PEP exposure to S. aureus tetracycline resistance a single system must carry
both at a common population denominator. The 2x2 crosses what is captured (exposure vs the
tetracycline phenotype) with the resolution it is captured at (population denominator vs
facility only). No column is usable in both rows, so nothing links — and where S. aureus
IS surveilled at a population denominator the axis is methicillin, not tetracycline.

Clean panel: boxes are labelled a-d and shaded by status (see the colour legend); every
description lives in the manuscript caption. Regenerable; headline count pulled live.
"""
from __future__ import annotations

from pathlib import Path

GREEN_F, RED_F, AMBER_F, GREY_F = "#d7ead9", "#f6d9d9", "#f9e6c7", "#ededed"


def counts(root: Path):
    try:
        from src.analysis.streamc_linkage import classify, load_systems
        _, dec = classify(load_systems(root))
        return dec["n_systems"], dec["linked"]
    except Exception:
        return None, None


def run(root: Path | str = None):
    root = Path(root) if root else Path(__file__).resolve().parents[2]

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle, Patch

    fig, ax = plt.subplots(figsize=(7.2, 4.8))

    def quad(x, y, fc, hatch, letter):
        ax.add_patch(Rectangle((x, y), 0.5, 0.5, facecolor=fc, edgecolor="0.6",
                               lw=1.1, hatch=hatch, zorder=0))
        ax.text(x + 0.25, y + 0.25, letter, ha="center", va="center",
                fontsize=27, weight="bold", color="0.2")

    quad(0.0, 0.5, GREEN_F, None, "a")     # exposure x population denominator
    quad(0.5, 0.5, GREY_F, None, "b")      # exposure x facility
    quad(0.0, 0.0, RED_F, "////", "c")     # phenotype x population denominator (the gap)
    quad(0.5, 0.0, AMBER_F, "\\\\\\\\", "d")  # phenotype x facility

    # structural labels only
    ax.text(0.25, 1.05, "population denominator", ha="center", fontsize=10.5, weight="bold")
    ax.text(0.75, 1.05, "facility — no denominator", ha="center", fontsize=10.5, weight="bold")
    ax.text(-0.03, 0.75, "doxy-PEP\nexposure", ha="right", va="center",
            fontsize=10.5, weight="bold")
    ax.text(-0.03, 0.25, "S. aureus\ntet-R phenotype", ha="right", va="center",
            fontsize=10.5, weight="bold")

    legend = [
        Patch(facecolor=GREEN_F, edgecolor="0.6", label="captured, usable"),
        Patch(facecolor=RED_F, edgecolor="0.6", hatch="////", label="absent — the gap"),
        Patch(facecolor=AMBER_F, edgecolor="0.6", hatch="\\\\", label="present, unusable"),
        Patch(facecolor=GREY_F, edgecolor="0.6", label="not applicable"),
    ]
    ax.legend(handles=legend, loc="upper center", bbox_to_anchor=(0.36, -0.02),
              ncol=4, frameon=False, fontsize=8.6, handlelength=1.4, columnspacing=1.3)

    ax.set_xlim(-0.34, 1.02)
    ax.set_ylim(-0.16, 1.13)
    ax.axis("off")
    fig.tight_layout()
    # Fig 1 is shipped from paper/jac/figures/; write both so `make all` keeps the
    # shipped copy in sync with the analysis (mirrors plots_plwh's dual destination).
    for d in ("outputs/figures", "paper/jac/figures"):
        out = root / d / "streamc_linkage.png"
        out.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(out, dpi=300, bbox_inches="tight")
    plt.close(fig)
    return out


if __name__ == "__main__":
    n_sys, n_link = counts(Path(__file__).resolve().parents[2])
    print(f"{n_link} of {n_sys} deployed systems link exposure to phenotype")
    print(f"wrote {run()}")
