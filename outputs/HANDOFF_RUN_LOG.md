# HANDOFF_RUN_LOG.md — JAC v5 revision pass

**Date:** 2026-09-13 · **Manuscript:** `paper/jac/JAC_manuscript.tex` (canonical) ·
**Target:** JAC Original Article, v5 · **Prior release:** v2.0.0
(Zenodo 10.5281/zenodo.22725070)

Executes the v5 handoff (`paper/jac/UK_data/JAC_v5_handoff.json`) plus the
strategic US-centric refocus. **WHO decision: KEEP** (per author, 2026-09-13) — the
Stream B corpus stays at 10 coded documents; US-centricity achieved via a Scope
paragraph and framing, not corpus surgery. UKHSA 2026 enters as external supporting
evidence in prose only (never in any coded corpus or denominator).

## Counting rule (resolves handoff Q2)

`scripts/jac_wordcount.py` (`make jac-wordcount`): main text = Introduction through
end of Discussion, excluding title page, synopsis, tables, figure legends/alt text,
section headings, in-text citation markers and back matter. This is the JAC IFA
scope. The reviewer's "~3500" counted headings/tables; the deterministic rule gives
**3412 before this pass**.

## Two source-grounded corrections that drove several tasks

1. **Soge benchmark (verified against `data/raw/papers/ciaf089_soge.pdf`, p.1191).**
   Soge's tetracycline-resistant *S. aureus* colonisation is **18% vs 8% → RR ≈ 2.25**
   (the *S. aureus*-matched benchmark). **1.42 is Soge's *gonococcal* figure**
   (NG tetR, >3 doses/mo, RR 1.42, CI 1.10–1.83) — a cross-organism import. The
   manuscript and `detectability.py` already had this right; `dilution.py`'s
   `RR_SOGE=1.42` and `CLAUDE.md`'s yardstick line were the mislabel.
2. **Metro "≈2×" is reproducible (resolves the G01 stale-number flag).** The combined
   PrEP+PLWH metro figure (`plots_plwh.py`, Fig B, msm_frac=1.0, 2024) gives best-cell
   **2.03× the densest US combined density (Washington, D.C., 6406/100k)** against the
   1.42 benchmark. The G01 note's non-reproducible "4.17×" was the *superseded*
   PrEP-only `dilution_metro.py`. The number stands; it is now stated with the
   comparator named (it is comparator-dependent, per T5).

## Task status

| Task | Status | Notes |
|---|---|---|
| T1 phi | **done** | Primary spec uses whole male-PLWH (msm_frac=1); `(male-PrEP+male-PLWH)` is correct, leading `\phi` was spurious (never defined) — deleted in manuscript + supplement. |
| T2 RR_SOGE relabel | **done** | Fig A title now "cross-organism benchmark RR=1.42; *S. aureus*-matched RR=2.25"; Fig 2 uses DET.RR_GC/RR_SAUREUS. `dilution.py`: `RR_SAUREUS=2.25` + `RR_GONOCOCCAL=1.42` added, `RR_SOGE` kept as backward-compat alias. All "Soge … 1.42"-as-*S. aureus*-benchmark strings relabelled to "cross-organism benchmark" across `dilution.py`, `dilution_metro.py`, `dilution_plwh.py`, `streamc_linkage.py`; superseded `outputs/feasibility_*.md` regenerated. Residual "Soge…1.42" adjacencies are all correct (they *label* 1.42 as gonococcal) or documentation. |
| T3 dose-sensitivity | **done** | `dilution_plwh.dose_sensitivity()` added; supplement Table (`tab:dose`) with d∈{0.50,0.75,1.00}: realistic 6.31→4.54→3.65 (DEFF1), 27.5→18.7→14.3 (DEFF25). Main-text invariance sentence softened to state the envelope (holds across realistic range; the realistic lower bound 3.65 dips below HR 3.89 only at the limiting d=1; HR/RR are different estimands). |
| T4 regenerate Fig A | **done** | `plots_plwh.py` title corrected; figure regenerated (300 dpi) and **visually verified** (min cell 1.9, no "Soge optimistic" label). |
| T5 metro comparator | **done** | Main text + supplement name the cross-organism benchmark (RR 1.42); supplement restores the verified 2.03× (≈2×). |
| T6 UKHSA prose | **done** | 3 placements — Intro one-liner, Discussion "Instrument requirements" paragraph, Limitations falsification tweak; `ukhsa2026` bib entry. Prose only; not counted anywhere. |
| T7 compress tet-mechanism | **done** | Cut "not academic"; moved determinant-mobility parenthetical to Supplement S2; tightened Mende. |
| T8 Scope paragraph | **done** | End of Methods; WHO named as international apex reference; counts described as US, not a global census. |
| T9 Ethics subsection | **done** | First Methods subsection; redundant Design-subsection IRB clause removed. |
| T10 Zenodo reference | **done** | `demidont2026compendium` @misc added; cited in Transparency declarations. |
| T11/T13 doc sync | **done** | README (canonical `JAC_manuscript.tex` + `make jac` + PLoS marked historical) and `METHODS_streamB.md` ("20%"→5-of-10 / 25 field-codings / 92% 23/25) updated. Historical release logs (`REPRODUCTION_LOG.md`, `DEPOSIT_CLEANUP_REPORT.md`) intentionally left as point-in-time v2.0.0 records; the current-state canonical pointer is README + this log. |
| T12 one figure writer | **done** | `plots_plwh.py` is now the sole writer of the four shipped PNGs. The superseded writers retarget to `_legacy`/`_preponly` names (`summary_figure.py`→`three_streams_legacy.png`, `dilution.py`→`feasibility_dilution_preponly.png`, `dilution_metro.py`→`*_preponly.png`) and `summary_figure` is dropped from the `make all` figure path. Makefile reordering can no longer change a shipped figure. |
| T14 combined-model tests | **done** | `tests/test_dilution_plwh.py` (6 tests): msm_frac=0 ≡ PrEP-only; PLWH raises f and lowers RR_needed; frozen primary 6.31/27.5/1.79/1.03; dose monotonicity + d=1.0→3.65; no "Soge" in the shipped figure writer. |
| T15 figure hygiene | **done** | Fig 2 in-plot labels ("observed trial HR" / "modelled RR detectability threshold") + verified; dpi 150→300; Supp Fig C alt text corrected (ceiling only "under realistic isolate volumes"). 300 dpi PNG meets the reviewer's fallback (vector not required). |
| T16/T17 language | **done** | Removed "vacuous join", "codified seam", "measurement gap in miniature"; kept "measurement inheritance"; left "distributive observability" (Supplement S6). |
| T18 build/count | **done** (this log) | See below. |

