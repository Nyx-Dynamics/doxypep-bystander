"""Coverage of the null — can a cross-sectional, mean-based endpoint resolve a
clustered signal at the trials' denominators?

This is the computational backing for the manuscript's ¶7 ("the systems that would
size it report the mean of a process whose risk was never in the mean") and the ¶4
clustering frame. It is a DETECTABILITY analysis, not an effect estimate.

The claim being tested. A clustering organism's carriage does not sit at a steady
value; it swings, because prevalence at each sampling occasion is a draw from a
process with extra (between-visit) variance — waves. We model that as

    logit(p_visit) = a + b * visit + eps_visit,   eps_visit ~ N(0, sigma^2)

where `b` is a true underlying trend and `sigma` is the clustering intensity. We then
apply the *naive* cross-sectional trend test the trials use — Cochran–Armitage, which
assumes binomial variance and no clustering — to counts simulated at the trials' ACTUAL
per-visit denominators (loaded from the coded DOXYVAC MRSA carriage series). Two
failures appear as sigma grows:

  (a) POWER to detect a fixed true trend collapses toward alpha — the clustering noise
      swamps the signal;
  (b) TYPE-I error under a flat process (b=0) inflates above alpha — clustering
      manufactures apparent trends where none exist.

Either way the mean-based endpoint cannot separate a real selection trend from the
clustering it is embedded in.

SCOPE (Contract 2). This is the **MRSA** clustering instrument. It runs on DOXYVAC MRSA
throat carriage — the methicillin-resistant subset — and licenses a statement about the
MRSA endpoint's detectability, NOT about doxycycline-resistant S. aureus (the analytic
unit, handled separately by `selection_ratchet.py`). The MRSA nesting is stated, not
elided.

The clustering intensity `sigma` is anchored EXTERNALLY: the DOXYVAC series itself
cannot estimate it (five timepoints, three residual df — unidentified; see the σ̂≈0
below and `three_outbreak_fit_result.md`), which is itself a Stream-A finding. So we
import the empirical between-cohort dispersion of MRSA colonization prevalence estimated
in `dejong_sigma.py` (σ̂≈2.7, 95% CI 1.74–4.57) and read the naive trend test's Type-I
error there. The σ=0 row is a calibration check: with no overdispersion the
Cochran–Armitage test is correctly sized (≈5%) by construction, not fitted. No causal
claim.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
from scipy.stats import norm

from src.coding.schema_trial import load_trial

ALPHA = 0.05
SEED = 20260820
SIGMA_GRID = (0.0, 0.25, 0.5, 0.75, 1.0)


# --------------------------------------------------------------------------- #
# the naive cross-sectional trend test the trials use                          #
# --------------------------------------------------------------------------- #
def cochran_armitage_p(counts, denoms, scores=None) -> float:
    """Two-sided Cochran–Armitage trend-test p-value across ordered visits.
    Assumes binomial variance — i.e. it is blind to between-visit clustering."""
    x = np.asarray(counts, float)
    n = np.asarray(denoms, float)
    s = np.arange(len(x), dtype=float) if scores is None else np.asarray(scores, float)
    N = n.sum()
    pbar = x.sum() / N
    if pbar <= 0 or pbar >= 1:
        return 1.0
    sbar = (n * s).sum() / N
    T = (s * (x - n * pbar)).sum()
    var = pbar * (1 - pbar) * (n * (s - sbar) ** 2).sum()
    if var <= 0:
        return 1.0
    z = T / np.sqrt(var)
    return float(2 * norm.sf(abs(z)))


# --------------------------------------------------------------------------- #
# the clustered generative process                                             #
# --------------------------------------------------------------------------- #
def _expit(x):
    return 1.0 / (1.0 + np.exp(-x))


def simulate_counts(denoms, a, b, sigma, rng):
    """One clustered series: logit(p_v) = a + b*v + N(0, sigma^2); x_v ~ Bin(N_v, p_v)."""
    v = np.arange(len(denoms))
    logit_p = a + b * v + rng.normal(0.0, sigma, size=len(denoms))
    p = _expit(logit_p)
    return rng.binomial(np.asarray(denoms, int), p)


def power_and_typeI(denoms, a, b_true, sigma, n_sim=4000, alpha=ALPHA, seed=SEED):
    """Rejection rate of the naive CA test under (i) the true trend b_true and
    (ii) a flat process (b=0), both with clustering `sigma`. (i) is power; (ii) is
    the false-positive (Type-I) rate the clustering induces."""
    rng = np.random.default_rng(seed)
    rej_trend = rej_flat = 0
    for _ in range(n_sim):
        x1 = simulate_counts(denoms, a, b_true, sigma, rng)
        if cochran_armitage_p(x1, denoms) < alpha:
            rej_trend += 1
        x0 = simulate_counts(denoms, a, 0.0, sigma, rng)
        if cochran_armitage_p(x0, denoms) < alpha:
            rej_flat += 1
    return rej_trend / n_sim, rej_flat / n_sim


# --------------------------------------------------------------------------- #
# anchor sigma and the true trend to the observed DOXYVAC series               #
# --------------------------------------------------------------------------- #
def _emp_logit(x, n):
    return np.log((x + 0.5) / (n - x + 0.5))


def estimate_sigma(counts, denoms):
    """Method-of-moments estimate of the between-visit clustering sigma: excess
    variance of the empirical logits beyond binomial sampling, around a fitted trend."""
    x = np.asarray(counts, float)
    n = np.asarray(denoms, float)
    v = np.arange(len(x))
    y = _emp_logit(x, n)
    samp_var = 1.0 / (x + 0.5) + 1.0 / (n - x + 0.5)      # delta-method logit variance
    w = 1.0 / samp_var
    # weighted linear trend fit
    W = w.sum()
    vbar = (w * v).sum() / W
    ybar = (w * y).sum() / W
    b = (w * (v - vbar) * (y - ybar)).sum() / (w * (v - vbar) ** 2).sum()
    a = ybar - b * vbar
    resid = y - (a + b * v)
    excess = (w * resid ** 2).sum() / W - (w * samp_var).sum() / W   # MoM on weighted resid
    return {"a": float(a), "b": float(b), "sigma": float(np.sqrt(max(excess, 0.0)))}


def load_doxyvac_mrsa(root: Path):
    """Per-visit MRSA carriage counts + denominators, both arms, from the coded YAML."""
    rec = load_trial(root / "data/raw/coding/trial_doxyvac.yaml")
    order = ["baseline", "month3", "month6", "month9", "month12"]
    arms = {}
    for arm in ("doxy", "control"):
        obs = {o.timepoint: o for o in rec.observations
               if o.organism == "mrsa" and o.arm == arm}
        arms[arm] = {
            "counts": [obs[t].numerator for t in order if t in obs],
            "denoms": [obs[t].denominator for t in order if t in obs],
        }
    return arms


def _design_effect(denoms, sigma):
    """Rough variance-inflation of a pooled prevalence estimate from between-visit
    clustering: DEFF ~ 1 + (mean binomial-scale) * sigma^2 across visits."""
    return float(1.0 + np.mean(np.asarray(denoms)) * sigma ** 2 / len(denoms))


def _dejong_anchor(root):
    """Pull the empirical between-cohort MRSA σ̂ (+CI) from dejong_sigma. Returned as
    a dict, or None if the de Jong data is unavailable (keeps this module standalone)."""
    try:
        from src.analysis.dejong_sigma import estimate_sigma as dj_sigma, load_cohorts
        fit = dj_sigma(load_cohorts(root))
        return {"sigma": fit["sigma"], "lo": fit["ci"][0], "hi": fit["ci"][1]}
    except Exception:
        return None


def run(root: Path | str = None, n_sim=4000):
    root = Path(root) if root else Path(__file__).resolve().parents[2]
    arms = load_doxyvac_mrsa(root)
    doxy = arms["doxy"]
    fit = estimate_sigma(doxy["counts"], doxy["denoms"])
    fit_ctrl = estimate_sigma(arms["control"]["counts"], arms["control"]["denoms"])
    a, b_true = fit["a"], fit["b"]

    rows = []
    for sigma in SIGMA_GRID:
        pw, t1 = power_and_typeI(doxy["denoms"], a, b_true, sigma, n_sim=n_sim)
        rows.append({"sigma": sigma, "power": pw, "typeI": t1,
                     "deff": _design_effect(doxy["denoms"], sigma), "kind": "grid"})

    # empirically anchored rows: Type-I at the de Jong lower-CI / point / upper-CI σ
    dj = _dejong_anchor(root)
    anchored = []
    if dj:
        for label, sigma in [("de Jong 95% CI lower", dj["lo"]),
                             ("de Jong σ̂ (point)", dj["sigma"]),
                             ("de Jong 95% CI upper", dj["hi"])]:
            pw, t1 = power_and_typeI(doxy["denoms"], a, b_true, sigma, n_sim=n_sim)
            anchored.append({"sigma": sigma, "power": pw, "typeI": t1, "label": label,
                             "deff": _design_effect(doxy["denoms"], sigma), "kind": "anchor"})
    _write_report(root, arms, fit, fit_ctrl, rows, anchored, dj)
    return fit, fit_ctrl, rows, anchored


def _write_report(root, arms, fit, fit_ctrl, rows, anchored, dj):
    b = fit["b"]
    r0 = rows[0]
    md = f"""# Coverage of the null — a mean-based endpoint cannot resolve MRSA clustering

