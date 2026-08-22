# CODEBOOK.md

Variable definitions and coding rules for the coded corpora. One YAML per
document under `data/raw/coding/`, built into `data/processed/` by
`src/coding/build_corpus.py`. **Every coded value carries a locator (page or
section). The builder raises on a missing locator; it does not emit a null.**

Coding is single-coder for the first pass; 20% is double-coded and agreement
reported in Phase F (`src/analysis/reliability.py`). Re-verify every field against
the source PDF at a locator — do not trust any external summary.

## Coded value format

Each field is an object:

```yaml
field_name:
  value: yes | no | partial | na        # controlled vocabulary per field below
  locator: "p. 4, Box 2" | "§Methods"   # REQUIRED, non-empty; page and/or section
  quote: "verbatim text supporting the value"   # strongly encouraged
  note: "coder reasoning if the value is not obvious"   # optional
```

`value` vocabulary: `yes`, `no`, `partial`, `na` (not applicable / not a graded
document). `partial` requires a `note` explaining the boundary.

## Stream B — guideline schema

**Schema and sampling frame in `METHODS_streamB.md` + `src/coding/schema_guideline.py`.**
Scope is governmental public-health authorities only; the schema is the richer
field set (bystander_treatment, s_aureus_location,
in_category_monitoring vs s_aureus_monitoring vs host_toxicity_labs, derived_from
lineage, institutional-memory pairing). The v1 5-field schema below is retained
for history; v1 coded records live in `data/raw/coding/superseded_streamb_v1/`.

### Coding rules from the reliability adjudication (2026-08-19)

Double-coding (`outputs/reliability_result.md`; 92% agreement, 5 docs) surfaced two
edge cases. Rules, now binding so Stream A inherits a tested schema:

1. **A blanket "no laboratory monitoring is needed" statement is a HOST-toxicity
   decision, not a microbiological-surveillance one** (PI adjudication, stricter
   reading). Where such a sentence sits in a dosing/prescribing context (next to
   the safety-bloodwork question — the LFT/CMP/CBC from the package insert), code
   `host_toxicity_labs = explicitly_none` (with the verbatim quote) and
   `s_aureus_monitoring = silent`. Reading it as a refusal to monitor staph would
   attribute a consideration the sentence does not show. `s_aureus_monitoring =
   explicitly_none` is reserved for a statement that specifically addresses
   monitoring FOR S. aureus / a bystander organism. (Consequence: the corpus is
   UNANIMOUS — 0 documents specify S. aureus monitoring — rather than a gradient
   with one contested cell.)
2. **`bystander_treatment = organism_named` requires naming in substantive/body
   text.** A mention **only** inside a cited reference title does NOT make it
   `organism_named`; the document keeps its body-level treatment
   (`generic_microbiome_resistance` or `silent`) and the reference mention is
   carried by `s_aureus_location = reference_title_only`. (Applies to Philadelphia
   and WHO.)

### v1 (retired)

Unit = one guideline document. Metadata: `unit`, `jurisdiction`, `citation`,
`doi`, `source_file`, `coder`, `code_date`.

Coded fields (each y/n/partial + locator):

1. **`discusses_staph_risk`** — Does the document discuss *S. aureus* / MRSA /
   staphylococcal resistance or colonization risk anywhere (background, harms,
   evidence review)? `yes` if named explicitly; `partial` if only "commensal
   organisms" / "other bacteria" without naming staph; `no` if absent.

2. **`requires_staph_monitoring`** — Does the document *require or recommend*
   monitoring, testing, or clinical assessment for *S. aureus* / MRSA / skin-and-
   soft-tissue infection at baseline or follow-up? `yes` / `no`.
   **This is the gate field** (see below).

3. **`requires_counselling_commensal_resistance`** — Does it require providers to
   counsel patients about resistance selection in commensal or non-target
   organisms? `yes` / `no` / `partial`.

4. **`harms_evidence_graded`** — Was the harms / antimicrobial-resistance evidence
   assessed with a formal grading framework (GRADE or equivalent, with explicit
   certainty ratings)? `yes` / `no` / `na` (document is not evidence-graded at
   all — code `na` and set `efficacy_evidence_graded` to `na` too).

5. **`efficacy_evidence_graded`** — Was the efficacy evidence formally graded?
   `yes` / `no` / `na`.

The load-bearing contrast is fields 4 vs 5 within a single document: a graded
efficacy question beside an ungraded harms question is the asymmetry the paper
reports. Code them from the same Methods section and quote both.

## Gate (Phase B)

If any guideline codes `requires_staph_monitoring: yes`, **stop and report** — the
"no system requires measurement" framing needs revision. A `yes` is not a failure;
it is a finding about which guideline, to be reported. The German and ECDC
statements are the most cautious and the likeliest to trip this.

## Stream A — trial schema (Phase C)

See **`CODEBOOK_streamA.md`** — it supersedes this section. In brief: unit = one
trial, but the load-bearing object is one `ResistanceObservation` per *reported
instance* of a result (schema in `src/coding/schema_trial.py`), because the same
DoxyPEP *S. aureus* number is reported with different denominators (5/31, 5/111,
28/222) and different drug labels (doxycycline measured, "tetracycline"
described). Three fields carry the thesis to the assay level:
`mechanism_discriminating` (can the endpoint separate tet(K) efflux from tet(M)
ribosomal protection? — a standard breakpoint cannot, per Grossman 2016 Table 1),
`phenotype_measured` vs `phenotype_as_labeled`, and
`denominator_intervention_affected`. Reporting analyses live in
`src/analysis/observations.py`; detectability
(`src/analysis/detectability.py`, Phase C) uses exact binomial / Fisher, not the
normal approximation Stream C used at large N.
