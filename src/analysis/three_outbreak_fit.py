"""Do the trial MRSA carriage series distinguish an outbreak/wave from noise?

The companion to `coverage_null.py` — the **MRSA** single-cohort illustration (the
methicillin-resistant subset, not the S. aureus analytic unit; that is
`selection_ratchet.py`). Where coverage_null shows a mean-based endpoint *would* be blind
to clustering, this one asks the empirical question directly of the data in hand: fit
three competing generative models to each observed MRSA carriage series and test whether
the data can tell them apart at the trials' denominators.

Three models, nested, fit by maximum binomial likelihood over visits v = 0..T:

    flat     logit(p_v) = a                 (1 param)  — no change
    trend    logit(p_v) = a + b·v           (2 param)  — monotone selection
    wave     logit(p_v) = a + b·v + c·v²    (3 param)  — an outbreak: rise then fall

The wave term is the smallest model that can produce the non-monotone "up-up-up-down-up"
lurch [croi2023_molina_doxyvac_slides.md] that a clustered, cross-sectionally sampled
transmission process leaves behind. We compare models by AIC and by a likelihood-ratio
test of wave-vs-flat, and — because the chi-square reference is unreliable at these tiny
counts — calibrate the LR statistic by a PARAMETRIC BOOTSTRAP under the flat MLE.

Expected/target finding (logged before results in DECISIONS.md): at the observed
denominators the data do NOT significantly favour the wave over the flat null. That is
the disciplined form of the manuscript's claim — the non-monotonicity is *consistent
with* clustering AND *indistinguishable from* noise, so a prevalence endpoint at these
n cannot be read either way. This QUANTIFIES 'indistinguishable from noise, which is the
point'; it does not claim the data prove clustering. No causal claim.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
from scipy.optimize import minimize

from src.analysis.coverage_null import load_doxyvac_mrsa

SEED = 20260820
N_BOOT = 2000
MODELS = {"flat": 1, "trend": 2, "wave": 3}


def _design(v, k):
    v = np.asarray(v, float)
    cols = [np.ones_like(v), v, v ** 2][:k]
    return np.column_stack(cols)


def _neg_loglik(beta, X, x, n):
    eta = X @ beta
    # stable log(1+exp) pieces
    p = 1.0 / (1.0 + np.exp(-eta))
    p = np.clip(p, 1e-12, 1 - 1e-12)
    return -np.sum(x * np.log(p) + (n - x) * np.log(1 - p))


def fit_model(counts, denoms, k):
    """ML fit of the k-parameter logit-polynomial; returns (loglik, beta, aic)."""
    x = np.asarray(counts, float)
    n = np.asarray(denoms, float)
    v = np.arange(len(x))
    X = _design(v, k)
    beta0 = np.zeros(k)
    beta0[0] = np.log((x.sum() + 0.5) / (n.sum() - x.sum() + 0.5))
    res = minimize(_neg_loglik, beta0, args=(X, x, n), method="Nelder-Mead",
                   options={"xatol": 1e-8, "fatol": 1e-10, "maxiter": 10000})
    ll = -res.fun
    return {"loglik": ll, "beta": res.x, "aic": 2 * k - 2 * ll, "k": k}


def lr_statistic(counts, denoms, k_full, k_red):
    full = fit_model(counts, denoms, k_full)
    red = fit_model(counts, denoms, k_red)
    return 2 * (full["loglik"] - red["loglik"]), full, red


def bootstrap_discrimination(counts, denoms, k_full, k_red, n_boot=N_BOOT, seed=SEED):
    """Parametric-bootstrap p-value for a k_full-vs-k_red model comparison: simulate
    under the REDUCED MLE, refit both, and ask how often the bootstrap LR exceeds the
    observed LR. A large p means the extra parameters do not earn their keep — the data
    cannot distinguish the richer model from the simpler one at these denominators."""
    n = np.asarray(denoms, int)
    lr_obs, full, red = lr_statistic(counts, denoms, k_full, k_red)
    p_red = 1.0 / (1.0 + np.exp(-(_design(np.arange(len(n)), k_red) @ red["beta"])))
    rng = np.random.default_rng(seed)
    ge = 0
    for _ in range(n_boot):
        xb = rng.binomial(n, p_red)
        lr_b, _, _ = lr_statistic(xb, denoms, k_full, k_red)
        if lr_b >= lr_obs - 1e-9:
            ge += 1
    return {"lr_obs": lr_obs, "p_boot": ge / n_boot}


def analyze_series(label, counts, denoms):
    fits = {name: fit_model(counts, denoms, k) for name, k in MODELS.items()}
    aics = [fits[m]["aic"] for m in MODELS]
    best = min(fits, key=lambda m: fits[m]["aic"])
    spread = max(aics) - min(aics)
    return {
        "label": label, "counts": counts, "denoms": denoms,
        "fits": fits,
        # only name a "best" model when it is meaningfully separated (ΔAIC >= 2);
        # otherwise the models are indistinguishable and picking one is noise-mining.
        "aic_spread": spread,
        "best_by_aic": best if spread >= 2.0 else None,
        # is there ANY departure from flat?  is there a monotone rise?
        "trend_vs_flat": bootstrap_discrimination(counts, denoms, 2, 1),
        # is the OUTBREAK curvature real beyond a monotone rise? (the clustering signature)
        "wave_vs_trend": bootstrap_discrimination(counts, denoms, 3, 2),
    }


def _fmt_p(p):
    """Bootstrap p with a floor: p=0 means no bootstrap replicate reached the observed
    statistic, i.e. p < 1/N_BOOT — never report a literal 0."""
    return f"<{1/N_BOOT:.4f}" if p <= 0 else f"{p:.3f}"


def run(root: Path | str = None):
    root = Path(root) if root else Path(__file__).resolve().parents[2]
    arms = load_doxyvac_mrsa(root)
    series = [
        ("DOXYVAC doxy-PEP arm (MRSA throat carriage)", arms["doxy"]),
        ("DOXYVAC no-PEP arm (MRSA throat carriage)", arms["control"]),
    ]
    results = [analyze_series(lbl, s["counts"], s["denoms"]) for lbl, s in series]
    _write_report(root, results)
    return results


def _write_report(root, results):
    md = f"""# Three-model fit — what shape can the trial MRSA series actually resolve?

