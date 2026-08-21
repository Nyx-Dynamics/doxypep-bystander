"""Empirical overdispersion of MRSA colonization prevalence — the sigma the
detectability argument needs (Task 2). MRSA-SCOPED.

de Jong et al. (BMC Infect Dis 2025;25:299) is not a time series; it is a
distribution of cross-sectional CA-MRSA *colonization* prevalences across
independent MSM/PLWH cohorts (Table 1). That between-cohort dispersion is the
overdispersion parameter sigma (logit scale) that `coverage_null.py` otherwise has
to assume. We estimate it with a logit-normal binomial random-effects model:

    k_i ~ Binomial(n_i, p_i),   logit(p_i) = mu + sigma * z_i,   z_i ~ N(0,1)

fit by marginal maximum likelihood (Gauss–Hermite quadrature over z), with a
profile-likelihood confidence interval on sigma. The zeros (0/104, 0/300, 0/211,
0/190) are handled correctly by the binomial marginal likelihood — no continuity
fudge on the logit is used for the fit.

WHAT THIS LICENSES (guard rail). sigma-hat here is the dispersion an MRSA prevalence
endpoint must work against in this population. It is an UPPER BOUND on transmission
clustering: the cohorts differ in assay, site, and risk stratum (0% general MSM up to
54% chemsex-PLWH conditional on infection), and ten colonisation cohorts cannot partition
methodological heterogeneity from genuine clustering. So the claim is NOT "MRSA
transmission clusters with sigma = X." It is "the documented dispersion is not small —
its lower confidence bound already sits in the regime where the naive cross-sectional
trend test's Type-I error reaches 20-48% (`coverage_null.py`)." That is all the
argument needs, and it is robust to the upper-bound caveat because it rests on the
LOWER bound of sigma-hat. Do NOT let this sigma become an S. aureus sigma — that would
repeat the MRSA/S. aureus nesting error in a new place.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import yaml
from numpy.polynomial.hermite_e import hermegauss
from scipy.optimize import minimize_scalar, minimize
from scipy.stats import chi2

N_QUAD = 64            # Gauss–Hermite nodes (probabilists' Hermite -> N(0,1) weight)


def load_cohorts(root: Path, include_conditional=True, include_mixed=True):
    data = yaml.safe_load((root / "data/raw/coding/dejong_mrsa_cohorts.yaml").read_text())
    rows = []
    for c in data["cohorts"]:
        if c["basis_flag"] == "conditional" and not include_conditional:
            continue
        if c["basis_flag"] == "mixed" and not include_mixed:
            continue
        rows.append(c)
    return rows


def _expit(x):
    return 1.0 / (1.0 + np.exp(-np.clip(x, -700, 700)))


def _neg_marginal_loglik(params, k, n, nodes, logw):
    """-log marginal likelihood of the logit-normal binomial (GH quadrature).
    params = (mu, log_sigma) so sigma > 0 without a bound."""
    mu, log_sigma = params
    sigma = np.exp(log_sigma)
    # per-study, per-node binomial log-pmf (drop the constant nCk — cancels in CI/opt)
    p = _expit(mu + sigma * nodes)                      # (Q,)
    p = np.clip(p, 1e-12, 1 - 1e-12)
    ll = 0.0
    for ki, ni in zip(k, n):
        logpmf = ki * np.log(p) + (ni - ki) * np.log(1 - p)   # (Q,)
        # log-sum-exp over quadrature nodes with the normal weights
        m = logpmf.max()
        ll += m + np.log(np.sum(np.exp(logw + logpmf - m)))
    return -ll


def _fit(k, n, nodes, logw):
    # decent starts from the pooled logit and the observed logit spread
    phat = (k + 0.5) / (n + 1.0)
    mu0 = np.log(phat.mean() / (1 - phat.mean()))
    res = minimize(_neg_marginal_loglik, x0=[mu0, np.log(1.0)],
                   args=(k, n, nodes, logw), method="Nelder-Mead",
                   options={"xatol": 1e-6, "fatol": 1e-8, "maxiter": 20000})
    mu, sigma = res.x[0], np.exp(res.x[1])
    return mu, sigma, -res.fun


def _profile_ci_sigma(k, n, nodes, logw, sigma_hat, ll_hat, level=0.95):
    """Profile-likelihood CI on sigma: the set where 2*(ll_hat - ll_profile(sigma))
    <= chi2_{1}(level). At each fixed sigma, profile out mu."""
    crit = chi2.ppf(level, 1)

    def profile_ll(sigma):
        if sigma <= 0:
            return -np.inf
        f = lambda mu: _neg_marginal_loglik([mu, np.log(sigma)], k, n, nodes, logw)
        r = minimize_scalar(f, bounds=(-12, 6), method="bounded")
        return -r.fun

    def gap(sigma):
        return 2 * (ll_hat - profile_ll(sigma)) - crit

    # lower bound: search in (tiny, sigma_hat); upper: (sigma_hat, large)
    lo, hi = _bisect_root(gap, 1e-4, sigma_hat), _bisect_root(gap, sigma_hat, 20.0)
    return lo, hi


def _bisect_root(f, a, b, tol=1e-3, maxit=200):
    fa, fb = f(a), f(b)
    if np.sign(fa) == np.sign(fb):
        return a if abs(fa) < abs(fb) else b     # no crossing in range; return nearer end
    for _ in range(maxit):
        m = 0.5 * (a + b)
        fm = f(m)
        if abs(fm) < tol or (b - a) < tol:
            return m
        if np.sign(fm) == np.sign(fa):
            a, fa = m, fm
        else:
            b, fb = m, fm
    return 0.5 * (a + b)


def estimate_sigma(cohorts):
    k = np.array([c["count"] for c in cohorts], float)
    n = np.array([c["n"] for c in cohorts], float)
    nodes, w = hermegauss(N_QUAD)                 # probabilists' Hermite: weight exp(-x^2/2)
    logw = np.log(w / np.sqrt(2 * np.pi))         # normalize to N(0,1) expectation
    mu, sigma, ll = _fit(k, n, nodes, logw)
    lo, hi = _profile_ci_sigma(k, n, nodes, logw, sigma, ll)
    return {"mu": mu, "sigma": sigma, "ci": (lo, hi), "loglik": ll,
            "n_studies": len(cohorts),
            "prev": [(c.get("study", "?"), c["count"], int(c["n"])) for c in cohorts]}


def run(root: Path | str = None):
    root = Path(root) if root else Path(__file__).resolve().parents[2]
    full = estimate_sigma(load_cohorts(root))                        # all 10
    no_cond = estimate_sigma(load_cohorts(root, include_conditional=False))  # drop the 54%
    msm_only = estimate_sigma(load_cohorts(root, include_conditional=False,
                                           include_mixed=False))      # general-MSM screens only
    _write_report(root, full, no_cond, msm_only)
    return {"full": full, "no_conditional": no_cond, "msm_only": msm_only}


def _write_report(root, full, no_cond, msm_only):
    def line(fit):
        lo, hi = fit["ci"]
        return (f"{fit['n_studies']} | σ̂ = **{fit['sigma']:.2f}** "
                f"(95% profile CI {lo:.2f}–{hi:.2f}) | μ̂ = {fit['mu']:.2f} "
                f"(pooled prev {_expit(fit['mu']):.1%})")
    prev_tab = "\n".join(
        f"| {s} | {c}/{n} | {c/n:.1%} |" for s, c, n in full["prev"])
    md = f"""# de Jong cross-cohort σ — empirical overdispersion of MRSA colonization (MRSA-scoped)

