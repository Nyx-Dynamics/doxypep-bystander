# DECISIONS.md

Dated analysis decisions, logged before results are known. Append-only.

## 2026-08-19 — NEJM Appendix + Protocol + Data-Sharing obtained

Four DoxyPEP source files ingested and hashed (appendix, protocol, data-sharing,
main text; papers/CHECKSUMS.md, all coded-source). Schema extended with two OPTIONAL
CodedFields on TrialRecord (`data_availability`, `resistance_endpoint_switched`);
optional so DuDHS/DOXYVAC are unaffected; +3 tests (26 pass). PI review 2026-08-19
tightened the framing below — kept only what the documents support verbatim.

- **Finding 1 — data withheld (the unassailable spine).** The Data Sharing Statement
  (posted 2023-04-06) answers "Will the data collected for your study be made
  available to others?" with **No**, every downstream field an em-dash. Coded
  `data_availability = no`. The evidentiary-adequacy floor: the S. aureus
  discrepancies cannot be adjudicated by re-analysis because the data is withheld.
  This finding stands alone and does not depend on Finding 2.
- **Finding 2 — internal inconsistency + pre-specification deviation (NOT
  concealment).** Two adjacent NEJM sentences on **p.1298** disagree: End Points
  names the PRIMARY AMR outcome for S. aureus as **tetracycline** resistance; Trial
  Procedures describes a **doxycycline** assay. Protocol pre-specified tetracycline
  (L253/258/280/498/527); results + Appendix Table 2 report doxycycline; no
  tetracycline-S.-aureus number is published anywhere in NEJM. Coded
  `resistance_endpoint_switched = yes`. **Direction correction (PI):** tetracycline is
  the BROADER surrogate (tet(K) = tetracycline-R but doxycycline-S; Grossman 2016), so
  doxycycline is the MORE CONSERVATIVE, more specific measure — it reports LESS
  resistance and is arguably the better assay. So this is a transparency problem (a
  declared primary endpoint replaced, unreconciled, data withheld), NOT evidence of
  hiding a tet(K) signal; the pharmacology runs the other way. The gonococcal endpoint
  was NOT switched (Appendix Table 1 keeps tetracycline). Appendix Table 2 Total
  column CONFIRMS the earlier Fig-4B reading exactly (mo6 11/51 & 3/29; mo12 5/31 &
  2/24). Earlier "NEJM Methods agree (tetracycline)" was wrong and is retracted — the
  methods assay sentence says doxycycline; the two NEJM sentences are quoted adjacent
  in the YAML, not smoothed into agreement.
- **CDC/NEJM discrepancy — narrowed, not resolved.** Prior status UNRESOLVED. Now:
  NEJM publishes no tetracycline-S.-aureus number, so CDC's "tetracycline-resistant
  S. aureus" REFLECTS the pre-specified tetracycline phenotype NEJM left unpublished
  and cannot map onto any NEJM table — hence not a CDC error against NEJM. It is NOT
  yet "resolved": to say the 20/428 figure IS the CROI number, we must see it in the
  CROI 2023 abstract (not in hand). Exact source + the 428/222 denominator remain
  PENDING that abstract. CDC observation notes say exactly this; do NOT assert error.

## 2026-08-18 — AIDSVu suppression sentinels are multi-valued, not just `-1`

CLAUDE.md/SCAFFOLD.md documented `-1` as the suppressed code. Inspection of all
28 state PrEP + PnR workbooks (2012–2025) found **four** distinct negative
sentinels in the measure columns: `-1` (548×), `-2` (282×), `-8` (458×),
`-9` (625×). Rates, counts and PrEP-to-Need ratios are never legitimately
negative.

**Decision:** the loader treats *any* negative value in a measure column as
suppressed → `NaN` (never `0`), rather than enumerating the four codes. Robust
to all observed sentinels and to any AIDSVu adds later. If a future measure
column can legitimately be negative, this rule must be revisited.

## 2026-08-18 — Embedded newlines live in data values, not only headers

The PrEP workbooks carry embedded newlines inside *state name cells*
(`'New\nHampshire'`, `'Washington,\nD.C.'`); the PnR workbooks do not. An early
loader normalised only column headers, so those two states failed to join
across the two sources and the outer merge produced 54 phantom geographies
instead of 52.

**Decision:** normalise embedded newlines/whitespace in text *values* (state,
abbreviation) as well as headers, before joining. Regression-tested.

