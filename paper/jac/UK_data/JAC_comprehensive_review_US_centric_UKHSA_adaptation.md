# Comprehensive Pre-Submission Review
## Proposed submission to *Journal of Antimicrobial Chemotherapy*
### Manuscript: *Guidance and surveillance capability for bystander Staphylococcus aureus tetracycline resistance under doxy-PEP: a three-stream evidence audit*

**Repository:** https://github.com/Nyx-Dynamics/doxypep-bystander  
**Zenodo:** https://doi.org/10.5281/zenodo.22725070  
**Review date:** 12 September 2026  
**Review scope:** novelty, JAC fit, scientific rigor, completeness, reproducibility, readability, figure quality, and pre-submission readiness, including public code/data audit.

---

# Executive diagnostic

**Recommendation: major revision before submission — targeted, not conceptual.**

The manuscript has a strong and potentially publishable scientific spine. The central contribution is not simply that doxy-PEP may select tetracycline resistance in *Staphylococcus aureus*; that concern is already established. The more original contribution is the empirical demonstration that the United States has a **measurement architecture problem**: a randomized/observational resistance signal exists, US public-health guidance recognizes antimicrobial-resistance concerns, yet deployed US surveillance systems do not link doxy-PEP exposure to the relevant *S. aureus* tetracycline-resistance phenotype at a common denominator.

That is a credible JAC contribution because it connects antimicrobial-resistance epidemiology, antimicrobial stewardship, surveillance design, and implementation policy.

There is **no fatal flaw in the three-stream design**. However, several manuscript/code synchronization problems should be repaired before submission. The most important are:

1. an undefined `\phi` in the manuscript dilution equation that is not present in the executable model;
2. a stale `RR_SOGE = 1.42` label in code/figures/tests, when the manuscript correctly treats the *S. aureus* cross-sectional contrast as approximately 2.25 and 1.42 as a gonococcal comparator;
3. lack of sensitivity analysis for the fixed dose-above-threshold parameter `d = 0.5`;
4. over-interpretation of the panel calculation as a formal surveillance power analysis rather than a simplified detectability bound;
5. repository drift between the current v4 paper, older methods/reproduction documentation, and figure-generation ownership;
6. one visible supplementary figure label and one alt-text statement that are scientifically inaccurate;
7. several JAC-specific submission details that are easily repairable;
8. the policy framing should be made explicitly **US-centric**, with the 2026 UKHSA plan used as an external supportive comparator rather than incorporated into the analytic corpus.

After these repairs, I would expect the paper to be suitable for external peer review at JAC.

---

# 1. Novelty and significance

## Overall assessment

**Novelty: strong if framed narrowly and empirically.**

The paper should not claim novelty for any of the following:

- the proposition that doxy-PEP may select antimicrobial resistance;
- the need to monitor antimicrobial resistance during doxy-PEP implementation;
- the observation that *S. aureus* can acquire tetracycline resistance;
- the general idea that surveillance systems measure what they are designed to measure.

Those points are already established.

The genuinely novel contribution is the **three-stream operational audit**:

1. **Stream A:** the resistance signal demonstrated in doxy-PEP evidence;
2. **Stream B:** whether US governmental doxy-PEP guidance translates that signal into an explicit *S. aureus* monitoring requirement;
3. **Stream C:** whether deployed US surveillance systems can actually observe the exposure–phenotype relationship at a compatible denominator.

The strongest single empirical finding is Stream C:

> US surveillance can observe proxies for doxy-PEP exposure and can observe multiple *S. aureus* resistance phenotypes, but the relevant doxy-PEP exposure and *S. aureus* tetracycline-resistance phenotype are not linked at a common population denominator in the systems audited.

The finding that *S. aureus* surveillance remains structurally centered on the **methicillin axis** is especially persuasive. This gives the paper a concrete surveillance-design mechanism rather than merely documenting absence.

## “Measurement inheritance”

The term is useful, but it should function as a synthesis rather than as a claim to have discovered an entirely new metascientific principle. The manuscript is strongest when “measurement inheritance” describes the empirical finding:

> Current monitoring inherits the variables and organizational structure of pre-existing surveillance systems, so new antimicrobial externalities may remain unobservable even when acknowledged in policy.

That formulation is both defensible and clinically intelligible.

---

# 2. JAC fit