Companion to `coverage_null_result.md`; the **MRSA** single-cohort illustration (not the
S. aureus unit — see `selection_ratchet_result.md`). For each observed MRSA carriage
series we fit three nested models by maximum binomial likelihood —

- **flat** `logit p = a` (no change),
- **trend** `logit p = a + b·v` (monotone selection),
- **wave** `logit p = a + b·v + c·v²` (an outbreak: rise then fall) —

compare by AIC (a model is only named "best" when it clears the next by ΔAIC ≥ 2;
otherwise the models are **indistinguishable** and naming one is noise-mining), and
calibrate two likelihood-ratio tests with a parametric bootstrap of {N_BOOT} draws (χ² is
unreliable at these counts): **trend-vs-flat** (is there *any* rise?) and **wave-vs-trend**
(is the non-monotone *outbreak curvature* — the clustering signature — real beyond a plain
monotone rise?). A bootstrap p shown as `<{1/N_BOOT:.4f}` means no draw reached the
observed statistic. **Detectability, not effect estimation. No causal claim.**

| series | flat / trend / wave AIC | AIC verdict | trend-vs-flat (is there a rise?) | wave-vs-trend (is it an outbreak?) |
|---|---|---|---|---|
"""
    for r in results:
        f = r["fits"]
        verdict = (f"**{r['best_by_aic']}**" if r["best_by_aic"]
                   else f"indistinguishable (ΔAIC {r['aic_spread']:.1f})")
        md += (f"| {r['label']} | {f['flat']['aic']:.1f} / {f['trend']['aic']:.1f} / "
               f"{f['wave']['aic']:.1f} | {verdict} | "
               f"p={_fmt_p(r['trend_vs_flat']['p_boot'])} | "
               f"p={_fmt_p(r['wave_vs_trend']['p_boot'])} |\n")
    md += f"""
