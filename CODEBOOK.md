# CODEBOOK.md

Variable definitions and coding rules for the coded corpora. One YAML per
document under `data/raw/coding/`, built into `data/processed/` by
`src/coding/build_corpus.py`. **Every coded value carries a locator (page or
section). The builder raises on a missing locator; it does not emit a null.**

Coding is single-coder for the first pass; 20% is double-coded and agreement
reported in Phase F (`src/analysis/reliability.py`). Re-verify every field against
the source PDF at a locator — do not trust any external summary, including
CLAUDE.md's "Verified guideline findings."

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

## Stream A — trial schema (Phase C, defined here for continuity)

Unit = one trial. Fields (defined in Phase C, listed for reference): *S. aureus*
measured (y/n); body site; identification method; susceptibility method and
breakpoint standard; phenotype (tetracycline / doxycycline / methicillin); n
colonized per timepoint; powered for the resistance endpoint (y/n); authors
concede underpowering (y/n). Detectability (`src/analysis/detectability.py`) uses
exact binomial / Fisher, not the normal approximation Stream C used.
