# JAC_R3_CHANGELOG.md

Submission-polish pass on the JAC v2 package → **v3**. Presentation only; the
science is unchanged. Source of truth: `JAC_manuscript_v3.tex`,
`JAC_supplement_v3.tex` (both compile clean, 0 undefined references, 0 undefined
control sequences). Every change below is editorial.

Legend: **[S]** = content moved to / retained in Supplement.

---

## Journal style

| Source | Change | Reason | Sci. value |
|---|---|---|---|
| Both files | US → **British spelling** (colonisation, favour, artefact, standardised, etc.); "World Health Organization" preserved as a proper noun; "analyses"/"analysis" unchanged | JAC IFA requires British spelling; reverses the earlier at-author-request US pass | none |
| Supplement opening | Deleted "US spelling is used (at author request)…" | Package now conforms to JAC style | none |
| `methicillin` | Confirmed throughout (not meticillin) | JAC IFA | none |

## BLOCKING corrections (R2 #1, #2)

| Source | Change | Reason | Sci. value |
|---|---|---|---|
| Supplement S3 (Coding) | Replaced "A blinded second coder double-coded…" with the machine-passes account (author screening + two blinded LLM coding passes; raw concordance; κ context-only) | S3 contradicted main-text Methods; "second coder" read as a human | none — describes the same coding, accurately |
| Methods "Sources and coding" + Limitations | "two independent machine passes" / "share a model lineage" → "two separate blinded LLM coding passes run through different interfaces (a command-line agent and a chat interface) but the same model family, so their errors are not independent; the 92% concordance measures reproducibility, not accuracy" | Names the actual failure mode (correlated errors); the two sections now match | none |

## HIGH corrections

| Source | Change | Reason | Sci. value |
|---|---|---|---|
| `references.bib` (refs to CDC, Diep, Liu, Donà, de Jong, van Baelen, CROI, molina, stevens, vanderlinden) | Stripped all audit annotations ("Verified quotes/in corpus", "Not in hashed corpus", PMID notes, n=36, verbatim CDC fragments); promoted DOIs from `note` to `doi` fields | Internal provenance must not appear in the submitted bibliography | none |
| Fig 2 alt text (main) | "14 to 64" → "6 to 28 (primary; 14 to 64 PrEP-only sensitivity)" | Stale PrEP-only number contradicted the combined-denominator primary | none |
| **[S]** Supplement Fig B/C alt text | "male-PrEP density" → "combined PrEP+PLWH exposure density"; "2.7%" → "6.4%"; "on PrEP" → "combined exposure" | Same stale-number fix; alt text is read by reviewers/screen readers | none |
| Metro multiple (main + S4 + Fig B caption) | Unified to "about twice (≈2×)" | Was stated as 1.8× in two places and ≈2× in the Fig B caption | none — same computed cell |

## Figure / alt-text repairs

| Source | Change | Reason | Sci. value |
|---|---|---|---|
| Fig 1 caption + alt | "matrix of twelve US surveillance systems" → "Schematic summary of the 12-system surveillance audit"; removed "column/row" matrix language | Figure is a schematic, not a literal 12-system plot | none |
| Fig 2 caption | Added: "The trial HR is shown as an empirical magnitude reference only; it is not numerically interchangeable with the surveillance RR threshold because the estimands differ." | Figure places HR and RR on one axis; caption must flag the estimand difference | none |
| **[S]** Supplement figures | Loaded the `caption` package so `\caption*` renders cleanly; removed the "Figure N: *" build debris; clean "Figure A/B/C." labels | LaTeX caption artefact | none |

## Methods-language cleanup

| Source | Change | Reason | Sci. value |
|---|---|---|---|
| Methods Stream C + Results + S4 | "closed universe of established US governmental surveillance systems" → "a prespecified set of 12 established US surveillance and data systems plausibly capable of capturing either exposure or phenotype at the required level" | The set mixes system types (AIDSVu, antibiograms, PDMPs, sentinel); avoids overclaiming exhaustiveness | none — **0/12** preserved |

## Compression (main text 3441 → 3378; ≤3400 target met)

| Source | Change | Reason | Moved? | Sci. value |
|---|---|---|---|---|
| "Literature coverage" subsection | Removed from main text; one-line pointer retained | JAC word limit | **[S] S5** (361/13/2 result intact) | none |
| `tet`(K)/`tet`(M) mechanism paragraph | Compressed ≈110 words; kept methicillin⊥tetracycline, tet(K)/tet(M) clinical difference, unresolved mechanism, single-breakpoint concealment, and the McDougal (69/3) and Mende (p=0.031) examples | JAC word limit | no | none |
| Discussion estimand-timeline restatement | Compressed ≈20 words | Redundant with Stream A | no | none |
| Table 1 (reporting-propagation) | **Retained** in main text | Carries the Lancet ID estimand row (load-bearing for the non-citation finding); target met without moving it | no | none |

## Verifications performed (stop-condition checks)

- **R2 #7** gonococcal "83% (212/256)": verified present in the CROI source (`croi2023_luetkemeyer_OA3.md`) — correctly cited to ref 14. No change.
- **R2 #5** metro 1.93 vs 2.59: reconciled and documented — 1.93 was a stale prose value (G01 note in `outputs/feasibility_plwh_result.md`), already removed; current figures regenerate from committed output.

## Flagged for the author (not changed)

- **R2 #6 Affiliation.** Affiliation 2 (Nyx Institute for Computational Medicine, PA) is an unregistered entity; R2 recommends dropping it, leaving Nyx Dynamics LLC (CT). **Judgment call — left as-is per R2's own instruction ("flagging, not deciding").**
- **R2 #9 de Jong reference** author list is "de Jong N, et al." — the co-author names are not on disk, so the list could not be expanded without inventing authors. Needs the author to supply the full list for JAC's author-count rule.

---

## Certifications

- **No new analysis was performed.**
- **No numerical result changed.**
- **HR 3.89 remains attributed to the published DoxyPEP trial** ("the final randomised DoxyPEP trial reported…"); not re-estimated.
- **Guidance count** remains **0/6** outbreak-matched and **0/10** coded.
- **Surveillance linkage count** remains **0/12**.
- **Primary detectability range** remains **RR ≈ 6–28**; **PrEP-only sensitivity** remains **RR ≈ 14–64**.
- **Colonisation was not recast as infection.**
- ***S. aureus* was not collapsed into MRSA**; methicillin and tetracycline resistance not conflated.
- **No population-level causal claim** and **no transmission claim** were introduced.
- **Reproducibility/repository/Zenodo claims** unchanged.
- Both `.tex` files compile cleanly; every figure and table is cited; every main-article figure has alt text directly below its legend.
