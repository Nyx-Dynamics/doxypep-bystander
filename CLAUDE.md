# CLAUDE.md — doxypep-bystander

Project context for Claude Code. Read this before touching anything.

## What this is

An ecological analysis asking whether population-level doxycycline post-exposure
prophylaxis (doxy-PEP) uptake is associated with rising tetracycline resistance in
*Staphylococcus aureus* — the bystander organism that sits outside the "sexually
transmitted infection" category and therefore outside most doxy-PEP surveillance.

PI: Adrian C. Demidont, DO. Nyx Institute for Computational Medicine.
No institutional affiliation; no restricted-data access (no PhysioNet/MIMIC).
Everything here must run on public data.

## Companion work (already done — cite, don't redo)

- **CID-132517**, correspondence submitted 18 Aug 2026, on Spinelli et al.'s
  misidentified interruption in a doxy-PEP interrupted time series. Establishes
  that this literature's ITS designs conflate a prescription with an event.
  *This repo must not repeat that error.* See "Identification" below.
- **MetaArXiv 150-journal audit** (Demidont): 50 policy units, zero with a code or
  runnable-artifact mandate. Cite for the reproducibility framing.
- A planned QSS case study on measurement inheritance. Separate repo. This repo is
  the empirical arm and should stay empirical.

## The claim, stated precisely

NOT: "doxy-PEP causes MRSA."
NOT: "the field ignored *S. aureus*." (Falsified — DuDHS, DoxyPEP, and Soge all
measured it.)

The claim is that **cumulative doxycycline exposure at population scale is
associated with tetracycline-resistant *S. aureus*, and that no surveillance system
is instrumented to detect it**, because exposure is recorded as a binary
prescription rather than as cumulative drug-days, and the bystander organism is
monitored with far less apparatus than the in-category organism.

## Hard constraints — violate these and the analysis is worthless

1. **The outcome is tetracycline-resistant *S. aureus*, not MRSA.** MRSA
   prevalence in this population is too low to power anything. Soge et al. found
   12/838 isolates (1%), 2 vs 10 by exposure, P=.53. MRSA may appear as a
   *negative control*, never as the primary endpoint.

2. **tetK vs tetM is not a footnote.** tetK (efflux) confers tetracycline
   resistance while leaving doxycycline active; tetM (ribosomal protection) does
   not. A doxy-PEP-eligible-population study found 13.2% tetracycline-resistant but
   2.0% doxycycline-resistant among the *same* isolates. Surveillance that reports
   "tetracycline" susceptibility is therefore loosely coupled to the drug actually
   taken. Any outcome variable must state which it is and carry that caveat into
   the interpretation.

3. **The interruption must be exogenous.** Use the CDC guideline release (2024) or
   the San Francisco citywide guideline (Oct 2022) — dated, external, applying to
   everyone in a geography at once. Never index on individual initiation. This is
   the exact error the CID letter identifies.

4. **Exposure intensity, not exposure status.** Soge: *any* doxy-PEP use was not
   associated with tetR (RR 1.14) or high-level tetR (RR 1.16); >3 doses/month was
   (RR 1.42, 1.45). Median use was 3 doses/month (IQR 2–6). A binary contrast is
   expected to be null. Model a continuous intensity proxy.

5. **The link is ecological and must be labelled as such** in every output.
   *S. aureus* isolates carry no sexual-behaviour tag. Geographic PrEP density is a
   proxy for doxy-PEP uptake, which is a proxy for population doxycycline-days.
   Two proxy layers. State this in the abstract, not the limitations.

## Identification strategy

- **Unit:** state-year (national panel), with a metro-level secondary analysis for
  SF / LA / NYC / Seattle / Chicago.
- **Exposure:** AIDSVu PrEP rate and PrEP-to-Need ratio, 2012–2025 annual. Male
  PrEP rate is the better proxy than overall (doxy-PEP is recommended for MSM and
  transgender women, explicitly *not* for cisgender women).
- **Outcome:** tetracycline non-susceptibility among *S. aureus* isolates.
- **Design:** controlled ITS on calendar time, guideline release as the
  interruption, with high- vs low-PrEP-density states as the contrast. Both arms
  on one clock. Pre-period slopes must be tested for parallelism — if they are not
  parallel, say so and switch to a different estimator rather than proceeding.
- **Negative controls (all three required):**
  - Beta-lactam / methicillin resistance — should NOT move with PrEP density.
  - Cisgender women — doxy-PEP not recommended; same clinics, same geography.
  - A non-tetracycline resistance phenotype in the same isolates.

  If the negative controls move with the exposure, the finding is confounding, and
  the paper reports that. Write the negative-control code before the primary
  analysis code.

## Data

**In repo already** (`data/aidsvu/`, copied from the project):
- State PrEP, annual 2012–2025 (`AIDSVu_State_PrEP_YYYY_*.xlsx`)
- State PrEP-to-Need ratio, annual 2012–2025 (`AIDSVu_State_PnR_YYYY_*.xlsx`)
- County PrEP-to-Need 2019 (`AIDSVu_County_PNR_2019.xlsx`)
- ~35 metro ZIP-level files — these are HIV prevalence/diagnoses/SDOH, **not PrEP**.
  Useful for covariates and metro definition only.

File shape: header junk in rows 1–3, real header row 4, data from row 5.
Columns use embedded newlines (`'State\nPrEP\nRate'`). Missing/suppressed values
are coded `-1`, not blank. Write one loader that handles all of this and use it
everywhere; do not re-parse ad hoc.

**To acquire** (Phase 1, only if Phase 0 passes):
- Pfizer ATLAS — global isolate-level susceptibility, public registration. Verify
  it still carries US *S. aureus* tetracycline MICs with state geography and
  adequate year coverage. This is the linchpin; check it first.
- CDC NHSN / AR Patient Safety Atlas — mostly healthcare-associated, facility
  level. Likely wrong population (hospital, not community). Evaluate, don't assume.
- State health department AR reports — WA (King County has the best doxy-PEP-era
  data), CA, NY. Variable formats, likely manual extraction.

## Phase 0 is a gate, not a warm-up

Before acquiring any outcome data, compute the dilution: what fraction of a
state's *S. aureus* isolates could plausibly originate from doxy-PEP-exposed
people, and what effect size in that subgroup would be needed to move the
state-level rate detectably? Use Soge's RR 1.42 as the optimistic within-exposed
effect.

**Kill criterion:** if the required within-subgroup effect exceeds what Soge
observed, state-level ecological analysis cannot detect this, and the project
pivots to metro-level or to a different design. Write that result up either way —
a documented negative feasibility result is a legitimate output and belongs in the
repo, not in a drawer.

Do not skip this because the data is interesting.

## Conventions

- Python 3.11+. pandas, statsmodels, matplotlib. No proprietary dependencies.
- Every figure and table regenerable from `make all` with no manual steps.
- Raw data immutable in `data/raw/`; never edited in place. All cleaning in code.
- Analysis decisions that could go either way get logged in `DECISIONS.md` with a
  date and a reason, before the result is known.
- Preregister the primary analysis (OSF) before touching outcome data. Given the
  companion critique of a paper that shipped without code or data, this repo goes
  public with both, and the preregistration timestamp matters.
- No result is written up as causal. The strongest available phrasing is
  "consistent with," and the ecological caveat travels with every claim.

## What would falsify this

Say it out loud in the README: if tetracycline resistance in *S. aureus* is flat
or declining in high-PrEP-density geographies after the guideline, while negative
controls behave, the hypothesis is wrong and the paper says so. That is a
publishable result and it is the reason the negative controls are mandatory.