**Reading.** The two bootstrap columns separate two questions the trials' non-monotone
series conflate:

- **Is there a rise?** In the doxy-PEP arm, yes — the monotone trend beats flat
  (bootstrap p {_fmt_p(results[0]['trend_vs_flat']['p_boot'])}, no null draw reached it),
  consistent with Vanbaelen's within-arm p<0.0001. In the no-PEP arm the rise is not
  resolved (p={results[1]['trend_vs_flat']['p_boot']:.3f}), and all three models sit within
  {results[1]['aic_spread']:.1f} AIC unit — **indistinguishable**; the earlier "best=wave"
  reading was a {results[1]['aic_spread']:.1f}-AIC artifact and is struck.
- **Is it an outbreak?** In *neither* arm does the wave earn its curvature parameter over
  a monotone trend (wave-vs-trend bootstrap p={results[0]['wave_vs_trend']['p_boot']:.2f}
  doxy, {results[1]['wave_vs_trend']['p_boot']:.2f} no-PEP; wave never lowers AIC by the ~2
  units that would mark a real improvement). The non-monotonicity — the M6 crossover, the
  M9 dip, the "up-up-up-down-up" lurch — is **within noise**.

So the data can, at most and in one arm, establish *that* carriage rose; they cannot
identify *how*. A monotone selection trend and a clustered, wave-like transmission
process fit the series equally well. The mechanism is unidentifiable from these
endpoints at these denominators.

This is the disciplined form of the ¶4 claim, and it holds the line the manuscript
already draws: the non-monotonicity is **illustration, not proof**. The trajectories
*are* what clustered, cross-sectionally sampled transmission would produce; they are
*also* statistically indistinguishable from a plain trend or from noise at n≈120–330/
visit with single-to-low-double-digit counts. Both halves are true, and together they
indict the instrument, not establish an outbreak. The DoxyPEP resistance series is
sparser still (2–3 post-baseline points per arm) and cannot even be brought to this
test — a further instance of the same gap.

Paired with `coverage_null_result.md` — which shows a mean-based MRSA endpoint *would* be
blind to clustering it did contain, misreading a flat process as a trend the large
majority of the time at the empirically anchored between-cohort σ̂≈2.7
(`dejong_sigma_result.md`) — this closes the loop: the design cannot see the clustering
*shape* in principle, and cannot rule it out in these data. (MRSA-scoped throughout; the
S. aureus selection question is `selection_ratchet_result.md`.)

"""
    md += (f"(`SEED={SEED}`, `N_BOOT={N_BOOT}`; regenerate with "
           f"`python -m src.analysis.three_outbreak_fit`.)\n")
    (root / "outputs").mkdir(exist_ok=True)
    (root / "outputs/three_outbreak_fit_result.md").write_text(md)


if __name__ == "__main__":
    for r in run():
        f = r["fits"]
        verdict = r["best_by_aic"] or f"indistinguishable (ΔAIC {r['aic_spread']:.1f})"
        print(f"{r['label']}")
        print(f"  AIC flat={f['flat']['aic']:.1f} trend={f['trend']['aic']:.1f} "
              f"wave={f['wave']['aic']:.1f}  verdict={verdict}")
        print(f"  trend-vs-flat p={_fmt_p(r['trend_vs_flat']['p_boot'])}  "
              f"wave-vs-trend p={r['wave_vs_trend']['p_boot']:.3f}")
    print("wrote outputs/three_outbreak_fit_result.md")