## 2026-08-18 — Geography set

Each file carries 52 geographies: 50 states + DC + Puerto Rico. Kept all 52 for
now; whether territories enter the panel is a Phase 2 decision to be logged when
the exposure contrast (high- vs low-PrEP-density) is defined.

## 2026-08-18 — Phase 0 gate: parameter choices (logged before the result)

Choices for `src/feasibility/dilution.py`, made before running:

- **Exposure proxy = male PrEP users**, not overall PrEP users. doxy-PEP is
  recommended for MSM/trans women, not cis women (CLAUDE.md constraint 5). Added
  `male_prep_users` to the loader for this. The MSM population fraction is *not*
  a separate input: the observed male PrEP-user count already counts the
  reachable exposed population directly, superseding a modelled MSM share.
- **Population denominator backed out of AIDSVu** as `prep_users / prep_rate *
  1e5` rather than importing a Census figure. This recovers AIDSVu's own adult
  denominator (internally consistent with the numerator) and avoids fabricating
  50+ state populations from memory. CA back-out ≈ 33.1M (adult 13+), sensible.
- **Baseline tetR R0 grid = {0.05, 0.10, 0.13}**, central 0.10. 0.13 is the
  tetracycline-resistant fraction observed in a doxy-PEP-eligible population
  (CLAUDE.md constraint 2); community S. aureus tetR is lower.
- **Isolate volume N grid = {1k, 10k, 100k}/state-year.** ATLAS is unacquired
  (Phase 1). N is bounded *generously high* on purpose so a failed gate does not
  hinge on the true N — 100k/state-year exceeds any real US surveillance stream.
- **Enrichment kappa = {1, 3, 5}.** kappa=1 is proportional sampling; up to 5x
  allows the exposed to be over-represented among sampled isolates.
- **Within-exposed RR = 1.42** (Soge, >3 doses/month) as the optimistic ceiling.
- **MDE** via two-proportion normal approx, alpha 0.05 two-sided, power 0.80.

## 2026-08-18 — Phase 0 RESULT: state-level design killed, pivot to metro

Gate FAILED: 0 of 81 grid cells detectable. Best-case (most generous) cell is
Washington D.C. at uptake 55%, 5x enrichment, N=100k, R0=13% → RR_needed = 1.93,
still above Soge's 1.42. Realistic cell (kappa=1, uptake 35%, R0=10%, N=1k) →
RR_needed ≈ 86 (~60x Soge). Median across cells ≈ 14.

**Decision:** abandon the state-level ecological design as primary; pivot to
metro-level (SF, King County, LA, NYC) per SCAFFOLD.md. That the single best
"state" is the city-state D.C. corroborates the direction of the pivot. The
metro design needs its own Phase 0 check (metro population denominators, metro
isolate volumes) before any outcome data is acquired — the state kill does not
transfer. Full write-up: `outputs/feasibility_result.md`.

## 2026-08-18 — Metro Phase 0: also fails; dilution is population-scale, not state-scale

No metro/county PrEP *user or rate* file is on disk — the AIDSVu metro
downloadable datasets (Prevention-Theorem project) carry HIV prevalence/SDOH by
ZIP, not PrEP; County PnR 2019 has only ratios and is suppressed for the target
counties; SF and King County are not even among the 34 available metro files.

Rather than fabricate metro densities, exploited the fact that the dilution
fraction is **population-independent** — `f = MALE_FRACTION * (male_prep_rate/1e5)
* uptake * kappa` (eq. 5). So the gate inverts to a required male-PrEP *density*
and compares it to the densest geography that actually exists in AIDSVu:
**Washington, D.C. at 2,694/100k adult males (2022)** — a city-state, a generous
empirical ceiling for any US metro (SF/King do not exceed it).

- **MALE_FRACTION = 0.5**: adult-male share of the isolate-generating population.
  Justified by AIDSVu internal consistency (male_prep_users/male_prep_rate*1e5 ≈
  adult-male population; over total adult pop ≈ 0.49).
- **ACHIEVABLE_MULTIPLE = 2.0**: a real metro may be at most 2x the densest
  observed US geography. Generous — no US metro is known to exceed D.C.

