# Coverage of the null — a mean-based endpoint cannot resolve MRSA clustering

The **MRSA** clustering instrument for the clustering frame (the methicillin-resistant
subset, not the S. aureus analytic unit — whose randomised signal is Luetkemeyer 2025,
HR 3.89). **Detectability, not effect estimation. No causal claim.**

MRSA carriage is modelled as `logit(p_visit) = a + b·visit + N(0, σ²)`: a true trend `b`
embedded in between-visit clustering of intensity `σ`. Counts are simulated at the
DOXYVAC doxy-PEP arm's ACTUAL per-visit denominators
(331, 304, 251, 193, 121) and scored with the naive
cross-sectional Cochran–Armitage trend test — the mean-based test a between-arm/level
reading implicitly relies on, which assumes binomial variance and is blind to
clustering. The trend `b = 0.37` logit/visit is anchored to the observed
1.8%→9.9% doxy-arm rise.

**σ=0 is a calibration check, by construction.** With no overdispersion the
Cochran–Armitage trend test is correctly sized: 5% false positives against
a nominal 5% (within Monte-Carlo error), and 96% power for the
observed-magnitude trend. The test is fair; what follows is its failure under clustering,
not a rigged null.

| clustering σ | power (real trend) | Type-I (flat process) | design effect |
|---|---|---|---|
| 0.00 *(calibration check)* | 96% | 5% | 1.0 |
| 0.25 | 92% | 9% | 4.0 |
| 0.50 | 84% | 22% | 13.0 |
| 0.75 | 79% | 35% | 28.0 |
| 1.00 | 76% | 48% | 49.0 |

**Empirically anchored — Type-I at the de Jong between-cohort σ̂** (`dejong_sigma_result.md`; MRSA colonization dispersion):

| σ (empirical) | power (real trend) | Type-I (flat process) |
|---|---|---|
| 1.74 — de Jong 95% CI lower | 81% | **67%** |
| 2.70 — de Jong σ̂ (point) | 86% | **78%** |
| 4.57 — de Jong 95% CI upper | 89% | **87%** |

**Read power and Type-I together — the test loses discrimination.** With no clustering
(σ=0) the test is fair. As σ grows, the false-positive rate climbs until the test rejects
almost regardless of whether a trend exists: at σ=0.5, Type-I is already
22%. At the empirically anchored σ̂ = 2.70 the flat-process
false-positive rate is **78%**, and even at the 95% CI lower bound
(σ = 1.74) it is **67%** — power
(86%) and Type-I (78%) are so close that a
"significant" cross-sectional trend carries almost no information about whether a real
trend exists. The mean-based endpoint cannot separate a real selection trend from the
clustering it is embedded in.

**The trials cannot rule this out with their own data — so the σ is external.**
Estimating σ from the observed DOXYVAC series gives σ̂ ≈ 0.00 (doxy arm) and 0.15 (no-PEP
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

(`SEED=20260820`; regenerate with `python -m src.analysis.coverage_null`.)
