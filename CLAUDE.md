# CLAUDE.md — doxypep-bystander

Project context for Claude Code. Read this before touching anything.

*Revised 2026-08-18 after the Phase 0 feasibility results. The ecological ITS
design is dead; the feasibility work is not a failed gate but the project's
strongest evidence. See "What changed" at the end.*

**PIVOT 2026-08-21 (Luetkemeyer 2025 Lancet ID final analysis — READ THIS FIRST).**
The DoxyPEP FINAL paper (Lancet Infect Dis 2025;25:873–83, coded in
`data/raw/coding/luetkemeyer2025_saureus_final.yaml`) ran a NEW randomised participant-level
analysis and DETECTED the bystander signal: incident doxy-R *S. aureus*, **HR 3.89 (95% CI
1.42–10.68), p=0.0044** (68/393 vs 5/163); paired colonisation-clearance null HR 1.01. The
paper's frame therefore changed from "the trial cannot see it" to **Signal → Mandate →
Inheritance**: the RCT detected the signal (Stream A); the guidelines require no measurement
of it (Stream B); no deployed surveillance can join exposure to phenotype at a population
denominator (Stream C). The upstream instrument generated information the downstream systems
cannot inherit. The old "trial underpowered / between-arm test non-significant / the ratchet"
framing is RETIRED — `selection_ratchet.py` deleted, its inference superseded by the trial's
own test. No POPULATION-level causal claim is made; the individual-level hazard is the
trial's finding, cited as such. Full log in DECISIONS.md (2026-08-21).

## The hypothesis

Doxycycline is one of a small number of oral agents for outpatient MRSA. Doxy-PEP
applies sustained population-scale tetracycline pressure to networks that
historically amplified community MRSA. **The consequence for outpatient MRSA
treatability cannot be projected from the existing evidence base** — not because
nobody looked, but because:

- **Clinical trials** measured *S. aureus* non-uniformly and at sample sizes that
  cannot support inference;
- **Guidelines** discuss the risk, require patients be counselled about it, and
  require no measurement of it;
- **Surveillance** cannot detect it at any geographic grain with a population
  denominator — demonstrated quantitatively, not asserted.

**This is a claim about evidentiary adequacy and measurement inheritance, not a population
effect estimate.** The trial's final analysis DID detect an individual-level signal
(HR 3.89) and we build on it; any sentence asserting a POPULATION-level causal effect
(that doxy-PEP has been shown to move community MRSA/S. aureus resistance) is a bug. The
deliverable shows the downstream systems cannot inherit the signal the trial resolved —
guidelines mandate no measurement, surveillance cannot link exposure to phenotype — and
quantifies how large an effect surveillance would need to see it.

PI: Adrian C. Demidont, DO. Nyx Institute for Computational Medicine.
No institutional affiliation, no restricted-data access. Public data only.

## The spine: one yardstick, three streams

Every stream answers the same question in the same units — **what within-exposed
relative risk would have been required for this evidence source to detect the
signal?** — benchmarked against the one empirical anchor the literature supplies:

> **RR = 1.42** — Soge et al., CID 2025;80:1188–96. Tetracycline-resistant
> *S. aureus* colonization, >3 doses/month vs none. Note that *any* doxy-PEP use
> was **not** associated (RR 1.14; high-level tetR RR 1.16). Median use 3
> doses/month, IQR 2–6.

- **Stream A (trials):** the Signal. The final trial detected incident doxy-R *S. aureus*
  (HR 3.89); the interim's RR-detectable-at-80%-power (min 3.8–5.1) is now explanatory —
  why the cross-sectional interim read null while the incidence estimand resolved it.
- **Stream B (guidelines):** undefined — nothing is measured. The degenerate case,
  and the point.
- **Stream C (surveillance):** RR needed to move a population rate given dilution.
  **Complete.** State grain: median RR_needed ≈ 14, best case 1.93. Metro grain:
  requires male-PrEP density 2.1×–33× the densest US geography; break-even needs
  325% of adult males on PrEP under realistic isolate volumes.