**Result:** 0 of 81 cells achievable. Least-demanding cell needs 2.1x D.C.'s
density and only under fantastical inputs (N=100k isolates/yr, 5x enrichment, 55%
uptake); realistic cells need 12–33x+ (i.e. >100% of males on PrEP, impossible).

**Decision / interpretation:** the ecological design fails at *both* state and
metro grain because population-scale sampling dilutes the signal below
detectability wherever a population denominator exists. The only lever that
rescues it is enrichment (kappa) — i.e. **targeted sexual-health-clinic sampling**
of *S. aureus* from the exposed population — a cohort design, not ecological.
This is the measurement-inheritance thesis made quantitative. Two forward paths
recorded in `outputs/feasibility_metro_result.md`: (1) a King County / SF clinic
cohort study (different design, own preregistration), or (2) write this two-level
negative result up as the surveillance-infrastructure paper. Choice deferred to PI.

## 2026-08-18 — Metro result HARDENED: robustness sweep + proxy-free break-even

Before writing anything up, hardened the metro negative result so it does not
rest on the D.C. proxy or on any single fixed assumption. Added to
`dilution_metro.py`: `robustness_sweep()` and `breakeven_frontier()`.

- **Assumption sweep** — male fraction {0.4,0.5,0.6} x achievable ceiling
  {1,2,3,5}x D.C., over the full R0xNxkappa x uptake grid. Result (logged before
  claiming invariance, then corrected against the data): at any *realistic* metro
  density (<= 2x the densest US geography) with male fraction <= 0.5, **0 of 81**
  cells are achievable. Cells open ONLY under a compound implausibility — a metro
  3-5x denser than any US geography that exists AND N=100k isolates/geography-year
  AND kappa >= 3 — at most 11/81 even then, and every such cell's high kappa is
  targeted clinic sampling (a cohort design, not the ecological one under test).
  NB: an initial test asserting "0 across ALL swept assumptions" was FALSE and was
  corrected; the honest invariant is "0 at realistic ceilings," which is stronger
  rhetorically because overturning it requires stacking implausibilities.
- **Break-even in proxy-free units** — the male-PrEP coverage (as % of ALL adult
  males) required to flip the gate. Realistic (N=1k, kappa=1): 325% — impossible.
  Fantastical best case (N=100k, kappa=5): 6.5% — still ~2.4x D.C.'s 2.7% and far
  above any real metro (MSM are single-digit % of men; PrEP covers a fraction).
  This unit needs no metro-specific datapoint to be recognised as unreachable.

Track B (real county PrEP density for SF/King/LA/NYC) confirmed out of reach: no
such file on disk (metro AIDSVu files are HIV/SDOH; County PnR 2019 suppressed for
these counties; SF/King not in the metro set). Would need a fresh AIDSVu download
or health-department outreach. Documented as a limitation, not silently skipped.

## 2026-08-18 — Phase A: panel-power bound for Stream C (choice logged BEFORE running)

The Stream C MDE assumes a single two-proportion comparison, but the design under
test was a controlled panel (~52 geographies x ~14 years). A referee's first
objection: panel power could lift RR_needed toward Soge's 1.42. SCAFFOLD Phase A
offers "extend the MDE OR state the compound implausibility." **Choice: do both.**

- **Extend the MDE** with a transparent effective-sample-size bound,
  `N_eff = G * T * N / DEFF`, sweeping the design effect DEFF in {1, 5, 10, 25}.
  DEFF=1 treats every geography-year isolate as an independent draw — an
  *optimistic ceiling* on panel power (ignores within-geography autocorrelation),
  chosen deliberately: if realistic cells stay undetectable even here, the kill is
  robust. The dilution fraction f is unchanged (the panel adds observations, it
  does not concentrate exposure); only the MDE shrinks.
- **Retain the compound-implausibility statement** for the best-case cell.

**Expected direction, logged before computing (so the check is honest):** panel
aggregation will *lower* RR_needed (raise detectability). Prediction:
  (a) realistic cells (single-comparison RR_needed ~14-86) remain > 1.42 across
      the whole DEFF range, so the qualitative kill holds; and
  (b) the best-case cell (single RR_needed 1.93, already a compound of four
      implausibilities) will fall *below* 1.42 under optimistic DEFF — confirming
      it must not be relied upon, only disclosed as fragile.
If instead (a) fails — realistic cells drop below ~1.42 — the quantitative claim
needs restating (this is one of the falsification conditions in CLAUDE.md).

