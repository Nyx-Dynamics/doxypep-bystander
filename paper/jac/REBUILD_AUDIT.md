# REBUILD_AUDIT.md — JAC Original Article rebuild

**Scope.** Editorial and structural rebuild of the validated manuscript into a
*Journal of Antimicrobial Chemotherapy* (JAC) Original Article. **No new science.**
Numbers, denominators, effect estimates, and claims are frozen; hierarchy and
framing are rebuilt to read AMR-surveillance-first.

- **Source of truth:** `paper/manuscript.tex` (validated PLOS ONE version, on
  `main`), `references.bib` (= `references-2.bib`), figures from
  `doxypep_tex_and_figures.zip`, repository `outputs/`, Zenodo
  DOI 10.5281/zenodo.22051031.
- **Journal authority:** `JAC_IFA.rtf` (JAC Instructions to Authors). The
  JAC‑Antimicrobial Resistance IFA was **not** used.
- **Template:** `TEMPLATE_PENDING` — no official JAC/OUP LaTeX class supplied;
  output is portable LaTeX to migrate later.
- **Outputs:** `JAC_manuscript.tex` (compiles, 17 pp double-spaced, 0 undefined
  refs), `JAC_supplement.tex` (compiles, 5 pp, 0 undefined refs), this file.

---

## 1. Certifications (required)

- **No new science was added.** No new experiments, searches, coding, simulations,
  sensitivity analyses, causal inference, or re-analysis of participant-level data.
- **No population-level causal claim** appears anywhere. No transmission claim
  appears anywhere.
- **HR 3.89 (95% CI 1.42–10.68; 68/393 vs 5/163; P=0.0044)** remains attributed to
  the **published DoxyPEP trial team** (Luetkemeyer et al., final analysis). The
  text states the trial "performed the appropriate participant-level test itself …
  we cite that randomised result directly and did not re-estimate it."
- ***S. aureus* was not collapsed into MRSA.** *S. aureus* is the analytic unit
  throughout; MRSA is explicitly marked as a subset/wrong-unit near-miss (Results
  Stream C; Discussion "phenotype axis"; Limitations).
- **Colonisation was not recast as infection.** The colonisation/infection
  distinction is preserved and flagged as unmeasured (Limitations).
- **MIC unit:** rendered as **mg/L** per JAC style (was "µg/mL"). This is an
  expression change, not a value change (MIC ≥16).
- **Doxycycline framing:** "one of a limited number of oral options" — no
  irreplaceability claim.

---

## 2. Section map (original → new location)

| Original (PLOS ONE) | New location (JAC) |
|---|---|
| Abstract (unstructured) | **Synopsis** — restructured to JAC headings (Background/Objectives/Methods/Results/Conclusions), ≤250 words |
| Author summary | Already removed on `main` for PLOS ONE; **not carried** (JAC has no such section) |
| Abbreviations (standalone) | Dropped as a section; abbreviations defined at first use per JAC |
| Introduction | **Introduction** (compressed; metascience terms removed from opening) |
| Results → Stream A | **Results → "Stream A: the trials resolved the signal…"** |
| Results → Stream B | **Results → "Stream B: guidance names the risk but instruments nothing"** |
| Results → Stream C | **Results → "Stream C: no deployed system links…"** |
| Results → literature attention | **Results → "The literature mirrors the instrumentation"** |
| Results → cross-stream observability | Condensed into **Discussion** (distributive paragraph) + **Supplement S1** |
| Discussion → Measurement inheritance | **Discussion → "Measurement inheritance"** (moved late, after empirical findings) |
| Discussion → Distributive observability | **Discussion** — compressed to one paragraph |
| Discussion → biologically unresolved | **Discussion → "The phenotype axis…"** + Limitations |
| Discussion → what instrument would answer | **Discussion → "What instrument would answer the question"** |
| Discussion → falsification/limits | **Discussion → "Limitations"** + Conclusions |
| Materials and methods → schema (vector M) | **Supplement S1** (relocated) |
| Materials and methods → design/sources/coding | **Materials and methods** (condensed) + **Supplement S2–S6** |
| Materials and methods → Stream A/B/C detail | **Materials and methods** (summary) + **Supplement S2–S4** (full) |
| Reproducibility | **Supplement S6** + Transparency declarations |
| Supporting information (S1 Text) | **Supplement S2–S4** |
| Declarations (COI/data/AI) | **Acknowledgements** (AI), **Funding**, **Transparency declarations** |

Combined Results/Discussion was **not** used (kept separate; JAC permits either).

---

## 3. Figures and tables (original → disposition)

| Original | Disposition |
|---|---|
| Fig 1 (measurement-inheritance chain; conceptual, no image file) | Relocated to **Supplement Table S1** (measurement vector across streams); not reproduced as a figure (earns no main-text space per JAC "sparingly") |
| Fig 2 (three streams vs reference line) = `three_streams.png` | **Main Figure 2** (detectability), with alt text |
| Fig 3 (surveillance linkage) = `streamc_linkage.png` | **Main Figure 1** (killer figure), with alt text |
| Table (signal propagation across venues) | **Main Table 1** (`tab:propagation`), content unchanged |
| Table (distributive observability ledger) | Compressed to Discussion prose; concept retained in **Supplement S1** |
| — (new) | **Main Table 2** (`tab:audit`) headline audit — built **only** from existing validated counts (HR 3.89; 0/6; 0/10; 0/12; RR≈14–64). No new classification. |
| Feasibility Figs A–C (`feasibility_dilution/metro/metro_breakeven.png`) | **Supplement Figures A–C**, captions unchanged |

