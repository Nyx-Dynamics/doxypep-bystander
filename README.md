# doxypep-bystander

**Signal → Mandate → Measurement Inheritance.** A reproducible research compendium asking
whether the systems built around doxycycline post-exposure prophylaxis (doxy-PEP) can
*follow* a bystander antimicrobial-resistance signal the pivotal trial has now detected.

PI: Adrian C. Demidont, DO — Nyx Dynamics, LLC (Fairfield, CT). ORCID 0000-0002-9216-8569.
Public data only; **no participant-level trial data** are used.

**Archived:** Zenodo [doi:10.5281/zenodo.22725070](https://doi.org/10.5281/zenodo.22725070)
(v2.0.0 — adds the combined PrEP+PLWH Stream C analysis and the JAC manuscript package;
supersedes v1.0.0, doi:10.5281/zenodo.22051031).

## The paper

The DoxyPEP trial's final analysis (Luetkemeyer et al., *Lancet Infect Dis* 2025;25:873–83)
reported a randomised, participant-level result: among those free of doxycycline-resistant
*Staphylococcus aureus* at baseline, doxy-PEP was associated with a **significant increase in
its incidence — HR 3.89 (95% CI 1.42–10.68)** — with no matching effect on carriage, and its
authors called for public-health surveillance of exactly this. This compendium asks the
question that fact raises, across three streams against one yardstick:

- **Stream A — the Signal.** The randomised trial detected the bystander signal (HR 3.89).
- **Stream B — the Mandate.** The guidelines built on the trial counsel about the harm but
  require no *S. aureus* measurement — including in every jurisdiction with a documented
  local CA-MRSA outbreak.
- **Stream C — the Inheritance.** No deployed US surveillance system links doxy-PEP exposure
  to an *S. aureus* tetracycline phenotype at a common population denominator; the
  architecture is standardised around the methicillin axis, and the exposed subgroup is too
  dilute to move a population rate under the realistic surveillance configurations evaluated
  here.

The upstream instrument generated information the downstream systems are not built to
receive — a structural gap we call **measurement inheritance**. The paper makes **no
population-level causal claim**. Manuscript: the current submission is the **Journal of
Antimicrobial Chemotherapy** Original Article in `paper/jac/`
(`JAC_manuscript_v3.tex`/`.pdf`, supplement `JAC_supplement_v3.tex`/`.pdf`, `references.bib`,
`figures/`); the earlier PLoS LaTeX source is retained in `paper/manuscript.tex`.

## Provenance: how this project began (and why the original design was not run)

The repository began as a **preregistered-*planned* ecological analysis** — testing whether
population-level doxy-PEP uptake was associated with rising tetracycline-resistant
*S. aureus*. A Phase-0 feasibility gate was run **before** any outcome data were touched, and
it **failed**: because the dilution fraction tracks exposure *density* not headcount, the
exposed subgroup is too dilute to move a population rate at any geographic grain with a
population denominator (under the primary combined PrEP+PLWH exposed denominator the
realistic-cell required within-exposed RR ≈ 6–28, and the more restrictive PrEP-only indexing
gives ≈ 14–64; the metro version needs exposure density about twice the densest US geography —
see `outputs/feasibility_plwh_result.md`, `outputs/feasibility_result.md`,
`outputs/feasibility_metro_result.md`). The ecological
design was therefore **not executed**, and the preregistration **remained a draft**
(`ECOLOGICAL_PREREGISTRATION_DRAFT_NOT_REGISTERED.md`) — there is **no timestamped OSF registration**. That negative
feasibility result is itself Stream C evidence, and it motivated the present
measurement-inheritance analysis.

## Reproducibility

Every figure and table regenerates from public inputs (one manual step: download the AIDSVu
inputs, below):

```
pip install -r requirements-lock.txt   # exact validated versions
python3 scripts/verify_aidsvu.py       # download AIDSVu inputs manually, then verify (see below)
make all                               # test-gated: full pytest suite, then regenerate outputs
make pdf                                # build paper/manuscript.pdf from paper/manuscript.tex (pdflatex + bibtex)
```

See `REPRODUCIBILITY.md` for the environment and expected runtime, `DECISIONS.md` for the
dated analysis-decision log, `METHODS_streamB.md` for the guideline sampling frame, and the
`CODEBOOK*.md` files for the coding rules.
Raw data in `data/raw/` is immutable; all cleaning is in code.

## Licensing & third-party data

Code (`src/`, `tests/`, `scripts/`, Makefile): **MIT** (`LICENSE-CODE`). Manuscript text and
figures: **CC BY 4.0** (`LICENSE-TEXT`). Externally-sourced inputs are **not** relicensed and
**not** redistributed — see `THIRD_PARTY_DATA.md`: publisher/guideline PDFs, verbatim
conference transcriptions, and the IQVIA-sourced AIDSVu datasets are all excluded, with
provenance travelling via `SOURCES.md` + `CHECKSUMS.md`. AIDSVu is retrieved and verified with
`scripts/verify_aidsvu.py` (which verifies manually-downloaded files against frozen hashes).
