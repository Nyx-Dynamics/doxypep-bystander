# Stream B denominator reconciliation — de-Jong-anchored purposive sample

Converts Stream B's denominator from a convenience set (jurisdictions assembled by
availability) to a **purposive** one whose selection rule is inherited from the paper's
own clustering evidence: the US jurisdictions where CA-MRSA/USA300 transmission in MSM is
documented. That set is defined by **de Jong 2025 Table 1 and its cited primary outbreak
sources** — the same source whose Table 1 supplies the between-cohort σ̂ in
`dejong_sigma.py`. One source, two structural jobs: the outbreak cities that prove MRSA
is clustered (Stream A) are the cities whose health departments should therefore monitor,
and do not (Stream B).

## Selection rule (for manuscript methods)

> **US jurisdictions with documented CA-MRSA/USA300 transmission or elevated clustered
> colonization in MSM (per de Jong 2025 and the primary outbreak literature it cites)
> that issued standalone governmental doxy-PEP guidance.** The denominator is inherited
> from the same source as the Stream A clustering estimate (`dejong_sigma.py`), so the
> jurisdictions where the bystander concern is epidemiologically grounded are exactly the
> jurisdictions whose guidance is assessed.

Governmental only (state/county/municipal health departments). Clinic and
provider-organization documents are excluded (below), explicitly, not silently.

## Task 1 — US documented-outbreak jurisdiction set (de Jong 2025, Table 1)

| jurisdiction | de Jong Table 1 source | endpoint | note |
|---|---|---|---|
| **San Francisco** | Diep 2008 [13], Ann Intern Med | USA300 MDR infection in MSM | one of de Jong's 3 "distinct clusters"; the canonical MSM-USA300 outbreak |
| **Chicago** | Popovich 2020 [26] | colonization 23% (40/171) MSM | one of de Jong's 3 "distinct clusters" |
| **New York City** | Shastry 2007 [12] | nasal colonization 33% (9/27) MSM w/ SSTI | |
| **Boston** | Szumowski 2009 [27] | colonization cohort, MSM risk factors | matched to Massachusetts state guidance |
| **Los Angeles County** | Lee 2005 [14] | CA-MRSA SSTI, MSM case-control | |
| **San Diego** | Mathews 2005 [16] | CA-MRSA in PLWH, MSM risk factor | |
| **Atlanta** | Hidron 2011 [17] | CA-MRSA infections, MSM risk factor | |

Seven US jurisdictions. International de Jong sites (Toronto, Italy, Paris, Amsterdam,
Brazil, Barcelona, Osaka, Tokyo) are excluded — Stream B's denominator is US governmental
guidance. Each row is traceable to a specific Table 1 citation.

## Task 2 — Intersection with on-disk governmental guidance (three categories)

**Matched** — documented-outbreak city *and* governmental guidance coded (the core
purposive sample). Coded blind; every one leaves *S. aureus* monitoring **silent**:

| jurisdiction | guidance (governmental) | S. aureus monitoring | bystander framing |
|---|---|---|---|
| San Francisco | SFDPH / City Clinic provider guide, 5/2026 | **silent** | generic microbiome ("being studied") |
| Chicago | Chicago CDPH clinical protocol, 2023 | **silent** | silent (bystander not named) |
| New York City | NYC DOHMH Dear Colleague, 2023 | **silent** | *S. aureus* named |
| Boston → Massachusetts | MA DPH fact sheet, 2024 | **silent** | generic microbiome |
| Los Angeles County | LA County DPH fact sheet, 2023 | **silent** | *S. aureus* named |
| San Diego | San Diego HHSA CAHAN advisory, 2023 | **silent** | *S. aureus* named |

**Gap** — documented-outbreak city with no governmental guidance located:

| jurisdiction | resolution |
|---|---|
| Atlanta (Georgia) | **confirmed-none.** No standalone governmental doxy-PEP guidance locatable. Georgia DPH's PEP page is **HIV-PEP only** (HB 1028 standing order; verified by fetch). Atlanta doxy-PEP provision runs through the CDC *Find Doxy PEP* directory listing and the Grady/Ponce de Leon clinic — directory/clinic level, **excluded**. That an outbreak city relies on CDC/clinic provision rather than its own health-department policy is itself a finding, not a hole in the sample. |

**Non-outbreak** — on-disk jurisdiction not in the de Jong outbreak set. Retained under a
**distinct rationale (high-exposure, not documented-outbreak)**, reported separately, not
folded into the outbreak-matched sample:

| jurisdiction | guidance | S. aureus monitoring | lineage |
|---|---|---|---|
| Detroit (MI) | Detroit PH STD protocol, 2022 | silent | adapted from SF City Clinic |
| Maryland / Baltimore | Maryland DOH fact sheet, 2024 | silent | adapted from DC DOH |
| Philadelphia | Philadelphia PDPH health advisory, 2024 | silent | **defer-to-CDC** (see split) |
| Rhode Island / Providence | RI DOH page, 2026 (on disk, **uncoded**) | — | non-outbreak; outside the purposive sample |

**Global tier (separate):** WHO 2026 — not a US subnational jurisdiction; retained in the
national/international corpus, not the subnational denominator.

## Task 3 — DC resolved

Washington DC is a known absence (no doxy-PEP guidance on disk). **DC is NOT a de Jong
documented-outbreak jurisdiction** — it has no Table 1 row (the only "Washington" mention
in de Jong concerns *E. coli* in Washington *State*, a different organism and citation).
Therefore its missing guidance **does not affect the de-Jong-anchored denominator**, and
the absence is explained rather than conspicuous. (Note: Maryland's coding shows DC DOH
materials exist and seeded Maryland's fact sheet, so DC guidance is not absent in general
— but DC is simply outside the purposive outbreak set.)

