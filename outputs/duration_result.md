# Stream A duration / sample-accrual — closing the "stopped early" claim

A **design-based sensitivity analysis** (not observed power), extending
`detectability_result.md`. For each primary-trial *S. aureus* comparison we solve for
the sample the design would have needed to reach 80% power against an **external**
benchmark (Soge et al.), and report the multiple over what the trial actually realised.
**Benchmark held at the matched RR = 2.25** (tetracycline-resistant *S. aureus*,
same organism, same source `detectability.py` uses); the cross-organism RR = 1.42
(gonococcal) is a **secondary** column, flagged. Required N uses the large-sample normal
approximation (valid where the required N lands — hundreds to thousands per arm); the
realised-denominator detectability in the companion report stays exact Fisher because
those counts are tiny. *S. aureus* unit throughout.

| comparison | basis | realised doxy/ctrl | p_ctrl | need doxy/ctrl @2.25 | **multiple @2.25** | multiple @1.42 (cross-org) | exact-Fisher check |
|---|---|---|---|---|---|---|---|
| doxypep_us month6 | colonized_participants | 11/51 · 3/29 | 10% | 185/105 | **3.6×** | 25× | 79% @ solved N |
| doxypep_us month6 | all_participants_swabbed | 11/192 · 3/75 | 4% | 715/279 | **3.7×** | 24× | N too large (approx) |
| doxypep_us month12 | colonized_participants | 5/31 · 2/24 | 8% | 196/152 | **6.3×** | 43× | 79% @ solved N |
| doxypep_us month12 | all_participants_swabbed | 5/111 · 2/51 | 4% | 647/297 | **5.8×** | 38× | N too large (approx) |

**The sample-size verdict.** At the twelve-month endpoint the trials headline, DoxyPEP
would have needed **≈6× its realised colonised *S. aureus* sample** to reach 80%
power for the matched RR 2.25 (≈43× for the cross-organism RR 1.42);
at six months, ≈3.6×. Across bases and timepoints the multiple never falls below
~3.6×. The exact-Fisher spot-check confirms the solved denominators deliver ~80%,
validating the approximation. These are lower bounds on what detection would have taken:
the realised sample is a small fraction of it.

**Duration is not inferable from the available schedule — stated, not fabricated.** The
*S. aureus* accrual has only two arm-split timepoints (month 6 and month 12), and the
per-visit denominators **decline** over follow-up (DoxyPEP colonised doxy arm 51 → 31;
all-swabbed 192 → 111) as retention drops. A declining two-point curve cannot support a
defensible extrapolation to the follow-up duration at which cumulative observations would
reach the required N — and because the swabs are repeated on a shrinking cohort, pooling
across visits would not accrue independent observations in any case. We therefore report
the **sample-accrual** result and do **not** infer a duration. Running longer at the
realised accrual would not have closed a ~6× gap; a larger enrolled cohort would have.

**The early efficacy stop is why the realised denominator is what it is.** DoxyPEP's
standard-of-care arm was closed at the 5/2022 DSMB efficacy interim (data through
5/13/2022 for SOC vs 12/1/2022 for doxy-PEP), truncating exactly the **control-arm**
*S. aureus* accrual — the smaller arm, which is the binding constraint on every
comparison above (control colonised n = 29 at M6, 24 at M12). DOXYVAC was likewise
DSMB-stopped for STI efficacy at ~9-month median follow-up, but
it measured only MRSA carriage and so has **no primary *S. aureus* denominator** — it
cannot be brought to this test at all (MRSA note below). In both pivotal trials the
primary STI-efficacy endpoint was met and the trial closed before the bystander endpoint
could accrue the sample its own design would have required.

**License.** The trials would have needed ≈6× their realised *S. aureus* sample
to power detection of the matched RR 2.25, and the early efficacy stop foreclosed
that accrual. This is design-based sensitivity against an external benchmark — **not** a
claim that a larger or longer trial *would have found* an effect, and **not** any
statement that the effect exists.

## MRSA — cannot be brought to this test

Primary-trial MRSA observations: **0**. MRSA has no
primary-trial *S. aureus*-style denominator (NEJM reports no methicillin breakdown;
DOXYVAC's MRSA carriage is the main trial + a reanalysis). The duration/sample-accrual
computation is *S. aureus*-only, as the detectability computation is — a finding, not a
gap.
