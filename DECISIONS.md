# DECISIONS.md

Dated analysis decisions, logged before results are known. Append-only.

## 2026-08-18 — AIDSVu suppression sentinels are multi-valued, not just `-1`

CLAUDE.md/SCAFFOLD.md documented `-1` as the suppressed code. Inspection of all
28 state PrEP + PnR workbooks (2012–2025) found **four** distinct negative
sentinels in the measure columns: `-1` (548×), `-2` (282×), `-8` (458×),
`-9` (625×). Rates, counts and PrEP-to-Need ratios are never legitimately
negative.

**Decision:** the loader treats *any* negative value in a measure column as
suppressed → `NaN` (never `0`), rather than enumerating the four codes. Robust
to all observed sentinels and to any AIDSVu adds later. If a future measure
column can legitimately be negative, this rule must be revisited.

## 2026-08-18 — Embedded newlines live in data values, not only headers

The PrEP workbooks carry embedded newlines inside *state name cells*
(`'New\nHampshire'`, `'Washington,\nD.C.'`); the PnR workbooks do not. An early
loader normalised only column headers, so those two states failed to join
across the two sources and the outer merge produced 54 phantom geographies
instead of 52.

**Decision:** normalise embedded newlines/whitespace in text *values* (state,
abbreviation) as well as headers, before joining. Regression-tested.

## 2026-08-18 — Geography set

Each file carries 52 geographies: 50 states + DC + Puerto Rico. Kept all 52 for
now; whether territories enter the panel is a Phase 2 decision to be logged when
the exposure contrast (high- vs low-PrEP-density) is defined.

## 2026-08-18 — Phase 0 gate: parameter choices (logged before the result)

Choices for `src/feasibility/dilution.py`, made before running:

- **Exposure proxy = male PrEP users**, not overall PrEP users. doxy-PEP is
  recommended for MSM/trans women, not cis women (CLAUDE.md constraint 5). Added
  `male_prep_users` to the loader for this. The MSM population fraction is *not*
  a separate input: the observed male PrEP-user count already counts the
  reachable exposed population directly, superseding a modelled MSM share.
- **Population denominator backed out of AIDSVu** as `prep_users / prep_rate *
  1e5` rather than importing a Census figure. This recovers AIDSVu's own adult
  denominator (internally consistent with the numerator) and avoids fabricating
  50+ state populations from memory. CA back-out ≈ 33.1M (adult 13+), sensible.
- **Baseline tetR R0 grid = {0.05, 0.10, 0.13}**, central 0.10. 0.13 is the
  tetracycline-resistant fraction observed in a doxy-PEP-eligible population
  (CLAUDE.md constraint 2); community S. aureus tetR is lower.
- **Isolate volume N grid = {1k, 10k, 100k}/state-year.** ATLAS is unacquired
  (Phase 1). N is bounded *generously high* on purpose so a failed gate does not
  hinge on the true N — 100k/state-year exceeds any real US surveillance stream.
- **Enrichment kappa = {1, 3, 5}.** kappa=1 is proportional sampling; up to 5x
  allows the exposed to be over-represented among sampled isolates.
- **Within-exposed RR = 1.42** (Soge, >3 doses/month) as the optimistic ceiling.
- **MDE** via two-proportion normal approx, alpha 0.05 two-sided, power 0.80.

## 2026-08-18 — Phase 0 RESULT: state-level design killed, pivot to metro

Gate FAILED: 0 of 81 grid cells detectable. Best-case (most generous) cell is
Washington D.C. at uptake 55%, 5x enrichment, N=100k, R0=13% → RR_needed = 1.93,
still above Soge's 1.42. Realistic cell (kappa=1, uptake 35%, R0=10%, N=1k) →
RR_needed ≈ 86 (~60x Soge). Median across cells ≈ 14.

**Decision:** abandon the state-level ecological design as primary; pivot to
metro-level (SF, King County, LA, NYC) per SCAFFOLD.md. That the single best
"state" is the city-state D.C. corroborates the direction of the pivot. The
metro design needs its own Phase 0 check (metro population denominators, metro
isolate volumes) before any outcome data is acquired — the state kill does not
transfer. Full write-up: `outputs/feasibility_result.md`.

## 2026-08-18 — Metro Phase 0: also fails; dilution is population-scale, not state-scale

No metro/county PrEP *user or rate* file is on disk — the AIDSVu metro
downloadable datasets (Prevention-Theorem project) carry HIV prevalence/SDOH by
ZIP, not PrEP; County PnR 2019 has only ratios and is suppressed for the target
counties; SF and King County are not even among the 34 available metro files.

Rather than fabricate metro densities, exploited the fact that the dilution
fraction is **population-independent** — `f = MALE_FRACTION * (male_prep_rate/1e5)
* uptake * kappa` (eq. 5). So the gate inverts to a required male-PrEP *density*
and compares it to the densest geography that actually exists in AIDSVu:
**Washington, D.C. at 2,694/100k adult males (2022)** — a city-state, a generous
empirical ceiling for any US metro (SF/King do not exceed it).

- **MALE_FRACTION = 0.5**: adult-male share of the isolate-generating population.
  Justified by AIDSVu internal consistency (male_prep_users/male_prep_rate*1e5 ≈
  adult-male population; over total adult pop ≈ 0.49).
- **ACHIEVABLE_MULTIPLE = 2.0**: a real metro may be at most 2x the densest
  observed US geography. Generous — no US metro is known to exceed D.C.

**Result:** 0 of 81 cells achievable. Least-demanding cell needs 2.1x D.C.'s
density and only under fantastical inputs (N=100k isolates/yr, 5x enrichment, 55%
uptake); realistic cells need 12–33x+ (i.e. >100% of males on PrEP, impossible).

**Decision / interpretation:** the ecological design fails at *both* state and
metro grain because population-scale sampling dilutes the signal below
detectability wherever a population denominator exists. The only lever that
rescues it is enrichment (kappa) — i.e. **targeted sexual-health-clinic sampling**
of *S. aureus* from the exposed population — a cohort design, not ecological.
This is the measurement-inheritance thesis made quantitative. Two forward paths
recorded in `outputs/feasibility_metro_result.md`: (1) a King County / SF clinic
cohort study (different design, own preregistration), or (2) write this two-level
negative result up as the surveillance-infrastructure paper. Choice deferred to PI.
