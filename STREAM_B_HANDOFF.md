# STREAM B HANDOFF — guideline coding

*Written 2026-08-18. Read `CLAUDE.md` first. This supersedes the Stream B section of
`SCAFFOLD.md`.*

## What Stream B establishes

The bystander risk to *S. aureus* is discussed, counselled, and unmeasured — while
in-category organisms (GC/CT/syphilis) are resolved with laboratory precision in the
same document. The claim is about **asymmetry within a single artifact**, not about
absence of concern.

## SCOPE DECISION (log in DECISIONS.md before coding)

**Include:** governmental public health authorities only — city, county, state,
national. These bodies both (a) set doxy-PEP policy and (b) hold the local
surveillance and outbreak record. That pairing is what makes the
institutional-memory comparison meaningful.

**Exclude:** FQHCs, community health centers, and clinic patient-education pages
(e.g. Howard Brown Health, Callen-Lorde). Rationale: these relay their health
department's language rather than making the policy decision under study. Coding
them would grade safety-net providers on a judgment they do not own, and would
dilute the monitoring column with documents that were never going to specify
monitoring. This is a scope decision, not a finding — state it in the methods.

Excluded documents are retained in `data/raw/guidelines/excluded/` with the
exclusion reason recorded, so the decision is auditable.

## Schema — `src/coding/schema_guideline.py`

Same locator-or-raise contract as Stream A. Every coded value carries a page or
section locator or the record raises.

| Field | Type | Values / notes |
|---|---|---|
| `jurisdiction` | str | city / county / state / national |
| `issuing_body` | str | exact name as printed |
| `document_title` | str | as printed |
| `document_type` | enum | `clinical_protocol` / `health_advisory` / `dear_colleague` / `patient_factsheet` |
| `version` | str | version + date; note if superseded |
| `effective_date` | date | |
| `bystander_treatment` | enum | `silent` / `generic_microbiome_resistance` / `organism_named` |
| `s_aureus_named` | bool | |
| `s_aureus_location` | enum | `body_text` / `patient_counselling_script` / `still_learning_list` / `reference_title_only` / `absent` |
| `in_category_monitoring` | str | verbatim + locator — expect mandated everywhere |
| `s_aureus_monitoring` | enum | `required` / `suggested` / `silent` / `explicitly_none` |
| `host_toxicity_labs` | enum | `required` / `suggested` / `silent` — the contrast that shows lab infrastructure exists |
| `derived_from` | str? | template lineage if the document states it |
| `local_mrsa_msm_literature` | str? | citation, or null |
| `literature_search_provenance` | str | terms + date — **required when the field above is null** |
| `same_institution_authored_both` | enum | `yes` / `no` / `same_city_different_institution` |
| `counselling_language_verbatim` | str | + locator |

### Guards that encode the thesis

- `s_aureus_monitoring == "explicitly_none"` requires a verbatim quote + locator.
- `local_mrsa_msm_literature is None` requires `literature_search_provenance`.
  A null cell means "none found under stated terms," never "none exists."
- `s_aureus_location == "reference_title_only"` requires the full citation.
- `bystander_treatment == "silent"` requires a note confirming the full document
  was reviewed, not just the summary section.

## Corpus

Sampling frame: NCSD "Doxy and STI PEP Sample Policies" compilation (third-party,
not assembled ad hoc — say so in methods), filtered to governmental authorities,
plus CDC MMWR, the Australian consensus statement, and the UK BASHH
non-endorsement position as an international contrast.

### Already in `/mnt/project/` or uploaded — code these first

| Jurisdiction | Document | Status |
|---|---|---|
| National (US) | CDC MMWR rr7302a1, 2024-06-06 | in project |
| National (AUS) | Cornelisse et al., MJA 2024 consensus | in project |
| San Francisco | SFDPH Provider Guide 5.5.26 | in project |
| San Diego County | CAHAN advisory, 2023-05-09 | uploaded |
| New York City | DOHMH Dear Colleague, 2023-11-09 | uploaded |
| Los Angeles County | DPH DoxyPEP factsheet, rev. May 2023 | uploaded |
| Philadelphia | PDPH-HAN-00446V, 2024-07-02 | uploaded |
| Chicago | CDPH SID-STI Clinical Protocol v1.0, eff. 2023-10-15 | uploaded |

### To retrieve

Seattle-King County (landing page currently errors — PDF reachable via
`cdn.kingcounty.gov`; **record the access failure and date, a corpus of public
documents should log which stopped being public**), California DPH, Alameda,
Santa Clara, Multnomah, Minnesota, New Mexico, Oregon, Michigan, Jefferson County.
Check whether a CDPH v2.0 exists post-dating the June 2024 CDC guideline.

## Coded exemplars (verified against the documents — use as fixtures)

**Chicago CDPH** — `bystander_treatment: silent`. Fifteen pages, four approver
signatures, no mention of antimicrobial resistance anywhere: not in counselling,
not as a knowledge gap, not for GC. Section V has five subsections (administration,
lab monitoring, side effects, storage, prevention). `host_toxicity_labs: required`
— LFTs, CMP, CBC per package insert, annually in patients with liver disease. Labs
are ordered; organisms are not. Also note: ineligibility criteria exclude
"anticipated or ongoing use of tetracyclines for non-STI prevention (e.g., acne
treatment)" — cumulative tetracycline exposure is tracked well enough to exclude
on, but the resistance inference is never drawn.

