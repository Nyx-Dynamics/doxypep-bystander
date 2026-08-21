# doxypep-bystander

Ecological analysis: is population-level doxycycline post-exposure prophylaxis
(doxy-PEP) uptake associated with rising **tetracycline-resistant
*Staphylococcus aureus*** — the bystander organism outside the STI-surveillance
frame — and is any surveillance system even instrumented to detect it?

PI: Adrian C. Demidont, DO — Nyx Institute for Computational Medicine.
Public data only. See `CLAUDE.md` for the precise claim and hard constraints,
`SCAFFOLD.md` for build order.

## The link is ecological — two proxy layers

*S. aureus* isolates carry no sexual-behaviour tag. Geographic PrEP density is a
proxy for doxy-PEP uptake, which is a proxy for cumulative population
doxycycline-days. No output is written as causal; the strongest phrasing is
"consistent with."

## Falsification statement

If tetracycline resistance in *S. aureus* is **flat or declining** in
high-PrEP-density geographies after the guideline interruption, while the three
negative controls (methicillin resistance, cisgender women, a non-tetracycline
phenotype) behave, **the hypothesis is wrong and this repo says so.** That is a
publishable result and it is why the negative controls are mandatory and are
coded before the primary analysis.

## Reproducibility

Every figure and table regenerates from `make all` with no manual steps. Raw
data in `data/raw/` is immutable; all cleaning is in code. The primary analysis
is preregistered (OSF) before any outcome data is touched; this repo ships
public with both code and data.

## Status

**Phase 0 complete — gate FAILED at the state level.** The dilution calculation
shows the doxy-PEP-exposed subgroup is too dilute inside a whole state's
*S. aureus* isolate stream: the within-exposed effect needed to move the
state-level rate detectably exceeds Soge's optimistic RR 1.42 at every plausible
setting (median required RR ≈ 14; see `outputs/feasibility_result.md`). Per the
kill criterion the project pivots to **metro-level** — but the **metro gate also
FAILS** (`outputs/feasibility_metro_result.md`): because the dilution fraction
tracks exposure *density*, not headcount, detection would require male-PrEP
density 2.1× to nearly 500× the densest geography that exists in the US
(Washington D.C.), i.e. more than 100% of males on PrEP under realistic isolate
volumes. Population-scale
ecological sampling dilutes the signal below detectability at every grain with a
population denominator. The only lever that rescues it — high isolate enrichment —
means **targeted sexual-health-clinic sampling** (a cohort design, not
ecological). Two forward paths are on the table: a King County/SF clinic cohort
study, or writing this two-level negative result up as the
surveillance-infrastructure paper (the measurement-inheritance thesis, made
quantitative).

The metro result is **hardened**: a robustness sweep shows the verdict is 0/135
achievable at any realistic metro density (≤2× the densest US geography) and is
insensitive to the male-fraction assumption; a proxy-free break-even shows
detection would require an implausible share of *all* adult males on PrEP (325%
under realistic isolate volumes — impossible; 6.5% even in the fantastical best
case, vs D.C.'s observed 2.7%). See `outputs/feasibility_metro_result.md`.

**Write-up in progress.** The surveillance-infrastructure / measurement-inheritance
paper — the empirical demonstration that no existing surveillance system can
detect the bystander signal — is drafted at `paper/manuscript.md` (with
`paper/references.bib`). Venue-neutral; every quoted figure regenerates from
`make all`. Convert with `pandoc paper/manuscript.md --citeproc -o out.docx`.
Phases 1–3 (outcome-data acquisition and the ITS) remain gated — and, per the
feasibility result, are not the path forward.