If Stream A's minimum detectable effects also exceed 1.42, one figure carries the
paper: three streams, one reference line, nothing clears it.

## Verified DoxyPEP primary-source findings (19 Aug 2026)

From the NEJM package obtained 19 Aug (main text, Supplementary Appendix, Protocol,
Data-Sharing Statement — all hashed, all coded-source). Two are load-bearing:

- **The pivotal trial shares no data.** The Data-Sharing Statement (posted 6 Apr
  2023) answers "Will the data collected for your study be made available to
  others?" — **No**, every downstream field an em-dash. Coded `data_availability =
  no`. This is the evidentiary-adequacy floor: the S. aureus discrepancies below
  cannot be settled by re-analysis because the individual-level data is withheld.
- **The keystone: the CROI 2023 abstract (OA-3) instantiates all three streams.**
  `data/raw/papers/croi2023_luetkemeyer_OA3.md` holds the verbatim abstract body +
  data table. Three exhibits in one abstract: (i) the **table caption** relabels the
  pooled result "phenotypic resistance to the **tetracycline antibiotic class**" while
  the S. aureus/Neisseria assays are doxycycline and only GC is tetracycline — the
  tet(K)/tet(M) conflation printed in the trial's own title; (ii) the **conclusion**
  calls a 4.7× per-carrier resistance rise "modest / no significant increase"; (iii)
  the **last sentence** ("surveillance ... is needed"; presentation: "longer term
  monitoring ... is needed") concedes the measurement gap. The GC footnote (TCN-R
  testing unavailable in **83%, 212/256** of GC diagnoses) is Stream C inside the RCT.
- **S. aureus phenotype LABEL mismatch (not a switch, not concealment).** The assay
  was **doxycycline** throughout (E-test MIC ≥16: CROI table, NEJM Trial Procedures,
  Appendix Table 2). "Tetracycline" is only a **label**, and it ORIGINATES in the CROI
  abstract table caption ("tetracycline antibiotic class"); NEJM's End Points sentence,
  CDC, and Szondy inherit it. Coded `saureus_endpoint_label_mismatch = yes`. (Direction
  matters: tetracycline is the broader surrogate, doxycycline the more conservative
  measure — no hidden signal.) *An earlier session over-read this as a "pre-specified
  tetracycline endpoint that was switched"; corrected 2026-08-19 — assay was always
  doxycycline.*
- **CDC/NEJM discrepancy RESOLVED via CROI 2023 OA-3** (Luetkemeyer oral abstract,
  slides in hand: `data/raw/papers/croi2023_luetkemeyer_OA3.md`). CDC's 20/428 and
  28/222 are the CROI S. aureus doxy-R panel (doxy-PEP arm) over the **all-swabbed**
  denominator (5%×428=20; 13%×222=28); assay doxycycline, relabeled "tetracycline."
  **Denominator deflation (the load-bearing new finding, in CDC's own sentence):** CDC
  attributes the rise to "those with S. aureus in their nares" (colonized) but divides
  by all-swabbed 428/222; the colonized counts CDC itself prints are 187 and 69, so
  per-carrier doxy-R is **20/187 = 11% → 28/69 = 41%**, ~3× the reported 5%→13%.
  Doxy-PEP cuts colonization 44%→31%, inflating the all-swabbed denominator and
  deflating the resistance rate over it. Caveat: CROI counts (187/69 colonized, 20/28
  resistant) do **not** reconcile with NEJM Appendix Table 2 (139/31, 12/5) — a venue
  discordance; magnitude is source-dependent, direction robust.

## Verified guideline findings (18 Aug 2026)

From Bachmann LH, Barbee LA, Chan P, et al. MMWR Recomm Rep 2024;73(RR-2):1–8,
verified against full text. Re-verify each with a locator during Stream B coding
rather than trusting this summary.

1. **Graded/ungraded asymmetry in the Methods.** The efficacy question received a
   systematic review with a GRADE evidence-to-decision framework and formal
   ratings (recommendation graded AI: strong, high quality). The harms question —
   explicitly including antimicrobial-resistant pathogen development — received a
   literature review for which evidence was *not graded*. Same document, same
   workgroup. The most important artifact in the project.
2. **Box 2 contains no *S. aureus* monitoring.** Required at follow-up:
   gonorrhea/chlamydia screening at anatomic sites, syphilis serology, HIV
   screening, side-effect assessment, risk-reduction counselling, reassessment of
   need, dose provision. Additional services: hepatitis B/C, vaccination,
   referrals. No staph, no MRSA, no SSTI assessment.
3. **Counselling about the unmeasured harm is required.** Providers must discuss
   potential resistance in other pathogens and commensal organisms and unknown
   long-term effects. Patients must be informed of a harm no system detects.
4. **MRSA dismissed on an underpowered null.** MRSA and ESBL *E. coli*
   colonization trends did not differ between arms — from DoxyPEP, where
   tetracycline-resistant *S. aureus* among those still colonized rose from 5%
   (20/428) to 13% (28/222) at 12 months.
5. **A monitoring recommendation exists — for the wrong organism.** Consideration
   is suggested for pathogens causing community-acquired pneumonia, having just
   reviewed *S. aureus* data and omitted staph.
6. **A positive signal sits in their own citation list.** Reference 24 (Lesens et
   al., Emerg Infect Dis 2007;13:488–90): PVL-positive MSSA more common among
   daily-doxycycline recipients; all PVL-positive doxycycline-resistant MSSA
   isolates occurred in doxycycline takers.

## Stream C — complete, and how to defend it

The dilution analysis (`src/feasibility/`) established that the exposed subgroup is
too dilute inside any population isolate stream. The key insight making it
generalize without metro-specific data: **the dilution fraction tracks exposure
density, not headcount**, so it inverts to a required density comparable against
the densest geography that exists.

**Known vulnerability — fix or bound before write-up.** The MDE assumes a single
two-proportion comparison, but the design under test was a controlled panel (≥50
geographies × ≥10 years). Panel power comes from the cross-sectional gradient and
repeated observation, and could be materially better than a one-shot contrast.
This does not threaten realistic cells — nothing recovers a 14× or 86× gap — but
the best case sits at RR_needed 1.93 against 1.42, only 1.36× away. A referee will
find this. Either extend the MDE to the panel case, or state explicitly that the
best-case cell compounds four simultaneous implausibilities (55% uptake, 5×
enrichment, 13% R0, 100k isolates/geography-year) and fails on any one alone.

**Two arguments that strengthen the result and are not yet claimed:**

- **κ is likely below 1, not above.** Surveillance *S. aureus* comes
  disproportionately from hospitalized and older patients; MSM on PrEP are young
  and outpatient. Proportional sampling (κ=1) is generous, not neutral. Add κ<1 to
  the grid and say so.
- **Uptake overstates exposure.** Soge's association was with >3 doses/month;
  median use was 3 (IQR 2–6). Roughly half of doxy-PEP users sit below the
  threshold at which any effect was observed, which approximately halves *f*
  again. Model the dose distribution rather than treating "on doxy-PEP" as binary
  — reproducing binary exposure coding is the failure mode being described.

## Hard constraints

1. **No causal claim.** The claim is unanswerability, not effect.
2. **tetK vs tetM.** tetK (efflux) leaves doxycycline active; tetM (ribosomal
   protection) does not. A doxy-PEP-eligible-population study found 13.2%
   tetracycline-non-susceptible vs 2.0% doxycycline-non-susceptible among the same
   isolates. Surveillance reporting "tetracycline" is loosely coupled to the drug
   taken. Every coded phenotype records which was measured; the discrepancy is
   itself a Stream C finding — a system that appears to capture the outcome may
   not.
3. **Colonization ≠ infection.** Trials measured nasal colonization; the clinical
   stake is treatment of infection. Grennan states the link is uncertain, and
   beta-lactams remain first-line for many *S. aureus* infections. Steel-man this.
   The honest version: the colonization–infection link is one more thing nobody
   measured.
4. **Do not overstate the MRSA baseline.** MSM identity is not itself a risk factor
   (Amsterdam 0%, Paris 0%, Barcelona 0%, Toronto 1.6%); elevated prevalence
   appears only in behaviorally defined subgroups (de Jong, BMC Infect Dis
   2025;25:299).
5. **The ITS/Spinelli correspondence is a SEPARATE work — keep it out of this
   paper.** The doxy-PEP ITS "time zero" correspondence (and its gonococcal/STI
   reference set: Spinelli, Lopez Bernal, Harrison, Schröder, Miko) belongs to a
   different manuscript. This paper's unit is *S. aureus*; do not re-import those
   citations here.

## Data

`data/raw/papers/` — ciaf234 Spinelli, ciaf043 Grennan/DuDHS, ciaf089-2 Soge,
dkaf066 Schröder, NEJM197905103001903 Harrison, ciaf591 DOXYVAC supplement,
12879_2025 de Jong, R23Y2026N02A0120 Donà, ciag126 Baghdadi.

`data/raw/aidsvu/` — state PrEP and PnR 2012–2025, county PnR 2019, ~35 metro ZIP
files (HIV/SDOH, not PrEP). Loader quirks are documented in `DECISIONS.md`: four
negative suppression sentinels (any negative → NaN, never 0), embedded newlines in
*values* as well as headers, 52 geographies including DC and PR.

Known gap, documented not hidden: no metro/county PrEP density file exists on disk;
SF and King County are absent from the AIDSVu metro set and County PnR 2019 is
suppressed for the target counties. The break-even framing was built to make the
argument without them.

Clinician-concern anchor: Donà et al., Ital J Dermatol Venereol 2026;161:120–5 —
91.7% of surveyed Italian STI-clinic dermatologists named MRSA selection as a
concern, tied with gonococcal resistance as highest-rated; perceived efficacy
chlamydia 47.2%, syphilis 14.3%, gonorrhea 2.8%.

## Conventions

- Python 3.11+. pandas, statsmodels, scipy, matplotlib. No proprietary deps.
- Coded corpus in `data/processed/`, generated from `data/raw/coding/*.yaml` — one
  YAML per document, every value carrying a page or section locator. The builder
  **fails** on a missing locator rather than emitting a null.
- Double-code 20% and report agreement. A one-person audit with no reliability
  estimate is the softness this project criticizes.
- `make all` regenerates every figure and table with no manual steps.
- `DECISIONS.md` append-only, dated, logged before results are known. The existing
  entries are the standard — keep it.
- Preregister the Stream A coding schema and detectability analysis before coding.

## What would falsify this

The old falsification statement (flat resistance in high-PrEP geographies) belongs
to the abandoned ecological design and must be replaced in `README.md`. The current
conditions:

- any guideline requires *S. aureus* monitoring → Stream B leg fails;
- any trial was adequately powered for the resistance endpoint → Stream A leg
  weakens;
- any surveillance system links doxycycline exposure to *S. aureus* phenotype →
  Stream C leg fails;
- the panel-power correction lifts Stream C's realistic cells near 1.42 → the
  quantitative claim needs restating.

**Code Stream B before Stream A**, so the guideline claim is tested early rather
than assumed.

## What changed (2026-08-18)

- Phase 0 was specced as a go/no-go gate. It is not. It is **Stream C evidence**,
  and stronger than the documentary table originally planned.
- The two forward paths in `feasibility_metro_result.md` are not alternatives.
  Path 2 (surveillance-infrastructure paper) is the paper; Path 1 (King County / SF
  clinic cohort) is what the paper *recommends*, and is a separate study with its
  own preregistration.
- `src/analysis/negative_controls.py` and `parallel_trends.py` belong to the dead
  ecological design. Delete them rather than leaving gated placeholders — a
  placeholder implies a phase that is no longer coming.
- `README.md` still describes the ecological framing and the old falsification
  statement. Rewrite it against this file.