**New York City DOHMH** — `s_aureus_location: patient_counselling_script`
(resistance risk listed for gonorrhea, staph infections, pneumonia,
*M. genitalium*, intestinal flora), and `s_aureus_monitoring: explicitly_none`
— "No laboratory monitoring is needed with doxy-PEP." Only `explicitly_none` in
the corpus so far. Also states the burden will fall first and hardest on the
population using it, then defers to evaluations "planned or underway."

**Philadelphia PDPH** — `s_aureus_location: reference_title_only`. Body text
covers *Neisseria* only. *S. aureus* appears once, inside the title of a cited
CROI 2023 abstract (Luetkemeyer, Dombrowski, Cohen et al., "Doxy PEP and
antimicrobial resistance in *N. gonorrhoeae*, commensal *Neisseria* and
*S. aureus*"). The staph findings were read closely enough to cite and dropped
without comment. Document title is *Updated Guidance from CDC* — every
substantive claim is CDC's; no local epidemiology added.

**Los Angeles County** — `still_learning_list` ("Could it increase or decrease the
bacteria that live on our skin, or cause bacterial resistance to doxycycline (for
example staph)?"). `derived_from: "San Francisco City Clinic, 2022"` — stated on
the document face.

**San Diego CAHAN** — `body_text`; names *S. aureus* and commensal *Neisseria* as
a tetracycline-plasmid reservoir. Actions Requested #5 mandates GC/CT at all
anatomic sites, syphilis, HIV at initiation and q3mo, and says to consider
hematopoietic, renal, and hepatic monitoring. Lab language exists; microbiological
monitoring does not.

**Australia (Cornelisse)** — Rec 8: culture **must** be collected for all GC
diagnoses to enable AMR surveillance. Research Rec 5: guidance on bystander
monitoring "should be developed." Explicit acknowledgement, explicit deferral.

## Template propagation — separate analysis, not a table column

`derived_from` records the relation, but the argument is between rows, not within
one. LA County states adaptation from SF City Clinic 2022 on its face. Test
whether other governmental documents share distinctive phrasing with the SF
source. If a single 2022 SF document seeded the national counselling posture,
"no jurisdiction requires staph monitoring" is a claim about one decision
replicated, not sixteen independent assessments — which is a *stronger* and
different finding. Write it as prose plus a lineage figure.

## Institutional memory — verified pairings

| Jurisdiction | Local MRSA-in-MSM literature | Same institution? |
|---|---|---|
| San Francisco | Diep 2008, Ann Intern Med, `10.7326/0003-4819-148-4-200802190-00204` — population-based, 9 hospitals, male-male sex RR 13.2, spatial clustering | yes (SFDPH/UCSF) |
| New York City | Galindo 2012, J Community Health, `10.1007/s10900-011-9463-6` — DOHMH co-authors (Weiss, Marx) | yes |
| Los Angeles | MMWR 2003;52:88 (no DOI); + Lee CID 2005;40:1529-34 (DOI unverified) | yes |
| Chicago | Popovich CID 2010;50:979-87 — HIV-framed, Cook County/Rush, **not** a CDPH MSM cluster study | `same_city_different_institution` |
| Philadelphia | none found | — |
| Seattle-King County | none found (two searches; Buskin MDR-HIV cluster lists MRSA as comorbidity only) | — |

Anchor for the "baseline was known" claim: Yeung et al., *J Am Acad Dermatol*
2019;80(3):591-602, `10.1016/j.jaad.2018.02.045` — states most MRSA in MSM is
USA300, "which confers resistance to quinolones, mupirocin, tetracycline, and
clindamycin," with nasal and perianal colonization as risk factors and
skin-to-skin transmission during sex. Mainstream dermatology review, five years
before CDC recommended doxy-PEP to the same population.

Supporting: David & Daum, Clin Microbiol Rev 2010, `10.1128/CMR.00081-09`;
Szumowski, CID 2009, `10.1086/599608` (Boston; nares + perianal swabs in 795
outpatients; 36.7% of colonized developed SSTI within 12 months vs 8.1%) — the
swabbing-was-feasible-and-informative citation.

## What would falsify Stream B

- Any governmental guideline **requires** *S. aureus* monitoring → the leg fails,
  and the paper says so.
- Any guideline names staph in body text with a specified method and interval →
  the asymmetry claim weakens substantially.
- If most documents turn out to be independent rather than template-derived, the
  propagation argument is dropped rather than softened.

## Build order

1. `schema_guideline.py` + a test asserting a record missing a locator **raises**.
2. Fixtures from the six coded exemplars above.
3. Code the eight documents already in hand.
4. **Stop and report** the schema and first six coded records before retrieving
   the remainder.
5. Retrieve the rest; log access failures with dates.
6. `reliability.py` — double-code 20%, report agreement.

Preregister the schema (OSF) before coding begins.

## Open items for AC

- Verify the Luetkemeyer CROI 2023 abstract was never published as a standalone
  paper. If confirmed, the primary US trial evidence on bystander staph exists
  only as a conference abstract — that is its own finding about where this
  evidence lives, and belongs in the paper.
- Confirm DOI for Lee CID 2005;40:1529-34.
- Chase PMID 22728758 ("High prevalence of colonization with *S. aureus* clone
  USA300 at multiple body sites among STD clinic patients: an unrecognized
  reservoir") — title is close to the thesis; establish jurisdiction and full cite.