Figure renumbering note: the linkage figure (PLOS Fig 3) becomes JAC Figure 1
because it is referred to first in the JAC Results order.

---

## 4. Every numerical result in the new main text (with source)

All trace to the validated manuscript / repository `outputs/`:

- Trial signal **HR 3.89 (1.42–10.68; 68/393 vs 5/163; P=0.0044)**; colonisation
  clearance **HR 1.01 (0.69–1.46)** — Luetkemeyer final analysis.
- Donà survey **91.7%** MRSA-selection concern.
- Interim **0 of 4** comparisons powered; **minimum detectable RR 3.8–5.1** vs
  benchmark **1.42–2.25**.
- Soge benchmark **RR≈2.25** (18% vs 8%, >3 doses/month); cross-organism **1.42**.
- Assay doxycycline, **E-test MIC ≥16 mg/L**.
- Propagation counts **5/31=16%; 16/137=12%; 28/222=13% (5%→13%); 5% vs 4%;
  5%→16%** (Table 1).
- Gonococcus phenotyping unavailable **83% (212/256)**.
- DOXYVAC MRSA carriage **1.8%→9.9%**.
- Guidance **0/6** outbreak-matched; **0/10** coded; **3** name *S. aureus*, **2**
  generic, **1** silent; agreement **92%**, **κ=0.58**.
- Surveillance **0/12**; **2** capture exposure; **0** capture phenotype.
- Dilution **RR≈14–64**; best case **≈1.93**; metro **2.1–33×**; **≈325%** of adult
  males.
- Literature **361 / 13 (3.6%) / 2**.

## 5. Numbers moved out of main text → retained in Supplement

- Full dilution **parameter grids** (uptake, κ, R₀, N) → **S4**.
- **Washington D.C. 2,694 per 100,000** density ceiling → **S4**.
- Interim detectability/duration output pointers → **S2**.
- Measurement-vector **M = {U,E,P,D,T,L,R}** and per-stream table → **S1**.
- Full per-document guideline coding table and 12-system matrix → repository
  (`data/processed/`), pointed to from **S3/S4** (not re-transcribed, to avoid
  introducing transcription error; a stop-condition).

---

## 6. Terminology and style changes (no meaning change)

- Spelling: the rebuild was first written in British spelling (JAC house style),
  then **converted to US spelling at author request** (2026-09-07):
  colonisation→colonization, randomised→randomized, organisation→organization,
  favour→favor, counselling→counseling, summaris*→summariz*, artefact→artifact,
  analysed→analyzed. Note: this **deviates from JAC's British-spelling rule** —
  see the submission checklist. "analyses" (noun) and "orthogonal(ly)" are
  identical in both and were left unchanged.
- "µg/mL" → "mg/L" (JAC MIC rule).
- *tet*(K)/*tet*(M) set in italic-gene style; "methicillin" retained (JAC keeps
  methicillin, not meticillin).
- References converted to **sequential superscript** (natbib `super` +
  `vancouver.bst`); reference list numbered.
- Opening paragraph stripped of metascience jargon ("measurement inheritance"
  introduced only in Discussion).

## 7. Prose merged / removed (with reason)

- Redundant second pass on Mayer/Flores propagation (PLOS repeated it in two
  paragraphs) **merged** into Table 1 + one sentence — repetition removal.
- Extended distributive-observability development (multi-paragraph) **compressed**
  to one Discussion paragraph — handoff positioning rule (avoid a second competing
  centrepiece); full concept retained in Supplement S1.
- Long "scope condition / forced onto MRSA" passage **condensed** into Limitations
  — no boundary condition lost.
- Cross-stream ledger table **converted to prose** — JAC "figures/tables sparingly."

No limitation or boundary condition was deleted.

## 8. References pruned from main text

- `sfdph2022` (San Francisco DPH, a municipal-guidance example) — non-load-bearing
  contextual citation; guidance discussion is unchanged. Remains in `references.bib`.
- `molina2023croi`, `vanderlinden1998` — present in `references.bib`, not cited in
  the JAC main text; available if a reviewer requests expansion.
- No primary source was replaced by a secondary source for brevity.

---

## 9. Verification status

- `JAC_manuscript.tex`: compiles (pdflatex+bibtex×2), **0 undefined citations/
  references**; main-text word count **2702** (Introduction→end of Discussion,
  excluding tables, figure legends/alt text, headings, citations) — within the
  **3500** limit. Synopsis ≤250 words, JAC headings.
- `JAC_supplement.tex`: compiles, **0 undefined refs**, all three feasibility
  figures resolve; every supplement section is cited in the main article.
- **Not committed.** Per handoff `do_not_commit_until`, this package awaits author
  review before any commit.
