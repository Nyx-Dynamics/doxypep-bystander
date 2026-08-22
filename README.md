# doxypep-bystander

**Signal → Mandate → Measurement Inheritance.** A reproducible research compendium asking
whether the systems built around doxycycline post-exposure prophylaxis (doxy-PEP) can
*follow* a bystander antimicrobial-resistance signal the pivotal trial has now detected.

PI: Adrian C. Demidont, DO — Nyx Dynamics, LLC (Fairfield, CT) and Nyx Institute for
Computational Medicine (Philadelphia, PA). ORCID 0000-0002-9216-8569.
Public data only; **no participant-level trial data** are used.

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
  dilute to move a population rate regardless.

The upstream instrument generated information the downstream systems are not built to
receive — a structural gap we call **measurement inheritance**. The paper makes **no
population-level causal claim**. Manuscript: `paper/manuscript.md` (built PDF
`paper/manuscript.pdf`), formatted for PLoS Biology (Meta-Research).

## Provenance: how this project began (and why the original design was not run)

The repository began as a **preregistered-*planned* ecological analysis** — testing whether
population-level doxy-PEP uptake was associated with rising tetracycline-resistant
*S. aureus*. A Phase-0 feasibility gate was run **before** any outcome data were touched, and
it **failed**: because the dilution fraction tracks exposure *density* not headcount, the
exposed subgroup is too dilute to move a population rate at any geographic grain with a
population denominator (median required within-exposed RR ≈ 14; the metro version needs
male-PrEP density many times the densest US geography — see
`outputs/feasibility_result.md`, `outputs/feasibility_metro_result.md`). The ecological
design was therefore **not executed**, and the preregistration **remained a draft**
(`PREREGISTRATION.md`) — there is **no timestamped OSF registration**. That negative
feasibility result is itself Stream C evidence, and it motivated the present
measurement-inheritance analysis.

## Reproducibility

Every figure and table regenerates from public inputs with no manual steps:

```
pip install -r requirements-lock.txt   # exact validated versions
make all                               # test-gated: full pytest suite, then regenerate outputs
make pdf                                # build the manuscript PDF (needs pandoc + pdflatex)
```

See `REPRODUCIBILITY.md` for the environment and expected runtime, `DECISIONS.md` for the
dated analysis-decision log, and `CLAUDE.md` for the full internal build/claim constraints.
Raw data in `data/raw/` is immutable; all cleaning is in code.

## Licensing & third-party data

Code (`src/`, `tests/`, Makefile): **MIT** (`LICENSE-CODE`). Manuscript text and figures:
**CC BY 4.0** (`LICENSE-TEXT`). Externally-sourced inputs are **not** relicensed — see
`THIRD_PARTY_DATA.md`: publisher and guideline PDFs are excluded (provenance travels via
`SOURCES.md` + `CHECKSUMS.md`), and the AIDSVu datasets carry a rights caveat.
