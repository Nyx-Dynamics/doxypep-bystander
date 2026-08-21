"""The selection ratchet — within US DoxyPEP, S. aureus (Task 1). S. AUREUS-SCOPED.

This is the clean, single-trial, single-assay instrument for the ¶4/§3.1 claim that
doxycycline resistance in *S. aureus* accumulates under selection (a ratchet), as
distinct from the MRSA-clustering claim (handled by `coverage_null.py` /
`three_outbreak_fit.py` / `dejong_sigma.py`). All quantities — colonization, doxy-R,
and the derived susceptible carriage — come from the SAME nares/oropharyngeal cultures,
the SAME two reported timepoints, and the SAME per-visit denominators, so the only thing
varying is the organism-subset. No cross-trial pooling (that would reintroduce
site/assay/schedule/denominator confounds).

DATA (CROI 2023 OA-3 PUBLISHED ABSTRACT TABLE, `croi2023_luetkemeyer_OA3.md`) — the same
source the manuscript §3.1 cites — all over the ALL-SWABBED denominator per visit:

  Doxy-PEP   M0  42.2% (141/334) colonized, 3.6%  (12/334) doxy-R
             M12 29.2% (40/137)  colonized, 11.7% (16/137) doxy-R
  SOC        M0  48.4% (78/161)  colonized, 11.8% (19/161) doxy-R
             M12 45.2% (28/62)   colonized, 4.8%  (3/62)   doxy-R

The abstract table reports M0 and M12 only (no M6), so this is a two-timepoint,
endpoints-only test on the AUTHORITATIVE PUBLISHED counts — chosen so the code regenerates
the per-carrier 8.5% → 40% the manuscript cites (rather than the CROI-slides venue's
11% → 41%; the venues do not reconcile, and that 5/16/28 discordance is itself a Stream A
finding, handled in the manuscript, not smoothed over here).

ARITHMETIC-BASE FINDING (Task 1, step 1). The reported resistance figure (3.6% → 11.7%) is
a fraction of the WHOLE COHORT (all-swabbed), NOT of carriers — every "Doxy-resistance"
cell shares its denominator with the isolation cell beside it. The per-carrier rate is
obtained by dividing by colonization first (12/141 = 8.5% → 16/40 = 40.0%). Both bases are
used correctly below: susceptible carriage = colonization − all-swabbed doxy-R =
colonization × (1 − per-carrier doxy-R).

WHAT THIS LICENSES (guard rail). "S. aureus susceptible carriage depletes consistent with
selection; the resistant fraction rises — the ratchet." NOT "we fit a monotonic model":
with two endpoints we run pre-specified DIRECTIONAL tests (one-sided decline; one-sided
per-carrier increase; a neutral-suppression contrast), never shape discovery. No causal
claim.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
from scipy.stats import fisher_exact, norm, poisson

# CROI 2023 OA-3 published abstract table; order = [baseline, month12]
DOXY = {"colonized": [141, 40],    # M0 141/334, M12 40/137 (Staph+)
        "resistant": [12, 16],     # M0 12/334,  M12 16/137 (doxy-R, all-swabbed)
        "swabbed":   [334, 137]}
SOC = {"colonized":  [78, 28],     # M0 78/161,  M12 28/62
       "resistant":  [19, 3],      # M0 19/161,  M12 3/62
       "swabbed":    [161, 62]}
TIMEPOINTS = ["baseline", "month12"]


def _series(arm):
    col = np.array(arm["colonized"], float)
    res = np.array(arm["resistant"], float)
    n = np.array(arm["swabbed"], float)
    susceptible = col - res                       # susceptible carriers (count)
    return {
        "n": n, "colonized": col, "resistant": res, "susceptible": susceptible,
        "colonization_prev": col / n,             # of all swabbed
        "resistant_prev": res / n,                # of all swabbed (the reported base)
        "susceptible_prev": susceptible / n,      # of all swabbed
        "per_carrier_R": res / col,               # of carriers (the selection quantity)
    }


def _ca_z(counts, denoms):
    """Cochran–Armitage trend z: z>0 rising, z<0 falling. Binomial-variance (naive)."""
    x = np.asarray(counts, float); nn = np.asarray(denoms, float)
    s = np.arange(len(x), dtype=float)
    N = nn.sum(); pbar = x.sum() / N
    if pbar <= 0 or pbar >= 1:
        return 0.0
    sbar = (nn * s).sum() / N
    T = (s * (x - nn * pbar)).sum()
    var = pbar * (1 - pbar) * (nn * (s - sbar) ** 2).sum()
    return float(T / np.sqrt(var)) if var > 0 else 0.0


def one_sided_decline_p(counts, denoms):
    """Pre-specified DIRECTIONAL test: is the series consistent with monotonic DECLINE?
    p = P(Z <= z_obs) — small when the trend falls. Confirmatory, not model selection."""
    return float(norm.cdf(_ca_z(counts, denoms)))


def per_carrier_increase(res, col):
    """One-sided Fisher exact for a rise in the per-carrier resistant fraction,
    baseline vs month-12. Independent of the colonization change."""
    b_r, b_c = int(res[0]), int(col[0])
    m_r, m_c = int(res[-1]), int(col[-1])
    table = [[m_r, m_c - m_r], [b_r, b_c - b_r]]     # M12 vs baseline; resistant vs susceptible
    _, p = fisher_exact(table, alternative="greater")
    return {"baseline": (b_r, b_c, b_r / b_c), "month12": (m_r, m_c, m_r / m_c), "p": float(p)}


def neutral_suppression_contrast(s):
    """Under NEUTRAL suppression the drug clears carriage regardless of resistance, so
    the per-carrier resistant fraction is unchanged and resistant CARRIAGE falls in
    proportion to colonization. Expected M12 resistant count under that null =
    baseline per-carrier R × M12 colonized. Selection shows up as observed >> expected."""
    base_pc = s["per_carrier_R"][0]
    exp_m12 = base_pc * s["colonized"][-1]
    obs_m12 = s["resistant"][-1]
    p_excess = float(poisson.sf(obs_m12 - 1, exp_m12))   # P(X >= obs | mean = expected)
    return {"expected": exp_m12, "observed": obs_m12, "p": p_excess,
            "resistant_prev_change": (s["resistant_prev"][0], s["resistant_prev"][-1]),
            "colonization_change": (s["colonization_prev"][0], s["colonization_prev"][-1])}


def analyze():
    out = {}
    for name, arm in [("doxy", DOXY), ("soc", SOC)]:
        s = _series(arm)
        out[name] = {
            "series": s,
            "susceptible_decline_p": one_sided_decline_p(s["susceptible"], s["n"]),
            "per_carrier": per_carrier_increase(s["resistant"], s["colonized"]),
            "neutral": neutral_suppression_contrast(s),
        }
    return out


def run(root: Path | str = None):
    root = Path(root) if root else Path(__file__).resolve().parents[2]
    res = analyze()
    _write_report(root, res)
    return res


def _fmt_prev(s, key):
    return " → ".join(f"{v:.0%}" for v in s[key])


def _write_report(root, res):
    d, sc = res["doxy"], res["soc"]
    ds, scs = d["series"], sc["series"]
    md = f"""# The selection ratchet — S. aureus within US DoxyPEP (S. aureus-scoped)