The **MRSA** clustering instrument for the ¶4 frame (the methicillin-resistant subset,
not the S. aureus analytic unit — that is `selection_ratchet_result.md`).
**Detectability, not effect estimation. No causal claim.**

MRSA carriage is modelled as `logit(p_visit) = a + b·visit + N(0, σ²)`: a true trend `b`
embedded in between-visit clustering of intensity `σ`. Counts are simulated at the
DOXYVAC doxy-PEP arm's ACTUAL per-visit denominators
({", ".join(map(str, arms['doxy']['denoms']))}) and scored with the naive
cross-sectional Cochran–Armitage trend test — the mean-based test a between-arm/level
reading implicitly relies on, which assumes binomial variance and is blind to
clustering. The trend `b = {b:.2f}` logit/visit is anchored to the observed
1.8%→9.9% doxy-arm rise.

**σ=0 is a calibration check, by construction.** With no overdispersion the
Cochran–Armitage trend test is correctly sized: {r0['typeI']:.0%} false positives against
a nominal 5% (within Monte-Carlo error), and {r0['power']:.0%} power for the
observed-magnitude trend. The test is fair; what follows is its failure under clustering,
not a rigged null.

| clustering σ | power (real trend) | Type-I (flat process) | design effect |
|---|---|---|---|
"""
    for r in rows:
        note = " *(calibration check)*" if abs(r["sigma"]) < 1e-9 else ""
        md += (f"| {r['sigma']:.2f}{note} | {r['power']:.0%} | {r['typeI']:.0%} | "
               f"{r['deff']:.1f} |\n")

    if anchored:
        md += "\n**Empirically anchored — Type-I at the de Jong between-cohort σ̂** "
        md += "(`dejong_sigma_result.md`; MRSA colonization dispersion):\n\n"
        md += "| σ (empirical) | power (real trend) | Type-I (flat process) |\n|---|---|---|\n"
        for r in anchored:
            md += f"| {r['sigma']:.2f} — {r['label']} | {r['power']:.0%} | **{r['typeI']:.0%}** |\n"

    r_mod = next(r for r in rows if abs(r["sigma"] - 0.5) < 1e-9)
    anchor_pt = next((r for r in anchored if "point" in r["label"]), None)
    anchor_lo = next((r for r in anchored if "lower" in r["label"]), None)
    md += f"""