The manuscript is a plausible fit for *Journal of Antimicrobial Chemotherapy* because the paper concerns:

- antimicrobial resistance;
- antimicrobial stewardship;
- resistance epidemiology;
- surveillance capability;
- antimicrobial implementation policy;
- an intervention that is already being operationalized in clinical practice.

The paper should remain framed as an **original empirical evidence audit**, not as a general policy essay or metascience commentary.

The manuscript’s quantitative component helps establish that the identified surveillance gap is not merely administrative: under realistic parameterizations, population-level systems may be insensitive to resistance effects in the range observed among exposed individuals.

### Current JAC-format alignment

The manuscript is already close to the Original Article format:

- structured synopsis: currently within the 250-word limit;
- main text: currently approximately 3412 words, below the 3500-word limit;
- conventional Introduction / Methods / Results / Discussion structure;
- funding and transparency sections;
- figures and supplementary analyses;
- public code and data deposit.

Because several additions are recommended below, approximately **150–200 words should be removed elsewhere** to preserve margin under the 3500-word limit.

---

# 3. Stream A — trial and observational resistance signal

## Strengths

Stream A is scientifically careful.

The manuscript appropriately distinguishes the final randomized time-to-event result from earlier cross-sectional reporting rather than treating them as interchangeable estimates.

The final published trial estimate for *S. aureus* tetracycline resistance is correctly handled as a time-to-event association:

- HR approximately **3.89**
- 95% CI approximately **1.42–10.68**

The manuscript is also correct not to meta-analyse heterogeneous *S. aureus* results across DoxyPEP, DOXYVAC, and other studies when the populations, specimens, resistance definitions, and estimands are incompatible.

The numerator/denominator propagation table is useful and makes an important methodological point: apparent changes across conference, interim, and final outputs may reflect changes in denominator and estimand rather than simple contradiction.

## Recommended wording discipline

Use terms such as:

- “estimand instability”;
- “denominator change”;
- “incompatible resistance measures”;
- “non-equivalent reported effects.”

Avoid implying that differing outputs are necessarily reporting errors unless the underlying source establishes an actual error.

---

# 4. Stream B — US doxy-PEP governmental guidance

## Core result

The outbreak-matched design is defensible and appropriately purposive.

The main result remains:

> **0/6 outbreak-matched US jurisdictions specified active *S. aureus* resistance monitoring in the audited doxy-PEP guidance.**

The expanded governmental-document set supports the same qualitative conclusion.

## Reliability

The current second coding pass covers five documents and 25 coded fields:

- 23/25 raw agreement;
- 92% agreement;
- bystander-treatment κ approximately 0.58;
- the key `s_aureus_monitoring` field is substantively stable.

The fact that the coders were model-based and from the same broad model family should remain transparent because their errors are not statistically independent. That limitation does not invalidate the central field, particularly where the underlying source documents can be directly inspected.

## Repository inconsistency to fix

`METHODS_streamB.md` retains stale language describing a “20% sample,” while the current reliability analysis uses **5/10 documents = 50%**.

This should be synchronized before submission.

---

# 5. US-centric scope: recommended adaptation

## Recommended design decision

**Do not add UKHSA to Stream B or Stream C as another analytic observation.**

The paper should instead become explicitly and consistently **US-specific**.

That produces a cleaner causal and methodological argument:

> **US resistance signal → US guidance → US deployed surveillance → US observability gap.**

The UK experience then functions as **external supportive policy evidence**, not as part of the denominator.

This avoids mixing fundamentally different document and surveillance functions across countries.

## Recommended scope caveat for Methods or end of Introduction

Suggested language:

> **Scope.** This analysis was intentionally restricted to the United States. The guidance documents and surveillance systems evaluated here were selected to determine whether US doxycycline post-exposure prophylaxis implementation is accompanied by surveillance capable of observing tetracycline resistance in a bystander organism. The resulting estimates therefore describe US guidance and surveillance architecture and should not be generalized to doxy-PEP monitoring internationally.

This is enough to prevent reviewers from reading the audit as an attempted global census.

---

# 6. UKHSA 2026 as supportive external evidence

## Why this strengthens the paper

The **UK Health Security Agency published a national doxy-PEP monitoring and evaluation plan on 30 April 2026**, applying to England.

The plan explicitly includes the objective:

