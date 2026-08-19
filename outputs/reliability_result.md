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

## Disagreements and adjudication (2026-08-19)

The two initial disagreements were both codebook edge-cases, not careless errors, and were adjudicated by the PI into binding rules (now in CODEBOOK.md):

- **nyc_dohmh_2023 / s_aureus_monitoring** — first pass `explicitly_none` vs second `silent`
- **philadelphia_pdph_2024 / bystander_treatment** — first pass `generic_microbiome_resistance` vs second `organism_named`

1. **NYC `s_aureus_monitoring`** (`explicitly_none` vs `silent`) → adjudicated to
   **`silent`** (the second coder's stricter reading). The "No laboratory
   monitoring is needed" sentence sits in Dosing and Prescribing, right after the
   NAAT/serology instructions — it answers the safety-bloodwork question, so it is
   `host_toxicity_labs = explicitly_none`, not a decision about microbiological
   surveillance. NYC is now the exact mirror of Chicago (Chicago orders host labs,
   silent on resistance; NYC waives host labs, names staph in counselling) — both
   fail to touch the organism, from opposite directions.
2. **Philadelphia `bystander_treatment`** (`generic_microbiome_resistance` vs
   `organism_named`) → binding rule: a mention only inside a reference title does
   NOT make `organism_named`; the mention is carried by
   `s_aureus_location = reference_title_only`.

## Reporting notes

- **`s_aureus_monitoring` is a descriptive CONSTANT, not a kappa.** After
  adjudication no document in the corpus specifies *S. aureus* monitoring — the
  field collapses to a single value, so chance agreement is 100% and kappa is
  undefined. Report it as: **0 of the coded governmental documents specify
  S. aureus monitoring** (hash-verified staph keyword search, guidelines/CHECKSUMS.md).
  The gate is unanimous, not a gradient with one contested cell.
- **`bystander_treatment` kappa = 0.58 (moderate)** on a five-document sample —
  stated plainly, not rounded up. Both disagreements were resolved into binding
  rules afterward; re-coding under those rules is the follow-through. This belongs
  in the limitations.
- The other fields with variance (`s_aureus_named`, `s_aureus_location`,
  `host_toxicity_labs`) agreed perfectly (kappa 1.0), including the key
  `s_aureus_location` (where the bystander appears), which is the load-bearing
  field for the paper.
