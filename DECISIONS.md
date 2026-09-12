# DECISIONS.md

Dated analysis decisions, logged before results are known. Append-only.

## 2026-08-20 — Build the clustering-detectability analysis (Contract 3, ¶7)

Alignment audit found intro ¶7 ("the systems report the mean of a process whose risk
was never in the mean") and ¶4's clustering frame had NO computational backing — the
non-monotonicity was illustrative only, and no clustering/simulation model existed.
PI: this is a build need. Design (logged before results):

- `src/analysis/coverage_null.py` — the structural demonstration. Carriage is modelled
  as an OVERDISPERSED (clustered) process: logit(p_visit) = trend + ε, ε ~ N(0, σ²).
  Simulate colonized counts at the trials' ACTUAL per-visit denominators (loaded from
  the coded DOXYVAC MRSA rows), then apply the naive cross-sectional trend test the
  trials use (Cochran-Armitage, which assumes binomial variance). Two failures reported
  as clustering σ grows: (a) POWER to detect a fixed true trend collapses toward α;
  (b) TYPE-I error under a flat process inflates above α (clustering fabricates trends).
  σ is ESTIMATED from the observed DOXYVAC series (residual logit variance beyond a
  fitted trend), so the 'realistic clustering' is data-anchored, not arbitrary. Endpoint
  is coverage/power (detectability), NOT an effect size (Contract 1). Unit is S. aureus
  carriage (MRSA rows used only because they are the coded carriage series; the argument
  is about the endpoint's structure, which is organism-agnostic).
- `src/analysis/three_outbreak_fit.py` — applied companion. Fit flat / monotone-trend /
  wave models by maximum likelihood to the observed non-monotone series (DOXYVAC 5-visit
  both arms; DoxyPEP colonisation 3-visit both arms) and compare by AIC + a parametric-
  bootstrap discrimination test. Expected/target finding: at the observed denominators
  the data do NOT significantly favour the clustered/wave model over the flat null (nor
  vice versa) — the cross-sectional series is statistically uninformative about
  clustering. This QUANTIFIES the manuscript's 'consistent with clustering,
  indistinguishable from noise, which is the point' WITHOUT claiming the data prove
  clustering (discipline: illustration becomes measured indistinguishability, not proof).

No causal claim. Seeded simulations for reproducibility. Both write outputs, get tests,
wire into `make`, and — once verified — are cited from Methods §2 and Results §3.1 to
close the audit's row-9/row-10 gap.

### Results (after the pre-registered design above)

Built, tested (9 new tests; full suite 94 passed), wired into `make trials`.

**coverage_null** (`outputs/coverage_null_result.md`). The naive Cochran-Armitage trend
test is calibrated at σ=0 (5% Type-I, 96% power for the observed-magnitude trend). As
clustering grows the two errors diverge: at σ=0.5, power 85% / Type-I **22%**; at σ=1.0,
power 77% / Type-I **48%** — a flat process is read as a significant trend nearly half
the time. The DOXYVAC series cannot constrain σ (σ̂≈0.00 doxy, 0.15 no-PEP, only 3
residual df — meaningless). Sharper-than-expected consequence: this REFRAMES Vanbaelen's
"within-arm trend significant in BOTH arms" — at the clustering these USA300 networks are
documented to carry, both-arms-significant is exactly the coverage-null signature
(clustering the endpoint can't see), not necessarily selection. Symmetric/neutral: the
endpoint fails in either direction, which is the point. Does NOT undercut the bystander
concern — it shows the instrument cannot adjudicate it.

**three_outbreak_fit** (`outputs/three_outbreak_fit_result.md`). Fit flat/trend/wave by
ML, two parametric-bootstrap tests. More nuanced (and more honest) than a blanket
"indistinguishable from noise": the doxy arm has a RESOLVABLE monotone rise
(trend-vs-flat p<0.001, consistent with Vanbaelen), but the OUTBREAK CURVATURE is
unidentifiable in BOTH arms (wave-vs-trend bootstrap p=0.43 doxy, 0.15 no-PEP; wave never
lowers AIC by ~2 over trend). The data can establish THAT carriage rose (one arm) but not
HOW — a monotone selection trend and a clustered wave fit equally well; the mechanism is
unidentifiable from these endpoints. HOLDS the manuscript's line (M6 non-monotonicity =
illustration, not proof) and quantifies it. The DoxyPEP resistance series (2-3 points/arm)
is too sparse to bring to the test — a further instance of the same gap. (Design note: I
had planned to fit DoxyPEP colonisation too; it has only 2-3 post-baseline points/arm, so
the fit runs on the two DOXYVAC 5-visit arms and the sparsity is reported as a finding.)

Net: Contract 3 (¶7) moves from UNSUPPORTED to computed — "the endpoint cannot resolve
clustering in principle (coverage_null) and cannot identify it in these data
(three_outbreak_fit)." A detectability claim; no causation; discipline intact.

## 2026-08-20 — Restructure into two correctly-scoped instruments (Contract 2 fix)

PI flagged a Contract-2 violation: coverage_null / three_outbreak_fit run on MRSA throat
carriage (the methicillin-resistant SUBSET), but the manuscript's declared analytic unit
is doxycycline-resistant S. aureus entire. The dichotomy — MRSA behaves as a clustered
network phenomenon, doxy-R S. aureus accumulates under selection — needs TWO instruments,
each on data that can bear it; do NOT demonstrate it by comparing the DOXYVAC MRSA curve
to the US S. aureus curve as fitted shapes (point-count asymmetry, cross-trial confounds,
MRSA⊂S. aureus nesting make that uninterpretable). No cross-trial pooling.

- **Task 1 — `selection_ratchet.py` (S. aureus-scoped).** Within US DoxyPEP only (single
  trial/assay/denominator). Recover susceptible carriage = colonization − all-swabbed
  doxy-R from the CROI slides (428/360/222 doxy; 202/91/65 SOC). DIRECTIONAL confirmatory
  tests only (three timepoints cannot support flat/trend/wave shape discovery): one-sided
  decline of susceptible carriage; one-sided per-carrier resistance increase; a
  neutral-suppression contrast (observed vs proportional-decline expectation).
  ARITHMETIC-BASE FINDING: the reported 5%→13% is over ALL-SWABBED, not per-carrier (slide
  states so) — the manuscript's "fraction-of-carriers" phrasing applies only to the
  derived per-carrier series (11%→41%); corrected.
- **Task 2 — `dejong_sigma.py` (MRSA-scoped).** de Jong Table 1 is not a time series; it
  is 10 cross-sectional MRSA COLONIZATION prevalences (recoverable count+n; infection-only
  and %-only studies dropped and listed). Fit logit-normal binomial random-effects for the
  between-cohort σ. σ̂ is an UPPER BOUND on transmission clustering (includes methodological
  heterogeneity, unpartitionable at 18 studies); the load-bearing claim rests on the LOWER
  CI. Kept MRSA-scoped; NOT imported as an S. aureus σ.
- **Task 3.** coverage_null & three_outbreak_fit remain MRSA-scoped, now stated as such;
  coverage_null imports the external de Jong σ̂ (its own series can't estimate σ: σ̂≈0 at 3
  resid df — a Stream-A finding); σ=0 row confirmed calibrated by construction (CA test
  correctly sized). three_outbreak_fit: "best=wave" struck for the no-PEP arm (ΔAIC 0.8 =
  indistinguishable, noise-mining); doxy trend-vs-flat reported as <1/N_BOOT not "0.000".

### Results (before any manuscript prose — held for PI number-check)

- **selection_ratchet (S. aureus):** doxy arm — susceptible carriage 39%→16%→18%
  (one-sided decline p=1.6e-11); per-carrier doxy-R 11%→41% (Fisher p=2.7e-07); resistant
  carriage rose to 28 vs 7 expected under neutral suppression (Poisson p=5.5e-09). SOC arm
  uninformative on every test (decline p=0.37; per-carrier fell 21%→11%, p=0.94). The
  ratchet is on the S. aureus unit — Contract 1 (detectability/direction, not effect) and
  Contract 2 (S. aureus, MRSA a subset) both respected.
- **dejong_sigma (MRSA):** σ̂ = 2.70 (95% profile CI 1.74–4.57); stable dropping the 54%
  (2.67) and to general-MSM-only (2.62). Prevalence spans 0%–54% over 10 cohorts.
- **coverage_null (MRSA), Type-I at the de Jong σ:** σ=0 calibrated (5%); at σ̂=2.70,
  Type-I(flat)=78%; at the lower CI σ=1.74, Type-I=67%. Both far exceed the 20–48% the
  argument needs — the claim rests on the lower CI, robust to the upper-bound caveat. At
  σ̂ power (86%) ≈ Type-I (78%): the test rejects regardless of truth — no discrimination.

## 2026-08-21 — Align selection_ratchet to the abstract table; fix §1 axis mislabel

Data-integrity pass on the doxy-R S. aureus series (PI-directed). Two fixes:
- **§1 line 110 axis mislabel:** "resistance among cultured isolates rose, from 5% to 13%"
  paired a per-carrier LABEL with the all-swabbed NUMBER (5→13 is the slides/CDC all-swabbed
  venue). Corrected to the per-carrier figures that match §3.1: doxy 8.5%→40%, SOC 24%→11%.
  (Line 135's "ratchets 5% to 13%" and line 149's quoted CDC "5%…13%" left as legitimate
  all-swabbed/CDC-venue figures.)
- **selection_ratchet.py re-anchored slides → abstract table.** Was computing on the CROI
  SLIDES (428/360/222; per-carrier 11%→41%) while the manuscript §3.1 cites the CROI
  ABSTRACT TABLE (8.5%→40%). Switched the module's counts to the published abstract table
  (doxy M0 141/334, 12/334; M12 40/137, 16/137; SOC M0 78/161, 19/161; M12 28/62, 3/62) so
  the code REGENERATES the 8.5%→40% the prose uses. Cost: abstract table is M0/M12 only, so
  the ratchet is now a two-endpoint directional test (no M6 midpoint). Active expansion
  HOLDS and is if anything cleaner: susceptible carriage 38.6%→17.5% (decline p=4.5e-6),
  per-carrier 8.5%→40% (Fisher p=9.6e-6), neutral-null 16 observed vs 3.4 expected
  (Poisson p=6.4e-7); SOC uninformative (susceptible rises 37%→40%, per-carrier falls
  24%→11%). NB: the slides-vs-abstract-vs-NEJM (5/16/28) venue discordance is NOT smoothed
  — it is the authors' inconsistency and remains a Stream A finding in §3.1; detectability.py
  deliberately keeps the NEJM peer-reviewed denominators. 8 ratchet tests pass.

## 2026-08-21 — Citation verification pass + reference-list reconciliation

Claim-support pass (12 parallel source-verifications + 2 web resolutions,
`citation_verification.md`): no cited source failed; every load-bearing number verified
verbatim. Applied safe metadata fixes (sfdph2022 real title+URL, cdc2024 full title,
diep2008 author-order note). Two prose tightenings held for PI (grossman "wash out"
attribution; CROI "~6%" clarity).

Reference-list reconciliation: PI identified that 6 uncited entries (`harrison1979`,
`lopezbernal2018`, `miko2012`, `schroder2025`, `spinelli2026`, `demidont2026cid`) belong
to a SEPARATE work — the ITS "time zero" correspondence to the CID editor re: the Spinelli
doxy-PEP ITS paper (gonococcal/STI-focused), not this S. aureus manuscript; they had bled
into the bib. Also removed `demidont2026metaarxiv` (the "150-journal audit" self-cite) and
its §2.6 in-text clause, per PI direction. `demidont2026cid` is a real submitted (not
published) correspondence; it had two inconsistent IDs in-repo (CID-S-26-03420 vs
CID-132517) — both now removed. Cleaned the bib header's "verified against the companion
CID correspondence" line and the stale CLAUDE.md "cite the CID letter" instruction.
Result: bib closed at 15 entries — every one cited, every citation resolved, citeproc
clean.

## 2026-08-21 — Stream C: recode the facility-antibiogram cell against CLSI M39

The antibiogram cell was coded "right unit, no denominator" — an understatement. PI
verified CLSI M39 (5th ed., 2022) text: it (a) REQUIRES S. aureus stratified into MRSA/MSSA
(methicillin axis mandated) and (b) treats non-primary agents as selectively
reportable/suppressible (supplemental agents tested only on resistant isolates not reported;
cascade rules may suppress). Tetracycline/doxycycline for S. aureus is such a supplemental
agent. Recoded to **right unit, non-standardized (M39), no population denominator**
(`phenotype_capture: facility_nonstandard_no_denom`). Scope discipline held: licensed claim
is inconsistency/non-standardization ("captured nowhere consistently, nowhere with a
population denominator"), NOT universal absence — M39 permits tetracycline reporting and
some labs do it; a single reporting lab must not falsify the claim.

Added the CROSS-TIER SYNTHESIS: the methicillin axis is the reported axis at every tier —
ABCs/EIP (pop-denom invasive MRSA), NHSN AR/LabID (MRSA), facility antibiogram (M39-mandated
MSSA/MRSA split). The architecture is standardized around methicillin at all levels; S.
aureus tetracycline resistance is orthogonal and falls through at each. This is the Stream C
analogue of the endpoint-substitution seam in Stream A (tet(K)/tet(M) mislabel; narrowing to
the methicillin subset) and Stream B (efficacy graded, harms un-graded) — the same
measurement-inheritance seam, now codified in a national laboratory standard.

Count UNCHANGED (still 2 exposure-only / 0 phenotype / 0 both / 0 linked); this deepens the
mechanism of the phenotype-side failure, it does not change the count. Updated: decomposition
table, licenses/not block (may claim non-standardized facility capture per M39; may NOT claim
universal facility absence), gap-register Stream C row. Scope bound from Task 5 unchanged
(closable by adding tetracycline AST for S. aureus to ABCs/EIP; none deployed).

## 2026-08-20 — Stream C CHECKPOINT (Task 1): the "81" is not a systems denominator

Validated what the Stream C "0/81" actually counts BEFORE trusting it (standing order:
don't run to a clean 0/N on a shaky denominator). Two findings, both flagged:

1. **The count is STALE.** `dilution.sensitivity_table` sweeps UPTAKE(3) × KAPPA(5) ×
   R0(3) × N(3) = **135 cells**, not 81. The "0/81" in the gap register, manuscript
   (~line 516), and README predates the κ<1 grid expansion (KAPPA 3→5 values). Correct
   figure is **0/135**.
2. **The 135 are PARAMETER-GRID SCENARIOS, not surveillance systems / jurisdictions /
   documents.** Each cell is a hypothetical (uptake, kappa, R0, N) combination. The grid
   answers a DILUTION/DETECTABILITY question — "is the doxy-PEP-exposed subgroup too
   dilute to move a population S. aureus tetR rate detectably?" (answer: yes, RR_needed
   far above Soge 1.42 across all favorable cells) — which is a legitimate finding but is
   NOT the LINKAGE question ¶6's third leg makes: "does any established surveillance
   system LINK doxy-PEP exposure to S. aureus phenotype at a common population
   denominator?" The linkage claim has NO principled systems denominator; it was being
   backed by a robustness sweep of a different model.

DECISION: re-anchor (Task 1 mandate: do not proceed to Task 2 on a convenience/parameter
denominator). Stream C is split into two legs:
- **Linkage leg (NEW, principled denominator):** a defined, closed universe of established
  US public-health surveillance systems (federal/state/metro) that could plausibly capture,
  at a population denominator, EITHER doxy-PEP/doxycycline exposure OR S. aureus
  tetracycline/doxycycline resistance. Coded three ways (exposure-side / phenotype-side /
  join) — Tasks 2–4. Anchor = option (c) systems universe, with AIDSVu (option b) as the
  concrete exposure-side member for the resolution/computational leg. This directly backs
  ¶6's third leg.
- **Dilution leg (EXISTING dilution.py/dilution_metro.py):** even if a linked
  population-denominator system existed, the exposed subgroup is too dilute to move the
  rate (0/135 state; metro needs implausible density). Kept as a SUPPORTING, deepening
  finding — Contract-1-compliant (RR_needed, not an effect), S.-aureus-scoped (R0 = S.
  aureus tetR) — and relabeled 0/135, not 0/81.

Old-vs-new: gap-register Row 7 currently cites "dilution.py → 0/81" as the linkage
evidence; that conflates dilution with linkage and is stale. To be replaced by the
decomposed linkage finding + the corrected dilution 0/135.

## 2026-08-20 — Stream B denominator: convenience → de-Jong-anchored purposive

Converted Stream B's denominator from a convenience set (jurisdictions on disk) to a
purposive one whose selection rule is inherited from de Jong 2025 Table 1 — the US
jurisdictions with documented CA-MRSA/USA300 in MSM (same source as `dejong_sigma.py`'s
σ̂). Full analysis in `streamb_denominator_reconciliation.md`.

- **Outbreak set (7, de Jong Table 1):** San Francisco (Diep 2008), Chicago (Popovich
  2020), NYC (Shastry 2007), Boston (Szumowski 2009), LA County (Lee 2005), San Diego
  (Mathews 2005), Atlanta (Hidron 2011). International sites excluded (US governmental
  denominator).
- **Intersection:** Matched 6 (SF, Chicago, NYC, Boston→MA, LA, San Diego) — all coded,
  all silent on S. aureus monitoring. Gap 1: Atlanta → confirmed-none (Georgia DPH page is
  HIV-PEP only, verified by fetch; doxy-PEP via CDC finder + Grady clinic, excluded).
  Non-outbreak reclassified: Detroit, Maryland, Philadelphia (+ RI uncoded).
- **Coded SF** (`gl_sf.yaml`) — was on disk (SFDPH/City Clinic provider guide 5/2026) but
  uncoded; the single most load-bearing outbreak jurisdiction. Coded blind: bystander =
  generic "microbiome/antibiotic resistance ... being studied" (S. aureus NOT named);
  S. aureus/staph/MRSA absent from the whole doc; monitoring silent; no host-toxicity
  labs. Corpus now 10; gate still clear (0 require S. aureus monitoring).
- **DC (Task 3):** not a de Jong outbreak jurisdiction → out of the purposive denominator;
  its missing guidance does not affect the sample (absence explained, not conspicuous).
- **Independent vs defer-to-CDC:** headline split so CDC-echoes are not counted as
  independent declines. Outbreak-matched 6 all substantive-independent, 0 defer-to-CDC, 0
  monitor. Philadelphia (non-outbreak) defers to CDC — dependent observation, separated.
- **Optional refinement applied:** of the 6, 3 name S. aureus (NYC/LA/San Diego), 2
  generic (SF/MA), 1 silent (Chicago) — even naming is uneven; none monitor.
- **Coded blind** to the expected "counseling at most" outcome; SF read from full text; no
  document departed from the pattern. Status: Stream B complete under the de-Jong rule
  (6/6 matched coded; Atlanta confirmed-none; 3 reclassified).
- **DC checked-and-excluded (on record):** not a de Jong documented-outbreak jurisdiction
  (no Table 1 row; the only "Washington" in de Jong is Washington *State* re: E. coli), so
  it is outside the purposive denominator. DC doxy-PEP provision is clinic-only
  (Whitman-Walker); the DC DOH role is a referral hotline, with no standalone governmental
  doxy-PEP guidance. Its absence therefore does not affect the sample — logged so the
  check is on record rather than a conspicuous gap.

## 2026-08-20 — Stream B independence check WITHIN the outbreak-matched six

Applied the same lineage test that excluded Philadelphia to the load-bearing six, from
document content (structure, section order, shared passages, stated derivation) — an
independence claim enforced on the non-outbreak tier must hold on the load-bearing tier.
Findings (`streamb_denominator_reconciliation.md` lineage table):
- **4 independently authored:** SF (lineage seed), Chicago (formal protocol, bystander
  silent), NYC (Dear Colleague, "staph infections" lay register), San Diego (health
  advisory, formal "Staphylococcus aureus" + commensal Neisseria/plasmid mechanism).
- **1 adapted within the six:** LA County — "Adapted from San Francisco City Clinic, 2022",
  carries SF's numbered "What are we still learning?" template → SF+LA = one lineage group,
  not two independent declines.
- **1 adapted from an external template:** Massachusetts — "Adapted from: DoxyPEP … Fact
  Sheet" (unnamed); its "benefits/risks/how-to-access" FAQ does NOT match SF's still-
  learning template, so the source is not one of the six.
- **Stronger result on organism-naming:** the 3 S. aureus-naming docs do NOT share a
  sentence — NYC ("staph infections", lay) and San Diego ("Staphylococcus aureus", formal)
  are independently authored in different registers/document types; LA names it ("for
  example staph") within the SF template. So ≥2 departments independently named and then
  independently declined to monitor — not one template propagating.
Restated headline: "6 outbreak jurisdictions, of which 4 independently authored, 0 require
or suggest S. aureus monitoring" (LA adapted from SF; MA from an external fact sheet;
Philadelphia, non-outbreak, defers to CDC).

## 2026-08-20 — Close Row 4 (early-stopping/duration) on a sample-accrual basis

Row 4 was the last partial Stream-A claim (documented, not computed). Extended the
design-based sensitivity analysis in `detectability.py` to quantify the duration/accrual
impact. Design (before results):
- Hold the benchmark at the matched RR 2.25 (Soge tet-R S. aureus, the number
  detectability.py uses); RR 1.42 (gonococcal) secondary, flagged cross-organism.
- For each primary-trial S. aureus comparison solve for the sample needed at 80% power,
  preserving the trial's arm ratio and control rate; report the multiple over realised.
  METHOD: normal approximation for the required (large) N — valid in that regime and
  where exact-Fisher region enumeration is impractical — with an exact-Fisher spot-check
  that the solved N delivers ~80%. Exact Fisher retained for the tiny realised counts.
- Duration: attempt only if the retention schedule supports a defensible extrapolation.
- S. aureus unit only; MRSA has no primary denominator (per detectability_result.md).

Results (before manuscript prose):
- Required-sample multiples (RR 2.25 matched): M6 colonised 3.6×, M6 all-swabbed 3.7×,
  M12 colonised **6.3×**, M12 all-swabbed 5.8×. Cross-organism RR 1.42: 24×–43×. Exact-
  Fisher spot-check at the solved N = 79% (validates the approximation; multiples are
  slight under-estimates → conservative). 0/4 remains, consistent.
- DURATION NOT INFERABLE, stated not fabricated: S. aureus has only 2 arm-split
  timepoints (M6, M12) and per-visit N DECLINES (colonised 51→31; all-swabbed 192→111) —
  a declining 2-point curve cannot support an accrual/retention extrapolation, and
  repeated swabs on a shrinking cohort do not accrue independent observations. Report the
  sample-size multiple; do not infer months.
- Early stop folded in as the REASON for the realised denominator: DoxyPEP's SOC arm was
  closed at the 5/2022 DSMB efficacy interim, truncating the control-arm accrual (the
  binding constraint: control colonised n=29 M6, 24 M12). DOXYVAC stopped ~9mo median but
  measured only MRSA — no S. aureus denominator, cannot enter the test.
- License: "would have needed ≈6× the sample; the efficacy stop foreclosed it." NOT "a
  longer/larger trial would have found an effect." Row 4 → computed (sample-size basis;
  duration not inferable). Intro flag: phrase ¶4/¶6 "stopped early" as sample-accrual
  foreclosure, not a duration claim.

## 2026-08-20 — Cross-trial non-monotonicity (M6/mid-study), held as illustration

PI observation: the non-monotone S. aureus/MRSA trajectory is in BOTH pivotal trials,
and the tell is that the arms move TOGETHER at the shared mid-study timepoint.
- DOXYVAC MRSA carriage: non-monotone in both arms; at M6 no-PEP (7.1%) > doxy (6.4%).
- DoxyPEP S. aureus colonization: falls in BOTH arms at M6 (SOC 48->38%, doxy 44->29%),
  recovers by M12 (43%, 31%). The SOC dip cannot be a doxy-PEP effect — a dose-response
  moves only the exposed arm, monotonically. Arms lurching together = a network/temporal
  process the cross-sectional endpoint samples but cannot resolve.
Discipline held (per PI + the M6 reasoning): ILLUSTRATION, not proof. The pattern is
consistent with clustered transmission AND with sampling noise at these single-to-low-
double-digit counts; the design cannot separate them — which is the point (indicts the
instrument). Denominators are read off the slides and NOT used for statistical weight;
formal within-arm trend would need the trials' supplements. Folded into manuscript S3.1
(cross-trial) building on the sharpened para 4 (network-continuity licensing + category
error). No causal claim.

## 2026-08-19 (overnight) — S. aureus broadening of Stream A

The clinical reframe fixes the unit as *S. aureus* (MRSA a subset). Checked whether
this needs recoding: Stream B (s_aureus_* fields) and Stream C (R0 = S. aureus tetR)
are already S. aureus-level — verified, no change. The work is concentrated in Stream A.

- **D1** — added `conference_abstract` source_type for the trial's own pre-publication
  data (CROI abstract table). First-party but not peer-reviewed; kept distinct from
  `primary_trial` and EXCLUDED from detectability so the power analysis uses published
  denominators. The CROI-vs-NEJM figure discordance is thereby preserved as data.
- **D2** — detectability stays on all-*S. aureus* primary-trial rows (the clinical
  unit); MSSA/MRSA coded as documented subsets, not fed into the power calc. Confirmed
  detectability UNCHANGED after broadening: 0/4 for both benchmarks.
- **D3** — DOXYVAC measured MRSA *carriage prevalence* (a different axis; Vanbaelen
  trend doxy p<0.0001 / no-PEP p=0.0139), but the per-timepoint denominators live in
  Molina's main paper, which is not in the corpus. Per the no-fabrication rule, NO
  observations coded for DOXYVAC S. aureus; documented at the trial level and flagged
  as an acquisition gap (get Molina, Lancet ID 2024). The different-axis measurement is
  itself part of the heterogeneity finding.
- Coded the CROI abstract-table S. aureus rows for DoxyPEP (8 obs: all-S.aureus + MRSA
  subset, exact fractions) as `conference_abstract`, with the table-caption
  'tetracycline class' relabel captured.
- New analysis `saureus_measurement_heterogeneity()` -> `outputs/saureus_heterogeneity.md`:
  the three trials share no measurement axis, no denominator basis, no assay, and none
  is mechanism-discriminating — the evidence for the manuscript's 'resist pooling' claim.
  Manuscript S3.1 leads with this; Methods S4.1-4.2 updated.
- Tests +3; full suite green. Nothing in Stream B/C changed.

## 2026-08-19 (night) — IDSA guidelines ingested; clinical-lens Introduction funnel

Two IDSA clinical guidelines ingested + hashed (papers/CHECKSUMS.md, coded-source):
`liu2011_idsa_mrsa_guideline.pdf` (ciq146) and `stevens2014_idsa_ssti_guideline.pdf`
(ciu296). They ground the clinical reframe and resolve the one TODO-verify citation.

- **liu2011 resolved (was TODO-verify).** The IDSA MRSA guideline lists "a tetracycline
  (doxycycline or minocycline) (A-II)" among oral CA-MRSA options, and states the
  tet(K)/tet(M) distinction WITH clinical consequence verbatim: "tet(K) confers
  resistance to tetracycline and inducible resistance to doxycycline … [while] tet(M)
  … resistance to all agents in the class." This puts the project's constraint-2
  measurement point inside a treatment guideline: a mechanism-blind "tetracycline
  class" endpoint cannot tell a clinician whether doxycycline still works. Wired into
  manuscript §2.1.
- **Author overlap verified.** Henry F. Chambers is an author of liu2011 and senior
  author of Diep 2008 (USA300 in MSM) — supports Introduction beat 4. Added diep2008
  to references.bib (canonical; not hashed).
- **Introduction rewritten to a 9-beat clinical funnel (PI-specified).** Doxy-PEP works
  and scales; every dose is bystander selective pressure; why S. aureus matters
  clinically (doxycycline an IDSA oral MRSA option; constrained alternatives); the MSM
  USA300 history; the TGW-underpowering / generalization limit; the trials' own call
  for monitoring; the 3-part research question; the distributive-justice stakes (named
  constituencies: diabetes, dialysis, post-surgical, oncology patients on oral
  anti-staph therapy); and the three streams. Externality paragraph in the Discussion
  aligned to the named constituencies + the IDSA armamentarium-erosion framing
  (stevens2014). Guardrails held: no causal claim; MRSA baseline steel-manned; register
  measured. manuscript.tex regenerated; compiles clean to 24pp; all citations resolve.

## 2026-08-19 (late) — CROI abstract BODY + TABLE obtained: the keystone exhibit

PI supplied the verbatim CROI 2023 abstract body and its data table (croiconference.org)
and proposes the whole paper can rest on this one abstract. Agreed — it instantiates
all three streams. Exact fractions added to `croi2023_luetkemeyer_OA3.md` (re-hashed).

- **Relabel origin located.** The abstract TABLE CAPTION reads *"phenotypic resistance
  to the tetracycline antibiotic class"* over columns whose S. aureus and commensal
  Neisseria assays are DOXYCYCLINE (E-test) and only GC is tetracycline. The tet(K)/
  tet(M) conflation the project is about is printed in the trial's OWN table title;
  NEJM End Points sentence, CDC, and Szondy inherit it. `saureus_endpoint_label_mismatch`
  note updated to name this origin.
- **Deflation now EXACT (arm-split fractions).** Doxy-PEP doxy-R S. aureus over all-
  swabbed 3.6% (12/334) -> 11.7% (16/137), concluded "without a significant increase
  ... modest ... unlikely clinical significance" (p=0.19). Per CARRIER (÷ Staph+):
  **12/141 = 8.5% -> 16/40 = 40.0%** (4.7x), while SOC falls 24.4% -> 10.7%. The
  colonization reduction (16%) the abstract headlines deflates the denominator its
  conclusion rests on.
- **Multi-venue count discordance sharpened.** M12 doxy-arm doxy-R S. aureus resistant
  count = 5 (NEJM appendix) / 16 (CROI abstract table) / 28 (CROI slides -> CDC). A
  5-to-28 range for one endpoint. CDC's 20/428, 28/222 match the SLIDES, not the
  published abstract table (12/334, 16/137) — the slides and abstract table disagree.
  With data withheld (data_availability=no), none can be adjudicated.
- **GC footnote = Stream C inside the trial.** Abstract footnote: TCN-R testing
  unavailable in **83% (212/256)** of GC diagnoses (culture not collected 57%, failed
  to grow 39%, contamination 5%). Even a funded RCT could not phenotype the in-category
  organism in most cases.
- **Authors concede the gap.** Abstract's last sentence ("surveillance ... is needed")
  and the presentation's final bullet ("longer term monitoring ... to understand the
  trajectory and clinical importance of microbial susceptibility patterns") are the
  trial team stating the instrumentation does not yet exist — the project's thesis.
- MRSA note refined: a primary denominator DOES exist in the CROI abstract table
  (doxy M0 20/334, M12 2/137) though events are ~nil; NEJM has none. Detectability
  unchanged (uses NEJM primary rows only).

## 2026-08-19 (evening) — CROI 2023 OA-3 slides obtained: CDC discrepancy RESOLVED + two corrections

The PI supplied the CROI 2023 oral-abstract slides (Luetkemeyer, OA-3, Feb 20 2023;
PI attended live) and made three points. Transcribed to
`data/raw/papers/croi2023_luetkemeyer_OA3.md` (hashed). This supersedes the framing
in the prior (afternoon) entry on two points.

- **CDC 20/428, 28/222 provenance RESOLVED (no longer "pending").** These are the
  CROI S. aureus DOXY-R panel (doxy-PEP arm, baseline & M12) over the **all-swabbed**
  denominator: 5%x428=20, 13%x222=28. CDC observation rows updated:
  phenotype_measured now **doxycycline** (was not_stated), denominator_basis now
  **all_participants_swabbed** (was unclear), with the verbatim CDC quote.
- **CORRECTION 1 — no tetracycline "endpoint switch."** The S. aureus assay was
  DOXYCYCLINE throughout (E-test MIC>=16): CROI methods table, NEJM Trial Procedures,
  NEJM Appendix Table 2. There was never a tetracycline-S.-aureus measurement.
  "Tetracycline" is only a LABEL (NEJM End Points sentence, protocol aims, CDC/Szondy
  downstream). The afternoon entry's "pre-specified tetracycline endpoint that got
  switched to doxycycline" over-read it. Field renamed
  `resistance_endpoint_switched` -> `saureus_endpoint_label_mismatch` (schema + YAML +
  tests); it now records a labeling inconsistency, not a measurement switch, and not
  concealment (tetracycline is the broader surrogate; doxycycline the more
  conservative measure — direction unchanged from the earlier correction).
- **CORRECTION 2 / NEW FINDING — denominator deflation (the PI's point #3), and it
  sits in CDC's own sentence.** CDC attributes the resistance rise to "those with
  S. aureus in their nares" (colonized) but divides by all-swabbed 428/222. CDC
  itself prints the colonized counts (187, 69), so per-carrier doxy-R is 20/187=11%
  -> 28/69=**41%**, ~3x the reported 5%->13%. Doxy-PEP cuts colonization (44%->31%),
  inflating the all-swabbed denominator and deflating the rate computed over it
  (`all-swabbed = per-carrier x colonization`). description_denominator_mismatch=yes
  on both CDC rows now carries this.
- **Residual discordance (do not smooth):** CROI counts (colonized 187/69, resistant
  20/28) do NOT reconcile with NEJM Appendix Table 2 (colonized 139/31, resistant
  12/5). Same trial, same endpoint, different venue — CROI denominators run ~1.3-2.2x
  larger. Logged in the CROI artifact as its own finding; magnitude of the deflation
  is source-dependent, direction is robust.
- **Detectability unaffected:** it still uses only NEJM primary_trial colonized
  denominators; the CROI/CDC all-swabbed numbers are guideline-source rows (excluded).

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

## 2026-08-21 — P0 revisions from the adversarial panel (Stream C panel-power; per-carrier reframe)

Six-reviewer adversarial panel (submission/PANEL_SYNTHESIS.md) converged on two
load-bearing fixes; both are revisions to how already-computed results are *presented*,
no new analysis.

1. **Stream C now reports the panel-power correction and anchors on the realistic cell.**
   The manuscript previously printed only the single-two-proportion grid (0/135; RR 2.9-53)
   while the repo's own feasibility_result.md computes the controlled-panel correction and
   labels the single-comparison median "retired." §3.3, the abstract, and Figure 1 now
   anchor on the realistic cell under the panel: RR_needed ~=14 (DEFF=1) to ~=64 (DEFF=25),
   above Soge's 1.42-2.25 across the range. The best case (RR~=1.0 at DEFF=1) is stated and
   explicitly disowned as compounding four implausibilities that fail individually.
   summary_figure.py rewired from sensitivity_table min/median to panel_summary
   realistic_RR_needed. Flagged as the single most exposed number by both the
   biostatistician and the surveillance epidemiologist independently.
2. **Per-carrier 8.5->40% reframed as bounded denominator-sensitivity, not a headline.**
   §3.1 now states the 16/40 month-12 numerator, calls it an illustration "not a tested
   quantity," and notes it inherits the same withheld-data uncertainty; the robust claim is
   the between-arm direction and a several-fold rise "under either denominator" (~3x
   all-swabbed, ~5x per-carrier). The 5/16/28 spread is presented as a reconciliation table
   (venue x numerator x denominator x basis) with "we do not suggest impropriety" — softened
   from "the counts do not reconcile." Abstract and topline aligned.

Deferred to a P1 pass (logged, not yet applied): tet(K) "inducible" wording (AMR reviewer:
Liu 2011 "inducible" describes clindamycin/MLS_B, not tet(K)); soften clustering "measured
property" + fix "18 vs 10 cohorts"; promote S. aureus-vs-MRSA scope note to the Intro;
"unmeasurable" -> "unmeasured as instrumented"; position measurement-inheritance vs
neighbours; credit the benefit side of the distributive-justice ledger.

116 tests green; PDF rebuilt.

## 2026-08-21 — P1 revisions from the adversarial panel (wording/precision)

Surgical fixes; no analysis changed except regenerating dejong_sigma's output doc.

- **Clustering "measured property" softened + study count fixed.** §3.1 now states the
  between-cohort→between-visit transfer is "an assumption, not an identity" (upper bound on
  a *different* variance component; we lean on the lower CI). "Eighteen studies" -> "the ten
  colonisation cohorts (of eighteen screened)" in the manuscript AND in dejong_sigma.py
  (docstring + generated result doc). σ̂ fit is on 10 colonisation cohorts, not 18.
- **"Loss of a class" recast as stake-sizing.** "predicted to shift toward tet(M)" -> "one
  would expect ... a mechanistic expectation, not a dynamic anyone has yet measured"; "loss
  of a class" -> "loss of the oral tetracyclines as a usable category," now noting the newer
  glycylcyclines/aminomethylcyclines (tigecycline, eravacycline, omadacycline) evade both
  determinants and remain.
- **Unit scope condition promoted to the Introduction.** New §1 paragraph states the
  empirical spine (dispersion, outbreak jurisdictions) exists only for the MRSA subset,
  marks the reliance as an early instance of the argument, forward-refs §4.
- **"unmeasurable" -> "unmeasured as instrumented"** in the Intro externality passage, with
  an added sentence that the harm is not unmeasurable in principle (§5 gives the instrument)
  but unpriced by deployed systems — the stronger governance claim. The one other occurrence
  (§2.5) already contrasts "un-built instrument" against "unmeasurable phenomenon" and is
  correct as written.

**tet(K) "inducible" — ADJUDICATED, NO CHANGE.** The molecular-AMR reviewer flagged
"tet(K) confers ... only inducible doxycycline resistance" as unsupported. Verified against
the source PDF (data/raw/papers/liu2011_idsa_mrsa_guideline.pdf): Liu 2011 states verbatim
"the tet(M) gene confers resistance to all agents in the class, tet(K) confers resistance
to tetracycline [78] and inducible resistance to doxycycline [79], with no impact on
minocycline susceptibility." The manuscript is faithful and attributes it to the guideline;
the reviewer conflated it with the clindamycin D-zone "inducible resistance" that also
appears in Liu. Kept as-is; quote logged for the response-to-reviews.

116 tests green; PDF rebuilt.

## 2026-08-21 — The Luetkemeyer 2025 pivot: Signal -> Mandate -> Inheritance

A new primary source arrived (PI-provided): Luetkemeyer AF, et al. **Lancet Infect Dis
2025;25:873-83**, the DoxyPEP FINAL analysis + open-label extension (10.1016/S1473-3099(25)00085-4;
ingested as luetkemeyer2025_lancetid_doxypep_final.pdf, SHA-256 pinned; coded in
data/raw/coding/luetkemeyer2025_saureus_final.yaml). It SUPERSEDES the NEJM 2023 interim +
CROI abstract/slides for the S. aureus endpoint.

**The fact that pivots the paper.** The investigators added a NEW randomised participant-level
analysis: among those free of doxy-R S. aureus at baseline, time to first detection by arm,
SC censored at crossover, Cox PH. Result: **HR 3.89 (95% CI 1.42-10.68), p=0.0044**
(68/393 vs 5/163; Fig 4B) — a statistically significant increase in incident doxy-R S. aureus.
Paired null: clearing colonisation HR 1.01 (0.69-1.46), p=0.98. Authors call the effect
"mixed" and call for public-health AMR surveillance of S. aureus (p.882).

**What this breaks, reported plainly.** The old thesis ("trial cannot see it -> guidelines
don't require it -> surveillance cannot see it") required proving the trial was incapable of
seeing the signal. The final trial SAW it. So the following became obsolete and were changed:
- "the trial's own between-arm test is non-significant" (was in FRAMING NOTE, §4, the
  claiming-box, the tet(M) para) -> removed everywhere; the trial's randomised test IS
  significant and we build on it.
- "We do not claim the per-carrier rise is statistically significant; the data are not public"
  -> the investigators ran the participant-level test themselves; retired.
- "As instrumented, the ... question cannot be answered" -> qualified: the trial answers the
  INDIVIDUAL-level incidence question; what is uninheritable is the POPULATION externality.
- The selection ratchet (one-sided Fisher, Poisson neutral-suppression, 8.5->40% inferential
  weight) is RETIRED: the final trial did the analysis properly, at participant level. Deleted
  src/analysis/selection_ratchet.py + its output doc + its tests (kept the sigma tests);
  removed from the Makefile trials target. The 2023/CROI/CDC denominators are retained only as
  the HISTORICAL reporting-evolution exhibit (§3.1).

**The new structure (PI-specified): Signal -> Mandate -> Inheritance.**
- Stream A (Signal): the RCT detects HR 3.89. §3.1 reopened with the signal + the estimand-
  evolution reading (2023 interim cross-sectional/reassuring -> 2024 CDC 5->13% + monitoring
  call -> 2025 incident-resistance HR 3.89: endpoint unchanged, question evolved). Power leg
  recast (interim cross-sectional estimand underpowered, min RR 3.8-5.1; incidence estimand
  adequate). Duration leg recast (the OLE supplied the accrual). New closing bridge: "what the
  trial does NOT answer" (mechanism, persistence, transmission, population, clinical infection,
  dose-response, beyond 12 mo, whether surveillance can follow) -> Streams B/C.
- Stream B/C unchanged in substance, strengthened: the trialists' own call for S. aureus AMR
  surveillance is a system that Stream C shows does not exist.
- Falsification (§5): the "adequately powered trial" leg is now MET; reported as the paper's
  premise, not a weakening.
- Figure 1 INVERTED: was "three streams, one line, nothing clears it"; now Stream A shows the
  OBSERVED HR 3.89 (CI whisker) clearing the Soge band, with the interim min-detectable RR as
  a faint tick (the effect landed at the edge of interim detectability); B/C show the
  inheritance failure. summary_figure.py rewired to HR_SAUREUS_FINAL constant (Fig 4B).
- references.bib: added luetkemeyer2025. Availability statement: GitHub
  (github.com/Nyx-Dynamics/doxypep-bystander) + Zenodo DOI 10.5281/zenodo.22051031 wired in.

No population-level causal claim is made. The individual-level hazard is the trial's finding,
reported as such; the claim is that the deployed guidance/surveillance cannot inherit it.

## 2026-08-21 — Push-readiness + Zenodo prep (repo NOT yet pushed)

State: three commits sit on `main` ahead of the last bundle commit — the pivot, the PLoS
formatting, and (pending) the submission-doc alignment. Working tree otherwise clean. NO git
remote is configured; nothing has been pushed.

**BLOCKER before any PUBLIC push (flagged, not executed — PI's call).** `git ls-files` shows
**66 copyrighted publisher PDFs (~57 MB)** tracked under data/raw/papers/ and
data/raw/guidelines/, and they are in the FULL history (many prior commits). Pushing this
tree to a public GitHub repo (github.com/Nyx-Dynamics/doxypep-bystander) would republish
copyrighted third-party articles. `.gitignore` now excludes these paths so no NEW PDF is
added (the Luetkemeyer 2025 PDF was deliberately NOT committed), but a `.gitignore` does not
touch history. The analysis does not need the PDFs at runtime (it reads coded YAML + public
data), and the deposit tarball already excludes them.

Recommended fix (do BEFORE adding a public remote), preserving commit history:
  pip install git-filter-repo
  git filter-repo --path-glob 'data/raw/papers/*.pdf' --path-glob 'data/raw/papers/*.docx' \
                  --path-glob 'data/raw/guidelines/*.pdf' --invert-paths
  # then: git remote add origin https://github.com/Nyx-Dynamics/doxypep-bystander.git
  #       git push -u origin main
Alternatives: (b) squash to a fresh single-commit history without the PDFs (orphan branch);
(c) keep the GitHub repo PRIVATE. Note: CDC MMWR and other US-government works are public
domain and could be retained if desired, but the simplest safe default is to strip all.

Also pending before public release: add a LICENSE file (none present) — e.g. MIT/BSD-3 for
code, CC-BY-4.0 for text/data — so Zenodo/GitHub reuse terms are explicit.

Zenodo: DOI 10.5281/zenodo.22051031 wired into the manuscript. The upload artifact is
`submission/doxypep-bystander-repo.tar.gz` (regenerated by `make deposit`; 2.0 MB; audited to
contain only our own manuscript.pdf, no copyrighted third-party PDFs).

## 2026-08-21 — Zenodo hardening (deposit-review punch-list) + history scrub

Acting on a detailed pre-upload review. Fixes applied:
- **P0.1 tarball/checksum design flaw.** `make deposit` no longer archives `submission/` (so a
  prior `.sha256` can no longer be embedded); the tarball's checksum is computed AFTER the
  archive is closed and lives beside it. Internal per-file manifest `CHECKSUMS.sha256` is added
  to the archive but does not contain the tarball's own hash. Verified: external checksum
  matches; archive does not contain its own tarball checksum.
- **P0.2 AppleDouble pollution.** Both archive targets build with COPYFILE_DISABLE=1 and
  exclude ._*/.DS_Store. Verified: 0 ._* members.
- **P0.3 stale source.** Deleted paper/manuscript.tex (pre-pivot, not part of the md->pdf build).
- **P0.4 README.** Rewritten around Signal->Mandate->Measurement Inheritance; the abandoned
  ecological design is now stated as provenance, and the false "preregistered (OSF)" claim is
  corrected — the prereg remained a DRAFT (no OSF timestamp), because Phase-0 killed the design.
- **P0.5 source-support items RESOLVED.** grossman2016 "wash back out" recast as an explicit
  inference from tet(M) molecular stability (not a measured population dynamic); the "~6% of
  isolates" wording corrected to "MRSA colonisation ~6% of sampled participants" at both spots.
  outputs/citation_verification.md updated: no open claim-support items remain.
- **P0.6 licensing.** Added LICENSE-CODE (MIT — code), LICENSE-TEXT (CC BY 4.0 — text/figures),
  THIRD_PARTY_DATA.md (rights/provenance). AIDSVu XLSX flagged: publicly downloadable and
  download-for-publication permitted, but IQVIA-sourced + "All Rights Reserved" -> NOT
  sublicensed CC BY; rehosting is a PI decision (keep vs exclude+retrieval). Included in the
  deposit by default, flagged.
- **P1.7 test count.** 116 -> "the complete pytest suite" in REVIEWER_GUIDE/COVER_LETTER/
  REPO_DEPOSIT_README. REPRODUCIBILITY.md documents the ~2.5-3 min runtime and the two slow
  modules (exact-Fisher detectability; clustering/bootstrap).
- **P1.8 env freeze.** Added requirements-lock.txt (exact versions; CPython 3.12.12 validated).
- **P1.9 MANIFEST.** 17pp -> 19pp; deposit description updated.
- **P2 simplification.** The Zenodo compendium (`make deposit`) now ships reproducibility
  artifacts only — no CLAUDE.md/SCAFFOLD.md/STREAM_B_HANDOFF.md, no submission/ layer; keeps
  DECISIONS.md. Added CITATION.cff + REPRODUCIBILITY.md. 175 members, 156 files in manifest,
  manifest verifies 156/156 on clean extraction.

**History scrub (this commit's successor):** `git filter-repo --invert-paths` on
data/raw/papers/*.pdf, *.docx and data/raw/guidelines/*.pdf removes the 66 copyrighted
publisher PDFs (~57 MB) from ALL history so the repo is safe for a PUBLIC push. Local copies
are backed up and restored to the working tree (untracked, gitignored) — analysis does not
need them. RESIDUAL rights items flagged for PI: (a) AIDSVu rehosting (above); (b) the two
verbatim CROI transcription markdowns (data/raw/papers/croi2023_*.md) remain tracked — decide
whether to strip those too before public push.

## 2026-08-22 — Strip CROI transcriptions + exclude AIDSVu (rights) ; retrieval script

Two further rights actions before the public push (PI-directed):
- **CROI transcriptions stripped from history.** data/raw/papers/croi2023_luetkemeyer_OA3.md
  and croi2023_molina_doxyvac_slides.md (verbatim third-party conference content) removed from
  ALL git history via filter-repo, gitignored, and restored to the working tree (untracked)
  for local reference. Nothing reads them at runtime (the only code mention is a docstring
  citation in three_outbreak_fit.py). Manuscript + methods references repointed to
  data/raw/papers/SOURCES.md provenance.
- **AIDSVu XLSX excluded (not just from the deposit — from the repo).** The 28 State PrEP/PnR
  XLSX (IQVIA-sourced, "All Rights Reserved") are stripped from history, gitignored, and NOT
  redistributed in the repo or Zenodo deposit. Provenance travels via data/raw/aidsvu/
  SOURCES.md (portal URL + retrieval date 2026-05-25) + CHECKSUMS.md (per-file SHA-256). New
  scripts/fetch_aidsvu.py fetch-and-verifies them; `make all` requires them present+verified.
  DEPOSIT_PATHS updated (aidsvu dir -> its SOURCES/CHECKSUMS + scripts/). README,
  REPRODUCIBILITY.md, THIRD_PARTY_DATA.md updated.

After this, the public git tree and Zenodo compendium contain NO third-party copyrighted
binaries or datasets — only our code, coded values (with locators), generated outputs, the
manuscript, and provenance/hashes for every external input.

## 2026-08-22 — Editable submission formats + author-block bug fix

- **Bug (fixed):** the manuscript YAML `author:` was an UNQUOTED scalar containing
  "Correspondence: " (colon-space), which YAML mis-parses and pandoc coerced to `\author{true}`
  — so the author name rendered NOWHERE in the built PDF (and .tex/.docx). Quoting the scalar
  fixes it; the PDF now shows "Adrian C. Demidont, DO" + the affiliation footnote. This
  affected the v1.0.0 PDF/deposit — re-cut after the fix.
- **Editable submission sources:** added `make tex` (standalone LaTeX + natbib, pairs with
  paper/references.bib) and `make docx` (citeproc + plos.csl, numbered refs baked, figures
  embedded). Both regenerable; gitignored like the PDF. PLoS accepts LaTeX+.bib or .docx;
  medRxiv takes the PDF.

## 2026-09-09 — Coding provenance correction (append-only; no prior entry modified)

The two logged coding passes (`claude-firstpass`, `claude-independent-2nd-pass`)
were the machine coding passes over already-selected documents. Author
identification, retrieval, and eligibility screening of all source documents
preceded them. That screening step was not logged at the time because decision
logging began when the machine coding passes began. No reconstruction of the
timing or sequence of the author's screening pass is claimed — no timestamped
record of it exists. This entry aligns the log with the Methods coding-provenance
paragraph (two independent machine passes; per-field agreement reported as raw
concordance, not independent human adjudication; shared model lineage disclosed as
a limitation).

## 2026-09-12 — Zenodo v2.0.0 (new version) + combined PrEP+PLWH Stream C

Minted a new Zenodo version (doi:10.5281/zenodo.22725070) superseding v1.0.0
(doi:10.5281/zenodo.22051031). The new deposit adds: the combined PrEP+PLWH
Stream C dilution analysis (src/feasibility/dilution_plwh.py, plots_plwh.py;
src/loaders/aidsvu.py load_prevalence; outputs/feasibility_plwh_result.md;
regenerated Stream C figures on the combined denominator), the AIDSVu State
Prevalence 2024 input (hashed in data/raw/aidsvu/CHECKSUMS.md, not redistributed),
and the Journal of Antimicrobial Chemotherapy manuscript package (paper/jac/).
Makefile: `make all` now regenerates the combined-denominator analysis and figures;
DEPOSIT_PATHS points at paper/jac; deposit recipes exclude LaTeX build artifacts.
CITATION.cff bumped to 2.0.0; PA affiliation dropped; both DOIs recorded.
