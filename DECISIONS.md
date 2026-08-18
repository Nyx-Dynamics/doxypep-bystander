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
