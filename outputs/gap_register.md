# Gap register — Methods ↔ Introduction alignment (revised 2026-08-20)

Maps each intro research-question claim to its supporting repository artifact and a
status. Revised after the Contract-2 restructuring into two correctly-scoped instruments.

## Contracts

| contract | statement | status |
|---|---|---|
| **1 — detectability, not effect** | every deliverable reports what it would take to *detect* a signal, never an effect size | **discharged** — detectability.py (min-RR), dilution.py (RR_needed), coverage_null.py (power/Type-I), selection_ratchet.py (directional/one-sided), dejong_sigma.py (σ). No effect estimator anywhere. |
| **2 — analytic unit is doxy-R *S. aureus*, not MRSA** | MRSA is a coded subset only | **discharged (as of this restructuring)** — the S. aureus selection question now has its own S. aureus-scoped instrument (`selection_ratchet.py`); the MRSA analyses (`coverage_null`, `three_outbreak_fit`, `dejong_sigma`) are explicitly MRSA-scoped with the nesting stated in every output. Previously VIOLATED (the clustering pair ran on MRSA while positioned as organism-agnostic backing for the S. aureus claim). |
| **3 — externality / unmeasurability** | the mean-based systems cannot size the harm | **computed, and scope-bounded** — coverage_null + dejong_sigma show a mean-based, cross-sectional MRSA endpoint is in its degraded regime at the empirical σ. Language says the *instruments deployed* cannot resolve it, NOT that the harm is unmeasurable by any instrument. |

## Register

| # | intro claim (¶) | supporting artifact | scope | status |
|---|---|---|---|---|
| 1 | trials underpowered for S. aureus (¶4,¶6) | `detectability.py` → 0/4, min-RR 3.8–5.1 | S. aureus | discharged |
| 2 | measurement non-uniform (¶4,¶6) | `observations.saureus_measurement_heterogeneity` | S. aureus | discharged |
| 3 | reporting narrowed to MRSA subset (¶3,¶5,¶6) | coded observations (trial YAMLs) | S. aureus/MRSA | discharged (observational) |
| 4 | **stopped early / short duration (¶4,¶6)** | **`detectability.duration_table` → `duration_result.md`**: DoxyPEP needed **≈6× its realised colonised S. aureus sample at M12** (≈3.6× at M6; ≈40× for cross-org RR 1.42) for 80% power at RR 2.25; the SOC arm's early-efficacy closure truncated the binding (control-arm) accrual | S. aureus | **computed (sample-size basis; duration not inferable — see note)** |
| 5 | **doxy-R S. aureus accumulates under selection — the ratchet (¶4, §3.1)** | **`selection_ratchet.py`** → susceptible carriage 39→16→18% (decline p=1.6e-11); per-carrier doxy-R 11→41% (p=2.7e-07); resistant carriage 28 obs vs 7 neutral-expected (p=5.5e-09); SOC uninformative | **S. aureus** | **computed** |
| 6 | guidelines require no S. aureus monitoring (¶5,¶6) | `reliability.py` (10 coded) + **`streamb_denominator_reconciliation.md`** (de-Jong-anchored purposive denominator): **0 of 6 documented-outbreak jurisdictions require/suggest S. aureus monitoring**. Independence checked *within* the six from document content: **4 independently authored** (SF, Chicago, NYC, San Diego), 1 adapted from SF (LA County), 1 from an external fact-sheet template (MA); the 2 organism-naming independents (NYC "staph infections", San Diego "*Staphylococcus aureus*") name it in different registers — not a propagating template. A further 1 (Philadelphia) defers to CDC, not counted. | S. aureus | discharged (purposive denominator; independence and defer-to-CDC both enforced) |
| 7 | surveillance can't link exposure→phenotype (¶6, Stream C) | **re-anchored** — **`streamc_linkage.py`** over a closed universe of **12 established US surveillance systems**: **2 capture exposure only** (PrEP proxy, pop-denom), **0 capture S. aureus tetracycline phenotype at a pop-denom, 0 both, 0 linked**. Failure = **no phenotype-side population-denominator instrument**. Mechanism (cross-tier codified seam): the architecture is standardized around the **methicillin axis at every tier** — ABCs/EIP (pop-denom, invasive **MRSA**), NHSN AR/LabID (**MRSA**), facility antibiogram (**CLSI M39 mandates the MRSA/MSSA split** and makes tetracycline **suppressible**) — while S. aureus tetracycline resistance is orthogonal and falls through at each; NARMS excludes S. aureus. The Stream C analogue of the Stream A/B endpoint-substitution seam, here codified in a lab standard. Facility antibiogram recoded **right unit, non-standardized (M39), no denominator** (claim = inconsistency, not universal absence). Resolution mismatch: exposure county/metro, phenotype facility-only. Dilution leg (`dilution.py`/`dilution_metro.py`) **corrected 0/81→0/135**, kept as *support*, not the linkage denominator. Scope-bound: *deployed* systems, not impossible. | S. aureus (MRSA systems flagged wrong-unit) | discharged (denominator re-anchored convenience→principled; decomposed; methicillin-axis mechanism; scope-bound) |
| 8 | **MRSA is clustered/outbreak-pattern, not steady-state (¶4)** | **`dejong_sigma.py`** → between-cohort σ̂=2.70 (CI 1.74–4.57), prevalence 0–54% over 10 cohorts | **MRSA** | **computed** |
| 9 | **a mean-based cross-sectional MRSA endpoint cannot resolve that clustering (¶4,¶7)** | **`coverage_null.py`** → Type-I 78% at σ̂ (67% at lower CI); σ=0 calibrated by construction | **MRSA** | **computed** |
| 10 | the DOXYVAC MRSA rise is real but its shape/clustering unidentifiable from the trial alone (¶4) | `three_outbreak_fit.py` → doxy trend-vs-flat p<1/N_BOOT; wave-vs-trend p=0.43/0.15; DOXYVAC internal σ̂≈0 (3 df, unidentified) | MRSA | computed |
| 11 | analytic unit = S. aureus, MRSA a subset (Contract 2, ¶5) | all analyses scoped; MRSA outputs state the nesting | both | discharged |

