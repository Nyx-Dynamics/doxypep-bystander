# de Jong cross-cohort σ — empirical overdispersion of MRSA colonization (MRSA-scoped)

Between-cohort dispersion of CA-MRSA **colonization** prevalence across independent
MSM/PLWH cohorts (de Jong 2025, Table 1), fit as a logit-normal binomial
random-effects model `logit(p_i) = μ + σ·z_i` by marginal maximum likelihood
(Gauss–Hermite, 64 nodes), with a profile-likelihood CI on σ. **MRSA subset,
not S. aureus (Contract 2).**

| cohort | MRSA colonized / n | prevalence |
|---|---|---|
| Shastry 2007, New York City | 9/27 | 33.3% |
| Szumowski 2009, Boston | 30/795 | 3.8% |
| Antoniou 2009, Canada | 8/500 | 1.6% |
| Giuliani 2010, Italy | 0/104 | 0.0% |
| Fouere 2012, Paris | 0/300 | 0.0% |
| Joore 2013, Amsterdam | 0/211 | 0.0% |
| Witzel 2014, Brazil | 2/302 | 0.7% |
| Imaz 2015, Barcelona | 0/190 | 0.0% |
| Popovich 2020, Chicago | 40/171 | 23.4% |
| De La Mora 2023, Barcelona | 13/24 | 54.2% |

Prevalence spans **0.0% to 54.2%** across cohorts.

| study set | n studies | σ̂ (logit scale) |
|---|---|---|
| all colonization cohorts | 10 | σ̂ = **2.70** (95% profile CI 1.74–4.57) | μ̂ = -5.88 (pooled prev 0.3%) |
| drop the conditional-on-infection 54% (De La Mora) | 9 | σ̂ = **2.67** (95% profile CI 1.79–3.27) | μ̂ = -4.82 (pooled prev 0.8%) |
| general-MSM screens only (drop mixed + conditional) | 6 | σ̂ = **2.62** (95% profile CI 1.63–11.39) | μ̂ = -5.76 (pooled prev 0.3%) |

**σ̂ = 2.70** (95% profile CI 1.74–4.57) on
the primary set. The estimate is stable to dropping the 54% outlier
(σ̂ = 2.67) and to restricting to general-MSM screens
(σ̂ = 2.62).

**What this licenses.** σ̂ is a deliberately conservative external sensitivity anchor for the
scale of heterogeneity — not an estimate of the trial's between-visit variance. The cohorts
differ in assay, site, and risk stratum, and ten colonisation cohorts cannot separate
methodological heterogeneity from genuine clustering. The load-bearing claim rests on the **lower**
confidence bound, not the point estimate: even σ = 1.74 is far into the
regime where the naive cross-sectional trend test's Type-I error is well above nominal
(~67% at this lower bound, rising to ~87% across the de Jong 95% CI; `coverage_null_result.md`). So the documented dispersion of the MRSA colonization
endpoint is *not small* — sufficient to place the mean-based trend test in its degraded
regime — which is all the detectability argument requires. This σ is for MRSA
colonization overdispersion and licenses a statement about the **MRSA** endpoint only;
it is not an S. aureus σ.

(Fit: logit-normal binomial, marginal ML; regenerate with
`python -m src.analysis.dejong_sigma`.)