- monitoring changes in AMR characteristics of bystander pathogens.

It specifically proposes use of the UKHSA **Second Generation Surveillance System (SGSS)** to monitor tetracycline resistance in bystander organisms such as ***Staphylococcus aureus*** among people aged 18–45 years.

This matters because UKHSA has prospectively recognized the exact externality that the manuscript identifies.

At the same time, the UK plan documents a key limitation:

- SGSS does **not** identify whether individuals have taken doxy-PEP;
- SGSS does **not** contain sexual-orientation information;
- therefore bystander-resistance analysis must rely on indirect ecological contrasts such as regional implementation timing and male:female resistance ratios.

Separately, doxy-PEP provision is captured in England through **GUMCAD**, including the `dPEP` code introduced in 2025.

Thus England provides an unusually strong external comparator:

> a national system can measure doxy-PEP provision and can measure *S. aureus* tetracycline resistance, yet the two measures are not directly linked at the individual exposure–phenotype level.

That observation does **not** weaken the US paper. It strengthens the paper’s policy inference: monitoring bystander resistance requires **purpose-built linkage or sentinel structures**, rather than assuming that routine surveillance systems will automatically answer the question.

## Recommended Discussion paragraph

> England provides an informative external comparator. In 2026, the UK Health Security Agency published a national doxy-PEP monitoring and evaluation plan that explicitly includes antimicrobial-resistance surveillance in bystander pathogens, including tetracycline resistance in *Staphylococcus aureus*. The proposed analysis uses the Second Generation Surveillance System, while doxy-PEP provision is separately captured through GUMCAD. However, the bystander-resistance surveillance data do not identify individual doxy-PEP exposure or sexual orientation, requiring ecological comparisons based on implementation timing, region and sex. Although the UK system was not included in the present US audit, its prospective inclusion of bystander-resistance monitoring supports the need for additional surveillance structures capable of linking doxy-PEP exposure with relevant resistance phenotypes.

## Preferred interpretation

The paper should **not** say:

> “The UK has solved the surveillance problem.”

It has not.

The stronger and more accurate inference is:

> “The UK has explicitly recognized the surveillance requirement and is building an architecture to monitor it; the remaining linkage limitations demonstrate why additional structure is necessary.”

## What to do with WHO

The WHO doxy-PEP guidance is not necessary to the analytic narrative.

Recommended action:

- **remove WHO from the coded or comparative analytic story**;
- retain it only if needed for a generic introductory statement that doxy-PEP guidance is now international.

The manuscript becomes more coherent if its empirical claims remain US-specific.

### Authoritative UKHSA source

UK Health Security Agency. *Monitoring and evaluation plan of doxycycline post-exposure prophylaxis (doxyPEP).* Published 30 April 2026. Applies to England.

https://www.gov.uk/government/publications/doxypep-monitoring-and-evaluation/monitoring-and-evaluation-plan-of-doxycycline-post-exposure-prophylaxis-doxypep

---

# 7. Stream C — deployed US surveillance capability

## Assessment

This is the strongest component of the paper.

The current audit decomposes **12 deployed US systems** and finds:

- systems containing population-level exposure proxies;
- systems containing *S. aureus* resistance information;
- **0 systems providing a population-denominator link between doxy-PEP exposure and *S. aureus* tetracycline phenotype**.

This is the paper’s central operational contribution.

## Methicillin-axis finding

The manuscript effectively demonstrates that major *S. aureus* surveillance infrastructure is historically organized around:

- MRSA/MSSA;
- invasive *S. aureus*;
- hospital-associated or healthcare-associated events;
- methicillin stratification.

Tetracycline susceptibility is not the organizing axis.

This explains *why* the doxy-PEP bystander phenotype is poorly observable rather than merely reporting that it is absent.

## Tone

The scientific argument is strong enough that it does not need rhetorical amplification.

Prefer:

- “no compatible linkage was identified”;
- “the exposure and phenotype are not observed at a shared denominator”;
- “existing systems do not directly identify the exposure–phenotype association.”

Use “vacuous join” and “codified seam” sparingly or remove them.

---

# 8. Quantitative detectability model

## Overall value

The model is useful because it addresses an important reviewer objection:

> Could ordinary population surveillance detect a doxy-PEP-associated *S. aureus* resistance effect even if exposure and resistance data were available?

The model shows why dilution matters.