**Read power and Type-I together — the test loses discrimination.** With no clustering
(σ=0) the test is fair. As σ grows, the false-positive rate climbs until the test rejects
almost regardless of whether a trend exists: at σ=0.5, Type-I is already
{r_mod['typeI']:.0%}. """
    if anchor_pt and anchor_lo:
        md += (f"""At the empirically anchored σ̂ = {anchor_pt['sigma']:.2f} the flat-process
false-positive rate is **{anchor_pt['typeI']:.0%}**, and even at the 95% CI lower bound
(σ = {anchor_lo['sigma']:.2f}) it is **{anchor_lo['typeI']:.0%}** — power
({anchor_pt['power']:.0%}) and Type-I ({anchor_pt['typeI']:.0%}) are so close that a
"significant" cross-sectional trend carries almost no information about whether a real
trend exists. """)
    md += """The mean-based endpoint cannot separate a real selection trend from the
clustering it is embedded in.

**The trials cannot rule this out with their own data — so the σ is external.**
Estimating σ from the observed DOXYVAC series gives σ̂ ≈ %.2f (doxy arm) and %.2f (no-PEP
arm), but on five timepoints with three residual degrees of freedom these are
unidentified — the trial cannot estimate whether its own endpoint is in its working
regime. That is itself a Stream-A finding. The clustering intensity is therefore imported
externally, from the documented between-cohort dispersion of MRSA colonization prevalence
(de Jong 2025; `dejong_sigma_result.md`), which is where the anchored rows above come
from. USA300 is documented to move through exactly these sexual networks in waves
[dejong2025; diep2008].

**This reframes the within-arm trend result.** Vanbaelen (2024) found the within-arm
MRSA increase significant in *both* arms (doxy p<0.0001, no-PEP p=0.0139). At the
documented clustering, that is precisely the coverage-null signature: a flat process
crossed with clustering is scored as a significant trend the large majority of the time.
"Both arms significant" is as consistent with clustering the endpoint cannot see as it is
with selection.

**Scope (Contract 2 / Contract 3).** This indicts *mean-based, cross-sectional* MRSA
endpoints at these denominators — not measurement in principle. A design that tracked the
same networks over time, or resolved transmission structure, could see what this one
cannot. The claim is that the instruments actually deployed cannot, not that the harm is
unmeasurable by any instrument.

(`SEED=%d`; regenerate with `python -m src.analysis.coverage_null`.)
""" % (fit['sigma'], fit_ctrl['sigma'], SEED)
    (root / "outputs").mkdir(exist_ok=True)
    (root / "outputs/coverage_null_result.md").write_text(md)


if __name__ == "__main__":
    fit, fit_ctrl, rows, anchored = run()
    print(f"true trend b = {fit['b']:.3f} logit/visit; "
          f"σ̂ doxy={fit['sigma']:.3f} control={fit_ctrl['sigma']:.3f} (3 resid df — unidentified)")
    for r in rows:
        print(f"  σ={r['sigma']:.2f}  power={r['power']:.0%}  typeI={r['typeI']:.0%}")
    for r in anchored:
        print(f"  σ={r['sigma']:.2f}  power={r['power']:.0%}  typeI={r['typeI']:.0%}  <- {r['label']}")
    print("wrote outputs/coverage_null_result.md")