The clean single-trial, single-assay test of whether doxycycline resistance in
*S. aureus* accumulates under selection. Colonization, doxy-R, and susceptible carriage
share the same cultures, timepoints, and denominators (CROI 2023 OA-3 published abstract
table — the same source §3.1 cites; M0 and M12 only). **No cross-trial pooling.
Directional confirmatory tests only — two endpoints cannot support shape discovery. No
causal claim.**

**Arithmetic base (verified).** The reported resistance figure (3.6% → 11.7%) is over the
WHOLE COHORT (all-swabbed), not carriers — in the abstract table every doxy-R cell shares
its denominator with the isolation cell beside it. Per carrier (dividing by colonization)
it is **8.5% → 40%** (12/141 → 16/40). The manuscript's stated "fraction-of-carriers"
reading applies to that *derived* per-carrier series, not the raw all-swabbed figure.

## Doxy-PEP arm — the ratchet

| quantity (of all swabbed) | baseline | month 12 |
|---|---|---|
| colonization | {ds['colonization_prev'][0]:.0%} | {ds['colonization_prev'][1]:.0%} |
| doxy-R (reported, all-swabbed) | {ds['resistant_prev'][0]:.1%} | {ds['resistant_prev'][1]:.1%} |
| **susceptible carriage** | **{ds['susceptible_prev'][0]:.1%}** | **{ds['susceptible_prev'][1]:.1%}** |
| per-carrier doxy-R | {ds['per_carrier_R'][0]:.1%} | {ds['per_carrier_R'][1]:.1%} |