However, several repairs are essential.

---

## 8.1 Undefined `\phi` — submission blocker

The manuscript and supplement currently include an equation of the form:

```text
f = phi × ((male-PrEP + male-PLWH) density / 10^5) × uptake × d × kappa
```

The executable combined-denominator model does **not** contain `phi`.

The code calculates exposed population from:

- male PrEP users;
- male PLWH cases multiplied by an MSM fraction;
- uptake;
- dose-above-threshold fraction;
- phenotype/capture factor `kappa`.

### Required fix

Either:

1. **remove `\phi` from the manuscript equation**, or
2. explicitly define it and implement it in code.

The cleaner solution is removal unless there is an intended biological or demographic parameter that is missing from the current code.

The manuscript equation must exactly represent the executable model.

---

## 8.2 `RR_SOGE = 1.42` is scientifically mislabelled

An older code path defines:

```python
RR_SOGE = 1.42
```

and identifies this as the Soge comparator.

That is incorrect for the *S. aureus* cross-sectional result used in the current manuscript.

The current manuscript appropriately represents the Soge *S. aureus* contrast as approximately:

- 18% versus 8%;
- RR ≈ **2.25**.

The **1.42** comparator belongs to a gonococcal resistance context, not the primary *S. aureus* comparator.

### Consequences

This stale label affects:

- detectability flags;
- metro calculations;
- supplementary plot annotations;
- tests;
- scientific interpretation of the threshold lines.

It does **not** change the algebraic `RR_needed` itself, but it changes whether a modelled threshold is declared detectable relative to a chosen benchmark.

### Required fix

Replace the ambiguous constant with explicit names:

```python
RR_SAUREUS = 2.25
RR_GONOCOCCAL = 1.42
```

or equivalent.

Remove all scientifically inaccurate uses of `RR_SOGE = 1.42`.

---

## 8.3 Supplementary Figure A contains a visible wrong label

The current supplementary heatmap still labels:

> “Soge optimistic RR = 1.42”

That label should not survive into submission.

Regenerate the figure after correcting the comparator definitions.

---

## 8.4 Dose-above-threshold parameter requires sensitivity analysis

The primary model fixes:

```text
d = 0.5
```

but does not adequately vary it.

Because approximately:

```text
RR_needed - 1 ∝ 1/d
```

the detectability threshold is materially sensitive to this assumption.

For example, if the realistic lower bound is approximately 6.31 at `d = 0.5`, then under `d = 1.0` a rough corresponding threshold is:

```text
1 + (6.31 - 1)/2 ≈ 3.66
```

That is much closer to the observed HR of 3.89.

This does **not** invalidate the model, because:

- HR and RR are different estimands;
- realistic surveillance design effects increase the threshold;
- the primary *S. aureus* cross-sectional comparator is approximately 2.25;
- other dilution assumptions remain conservative.

But the present statement that realistic population thresholds “exceed the trial HR” is not fully robust to the dose parameter.

### Required sensitivity

At minimum calculate:

```text
d ∈ {0.50, 0.75, 1.00}
```

Preferably report the effect in the supplement and summarize it briefly in the main text.

The paper should emphasize the full parameter envelope, not a single `d`.

---

## 8.5 Reframe the panel calculation as a detectability bound

The model currently uses an effective sample size approximation resembling:

```text
N_eff = G × T × N / DEFF
```

This is useful as a bounding calculation.

It is **not** a full longitudinal ecological power model.

Actual identification would also depend on:

- geographic exposure heterogeneity;
- temporal exposure variation;
- secular resistance trends;
- within-geography serial correlation;
- repeated sampling;
- laboratory testing practices;
- exposure misclassification;
- phenotype ascertainment;
- other tetracycline use;
- healthcare sampling structure.

### Recommended terminology

Use:

- “simplified detectability bound”;
- “bounding calculation”;
- “best-case/parameterized surveillance threshold.”

Avoid language implying that the calculation is a formal prospective sample-size or power analysis for a specific national surveillance design.

---

## 8.6 Metro density analysis needs comparator clarity

The metro calculation currently uses the stale 1.42 comparator.

If the calculation is retained, it should either:

1. explicitly identify 1.42 as a deliberately stringent gonococcal benchmark; or
2. compute the required density under **both 1.42 and 2.25**.