## Per-task licenses (guard rails — what each analysis may and may not claim)

- **Task 1 (`selection_ratchet.py`) licenses:** "S. aureus susceptible carriage depletes
  consistent with selection, and the resistant fraction rises — the ratchet — in the
  doxy-PEP arm; the SOC arm is uninformative." **Not:** "we fit a monotonic model" (the
  tests are pre-specified and directional), and **not** any causal claim.
- **Task 2 (`dejong_sigma.py`) licenses:** "documented cross-cohort MRSA-colonization
  dispersion is large enough (lower CI σ=1.74) that the naive cross-sectional trend test
  sits in its degraded regime." **Not:** "σ = 2.70 is the transmission-clustering value"
  (σ̂ is an upper bound, inflated by methodological heterogeneity across cohorts), and this
  σ is **MRSA-only**, not an S. aureus σ.
- **Task 3 (`coverage_null.py`, `three_outbreak_fit.py`) licenses:** "the DOXYVAC MRSA
  rise is real but its shape and its clustering are unidentifiable from the trial alone,
  and a mean-based MRSA endpoint would be blind to clustering at the documented σ."
  **Not:** "the control arm shows a wave" (struck — a 0.8-AIC artifact), and **not** a
  claim about S. aureus.
- **Row 4 (`duration_table`) licenses:** "the trials would have needed ≈k× their realised
  *S. aureus* sample to power detection of the matched RR 2.25 (≈6× at M12), and the early
  efficacy stop foreclosed that accrual." **Not:** "a longer/larger trial would have found
  an effect" (no effect/causal claim), and duration is **not** inferred (the 2-point,
  declining retention schedule cannot support a defensible extrapolation — reported as
  sample-accrual foreclosure). **Scope:** S. aureus only; MRSA has no primary denominator
  and cannot enter this test.
- **Contract 3 scope:** the demonstration indicts *mean-based, cross-sectional* MRSA
  designs at these denominators — **not** measurement in principle. A time-resolved or
  network-resolved design could see what these cannot.

## Open / deferred

- Row 4 (duration/early-stopping) is now **computed** on a sample-accrual basis
  (`duration_result.md`). **Duration itself is not inferable** from the 2-point, declining
  retention schedule — reported as a sample-size multiple, not a follow-up-months claim.
  Intro flag: the "stopped early" language in ¶4/¶6 should be phrased as **sample-accrual
  foreclosure** (the trials would have needed ≈6× the S. aureus sample; the efficacy stop
  cut the control-arm accrual) rather than a duration/"longer trial" claim.
- Manuscript prose for the two new instruments is **held** pending PI check of the numbers
  above (σ̂ and the Type-I at σ̂), per the handoff instruction. The prior-turn Methods §2.3
  and Results §3.1 additions were **reverted** because they carried the Contract-2
  conflation this restructuring corrects.
- De Jong denominators: **sufficient** (10 cohorts with recoverable count+n ≥ the ~10
  threshold). One study dropped (Ikeuchi 2021, Tokyo — colonization/infection mixed, no
  clean count); infection-only studies excluded (no colonization denominator).