## 2026-08-18 — Phase A RESULT: prediction confirmed; Stream C headline retired

Both pre-registered predictions held (see `outputs/tables/feasibility_panel_power.csv`):

- **(a) holds.** Realistic cell (kappa=1, R0 10%, N=1000, uptake 35%) RR_needed =
  **4.15** at optimistic DEFF=1, rising to **16.8** at DEFF=25 — above Soge's 1.42
  across the entire design-effect range. The qualitative kill survives for
  realistic surveillance conditions.
- **(b) holds.** Best cell RR_needed falls to **1.03** at DEFF=1 (from 1.93
  single-comparison) — below 1.42. The best case is disowned, not cited as "close."

**Consequence — narrative correction.** Under a panel, the grid median RR_needed
collapses from 14 to **1.48** and 38/81 cells become nominally detectable at DEFF=1.
The old "0 of 81, median ~14" headline was a single-two-proportion artifact and is
**retired**. The Stream C claim is re-anchored on the realistic cell: *under
realistic surveillance conditions the signal is undetectable even by a controlled
panel (RR_needed 4-17x the observed effect); detection requires a compound of
generous assumptions that fail individually.* This makes Phase A items 2 (kappa<1)
and 3 (dose distribution) **load-bearing** — both push the realistic cell further
from 1.42 — rather than optional.

Two downstream docs now contain superseded numbers, to fix when reframing to the
three-streams paper: (i) `README.md` and `paper/manuscript.*` lead with "median
14 / 0-of-81" — reframe to the realistic-cell claim; (ii) the revised `CLAUDE.md`
summarises metro as "2.1x-33x" — the full-table range is 2.1x to ~480x (the 33x
was an early figure-slice number; even the N=100k slice maxes at 48x).

## 2026-08-18 — Phase A items 2+3: kappa<1 and dose distribution (logged BEFORE running)

Two refinements to the dilution model, both of which the current model omits in the
generous direction. Choices:

- **Item 2 — kappa < 1.** Extend KAPPA_GRID from {1,3,5} to {0.2,0.5,1,3,5}.
  Surveillance *S. aureus* skews hospitalized/older; doxy-PEP-exposed MSM are young
  and outpatient, so they are *under*-represented in a population isolate stream.
  kappa=1 (proportional) is generous, not neutral. The **realistic cell** moves from
  kappa=1 to **kappa=0.5** (moderate under-sampling; kappa=0.2 kept as a plausible
  more-extreme point). The value is illustrative — the argument is directional, not
  a precise kappa — so it is swept, not asserted.
- **Item 3 — dose distribution.** Soge's RR 1.42 attaches to >3 doses/month; median
  use is 3 (IQR 2-6), so ~half of doxy-PEP users sit below the threshold at which any
  effect was seen (any use: RR 1.14, ~null). Introduce
  `DOSE_ABOVE_THRESHOLD = 0.5` and scale effective exposure by it, so the isolate
  fraction carrying the benchmarkable RR-1.42 effect is the >3-doses/month subgroup
  only. This keeps the yardstick (RR_needed vs 1.42) internally consistent and is
  exactly the un-doing of the binary exposure coding the paper criticises.

**Expected direction, logged before computing:** both refinements *reduce* effective
f (kappa<1 and dose<1), so RR_needed *rises* — more undetectable. Prediction:
  (a) the realistic cell (now kappa=0.5, dose 0.5; f cut ~4x vs old kappa=1) rises
      from 4.15 to ~13-14 at optimistic panel DEFF=1, restoring a comfortable margin
      over 1.42 that the panel correction had thinned; and
  (b) the best case (kappa=5, N=100k) stays below 1.42 under optimistic panel power
      even after dose halving (1.03 -> ~1.06), so it remains disowned.
Both refinements applied model-wide (state, panel, metro). If instead the realistic
cell does NOT rise, a modelling error is implied — investigate before trusting.

## 2026-08-18 — Phase A items 2+3 RESULT: prediction confirmed; realistic margin restored

Applied kappa<1 (KAPPA_GRID {0.2,0.5,1,3,5}, realistic cell now kappa=0.5) and
DOSE_ABOVE_THRESHOLD=0.5, model-wide. Both predictions held:

- **(a) confirmed.** Realistic-cell RR_needed under the panel rose from 4.15 to
  **13.6** at optimistic DEFF=1, and to **64** at DEFF=25 — a comfortable margin
  over 1.42 restored across the whole design-effect range (was 4-17x, now 14-64x).
