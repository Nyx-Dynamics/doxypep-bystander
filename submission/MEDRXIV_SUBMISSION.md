# medRxiv submission — field-by-field

Copy-paste into the medRxiv submission form. Upload `paper/manuscript.pdf` as the manuscript
file. (medRxiv posts a PDF; the editable `.tex`/`.docx` are for the journal, not medRxiv.)

---

**Title**
Monitoring That the Instrument Cannot Provide: Measurement Inheritance and Tetracycline-Resistant Staphylococcus aureus in Doxycycline Post-Exposure Prophylaxis

**Short/running title**
Measurement inheritance in doxy-PEP bystander resistance

**Article type**
New Results

**Subject area / category** (medRxiv)
Primary: Infectious Diseases (except HIV/AIDS)
Alternates if the primary is unavailable: Public and Global Health; Epidemiology

**Authors**
Adrian C. Demidont, DO — sole author and corresponding author.
Affiliations: (1) Nyx Dynamics, LLC, Fairfield, CT, USA; (2) Nyx Institute for Computational
Medicine, Philadelphia, PA, USA.
ORCID: 0000-0002-9216-8569
Corresponding email: acdemidont@nyxdynamics.org

**Keywords**
doxycycline post-exposure prophylaxis; antimicrobial resistance; Staphylococcus aureus;
public health surveillance; measurement inheritance; meta-research; reproducibility

---

**Abstract** (plain text for the form)

Doxycycline post-exposure prophylaxis (doxy-PEP) reduces bacterial STIs and has been scaled
across sexual-health systems since citywide (San Francisco, 2022) and national (CDC, 2024)
guidance. Doxycycline selects for tetracycline resistance beyond its target organism;
Staphylococcus aureus — a commensal and pathogen that carries mobile tetracycline-resistance
determinants, that once spread community MRSA through the same sexual networks, and for which
doxycycline is one of few oral treatment options — is the natural bystander, with a clinical
stake. The pivotal trial's final analysis has now demonstrated such a signal — a significant
increase in incident doxycycline-resistant S. aureus — and its authors call for public-health
surveillance of it. We ask not whether doxy-PEP drives population-level resistant S. aureus,
but whether the guidance and surveillance now in place could follow the signal the trial
resolved — whether they are instrumented to inherit it at all.

We audit the doxy-PEP evidence base in three streams scored against one yardstick, the
within-exposed effect each could detect: the primary trials, the guidelines built on them,
and population surveillance. All coding carries page/table locators; all sources are
SHA-256-pinned; the surveillance stream decomposes a defined universe of deployed systems and
adds a quantitative feasibility model; every figure and table regenerates from one command.

In its final analysis (as-randomised plus open-label extension), the DoxyPEP trial reports a
statistically significant increase in incident doxycycline-resistant S. aureus under doxy-PEP:
among participants free of it at baseline, hazard ratio 3.89 (95% CI 1.42-10.68, p=0.0044;
68/393 vs 5/163), while the hazard of clearing colonisation did not differ (HR 1.01, p=0.98).
The finding emerged only as the estimand caught up to it: the 2023 interim reported a
cross-sectional resistance fraction (labelled for the "tetracycline class" though the
S. aureus assay was doxycycline, and given three irreconcilable ways across its own venues)
and read it as "modest"; the 2024 federal guideline repeated a 5%-to-13% rise among the
colonised and appended a monitoring call; the 2025 final incidence analysis returned HR 3.89.
The endpoint never changed; the question asked of it did — and the implementation architecture
did not change with it. Every governmental guideline we coded — including all six
jurisdictions with documented local CA-MRSA outbreaks — counsels about the harm while
requiring no measurement of it; and of twelve established surveillance systems none links
doxy-PEP exposure to an S. aureus tetracycline phenotype at a common population denominator.
Of 361 doxy-PEP papers (2015-2026), 13 (3.6%) name a bystander staphylococcal organism and 2
measure it against an exposure contrast.

The randomised trial answered the question it was built to answer. What remains unanswerable
as instrumented is everything downstream of that individual-level fact — whether the signal
propagates into a population externality — because the guidance mandates no S. aureus
measurement and no deployed surveillance system can join exposure to the phenotype at a
population denominator. The upstream instrument generated information the downstream systems
are not built to receive. We offer this as a quantified instance of measurement inheritance,
and make no population-level causal claim.

---

**Funding statement**
None. This work received no funding and was completed independently.

**Competing interest statement**
A.C.D. reports former employment at Gilead Sciences (01/2020–11/2024) with prior ownership of
corporate stock, all divested by 12/2024; Gilead played no role in this work. A.C.D. is sole
owner of Nyx Dynamics, LLC. No other competing interests.

**Author contributions** (single author, CRediT)
A.C.D.: Conceptualization, Methodology, Software, Formal analysis, Data curation,
Investigation, Writing – original draft, Writing – review & editing, Visualization.

**Data availability statement**
All data are public and all analysis code is openly available at
https://github.com/Nyx-Dynamics/doxypep-bystander (release v1.0.0), archived at Zenodo
(DOI 10.5281/zenodo.22725070); every figure and table regenerates via `make all`. No
participant-level trial data were used. Third-party inputs (publisher/guideline PDFs,
conference transcriptions, and the IQVIA-sourced AIDSVu datasets) are not redistributed;
their provenance and SHA-256 hashes travel with the repository.

**Ethics / human subjects**
No ethical approval was required. This is a secondary analysis of publicly available,
aggregate, published data (clinical-trial reports, governmental guidelines, and public
surveillance-system documentation); no participant-level data and no human-subjects research.

**Clinical trial**
Not applicable — this is not a clinical trial (no registration number).

**Dual-use research of concern**
No.

**Use of AI**
A large language model was used for writing and analysis-engineering assistance; the
scientific argument, source reading, model specification, and conclusions are the author's
own; the author verified every value and quotation against primary sources; no AI tool is
credited as an author. (Also stated in the manuscript Declarations.)

**Preprint / concurrent submission note**
This preprint is posted concurrently with submission to a peer-reviewed journal (PLOS Biology,
Meta-Research). The public repository and Zenodo archive are linked above.

**License (medRxiv reuse)**
CC-BY 4.0 (matches the manuscript text license; recommended for maximum reuse).

---

## Files to upload

- **medRxiv:** `paper/manuscript.pdf` (built via `make pdf`; author-block verified present).
- **Journal (PLOS) editable source — pick per their portal:**
  - LaTeX: `paper/manuscript.tex` (`make tex`) + `paper/references.bib` (set the PLOS `.bst`
    at compile, e.g. plos2015.bst; the file uses natbib).
  - Word: `paper/manuscript.docx` (`make docx`) — PLOS numbered references baked in, figures
    embedded. Usually the least-friction editable format.
- Figures for PLOS (uploaded separately at their required resolution): `outputs/figures/*.png`.
