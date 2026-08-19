# Stream B inter-coder reliability (Phase F)

First pass: `claude-firstpass` (gl_*.yaml). Second pass: `claude-independent-2nd-pass`
(blind, coded from the source PDFs + codebook only; see
`data/raw/coding/reliability/second_pass.json`). Sample: **5 documents**
spanning all `s_aureus_location` categories, 25 field-codings.

**Overall percent agreement: 92%** (23/25).

Per field:

| field | n | % agreement | Cohen's kappa |
|---|---|---|---|
| bystander_treatment | 5 | 80% | 0.58 |
| host_toxicity_labs | 5 | 100% | 1.00 |
| s_aureus_location | 5 | 100% | 1.00 |
| s_aureus_monitoring | 5 | 80% | 0.00 |
| s_aureus_named | 5 | 100% | 1.00 |

## Disagreements (the codebook-refinement points)

- **nyc_dohmh_2023 / s_aureus_monitoring** — first pass `explicitly_none` vs second `silent`
- **philadelphia_pdph_2024 / bystander_treatment** — first pass `generic_microbiome_resistance` vs second `organism_named`

### Adjudication needed (proposed codebook rules)

- **`s_aureus_monitoring` when a document says 'no laboratory monitoring is
  needed' generally.** Does a blanket no-monitoring statement code as
  `explicitly_none` (it affirmatively denies monitoring, which includes the
  bystander) or `silent` (it is not S. aureus-specific)? Proposed: `explicitly_none`
  — the strongest 'we do not measure it' signal — but this needs a codebook rule.
- **`bystander_treatment` when S. aureus is named ONLY in a reference title.** Does
  a citation-title mention make `bystander_treatment = organism_named`, or does it
  stay at the body-level treatment (`generic_...`) with the mention captured by
  `s_aureus_location = reference_title_only`? Proposed: the latter (organism_named
  requires naming in substantive text), so `s_aureus_location` carries the
  reference mention. Needs a codebook rule.

Kappa is small-N and unstable here; read it with the percent agreement and the
disagreement list. The two disagreements are edge-case rule ambiguities, not
careless errors — resolving them in the codebook and re-coding is the next step.
