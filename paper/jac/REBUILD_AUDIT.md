# REBUILD_AUDIT.md — JAC Original Article (current state)

**Release:** v2.0.0 · **Zenodo DOI:** 10.5281/zenodo.22725070 (supersedes v1.0.0,
10.5281/zenodo.22051031). This audit reflects the **current JAC v3 manuscript
state**, which is the canonical submission. Presentation only — no scientific
result was changed at any point in the rebuild.

## Canonical files

| Role | File | Note |
|---|---|---|
| Manuscript source | `paper/jac/JAC_manuscript.tex` | byte-identical to `JAC_manuscript_v3.tex` |
| Manuscript PDF | `paper/jac/JAC_manuscript.pdf` | byte-identical to `JAC_manuscript_v3.pdf` |
| Supplement source | `paper/jac/JAC_supplement.tex` | byte-identical to `JAC_supplement_v3.tex` |
| Supplement PDF | `paper/jac/JAC_supplement.pdf` | byte-identical to `JAC_supplement_v3.pdf` |
| Bibliography | `paper/jac/references.bib` | audit annotations stripped; DOIs in fields |

Versioned `*_v2.*` / `*_v3.*` files are retained as history; the unversioned
aliases track v3.

## Current state (verified)

- **Journal style:** British spelling throughout (JAC IFA); methicillin (not
  meticillin); MIC in mg/L; superscript Vancouver references; structured synopsis.
- **Title (locked):** *Guidance and surveillance capability for bystander
  Staphylococcus aureus tetracycline resistance under doxy-PEP: a three-stream
  evidence audit.*
- **Affiliation:** single — Nyx Dynamics, LLC, Fairfield, CT (the unregistered
  Nyx Institute / Philadelphia affiliation was dropped).
- **Word counts** (reproducible via `scripts/jac_wordcount.py` / `make jac-wordcount`):
  main text **3412** (Introduction–Discussion; limit 3500); synopsis **234**
  (limit 250). Main text rose from 3378 by ~34 words when the reliability
  subsample was disclosed (below); still well under the limit.
- **Dilution specification:** the **combined PrEP+PLWH exposed denominator**
  (AIDSVu 2024; every male person living with HIV counted as exposed) is the
  **primary** specification. PrEP-only indexing (AIDSVu 2022) is retained as the
  more restrictive **sensitivity** specification.
- **Detectability:** primary realistic-cell **RR ≈ 6–28**; PrEP-only sensitivity
  **RR ≈ 14–64**. Metropolitan best cell needs ≈ 2× the densest US geography's
  combined exposure density (Washington, D.C., **6,406 per 100,000 adult males**,
  2024). All values regenerate from `outputs/feasibility_plwh_result.md`.

## Frozen scientific results (unchanged)

HR **3.89** (95% CI 1.42–10.68; 68/393 vs 5/163), attributed to the published
final DoxyPEP trial (not re-estimated) · guidance **0/6** outbreak-matched, **0/10**
coded · surveillance linkage **0/12** · McDougal 69/3 *tet*(K)/*tet*(M) split ·
Mende *tet*(M) p=0.031. Boundaries preserved: no population-level causal claim; no
transmission claim; colonisation ≠ infection; *S. aureus* not collapsed into MRSA;
methicillin vs tetracycline/doxycycline distinct; *tet*(K) vs *tet*(M) distinct.

## Changes since the previous (v1.0.0 / PLOS) audit

- Retargeted PLOS → JAC Original Article; British spelling; combined-denominator
  Stream C primary; figures regenerated on the combined denominator; Table 1
  estimand row; reliability subsample now disclosed (5 of 10 documents, 25
  field-codings, 92% [23/25]); coding described as two blinded LLM passes (not a
  human second coder), correlated-error caveat stated; bibliography sanitised;
  data/code availability now cites doi:10.5281/zenodo.22725070.

All prior audit content (US-spelling conversion notes, the 2702-word count, the
14–64-as-primary figure, and the old DOI) is superseded by the above.