- **Susceptible carriage depletes**, consistent with the decline selection predicts:
  one-sided trend test **p = {d['susceptible_decline_p']:.2g}**
  ({_fmt_prev(ds,'susceptible_prev')} of all swabbed).
- **Per-carrier resistance rises**: {d['per_carrier']['baseline'][0]}/{d['per_carrier']['baseline'][1]}
  ({d['per_carrier']['baseline'][2]:.1%}) → {d['per_carrier']['month12'][0]}/{d['per_carrier']['month12'][1]}
  ({d['per_carrier']['month12'][2]:.1%}), one-sided Fisher **p = {d['per_carrier']['p']:.2g}**.
- **Conservation-of-carriers / selection vs neutral suppression.** Resistant carriage
  *rose* absolutely ({d['neutral']['resistant_prev_change'][0]:.1%} →
  {d['neutral']['resistant_prev_change'][1]:.1%} of all swabbed) *even though* total
  colonization *fell* ({d['neutral']['colonization_change'][0]:.0%} →
  {d['neutral']['colonization_change'][1]:.0%}). Neutral suppression — clearing carriage
  regardless of resistance — predicts resistant carriage should fall in proportion, to an
  expected ~{d['neutral']['expected']:.0f} resistant carriers at M12; **{d['neutral']['observed']:.0f}**
  were observed (one-sided Poisson **p = {d['neutral']['p']:.2g}**). The susceptible loss
  decomposes as (total-carriage loss) + (resistant expansion): susceptibles are cleared
  while resistants expand — the ratchet.

## SOC arm — uninformative (as expected)

| quantity (of all swabbed) | baseline | month 12 |
|---|---|---|
| colonization | {scs['colonization_prev'][0]:.0%} | {scs['colonization_prev'][1]:.0%} |
| susceptible carriage | {scs['susceptible_prev'][0]:.1%} | {scs['susceptible_prev'][1]:.1%} |
| per-carrier doxy-R | {scs['per_carrier_R'][0]:.1%} | {scs['per_carrier_R'][1]:.1%} |

The SOC susceptible series does not deplete (it rises, {_fmt_prev(scs,'susceptible_prev')};
decline p = {sc['susceptible_decline_p']:.2g}, not significant) and per-carrier resistance
*falls* ({scs['per_carrier_R'][0]:.1%} → {scs['per_carrier_R'][1]:.1%}; increase Fisher
p = {sc['per_carrier']['p']:.2g}). With {int(scs['n'][-1])} swabbed at M12 this arm is
**underpowered and uninformative**, not a contrasting shape — stated as such.

**Licenses.** S. aureus susceptible carriage depletes consistent with selection and the
resistant fraction rises — the ratchet — in the doxy-PEP arm; the SOC arm is
uninformative. This is a directional, hypothesis-confirming result on the S. aureus unit,
not a fitted model and not a causal claim.

(Regenerate with `python -m src.analysis.selection_ratchet`.)
"""
    (root / "outputs").mkdir(exist_ok=True)
    (root / "outputs/selection_ratchet_result.md").write_text(md)


if __name__ == "__main__":
    res = run()
    for name in ("doxy", "soc"):
        r = res[name]; s = r["series"]
        print(f"{name.upper()}  susceptible carriage {_fmt_prev(s,'susceptible_prev')}"
              f"  decline p={r['susceptible_decline_p']:.2g}")
        print(f"      per-carrier R {s['per_carrier_R'][0]:.1%}->{s['per_carrier_R'][-1]:.1%}"
              f"  Fisher p={r['per_carrier']['p']:.2g}"
              f"  | neutral-null expected {r['neutral']['expected']:.0f} vs obs "
              f"{r['neutral']['observed']:.0f}  p={r['neutral']['p']:.2g}")
    print("wrote outputs/selection_ratchet_result.md")
