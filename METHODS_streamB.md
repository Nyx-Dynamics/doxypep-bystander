# Stream B — sampling frame, scope, and final denominator

*Final methodological record. Written 2026-08-19 while the corpus was fresh; revised
2026-08-22 to the final de-Jong-anchored design. The per-jurisdiction table and the
independence analysis live in `outputs/streamb_denominator_reconciliation.md`; this file is
the narrative methods/provenance.*

## From convenience set to purposive denominator

The frame began as an availability-based set of jurisdictional doxy-PEP policies (assembled
from the NCSD "Doxy and STI PEP Sample Policies" compilation plus apex bodies WHO, CDC,
Australia). It was then **converted to a purposive denominator** whose selection rule is
inherited from the paper's own clustering evidence: the US jurisdictions where CA-MRSA/USA300
transmission in MSM is documented, defined by **de Jong 2025 Table 1 and its cited primary
outbreak sources** — the same source that supplies the between-cohort σ̂ in `dejong_sigma.py`.
One source does two structural jobs: the outbreak cities that prove MRSA is clustered
(Stream A) are the cities whose health departments should therefore monitor, and do not
(Stream B).

## Scope filter (governmental authorities only)

The unit of analysis is a **governmental public-health authority** — city, county, state,
national, or global. These bodies both set doxy-PEP policy and hold the local surveillance /
outbreak record, and that pairing is what makes the comparison meaningful. Clinic and
professional-society documents are excluded (below), explicitly, not silently.

## Final denominator (de-Jong-anchored)

**Outbreak-matched sample — 6 of 6** US documented-outbreak jurisdictions (de Jong 2025
Table 1) with standalone governmental doxy-PEP guidance, each traceable to a Table 1 outbreak
citation: San Francisco (Diep 2008), Chicago (Popovich 2020), New York City (Shastry 2007),
Boston → Massachusetts (Szumowski 2009), Los Angeles County (Lee 2005), San Diego (Mathews
2005). The one outbreak jurisdiction without governmental guidance — **Atlanta** — is
confirmed-none (doxy-PEP provision runs through the CDC directory / Grady clinic, not a
health-department policy). Three on-disk documents fall **outside** the outbreak set and are
retained under a distinct high-exposure rationale, reported separately (Detroit, Maryland,
Philadelphia); Philadelphia defers to CDC and is a dependent observation, not an independent
decline. WHO (global tier) is kept in the international corpus, not the subnational
denominator.

## Coding and reliability

Ten governmental documents are coded (`data/raw/coding/gl_*.yaml`), each value carrying a
page/section locator. Coding was **double-coded** — a blind independent second pass on a
5-of-10-document subsample (25 field-codings)
(`data/raw/coding/reliability/second_pass.json`); **92% agreement (23/25)**, Cohen's κ per
field, and the two edge-case disagreements were adjudicated by the PI into binding CODEBOOK
rules (`outputs/reliability_result.md`, `CODEBOOK.md`). The coding is PI-verified.

## Result

Under the de-Jong selection rule, **0 of 6** outbreak-matched jurisdictions require or suggest
*S. aureus* monitoring. Within the six, **4 are independently authored** (SF, Chicago, NYC,
San Diego), 1 (LA County) is adapted from SF, and 1 (Massachusetts) from an external
fact-sheet template; the two organism-naming independents (NYC, San Diego) name *S. aureus* in
different registers, so the naming is not a propagating template. Details and the independence
table: `outputs/streamb_denominator_reconciliation.md`.

## Exclusions (governmental-only, with reasons)

Excluded documents are retained in `data/raw/guidelines/excluded/` with per-file reasons.
Categories and rationale: FQHCs / community health centers (relay their health department's
language — Howard Brown, Open Door Health, Callen-Lorde, Fenway); patient-navigation/outreach
(VOICES); nonprofit advocacy / patient education (ASHA); professional societies (DSTIG, IUSTI
Europe); advocacy comments (Fenway's comment to CDC). Coding these would grade bodies on a
policy judgement they do not own and dilute the monitoring column.

## Retrieval discipline

Absence in this corpus means "not retrieved under the stated attempts," never "does not
exist." The earlier intermediate retrieval log (Seattle–King County access failure, UK
BASHH, ECDC, and other non-retrieved state/county jurisdictions) is **superseded by the
purposive design**: those jurisdictions are not in the de-Jong outbreak set, so their
non-retrieval does not affect the outbreak-matched denominator or the 0/6 result. The one
outbreak jurisdiction without guidance (Atlanta) is treated as confirmed-none, with the
negative-search caveat stated in the reconciliation.