- **(b) confirmed.** Best case stays below 1.42 under optimistic panel power (1.03
  -> 1.07 after dose halving); still disowned.
- Single-comparison best case 1.93 -> **2.87** (dose halving). Metro least-demanding
  cell 2.1x -> **4.2x** D.C.; break-even realistic 325% -> **651%** of all adult
  males, fantastical best 6.5% -> **13.0%**. All move in the predicted (more
  undetectable) direction.

Net: the panel correction (which had thinned the realistic margin to ~4x) is more
than offset by the two refinements; the Stream C claim now rests on the realistic
cell at 14-64x the observed effect, robust to design effect. Grid size 81 -> 135
(5 kappa values). All outputs regenerated; 28 tests pass. `outputs/*.md` prose that
hard-coded "kappa=1 / proportional sampling" corrected to the kappa=0.5 realistic
framing. Phase A complete.

## 2026-08-18 — Phase B: Stream B guideline coding + gate result

Built the coding harness (`src/coding/schema.py` pydantic locator-or-raise;
`build_corpus.py`) and CODEBOOK.md. Locator is mandatory and non-empty; a record
missing one raises at load, never nulls (tested first). Coded all six guideline
units from the source PDFs — CDC, Australia, Germany DSTIG, ECDC, IUSTI Europe, SF
provider guide — each field with a page/section locator and a verbatim quote, read
from the PDFs directly (not from CLAUDE.md's summary, per CODEBOOK instruction).

**Coder = `claude-firstpass`.** This is a machine first pass; it needs PI
verification and 20% human double-coding (Phase F reliability) before it is
citable. Recorded honestly rather than attributed to the PI.

**GATE CLEAR: 0 of 6 units require S. aureus/MRSA monitoring.** The "no system
requires measurement" framing holds. Reported near-misses (not hidden): Australia
Rec 5 (develop guidance on whether/how to monitor bystander-organism AMR) and
IUSTI (off-target AMR monitoring as a service-framework principle) — both
system-level and non-staph-specific, neither a clinical staph-monitoring mandate.

**CDC grading asymmetry confirmed at locators:** efficacy graded (p. 7, AI /
high-quality / strong) vs harms "Evidence was not graded" (p. 4), same Methods
section — the only formally graded unit; the other five are consensus/position/
considerations documents (na/na). Coding judgement calls logged in each YAML's
`note`. Result: `outputs/guidelines_result.md`.

## 2026-08-18 — Phase C: DoxyPEP coded (PI reconciliation seeded it)

Coded `data/raw/coding/trial_doxypep.yaml` (20 resistance observations, one per
reported instance) + `src/coding/build_trials.py`. Findings, all auto-surfaced:

- **Denominator discordance** at month-12 doxy S. aureus: {31 colonized, 111
  all-swabbed, 222 CDC-unclear}; the rate moves 3.6x on basis choice alone.
- **The PI's sharper reframe holds in the coding.** Szondy (meta-analysis)
  RECONCILES to NEJM exactly (doxy follow-up MSSA 15/71 + MRSA 1/11 = 16/82 =
  NEJM mo6+12 pooled; control 5/53; baseline 25/214~25/215). CDC's 20/428 ->
  28/222 reconciles to NEITHER numerator nor denominator of NEJM. The guideline
  driving national practice is the non-reconciling source; recorded via
  description_denominator_mismatch + basis 'unclear'.
- **Relabeling (10):** NEJM measured DOXYCYCLINE (ETEST MIC>=16); both Szondy
  ('TCN resistance') and CDC ('tetracycline') relabel it. Numbers reconcile for
  Szondy, not CDC.
- **MRSA has 0 primary-trial denominators** — NEJM has no methicillin split; the
  1/11, 2/6 MRSA pair CDC leans on ('MRSA did not differ') traces to the CROI 2023
  abstract (via Szondy), not the primary publication. A finding, not a gap.
- Gate CLEAR: no power calculation stated for the resistance endpoint.

Judgment calls flagged for PI:
- **Assay-descriptor fields** (body_site, susceptibility_method, breakpoint_*) are
  typed `CodedField` whose value is yes/no/partial/na; free-text descriptors have
  no home in `.value`. Coded value='yes'/'partial' with the verbatim in `quote`.
  If free-text descriptors were intended, the schema needs a text field type.
- **DoxyPEP gonococcus not coded.** Its endpoint is MIC>=2 (NEJM Fig 4A labels
  this 'high-level'; conventionally high-level gonococcal tetR = tetM plasmid at
  >=16). Whether MIC>=2 is mechanism-discriminating is ambiguous, so DoxyPEP is
  left S. aureus-only. Consequence: `blindness_asymmetry()` (within-trial) does not
  fire for DoxyPEP. The real asymmetry is CROSS-trial (gonococcus trials —
  Soge/DOXYVAC — use discriminating methods; S. aureus is measured blind), which
  the within-trial function cannot capture. Worth a schema/analysis note.

## 2026-08-19 — Stream B SCOPE DECISION + schema v2 (logged before coding)

Per STREAM_B_HANDOFF.md (PI), Stream B is re-scoped and re-schema'd. This
SUPERSEDES the v1 5-field guideline coding.

**Scope: governmental public-health authorities only** (city/county/state/
national). These bodies both set doxy-PEP policy AND hold the local surveillance/
outbreak record — the pairing that makes the institutional-memory comparison
meaningful. **Excluded:** FQHCs / community health centers / clinic patient-
education (Howard Brown), and professional societies (German DSTIG, IUSTI). This
is a scope decision, not a finding; excluded docs retained in
`data/raw/guidelines/excluded/` with reasons. ECDC left pending a PI call
(EU agency but a considerations doc, not a jurisdictional policy).

**Thesis (refined):** the asymmetry is WITHIN a single artifact — S. aureus
discussed/counselled/unmeasured while in-category organisms (GC/CT/syphilis) are
resolved with lab precision in the same document.

**Schema v2** (`src/coding/schema_guideline.py`): richer field set (jurisdiction,
issuing_body, document_type, bystander_treatment, s_aureus_location,
in_category_monitoring, s_aureus_monitoring, host_toxicity_labs, derived_from,
local_mrsa_msm_literature + literature_search_provenance,
same_institution_authored_both, counselling_language_verbatim), same
locator-or-raise contract, with guards encoding the thesis (explicitly_none needs
a verbatim quote; a null local-literature cell needs search provenance; silent
needs a full-document-reviewed note).

**v1 retirement:** the v1 records (`guideline_*.yaml`, 5-field), `build_corpus.py`,
and the GuidelineRecord in `schema.py` are superseded. v1 coded Germany/ECDC/IUSTI,
now out of scope. v2 records use the `gl_*.yaml` pattern and `build_guidelines.py`.
CodedField is shared and unchanged.

**Uploaded/ingested (2026-08-19):** LA County factsheet, San Diego CAHAN, NYC
DOHMH dear-colleague, Chicago CDPH protocol -> guidelines/. Yeung 2019 JAAD
(institutional-memory anchor) -> papers/. NB: Chicago PDF in hand is 7 pp, not the
15 pp the handoff exemplar cites — will code the PDF and flag the discrepancy.

## 2026-08-19 — Stream B: thin-pointer state pages + a recurring governance split

Ingested but NOT coded: `guideline_ri_doh_page_2026.pdf` (Rhode Island Dept of
Health). In scope (state governmental authority) but the doxy-PEP page is a
one-line pointer ("Learn more about Doxy-PEP…") with no codeable guidance —
no monitoring, counselling, or bystander content. Coding an empty stub would pad
the corpus and misrepresent; flagged for retrieval of the substantive page it
links to instead.

**Recurring governance split (worth a paper line):** the substantive doxy-PEP
clinical guidance in several jurisdictions sits at a level/institution *outside*
the coded governmental corpus, while the governmental page is thin:
- Baltimore → Maryland: MD state factsheet (silent on staph); the S. aureus
  reservoir was documented at the Baltimore CITY health dept clinic (Miko 2012).
- Rhode Island: RI DOH page is a pointer; the substantive clinical guidance /
  authorship (Mishriky & Chan CID viewpoint) lives at Open Door Health / RI PHI —
  a nonprofit clinic, excluded from the governmental corpus by scope.
The bystander falls between governance layers. Not a coding decision — an
institutional-memory observation to develop in the write-up.

Excluded this batch: ASHA (national nonprofit education org).

## 2026-08-19 — Correction (PI): RI DPH <-> Open Door is a COLLABORATION, not a split

Amends the prior "governance split" note for Rhode Island. RI DOH and Open Door
Health are collaborators (co-produce the doxy-PEP guidance), so they cannot be
cleanly untangled — Open Door effectively co-constitutes RI's substantive
guidance rather than merely relaying it. Decision confirmed: NO clinic-relay tier.
The Baltimore->Maryland case remains a genuine level split (city surveillance vs
state policy); RI is a collaboration and is treated as a single entangled unit.

## 2026-08-19 — Stream A rigor: CDC discrepancy (high-scrutiny) + Szondy relabelled

**CDC S. aureus figures = UNRESOLVED, not a finding.** CDC MMWR prints tetR
S. aureus 20/428 -> 28/222 (doxy arm). These do not obviously map onto the NEJM
Fig 4B figure, but that is NOT coded as a reconciliation failure: benign
explanations are live — (i) CDC frames a 12-month follow-up window whose
denominator need not equal the NEJM figure's; (ii) CDC cites BOTH the NEJM paper
and a CROI 2023 abstract, so the numbers may be CROI-sourced; (iii) swab-count vs
participant-count. Actions before ANY manuscript use: establish the exact analysis
population behind 428/222; check CROI-vs-NEJM provenance (NEJM Supplementary
Appendix + the CROI abstract). CDC `phenotype_measured` set to `not_stated` (assay
unknown), which also de-couples CDC from the NEJM discordance grouping — so the
analysis no longer *asserts* a CDC reconciliation failure. The robust finding is
narrower and stands: NEJM's OWN basis choice (colonized 31 vs all-swabbed 111)
moves the month-12 headline 3.6x. An unreconciled-numbers claim against CDC would
draw the sharpest review scrutiny; being wrong there costs the rest of the paper.

**Szondy re-tagged `secondary_synthesis` (was `meta_analysis`).** Verified: Szondy
2024 (IJID; Semmelweis) is "a systematic review and meta-analysis of randomized
[trials]". Its Table 2 S. aureus rows are pooled EXTRACTION of the DoxyPEP/CROI
data — a second reading of the same underlying data, not an independent
observation. It reconciles to NEJM by construction, so it is a reconciliation
CHECK, not corroboration, and (like every non-primary source) is excluded from
detectability inputs. Added `secondary_synthesis` to the SourceType enum. Trial
count stays 1 (Szondy was never a separate TrialRecord).

## 2026-08-19 — Stream B reliability (double-coding) + sampling frame

**Sampling frame** written to `METHODS_streamB.md`: NCSD "Doxy and STI PEP Sample
Policies" compilation + WHO/CDC/Australia/BASHH, filtered to governmental
authorities; exclusions (FQHCs, patient-navigation, nonprofit/advocacy,
professional societies, advocacy comments) with reasons; dated retrieval log
including Seattle-King County's broken landing page and the not-yet-retrieved
jurisdictions.

**Inter-coder reliability** (`outputs/reliability_result.md`,
`src/analysis/reliability.py`): an INDEPENDENT blind second coding
(`claude-independent-2nd-pass`, coded from the PDFs + codebook only, not shown the
first pass) of a 5-document sample spanning all s_aureus_location categories.
**Overall agreement 92% (23/25).** Per field: s_aureus_named, s_aureus_location,
host_toxicity_labs all 100% (kappa 1.0 — the key 'where does the bystander appear'
field is perfectly reliable, incl. reference_title_only); bystander_treatment 80%;
s_aureus_monitoring 80% (kappa unstable at small N). Two disagreements, both
codebook edge-cases (not errors), resolved with binding rules in CODEBOOK.md:
(1) blanket 'no monitoring needed' -> explicitly_none [NYC flagged for PI];
(2) reference-title-only naming does not make bystander_treatment organism_named
[Philadelphia/WHO]. Schema is now tested, not assumed, before Stream A.

## 2026-08-19 — Stream A written: DuDHS + DOXYVAC coded, detectability computed

Three primaries now coded (DoxyPEP, DuDHS, DOXYVAC) — Szondy reclassified as
secondary_synthesis, so the trial count is 3.

- **DuDHS** (Grennan, doxy-PrEP feasibility RCT, n=52): S. aureus by DISK DIFFUSION
  (mechanism-blind); only 9 carriers; 6 emergent doxycycline-resistant (5 immediate
  vs 1 deferred, P=.077) — a real-looking split the trial cannot resolve.
- **DOXYVAC** (Molina/ANRS 174): the AMR substudy (ciaf591) measured GONOCOCCUS
  with the full apparatus — WGS + tetM PCR (mechanism-DISCRIMINATING): high-level
  tetR 11/31 (doxy) vs 5/40 (no-PEP), P=.043. S. aureus measured only as MRSA
  throat carriage in the main trial; conclusion_contested=yes (Vanbaelen 2024c
  population-selection reanalysis, MRSA 2%->12% doxy vs 2%->10% control).
- **Mechanism asymmetry is CROSS-trial** (confirmed): in-category gonococcus gets
  tetM PCR/WGS; bystander S. aureus gets standard breakpoint / disc diffusion — in
  different trials, so within-trial blindness_asymmetry() is empty. Added
  cross_trial_blindness().
- **detectability.py** (exact Fisher power, per basis): 0 of 4 primary S. aureus
  arm comparisons are powered to detect Soge's RR 1.42; minimum detectable RR
  3.8-5.1x, power 2-6%. Exact test used because per-arm counts are single- to
  low-double-digit (normal approximation invalid). MRSA: 0 primary denominators.
  outputs/detectability_result.md.

## 2026-08-19 — Two statistical cautions on detectability (pre-commit, PI-directed)

Applied before the finding leaves the repo, both from the PI:

- **Caution 1 — name the method.** What detectability.py computes is NOT post-hoc /
  observed power (effect fixed at the trial's own estimate — rejected on sight by
  statistical reviewers). The effect is fixed A PRIORI from a source EXTERNAL to the
  trials (Soge). Renamed and documented throughout as a **design-based sensitivity
  analysis**; verbatim methods language carried into the report.
- **Caution 2 — check the benchmark.** Soge's RR 1.42 is the GONOCOCCAL >3-doses/mo
  figure — cross-organism. Soge's own *S. aureus* result was tetR colonization
  **18% vs 8% (P<.0001)**, RR approximately **2.25** — the same-organism, matched
  benchmark. Added RR_SAUREUS=2.25 as primary, kept RR_GC=1.42 as flagged secondary.
  Result holds either way: **0/4** comparisons powered for EITHER; min detectable RR
  3.8-5.1 exceeds both.

## 2026-08-19 — Mende 2016 ingested and verified (the "null" that confirms mechanism)

Verified before citing (`nihms-805541.pdf` -> data/raw/papers/), per PI "treat it as
a lead." Mende K, et al. Diagn Microbiol Infect Dis 2016 (10.1016/j.diagmicrobio.
2016.07.014). US military, 168 injured deployers, 55% on antimalarial doxycycline:
**no difference in overall tetracycline-class resistance** (the mechanism-BLIND
endpoint) BUT **tet(M) genes significantly MORE common in the doxycycline-exposed
group, P=0.031** (the mechanism-DISCRIMINATING endpoint). This is constraint 2 /
Grossman shown INSIDE one study: total prevalence flat while tet(M) composition
shifts. Surface honestly as a null; engaged, it supports the assay-level thesis.
Caveats logged in SOURCES.md: military (not MSM), antimalarial dosing (not doxy-PEP),
n=168. Not coded as a trial — catalogued as a comparator.

## 2026-08-19 — Defined literature search: the measurement gap in the literature itself

Query defined a priori (PI-directed: stated bounds, denominator = doxy-PEP papers,
numerator = those naming a bystander organism). Two NCBI E-utilities esearch queries,
2015-2026, verbatim in outputs/literature_search_result.md. **361** doxy-PEP papers;
**13 (3.6%)** name a bystander staphylococcal organism; hand classification of the 13
(each by PMID, checked against an authoritative PMID<->title pairing, not position):
only **5 (1.4%)** MEASURE tetR *S. aureus* at all, only **2** against a doxy-PEP
EXPOSURE contrast (Soge; DuDHS at pilot n). The gap the three streams document inside
trials/guidelines/surveillance is reproduced in the surrounding literature. Counts
frozen to data/raw/literature_search/snapshot.json (PubMed grows); `make literature
ARGS=--refresh` re-queries. New module src/analysis/literature_search.py + 4 tests.
esearch runs via curl (sandbox TLS proxy uses a self-signed cert urllib rejects).