The conclusion that the most favorable metro cell requires approximately twice the densest observed US exposure geography is not invariant to the comparator.

Under a 2.25 benchmark, the density requirement can fall substantially.

Therefore this result must not be presented as comparator-independent.

---

# 9. Reproducibility and repository audit

## Strong features

The project is unusually transparent for this type of paper.

The current release documentation reports:

- 111 tests passed;
- CPython 3.12.12;
- locked dependencies;
- reproducible JAC compilation;
- checksums;
- no skipped tests in the release run.

The AIDSVu inputs that cannot be redistributed are appropriately handled through retrieval/checksum provenance rather than silently bundled.

The public repository plus Zenodo archive is a major strength.

## Problems to repair

### 9.1 Two code paths generate the same main figure

`src/analysis/summary_figure.py` still generates the older PrEP-only Stream C range.

`src/feasibility/plots_plwh.py` generates the updated combined PrEP + PLWH figure.

The Makefile happens to execute the newer writer later, so the final `make all` output is correct, but two scripts own the same scientific output.

That is fragile.

### Required fix

Establish **one authoritative writer per figure**.

The older script should either:

- call the combined model;
- stop writing the current manuscript figure;
- or be retired from the production path.

---

### 9.2 `make jac` does not regenerate analysis

The manuscript build compiles the figures that already exist.

A clean reproducibility workflow should make it obvious whether:

```text
make jac
```

means “compile the paper only” or “regenerate analysis and compile the paper.”

If compilation-only is intentional, document it clearly.

A robust top-level production target should regenerate analysis before manuscript compilation.

---

### 9.3 Repository version drift

Several documents still identify v3 as canonical even though the current manuscript is labelled v4.

Since v4 appears to be scientifically identical to v3 except for release/header labeling, a new Zenodo scientific release may not be necessary solely for that comment change.

However, all user-facing repository documentation should agree on:

- current manuscript version;
- canonical archive;
- corresponding commit;
- whether v4 contains scientific changes or only packaging/label changes.

---

### 9.4 Tests should cover the current primary combined model

The test suite retains strong coverage of the older PrEP-only model but lacks dedicated tests for the combined PrEP + PLWH primary path.

Add tests establishing at least:

1. `msm_frac = 0` reproduces the PrEP-only result for the same year;
2. including PLWH increases exposed fraction `f`;
3. including PLWH lowers `RR_needed`;
4. the frozen primary lower-bound value is reproduced;
5. the upper realistic design-effect value is reproduced;
6. the production figure receives the combined-model values;
7. no production output contains the obsolete `Soge 1.42` label.

---

# 10. Completeness of evidence base

## Evidence that should remain central

The manuscript already contains the crucial evidence classes:

- randomized trial;
- observational resistance follow-up;
- governmental doxy-PEP guidance;
- deployed US surveillance architecture;
- quantitative dilution/detectability analysis.

## Add or update

A short literature update should include contemporary evidence that directly bears on the manuscript, particularly:

- 2025/2026 observational data concerning tetracycline-resistant *S. aureus* among doxy-PEP users;
- recent *S. aureus* tetracycline nonsusceptibility/co-resistance epidemiology where relevant;
- UKHSA 2026 as the external surveillance-policy comparator.

Avoid turning this into a general doxy-PEP AMR review. The evidence update should serve the three-stream thesis.

---

# 11. Readability and conceptual economy

## Strengths

The three-stream structure is intuitive.

The manuscript’s core question can be understood quickly:

> A resistance signal exists. Is US policy asking for it to be measured, and can US surveillance actually measure it?

That is excellent narrative architecture.

## Where density increases unnecessarily

The Discussion currently carries several conceptual labels:

- measurement inheritance;
- codified seam;
- distributive observability;
- Goodhart-style arguments;
- externality framing.

Not all are needed.

### Recommendation

Retain **measurement inheritance** as the main conceptual synthesis.

If “distributive observability” remains useful, consider moving it to the supplement or using it once.

The paper will be more persuasive to JAC readers if its primary vocabulary remains:

- resistance phenotype;
- exposure ascertainment;
- surveillance denominator;
- linkage;
- sentinel surveillance;
- detectability;
- externality.

The epidemiology is strong enough to carry the argument without heavy metascientific terminology.

---

# 12. Figures

## Main Figure 1 — surveillance linkage

Conceptually strong.

