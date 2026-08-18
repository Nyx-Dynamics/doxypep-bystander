# SCAFFOLD.md — build order

Hand this and `CLAUDE.md` to Claude Code. Build in phase order. Do not start a
phase before the previous one's gate passes.

## Repo layout

```
doxypep-bystander/
├── CLAUDE.md                  # project context — read first
├── SCAFFOLD.md                # this file
├── README.md                  # public-facing; includes falsification statement
├── DECISIONS.md               # dated analysis decisions, logged before results
├── PREREGISTRATION.md         # OSF preregistration draft
├── Makefile                   # make all regenerates every figure and table
├── requirements.txt
├── data/
│   ├── raw/                   # immutable; never edited
│   │   ├── aidsvu/            # copied from project
│   │   └── outcomes/          # Phase 1 acquisitions
│   ├── interim/               # generated; gitignored
│   └── processed/             # analysis-ready panels; committed if small
├── src/
│   ├── loaders/
│   │   ├── aidsvu.py          # THE AIDSVu loader — one implementation
│   │   └── outcomes.py
│   ├── feasibility/
│   │   └── dilution.py        # Phase 0 gate
│   ├── panel/
│   │   └── build.py           # state-year panel assembly
│   ├── analysis/
│   │   ├── negative_controls.py   # written and run BEFORE primary
│   │   ├── parallel_trends.py
│   │   └── its.py                 # primary controlled ITS
│   └── figures/
├── tests/
│   ├── test_aidsvu_loader.py  # -1 sentinel, header offset, newline columns
│   └── test_panel.py
├── notebooks/                 # exploration only; nothing load-bearing
└── outputs/
    ├── figures/
    └── tables/
```

## Phase 0 — feasibility gate

**Goal:** determine whether the signal is detectable at all before spending effort
on outcome-data acquisition.

1. `src/loaders/aidsvu.py` — parse all state PrEP and PnR files into one tidy
   frame: `state, year, prep_users, prep_rate, male_prep_rate, pnr, male_pnr`.
   Handle: header at row 4, embedded newlines in column names, `-1` = suppressed
   (must become `NaN`, never zero), stability flags.
   Tests first. This loader is used by everything downstream.

2. `src/feasibility/dilution.py` — the gate. Inputs:
   - state population, MSM population fraction (published estimates)
   - PrEP users per state (from AIDSVu, observed)
   - assumed doxy-PEP uptake among PrEP users (bound it: 20%–55%; Spinelli's clinic
     saw 55%, which is a high-water mark from a San Francisco sexual health clinic
     and should not be treated as national)
   - *S. aureus* isolate volume per state and the fraction plausibly originating
     from this population
   - within-exposed effect size = Soge RR 1.42

   Output: minimum detectable state-level change in tetracycline
   non-susceptibility, with a sensitivity surface across the uptake bound.

3. **Gate.** If the implied state-level change is below plausible surveillance
   noise, stop. Write `outputs/feasibility_result.md` stating the negative result
   and pivot to metro-level (SF, King County, LA, NYC) where uptake density is far
   higher and King County has actual doxy-PEP-era isolate data.

Do not proceed to Phase 1 on optimism.

## Phase 1 — outcome data acquisition

Only if Phase 0 passes, and target whichever geographic level Phase 0 says is
viable.

1. Verify ATLAS coverage first — US *S. aureus*, tetracycline MIC, state
   geography, years spanning 2018–2025. If ATLAS lacks state geography or
   post-2023 years, the national design dies and the metro design is all that
   remains. Check this before writing any ingestion code.
2. Evaluate NHSN/AR Atlas for population mismatch (healthcare-associated vs
   community). Document the decision in `DECISIONS.md` either way.
3. State/county health department extraction: WA first (King County), then CA, NY.
4. `src/loaders/outcomes.py` with tests, same discipline as the AIDSVu loader.

Record, per source: which breakpoint standard (CLSI vs EUCAST), which year's
breakpoints, and whether the reported phenotype is tetracycline or doxycycline.
Breakpoint drift across years is a real confounder and must be in the panel as a
covariate, not discovered later.

## Phase 2 — panel and negative controls

1. `src/panel/build.py` — state-year (or metro-year) panel joining exposure,
   outcome, covariates, and the guideline-release indicator.
2. `src/analysis/parallel_trends.py` — test pre-period slope parallelism between
   high- and low-exposure geographies. **If pre-trends are not parallel, log it and
   change the estimator.** Do not proceed and mention it in limitations.
3. `src/analysis/negative_controls.py` — run and report before the primary
   analysis is written. Methicillin resistance, cisgender women, non-tetracycline
   phenotype.

## Phase 3 — primary analysis

`src/analysis/its.py`. Controlled ITS, calendar time, guideline release as the
interruption, both arms on the same clock, continuous exposure intensity.

Preregister before this runs.

## Phase 4 — write-up

Venue undecided and downstream of what Phase 0–3 produce. If the effect is real
and clean: an ID or AMR journal. If the finding is that the question is
unanswerable with existing surveillance, that is a
surveillance-infrastructure paper and arguably the more important one — it is the
empirical demonstration of the measurement-inheritance thesis.

Either way the repo ships public with code and data, and the README says so
explicitly.

## First commands for Claude Code

```
1. Read CLAUDE.md in full.
2. Scaffold the directory tree above with empty placeholder files and a Makefile.
3. Write requirements.txt (python 3.11, pandas, statsmodels, matplotlib, pytest,
   openpyxl).
4. Write tests/test_aidsvu_loader.py FIRST, against the known file quirks:
   header at row 4, embedded-newline column names, -1 sentinel for suppressed.
5. Then implement src/loaders/aidsvu.py until the tests pass.
6. Stop and report the parsed panel shape and year coverage before continuing.
```

Do not build Phase 1 code speculatively while Phase 0 is unresolved.