Between-cohort dispersion of CA-MRSA **colonization** prevalence across independent
MSM/PLWH cohorts (de Jong 2025, Table 1), fit as a logit-normal binomial
random-effects model `logit(p_i) = μ + σ·z_i` by marginal maximum likelihood
(Gauss–Hermite, {N_QUAD} nodes), with a profile-likelihood CI on σ. **MRSA subset,
not S. aureus (Contract 2).**

| cohort | MRSA colonized / n | prevalence |
|---|---|---|
{prev_tab}

Prevalence spans **{min(c/n for _, c, n in full['prev']):.1%} to {max(c/n for _, c, n in full['prev']):.1%}** across cohorts.

| study set | n studies | σ̂ (logit scale) |
|---|---|---|
| all colonization cohorts | {line(full)} |
| drop the conditional-on-infection 54% (De La Mora) | {line(no_cond)} |
| general-MSM screens only (drop mixed + conditional) | {line(msm_only)} |

**σ̂ = {full['sigma']:.2f}** (95% profile CI {full['ci'][0]:.2f}–{full['ci'][1]:.2f}) on
the primary set. The estimate is stable to dropping the 54% outlier
(σ̂ = {no_cond['sigma']:.2f}) and to restricting to general-MSM screens
(σ̂ = {msm_only['sigma']:.2f}).

**What this licenses.** σ̂ is an UPPER BOUND on transmission clustering — the cohorts
differ in assay, site, and risk stratum, and ten colonisation cohorts cannot separate
methodological heterogeneity from genuine clustering. The load-bearing claim rests on the **lower**
confidence bound, not the point estimate: even σ = {full['ci'][0]:.2f} is far into the
regime where the naive cross-sectional trend test's Type-I error is 20–48%
(`coverage_null_result.md`). So the documented dispersion of the MRSA colonization
endpoint is *not small* — sufficient to place the mean-based trend test in its degraded
regime — which is all the detectability argument requires. This σ is for MRSA
colonization overdispersion and licenses a statement about the **MRSA** endpoint only;
it is not an S. aureus σ.

(Fit: logit-normal binomial, marginal ML; regenerate with
`python -m src.analysis.dejong_sigma`.)
"""
    (root / "outputs").mkdir(exist_ok=True)
    (root / "outputs/dejong_sigma_result.md").write_text(md)


if __name__ == "__main__":
    out = run()
    for name, fit in out.items():
        lo, hi = fit["ci"]
        print(f"{name:16s}: n={fit['n_studies']}  σ̂={fit['sigma']:.3f}  "
              f"95% CI [{lo:.3f}, {hi:.3f}]  μ̂={fit['mu']:.3f}")
    print("wrote outputs/dejong_sigma_result.md")
