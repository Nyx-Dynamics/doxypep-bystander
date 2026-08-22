# Stream A detectability — a design-based sensitivity analysis

**This is NOT post-hoc / observed power.** For each primary-trial *S. aureus* arm
comparison we compute, from the arm sizes and observed control rate alone, the
power to detect an effect size fixed A PRIORI from a source **external** to the
trials (Soge et al.), and the minimum detectable relative risk at 80% power. The
effect is not read off the trials' own results — that is what makes this a
design/sensitivity calculation, not observed power. Exact Fisher (per-arm counts
are single- to low-double-digit, where the normal approximation misleads).

**Benchmarks (both external; conclusion holds for either):**
- **RR = 2.25** — the *S. aureus*-MATCHED benchmark. Soge: tetracycline-
  resistant *S. aureus* colonization **18% vs 8% (P<.0001)** in doxy-PEP users vs
  non-users, RR ≈ 2.25. The defensible, same-organism number.
- **RR = 1.42** — Soge's gonococcal >3-doses/month figure; a **cross-organism**
  import, reported for continuity and flagged as such.

Result: **0 of 4** comparisons are powered (≥80%) to detect the
matched **RR 2.25**; **0 of 4** to detect the cross-organism
RR 1.42. Either way, none are.

| trial | timepoint | basis | doxy | control | p_ctrl | min detectable RR (80%) | power@2.25 | power@1.42 |
|---|---|---|---|---|---|---|---|---|
| doxypep_us | month6 | colonized_participants | 11/51 | 3/29 | 10% | 3.80 | 24% | 6% |
| doxypep_us | month6 | all_participants_swabbed | 11/192 | 3/75 | 4% | 3.95 | 23% | 5% |
| doxypep_us | month12 | colonized_participants | 5/31 | 2/24 | 8% | 4.95 | 11% | 3% |
| doxypep_us | month12 | all_participants_swabbed | 5/111 | 2/51 | 4% | 5.05 | 10% | 2% |

Every cell's minimum detectable RR (**3.8–5.1**) sits above **both** the matched
2.25 and the cross-organism 1.42 — so the 2023 interim CROSS-SECTIONAL
comparisons were underpowered for the prespecified resistance benchmarks. This explains why
the interim presentation read as non-informative; it does NOT apply to the 2025
participant-level time-to-event analysis (Luetkemeyer 2025), which detected the signal
(incident doxy-R *S. aureus*, HR 3.89, 95% CI 1.42-10.68). The Stream A point is that the
interim cross-sectional estimand was inadequate to a signal the incidence estimand later
resolved — not that the trial could never support inference.

Methods language to carry into the manuscript verbatim: *"a design-based
sensitivity analysis (not observed power): the minimum detectable effect and the
power to detect an externally specified relative risk, with the benchmark drawn
from a source independent of the trials assessed."*

## MRSA — no primary-trial denominator

Primary-trial MRSA observations: **0**. NEJM
reports no methicillin breakdown; the only MRSA numbers are a secondary synthesis
(Szondy) / the CROI abstract, and the DOXYVAC MRSA carriage sits in the main trial
+ a reanalysis (Vanbaelen 2024c). Detectability for MRSA cannot be computed from
primary data — a finding, not a gap.
