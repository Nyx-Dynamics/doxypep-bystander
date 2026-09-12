# JAC_submission_checklist.md (current state — v3 / release v2.0.0)

Verified against `JAC_manuscript.tex` / `JAC_supplement.tex` (canonical = v3).
✅ done · ⚠️ author action.

## Article type and structure
- ✅ **Original Article**; structured **Synopsis** (Background/Objectives/Methods/Results/Conclusions).
- ✅ Required sections in order: Synopsis, Introduction, Materials and methods, Results, Discussion, Acknowledgements, Funding, Transparency declarations, References.
- ✅ Main text **3412 words** (≤3500; `make jac-wordcount`); synopsis **234** (≤250).
- ✅ Title page: locked title, single affiliation (Nyx Dynamics, LLC, Fairfield, CT), running title, corresponding-author telephone **+1-215-901-2366** and full ORCID 0000-0002-9216-8569 (no placeholders).

## Style
- ✅ **British spelling** throughout; **methicillin** (not meticillin); MICs in mg/L.
- ✅ *Staphylococcus aureus* italic, abbreviated *S. aureus* after first use; *tet*(K)/*tet*(M) gene style.
- ✅ Sequential superscript references (vancouver.bst); numbered reference list with no internal audit annotations.
- ✅ Past tense for this study's results; present tense for established knowledge.

## Figures and tables
- ✅ Used sparingly: 2 main figures + 2 main tables; feasibility figures in the Supplement.
- ✅ **Alt text** directly under each figure legend. Fig 2 caption states the trial HR is a magnitude reference, not interchangeable with the surveillance RR threshold.
- ⚠️ Figures sized to 88 mm / 180 mm at production (content unchanged).

## Policies and declarations
- ✅ **Funding** section (unfunded). **Transparency declarations** before References; former Gilead employment (divested 2024) disclosed; no other conflicts.
- ✅ **LLM use** disclosed in Acknowledgements and the cover letter.
- ✅ **Ethics:** public data only, no human subjects — stated in Methods.
- ✅ **Data/code availability:** public repository + Zenodo **doi:10.5281/zenodo.22725070**; supplementary data cited in the main article; every coded source SHA-256-pinned.
- ✅ Cover letter: original/unpublished, not under consideration elsewhere, not previously submitted to JAC; title and affiliation match the manuscript.

## Final numerical results (verified present, unchanged)
- ✅ HR **3.89** (1.42–10.68; 68/393 vs 5/163), attributed to the trial.
- ✅ Guidance **0/6** outbreak-matched, **0/10** coded; surveillance **0/12**.
- ✅ Primary detectability **RR ≈ 6–28** (combined PrEP+PLWH); PrEP-only sensitivity **RR ≈ 14–64**.
- ✅ Reliability disclosed as a subsample (5 of 10 documents, 25 field-codings, 92% [23/25]).
- ✅ No population-level causal claim; no MRSA/*S. aureus* conflation; colonisation ≠ infection.

## Pending / template
- ⚠️ **TEMPLATE_PENDING:** migrate into the official JAC/OUP LaTeX class when obtained.
- Both `.tex` compile clean (0 undefined references); build with `make jac`.
