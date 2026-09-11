# JAC_submission_checklist.md

Populated against `JAC_IFA.rtf` (verified). ✅ done · ⚠️ needs author action · ⏳ pending official template.

## Article type and structure
- ✅ Article type: **Original Article** (published under "Original research").
- ✅ Structured **Synopsis** with headings Background/Objectives/Methods/Results/Conclusions, ≤250 words.
- ✅ Required sections present in order: Synopsis, Introduction, Materials and methods, Results, Discussion, Acknowledgements, Funding, Transparency declarations, References.
- ✅ Main text ≤ **3500 words** (2702; see word-count report).
- ✅ Title page: title, author + full affiliations, corresponding-author contact, **running title**.
- ⚠️ Corresponding-author **telephone/fax**: placeholder in title page — insert real number before submission.

## Style (verified)
- ⚠️ **Spelling: JAC mandates British spelling, but the text was converted to US spelling at author request.** Reconcile before submitting to JAC (revert to British, or confirm the target journal accepts US spelling). **methicillin** (not meticillin) retained.
- ✅ MICs in **mg/L**.
- ✅ *Staphylococcus aureus* italic, abbreviated to *S. aureus* after first use.
- ✅ *tet*(K)/*tet*(M) gene nomenclature.
- ✅ References: sequential **superscript** numerals, placed after punctuation; numbered reference list (`vancouver.bst`).
- ✅ Past tense for study results; present tense for established knowledge.
- ⚠️ Double-spaced, **continuous line numbers, no page numbers**: satisfied in portable source (`lineno`, `\pagestyle{empty}`); re-confirm when migrated to official template.

## Figures and tables
- ✅ Used sparingly: 2 main figures + 2 main tables; feasibility figures relocated to Supplement.
- ✅ **Alt text** provided directly under each figure legend, preceded by "Alt text:".
- ⚠️ Figure sizing to **88 mm / 180 mm** and font specs: source figures are the validated PNGs; confirm/redraw to JAC dimensions at production (content must not change — see figure_rules).
- ✅ Tables cell-based, Arabic numerals, descriptive headings.

## Policies and declarations
- ✅ **Funding** section (unfunded stated).
- ✅ **Transparency declarations** section present, before References; concise, no financial detail.
- ✅ **LLM use** disclosed in Acknowledgements **and** cover letter (JAC requirement); no AI author.
- ✅ **Ethics:** no human-subjects/individual-level data (public data only) — stated in Methods; no approval required.
- ✅ **Data availability:** public data + open code + citable DOI; supplementary data **cited** in the main article.
- ✅ Cover letter states: original/unpublished, not under consideration elsewhere, **not previously submitted to JAC**.
- ✅ Not a clinical trial (no trial registration required for this audit).

## Pending / template
- ⏳ **TEMPLATE_PENDING:** migrate `JAC_manuscript.tex` / `JAC_supplement.tex` into the official JAC/OUP LaTeX template once obtained.
- ⚠️ Open-access vs subscription decision is made **after acceptance** (no charge if subscription selected) — not part of submission files; excluded from cover letter per instruction.

## Compile status
- ✅ `JAC_manuscript.tex` compiles, 0 undefined references.
- ✅ `JAC_supplement.tex` compiles, 0 undefined references, all figures resolve.
