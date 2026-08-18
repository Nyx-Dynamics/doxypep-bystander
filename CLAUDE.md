# CLAUDE.md — doxypep-bystander

Project context for Claude Code. Read this before touching anything.

*Revised 2026-08-18 after the Phase 0 feasibility results. The ecological ITS
design is dead; the feasibility work is not a failed gate but the project's
strongest evidence. See "What changed" at the end.*

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

**This is a claim about evidentiary adequacy, not about effect size.** Any sentence
asserting that doxy-PEP causes MRSA is a bug. The deliverable shows the question is
unanswerable as instrumented, and quantifies how large an effect would have to be
to become visible.

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

- **Stream A (trials):** RR detectable at 80% power given observed n colonized.
- **Stream B (guidelines):** undefined — nothing is measured. The degenerate case,
  and the point.
- **Stream C (surveillance):** RR needed to move a population rate given dilution.
  **Complete.** State grain: median RR_needed ≈ 14, best case 1.93. Metro grain:
  requires male-PrEP density 2.1×–33× the densest US geography; break-even needs
  325% of adult males on PrEP under realistic isolate volumes.

If Stream A's minimum detectable effects also exceed 1.42, one figure carries the
paper: three streams, one reference line, nothing clears it.

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
5. **Cite the CID letter, don't re-litigate it.** CID-132517, submitted 18 Aug
   2026, covers the ITS identification problem. One sentence, no more.

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