## Task 4 — Stream B status under the de-Jong rule

The reconciliation required, relative to the prior convenience set:

- **+1 coded (added):** San Francisco — the single most load-bearing outbreak jurisdiction
  (Diep 2008), on disk but previously uncoded. Now coded (`gl_sf.yaml`).
- **1 gap resolved:** Atlanta → confirmed-none (finding: outbreak city, no governmental
  doxy-PEP policy).
- **3 reclassified** from the (implicit) core set to **non-outbreak / high-exposure**:
  Detroit, Maryland, Philadelphia. (RI, on disk but uncoded, is likewise non-outbreak and
  stays outside the purposive sample.)

**Statement:** Under the de-Jong selection rule, the outbreak-matched sample is now
**complete — 6 of 6 documented-outbreak jurisdictions with governmental guidance are
coded, and the one outbreak jurisdiction without guidance (Atlanta) is confirmed-none.**
The three non-outbreak on-disk documents are retained under their own rationale. (Caveat:
"confirmed-none" for Atlanta rests on a targeted search plus a fetch of the Georgia DPH
page; a negative can never be fully closed, but no standalone governmental doxy-PEP
guidance was locatable.)

## Independent vs defer-to-CDC (headline discipline)

The gate must not conflate independent declines with echoes of the CDC gap.

- **Outbreak-matched sample (6):** all six issue **substantive governmental guidance**;
  **none defer to CDC** for their doxy-PEP policy (SF defers to CDC only for STI
  *treatment*, not for its prescribing/monitoring policy). **0 of 6 require or suggest
  *S. aureus* monitoring.**
- **Full US subnational corpus (9, excl. WHO):** the three non-outbreak additions include
  **Philadelphia, which defers to CDC** — titled "Updated Guidance from CDC," every
  substantive claim CDC's. It is a **dependent observation** (inherits CDC's
  non-monitoring), not an independent decline, and is reported separately.

**Optional refinement (applied cleanly, outbreak-matched set):** even naming the organism
is uneven — 3 of 6 name *S. aureus* specifically (NYC, LA County, San Diego), 2 invoke
only a generic "microbiome / antibiotic resistance" (SF, Massachusetts), and 1 is silent
on the bystander entirely (Chicago). All 6, including the 3 that name it, require no
monitoring.

## Lineage / independence within the outbreak-matched six

The same independence test that excluded Philadelphia (a CDC echo) applied *within* the
six, from document content — structure, section ordering, shared passages, stated
derivation. Result:

| jurisdiction | document form | authorship | source | *S. aureus* language |
|---|---|---|---|---|
| San Francisco | provider guide (clinical protocol) | **independent (lineage SEED)** | origin — others adapt from it | generic microbiome ("being studied") |
| Chicago | clinical protocol (7 pp) | **independent** | derived_from none | silent (bystander not named) |
| New York City | Dear Colleague letter | **independent** | derived_from none | "…gonorrhea, **staph infections**, pneumonia, *M. genitalium*…" (lay, Counseling Messages) |
| San Diego | health advisory (CAHAN) | **independent** | derived_from none | "…other pathogens (e.g., ***Staphylococcus aureus***), and commensal *Neisseria*… reservoir for tetracycline-resistant plasmids…" (formal, body text) |
| Los Angeles County | patient factsheet | **adapted — from SF (within the six)** | "Adapted from San Francisco City Clinic, 2022"; carries SF's "What are we still learning?" template | "…bacterial resistance to doxycycline (**for example staph**)?" (still-learning question) |
| Massachusetts | patient factsheet | **adapted — external template** | "Adapted from: DoxyPEP … Fact Sheet" (source not named; structure does **not** match SF's or any of the six) | generic microbiome (not named) |

**Independence tally: 4 of 6 independently authored** (SF, Chicago, NYC, San Diego); 1
(LA County) adapted from SF *within the six*, so SF+LA are one lineage group, not two
independent declines; 1 (Massachusetts) adapted from an unidentified external fact-sheet
template. The two patient factsheets (LA, MA) are **not** the same template — LA carries
SF City Clinic's numbered "still-learning" structure, MA a different "benefits / risks /
how to access" FAQ — so MA's source is not one of the six.

> **Restated headline:** *Of 6 US documented-outbreak jurisdictions with governmental
> doxy-PEP guidance, 4 are independently authored (San Francisco, Chicago, NYC, San
> Diego), 1 (LA County) is adapted from San Francisco, and 1 (Massachusetts) from an
> external fact-sheet template; all six — and all four independent — require or suggest
> **0** S. aureus monitoring. A further jurisdiction (Philadelphia) deferred to CDC and is
> not counted.*

**The organism-naming is independent, not a propagating template — the stronger result.**
Of the three that name *S. aureus*, **two (NYC and San Diego) are independently authored**
and name it in different registers ("staph infections" in a lay counseling list vs the
formal "*Staphylococcus aureus*" with a commensal-*Neisseria*/plasmid mechanism), in
different document types (Dear Colleague vs health advisory). The third (LA County) also
names it ("for example staph") but within the SF-derived template. So the naming is not
one sentence copied across departments: at least two health departments **independently**
named the organism and then, independently, declined to monitor it. That naming-without-
monitoring is a stronger indictment than a single template would be.

## Exclusions (governmental-only, stated)

Clinic and provider-organization documents in `data/raw/guidelines/excluded/` are excluded
with the stated reason: **"excluded — neither carries surveillance authority nor issues
public-health monitoring policy."** These include the FQHC/clinic and professional-society
documents (Callen-Lorde, Fenway, Howard Brown, Open Door Health, ASHA, VOICES) and, for
the Atlanta gap specifically, the Grady/Ponce clinic service and the CDC *Find Doxy PEP*
directory listing.
