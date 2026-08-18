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

Phase 0 (feasibility gate) in progress. The AIDSVu loader and its tests are
complete; downstream phases are gated and not yet implemented.