The 2×2 representation is an effective visual summary of:

- exposure available/unavailable;
- phenotype available/unavailable;
- linkage gap.

The use of shape/hatching as well as colour is a strength for accessibility.

**Recommendation: keep.**

## Main Figure 2 — detectability

The log-scale representation is useful.

However, displaying:

- an observed **hazard ratio**;
- a modelled **risk-ratio threshold**

on the same numeric axis creates a risk of visual equivalence even if the caption explains the estimand difference.

### Recommendation

Label these directly in the plot:

- “Observed trial HR”
- “Modelled RR detectability threshold”

Do not make the reader infer the difference from the caption alone.

## Supplement Figure A

Must be regenerated because of the inaccurate `Soge 1.42` label.

## Supplement Figure C alt text

The current alt text overstates the figure by saying all values lie above both observed density and the physical ceiling.

The caption is more qualified.

The alt text must match the actual plotted result and should not state that all modeled cells exceed the physical ceiling unless that is literally true.

## Resolution

The current PNGs are around 150 dpi.

These are predominantly line/text graphics, so vector output is preferable.

Recommended:

- PDF/SVG/EPS where accepted;
- otherwise export at least 300 dpi at final publication dimensions.

Ensure final label size is readable at JAC column width.

---

# 13. JAC submission housekeeping

Before submission, verify all of the following.

## Word counts

- Synopsis ≤250 words.
- Main text ≤3500 words.
- Preserve enough headroom for the UKHSA paragraph and sensitivity clarification.

## Methods: Ethics heading

JAC instructions call for an Ethics heading as the first Methods section for research involving humans or animals.

This study uses public documentary and aggregate surveillance material rather than individual-level participant research.

For technical-check clarity, add a short first subsection such as:

### Ethics

> This study analysed publicly available guidance, surveillance documentation and aggregate published data and did not involve individual-level human participant data; institutional review board approval was therefore not required.

Adjust to the author’s institutional/legal circumstances as needed.

## Data/software citation

The Zenodo archive should appear as a formal data/software citation in the reference list, not only as a URL in Transparency.

Include the DOI:

> https://doi.org/10.5281/zenodo.22725070

and identify the deposit appropriately as software/data/materials.

## LLM disclosure

The current disclosure is appropriately transparent.

JAC also requires relevant AI/LLM use to be declared in the cover letter.

Ensure the cover letter and manuscript disclosure are mutually consistent.

## Corresponding author information

Check JAC title-page requirements at submission.

The current manuscript includes telephone and e-mail information. If JAC still requires fax on the title page, add it only if the author wishes to provide one and it is current.

---

# 14. Recommended revised manuscript spine

The strongest final paper would read as follows:

### Introduction
1. Doxy-PEP is effective against selected bacterial STIs.
2. Its antimicrobial externalities extend beyond the target organisms.
3. *S. aureus* provides a measurable bystander-resistance phenotype.
4. A surveillance concern only becomes actionable if exposure and phenotype can be observed together.
5. Objective: audit whether US guidance and deployed US surveillance provide that observability.

### Stream A
**What resistance signal has been observed?**

### Stream B
**Does US doxy-PEP governmental guidance specify monitoring of the bystander phenotype?**

### Stream C
**Can deployed US surveillance link doxy-PEP exposure with *S. aureus* tetracycline resistance?**

### Detectability analysis
**If exposure and phenotype were only observed at broad population level, would effects of plausible magnitude be detectable?**

### Discussion
1. Signal exists.
2. US guidance does not operationalize *S. aureus* monitoring.
3. Existing US systems do not link exposure and phenotype.
4. The methicillin-centered surveillance architecture explains the gap.
5. Population-level dilution limits passive detection.
6. England’s 2026 UKHSA plan independently demonstrates recognition of the same bystander-surveillance requirement and the need for additional linkage structures.
7. Policy implication: exposure-linked sentinel surveillance rather than reliance on routine systems alone.

---

# 15. Recommended central conclusion

A tighter central conclusion would be:

> Randomized and observational evidence establishes a doxycycline/tetracycline-resistant *Staphylococcus aureus* signal among doxy-PEP-exposed populations. In the United States, the governmental guidance and deployed surveillance systems audited here do not provide a common denominator linking doxy-PEP exposure to that phenotype, while existing *S. aureus* surveillance remains principally organized around methicillin resistance. Simplified detectability bounds further suggest that routine population surveillance may be insensitive to resistance effects of clinically plausible magnitude under realistic parameterizations. England’s 2026 national monitoring plan independently illustrates the need for purpose-built bystander-resistance surveillance, while also demonstrating the limitations of systems in which exposure and phenotype remain separately observed. US doxy-PEP implementation therefore requires additional exposure-linked sentinel surveillance if the population trajectory of this antimicrobial externality is to be estimated directly.

---

# 16. Priority repair list

## Submission blockers

1. **Remove or define `\phi`** so manuscript and executable model are identical.
2. **Correct the 1.42 comparator throughout code, figures and tests.**
3. **Regenerate Supplementary Figure A.**
4. **Add dose-threshold sensitivity** including `d = 1.0`.
5. **Reframe the panel calculation as a simplified detectability bound.**
6. **Clarify metro results under both 1.42 and 2.25, or explicitly identify the chosen comparator.**

## High-priority reproducibility fixes

7. Establish one authoritative writer for `three_streams`.
8. Add tests for the combined PrEP + PLWH primary model.
9. Synchronize `METHODS_streamB.md`, README, reproduction log, and v4 naming.
10. Ensure the production build regenerates or clearly documents figure provenance.

## Manuscript improvements

11. Make the analytic scope explicitly **US-specific**.
12. Add UKHSA 2026 in the Discussion as **external supportive evidence**, not an analytic observation.
13. Drop WHO from the analytic narrative unless needed for generic background.
14. Add recent *S. aureus* resistance literature selectively.
15. Trim approximately 150–200 words of conceptual/repetitive Discussion prose.
16. Reduce unnecessary metascience terminology.
17. Fix Supplement Figure C alt text.
18. Prefer vector or ≥300 dpi figure output.
19. Add formal Zenodo data/software citation.
20. Add/verify Ethics subsection and cover-letter AI disclosure.

---

# 17. Readiness scorecard

| Domain | Current | After repairs |
|---|---:|---:|
| JAC fit | 8/10 | 9/10 |
| Novelty | 8/10 | 8.5/10 |
| Scientific rigor | 7/10 | 8.5/10 |
| Reproducibility | 8/10 | 9.5/10 |
| Evidence completeness | 7.5/10 | 9/10 |
| Readability | 8/10 | 8.5/10 |
| Figure quality | 7.5/10 | 9/10 |
| Submission readiness | **major targeted revision** | **ready for external review** |

---

# Bottom line

The paper should **not be rebuilt**. Its core design is sound, the three-stream architecture is persuasive, and the public code/data package is substantially stronger than is typical for a policy/surveillance audit.

The needed work is precision work:

- align equations with code;
- repair comparator nomenclature;
- broaden sensitivity around the one assumption that materially affects the detectability headline;
- simplify the interpretation of the panel model;
- synchronize the repository;
- sharpen the paper as an explicitly **US surveillance audit**;
- use the **UKHSA 2026 monitoring plan as external support for the need to build additional US surveillance infrastructure**.

That last adaptation improves the paper. It avoids overclaiming international generalizability while showing that another national public-health authority has independently identified the same bystander-AMR surveillance requirement and has begun constructing dedicated monitoring around it.

---

# Source anchors for the UKHSA adaptation

**UK Health Security Agency.** *Monitoring and evaluation plan of doxycycline post-exposure prophylaxis (doxyPEP).* Published 30 April 2026; applies to England.  
https://www.gov.uk/government/publications/doxypep-monitoring-and-evaluation/monitoring-and-evaluation-plan-of-doxycycline-post-exposure-prophylaxis-doxypep

Key points relevant to this manuscript:

- national monitoring objective explicitly includes AMR changes in **bystander pathogens**;
- proposes SGSS monitoring of **tetracycline resistance in *Staphylococcus aureus*** in people aged 18–45;
- doxy-PEP provision is captured separately through **GUMCAD**, including the `dPEP` code;
- SGSS does not identify **individual doxy-PEP use** or **sexual orientation**;
- bystander-resistance analyses therefore rely on regional rollout, time trends and sex-ratio comparisons rather than direct individual exposure–phenotype linkage.

**JAC / Oxford Academic author instructions** should be rechecked immediately before upload because submission requirements can change.

