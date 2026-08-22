# Ecological analysis — preregistration DRAFT (NEVER REGISTERED)

> **Status: DRAFT ONLY. This was never finalised and never timestamped at OSF. The
> ecological design it describes was NOT executed.** It is retained purely as historical
> provenance for how the project began. There is **no OSF preregistration** for this work.

## Why this exists, and why it was abandoned

The project began as a *planned* preregistered ecological analysis — testing whether
population-level doxy-PEP uptake (via a geographic PrEP-density proxy) was associated with
rising tetracycline-resistant *S. aureus*. A Phase-0 feasibility gate was run **before** any
outcome data were touched, and it **failed**: the exposed subgroup is too dilute to move a
population rate at any geographic grain with a population denominator (see
`outputs/feasibility_result.md`, `outputs/feasibility_metro_result.md`). The ecological
design was therefore **not executed**, this preregistration was **left as a draft**, and the
negative feasibility result became Stream C evidence in the measurement-inheritance analysis
that this repository actually reports (see `README.md`, `paper/manuscript.md`).

## The draft plan (as far as it got — not executed)

- Hypothesis (directional), exposure (continuous PrEP-density intensity proxy), outcome
  (tetracycline non-susceptibility in *S. aureus* — with the tet(K)/tet(M) caveat), unit and
  clock.
- Interruption: exogenous, dated, geography-wide (CDC guideline 2024 or SF Oct 2022); never
  individual initiation.
- Estimator: controlled interrupted time series; pre-trend parallelism test and a
  pre-specified fallback estimator if it failed.
- Negative controls (all three) and their pass/fail criteria.

None of the above was carried out; the feasibility gate closed the design first.
