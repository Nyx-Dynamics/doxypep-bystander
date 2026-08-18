# SCAFFOLD.md — build order

*Revised 2026-08-18. Stream C is complete; the remaining work is Streams B and A
plus the projection. Read `CLAUDE.md` first.*

## Status

| Stream | What it establishes | State |
|---|---|---|
| C — surveillance | No population grain can detect the signal | **Complete** (needs hardening, below) |
| B — guidelines | The risk is discussed, counselled, and unmeasured | Not started |
| A — trials | Measured non-uniformly, underpowered | Not started |
| Projection | Oral MRSA option set under uncertainty | Not started |

## Repo layout

```
doxypep-bystander/
├── CLAUDE.md              # project context — read first
├── SCAFFOLD.md            # this file
├── README.md              # REWRITE — still describes the dead ecological design
├── DECISIONS.md           # append-only, dated (existing entries are the standard)
├── CODEBOOK.md            # variable definitions, Streams A and B
├── PREREGISTRATION.md     # Stream A schema + detectability, pre-OSF
├── Makefile
├── data/
│   ├── raw/{papers,guidelines,coding,aidsvu}/
│   └── processed/
├── src/
│   ├── feasibility/       # Stream C — dilution.py, dilution_metro.py (DONE)
│   ├── coding/            # schema.py (pydantic), build_corpus.py
│   ├── analysis/
│   │   ├── detectability.py   # Stream A — same units as feasibility
│   │   ├── reliability.py     # double-coding agreement
│   │   └── projection.py
│   └── figures/
│       └── three_streams.py   # THE figure — one reference line at RR 1.42
├── tests/
├── paper/                 # manuscript.md, references.bib
└── outputs/{figures,tables}/
```

**Delete:** `src/analysis/negative_controls.py`, `src/analysis/parallel_trends.py`.
They belong to the abandoned ecological ITS. A gated placeholder implies a phase
that is still coming; these are not.

## Phase A — harden Stream C (do first, it is small)

1. **Panel-power bound.** The MDE assumes one two-proportion comparison; the design
   under test was a panel. Either extend the MDE, or add an explicit statement that
   the best-case cell (RR_needed 1.93 vs 1.42) compounds four simultaneous
   implausibilities and fails on any one alone. This is the referee's first
   objection — answer it in the repo, not in review.
2. **Add κ < 1 to the grid.** Surveillance *S. aureus* skews hospitalized and
   older; the exposed skew young and outpatient. Proportional sampling is generous.
   Justify in `DECISIONS.md` before running.
3. **Model the dose distribution.** Soge's effect attaches to >3 doses/month;
   median use is 3 (IQR 2–6). Replace binary "on doxy-PEP" with the share above
   threshold — roughly halving *f*. Reproducing binary exposure coding is the
   failure mode under description.

Each of these moves the result in a known direction. Log the expected direction in
`DECISIONS.md` before running, so the check is honest.

## Phase B — Stream B (guidelines)

Load-bearing and easiest to falsify. Do it before Stream A.

1. `CODEBOOK.md` — guideline schema: discusses staph risk in background;
   requires staph monitoring; requires patient counselling re commensal resistance;
   harms evidence formally graded; efficacy evidence formally graded. Each field
   y/n **plus locator**.
2. Acquire into `data/raw/guidelines/`: CDC 2024 (MMWR 73(RR-2)), San Francisco
   citywide (Oct 2022), Australian consensus (Cornelisse, Med J Aust
   2024;220:381–6), German DSTIG (Werner, J Dtsch Dermatol Ges 2024;22:466–78),
   ECDC (Mårdh & Plachouras, Euro Surveill 2023;28:2300621).
3. Hand-code to `data/raw/coding/guideline_*.yaml`. No locator, no value.
4. `src/coding/schema.py` (pydantic) + `build_corpus.py`. A record missing a
   locator must **raise**, not validate. Test that first.

**Gate.** If any guideline requires staph monitoring, report and stop for review —
the framing needs revision.

The German and ECDC statements are more cautious than CDC and are the natural
comparators. If they *do* require monitoring, that is not a failure — it is a
finding about US guidelines specifically, and the paper reframes accordingly.

## Phase C — Stream A (trials) and detectability

1. Extend `CODEBOOK.md`: *S. aureus* measured y/n; body site; identification
   method; susceptibility method and breakpoint standard; phenotype (tetracycline /
   doxycycline / methicillin); n colonized per timepoint; powered for the
   resistance endpoint; authors concede underpowering.
2. Code from PDFs: Luetkemeyer NEJM 2023;388:1296–306 (DoxyPEP — nares done, 5%→13%
   among colonized, MRSA null); Grennan CID 2026;82:1054–62 (DuDHS — nares done,
   6 resistant isolates, P=.077, concedes underpowered); Molina Lancet Infect Dis
   2024 + CID substudy (DOXYVAC — full apparatus at gonococcus, no staph); Molina
   Lancet Infect Dis 2018;18:308–17 (IPERGAY OLE); Stewart NEJM 2023;389:2331–40
   (dPEP-KE); Bolan Sex Transm Dis 2015;42:98–103.
   n colonized is often in a figure legend, not a table.
3. `src/analysis/detectability.py` — minimum detectable relative increase in
   doxycycline-resistant *S. aureus* at 80% power, given observed n colonized and
   baseline prevalence. **Exact binomial or Fisher, not normal approximation** —
   these n are small and the approximation will mislead. Note this differs from the
   Stream C MDE, which used the normal approximation at large N; document why the
   methods differ.

## Phase D — the figure

`src/figures/three_streams.py`. Minimum detectable RR per evidence source — one
row per trial, one row per surveillance grain — against a single reference line at
Soge's observed 1.42, with Stream B rendered as "not measured" rather than a
number. If nothing clears the line, this panel is the paper.

## Phase E — projection

Oral MRSA option set (doxycycline, TMP-SMX, clindamycin, linezolid) under a range
of resistance trajectories, with co-resistance structure from Soge — options are
correlated, not independent. Wide bounds are the finding. Label every output
illustrative; do not fit trajectories to data that does not exist.

## Phase F — reliability and write-up

1. `src/analysis/reliability.py` — double-code 20%, report agreement.
2. Rewrite `README.md`: new name/framing, and replace the falsification statement
   (the current one describes the dead ecological design).
3. Reconcile `paper/manuscript.md` against this scaffold — confirm which framing it
   was drafted under before extending it.

Venue candidates: *Clinical Infectious Diseases* (perspective), *Lancet Infectious
Diseases* (comment), *JAC*, or an AMR-policy venue. The companion QSS paper takes
the measurement-inheritance argument; this one stays clinical and empirical.

## First commands for Claude Code

```
1. Read CLAUDE.md in full.
2. Delete src/analysis/negative_controls.py and parallel_trends.py.
3. Phase A item 1 only: add the panel-power bound or the explicit
   compound-implausibility statement to src/feasibility/. Log the choice in
   DECISIONS.md BEFORE implementing.
4. Stop and report.
```

Do not start Stream B coding until Phase A is reviewed.