## Validation

- **JAC build:** `make jac` — manuscript + supplement compile clean; **0 undefined
  citations** on the final pass (new keys `ukhsa2026`, `demidont2026compendium`
  resolve; 7 bibtex warnings are the benign corporate-author @misc pattern shared
  with existing `aidsvu`/`luetkemeyer2023croi`).
- **Word count:** main text **3499 / 3500**; synopsis **234 / 250**. NOTE: margin is
  ~1 word — see "Open for author" below.
- **Figures:** regenerated at 300 dpi via `plots_plwh.py` (three_streams, Fig A/B/C);
  combined values confirmed — Stream C bar RR 6.3–27.5, Fig A min 1.9, Fig B 2.03×.
- **Tests:** full suite **117 passed in 166.2s (0 failures, 0 skips)** after all code
  edits — the v2.0.0 baseline of 111 plus 6 new combined-model tests
  (`tests/test_dilution_plwh.py`).
- **Gate robustness (T2 escalation check):** raising the benchmark from 1.42 to 2.25
  does **not** flip any main-text claim — the state gate stays FAIL (best-case
  single-comparison RR_needed 2.87 > 2.25; 0/135 detectable), and the manuscript's
  Stream C numbers (6–28, 1.03, 1.79) are comparator-independent raw RR_needed values.

## Makefile reproducibility audit (`make all`)

Every module referenced by the Makefile exists; no deleted-design module
(`selection_ratchet`, `negative_controls`, `parallel_trends`, `summary_figure`) is
referenced. Three fixes to the `all` recipe:

- **Removed a duplicate `streamc_linkage` run** — it already runs via the
  `feasibility` prerequisite; the recipe invoked it a second time.
- **Removed `architecture_figure`** (writes `measurement_inheritance.png`) — used by
  no shipped artifact (JAC package or historical PLoS `.tex`); only the scratch
  `manuscript.generated.tex` referenced it. A stale run; invoke directly if ever
  needed.
- **Fixed a shipped-figure reproducibility gap:** `linkage_figure` (JAC Fig 1,
  `streamc_linkage.png`) wrote only `outputs/figures/`, so `make all` refreshed the
  analysis copy but not the *shipped* `paper/jac/figures/` copy. It now writes both
  (mirroring `plots_plwh`) at 300 dpi. `plots_plwh` remains the last figure step and
  sole writer of the four combined PNGs.

Stale "canonical = PLoS / *_v3" comments in the Makefile corrected to JAC / *_v4.

## Status: all 18 tasks complete

Metro number **restored** to the main text ("about twice the combined male exposure
density of the densest US geography") with the comparator named; the verified 2.03×
and D.C. 6406/100k sit in the supplement. All reviewer-flagged hygiene cleared.

## Open for author

- **Word-count margin is ~1 word (3499/3500).** The reviewer suggested ~150–200 words
  of slack; reaching it means further trimming the Discussion, which touches your
  calibrated argumentation — left to your discretion.
- **No Zenodo mint / v5 snapshot** created (per handoff ground rule). Canonical
  `JAC_manuscript.tex`/`JAC_supplement.tex` hold the current v5 state; mint a new
  Zenodo version and cut `*_v5.*` snapshots when you're ready to archive.
- **ScholarOne upload** (author-side): manuscript PDF, Fig 1 `streamc_linkage.png` +
  Fig 2 `three_streams.png` as separate files, supplement PDF, cover letter; declare
  LLM use in the cover letter to match the manuscript disclosure.
