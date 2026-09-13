# Stream C — the linkage decomposition (deployed surveillance systems)

Backing intro ¶6's third leg: **does any deployed US public-health surveillance system
link doxy-PEP exposure to *S. aureus* tetracycline/doxycycline resistance at a common
population denominator?** Answer, decomposed rather than counted. **Capability/linkage,
not effect (Contract 1). Deployed systems, not in principle (Contract 3). Unit is
*S. aureus* tetracycline resistance; MRSA/methicillin systems are a flagged wrong-unit
near-miss (Contract 2).**

## Denominator (re-anchored — see the checkpoint note)

The prior Stream C figure ("0/81") was a **dilution parameter grid**, not a systems
denominator, and was stale (the grid is 135 cells). It is retained below only as a
separate *dilution* finding. The linkage denominator is a **closed universe of established
US public-health surveillance systems** under the stated rule:

> Established US public-health surveillance systems (federal, state, or metro) that plausibly capture, at a population denominator, either doxy-PEP/doxycycline exposure or S. aureus antimicrobial-resistance phenotype.

**12 systems** meet the rule and are coded on their own terms (blind to
the expected 0-linked answer). Excluded, with reason: **CDC Find Doxy PEP directory** (a provider/location directory, not surveillance — carries no population denominator or phenotype data); **Commercial AST networks (Pfizer ATLAS, BD Insights, PINC AI, IQVIA)** (commercial/research convenience datasets, not public-health surveillance; no population denominator (parallel to Stream B excluding clinics)); **Doxy-PEP RCTs and observational cohorts (DoxyPEP, DOXYVAC, Soge)** (one-off research studies, not deployed surveillance systems).

## Task 2 — three-way decomposition

| system | tier | exposure @ pop-denom | phenotype (S. aureus tetR) @ pop-denom | links | note |
|---|---|---|---|---|---|
| AIDSVu (Emory/Rollins + Gilead) | national_academic | yes (proxy_pop) | — | — | county_metro_state / none |
| CDC NCHHSTP AtlasPlus | federal | yes (proxy_pop) | — | — | state_county / none |
| NHSN Antimicrobial Use (AU) Option | federal | — (facility_no_denom) | — | — | facility / none |
| State Prescription Drug Monitoring Programs (PDMPs) | state | — (not_captured) | — | — | state / none |
| Metro STD/HIV sentinel surveillance (e.g., SF DPH, NYC DOHMH) | metro | — (sentinel_no_denom) | — | — | clinic_sentinel / none |
| NARMS (National Antimicrobial Resistance Monitoring System) | federal | — (not_captured) | — | — | none / none |
| GISP / eGISP (Gonococcal Isolate Surveillance Project) | federal_sentinel | — (not_captured) | — (wrong_organism) | — | none / sentinel_clinics |
| ABCs / EIP invasive S. aureus surveillance | federal_sitebased | — (not_captured) | — (wrong_phenotype_pop) ⚠ MRSA (wrong unit) | — | none / eip_sites |
| NHSN AR Option / MRSA LabID Event | federal | — (not_captured) | — (facility_no_denom) ⚠ MRSA (wrong unit) | — | none / facility |
| AR Lab Network (ARLN, ELC-funded regional/state AR labs) | federal_state | — (not_captured) | — | — | none / none |
| NNDSS (National Notifiable Diseases Surveillance System) | federal | — (not_captured) | — | — | none / none |
| Hospital / health-system cumulative antibiograms | facility | — (not_captured) | — (facility_nonstandard_no_denom) | — | none / facility |

**Decomposed result:** of 12 systems — **2 capture
exposure only** (at a population denominator, as a PrEP *proxy*), **0
capture *S. aureus* tetracycline phenotype only** at a population denominator,
**0 capture both but unlinked**, and **0 link the two.**

**The failure is specific:** no phenotype-side population-denominator capture (exposure exists; the S. aureus tetracycline unit is surveilled nowhere with a population denominator). It is *not* "both halves exist and nobody joined them."
The exposure half exists (PrEP density at county/metro); the phenotype half — *S. aureus*
tetracycline/doxycycline resistance at a population denominator — **does not exist in any
deployed system.** Two near-misses explain why:

- **Wrong unit, right denominator:** ABCs / EIP invasive S. aureus surveillance, NHSN AR Option / MRSA LabID Event — the one
  population-based *S. aureus* surveillance platform (ABCs/EIP) reports the **methicillin**
  subset (invasive MRSA), not tetracycline/doxycycline susceptibility. The platform that
  *could* carry the unit exists but is not instrumented for it.
- **Right unit, non-standardized, no denominator:** Hospital / health-system cumulative antibiograms
  — the only routine source of *S. aureus* tetracycline/doxycycline susceptibility is the
  facility cumulative antibiogram, and it is inconsistent even at facility level. **CLSI
  M39 (5th ed., 2022)**, the national standard for antibiogram presentation, (a) **requires**
  *S. aureus* to be split into MRSA and MSSA — the methicillin axis is mandated — and (b)
  treats non-primary agents as **selectively reportable/suppressible** (supplemental agents
  tested only on resistant isolates are not reported; cascade rules may suppress agents).
  Tetracycline/doxycycline for *S. aureus* is such a supplemental agent — not in the
  required presentation and suppressible — so facility tetracycline data are
  **non-standardized and patchy across labs**, and carry no population base regardless.
  The claim is inconsistency, not universal absence: some labs report it; a single one does
  not falsify a claim about the standard and the resulting patchwork.
- NARMS, the closest-named federal AR system, excludes *S. aureus* entirely (enteric
  bacteria only); *S. aureus* is not NNDSS-notifiable (only VISA/VRSA).

## The methicillin axis at every tier — the codified seam (cross-tier synthesis)

At each tier where *S. aureus* is surveilled at all, the **reported axis is methicillin**,
not tetracycline:

- **Population denominator:** ABCs/EIP surveils invasive **MRSA/MSSA** (the methicillin
  split) in its catchment sites.
- **Facility, administrative:** NHSN AR Option / LabID reports **MRSA** events.
- **Facility, cumulative antibiogram:** CLSI M39 **mandates** the **MRSA/MSSA** split and
  makes tetracycline suppressible.

The surveillance architecture is **standardized around the methicillin axis at every
level**, and *S. aureus* tetracycline/doxycycline resistance is **orthogonal to that axis**
— so it falls through at each tier: absent where the denominator exists (methicillin
instead), suppressible and non-standardized where the unit is nominally reportable. This is
the Stream C analogue of the endpoint-substitution seam already found in Stream A (the
tet(K)/tet(M) mislabel and the narrowing from *S. aureus* to its methicillin subset) and
Stream B (efficacy graded, harms un-graded): the same measurement-inheritance seam, here
**codified in a national laboratory standard**. The phenotype half is not merely un-built;
the standard that governs it is organised around a different axis.

## Task 3 — resolution analysis (the mechanism)

The linkage cannot be made even in principle with deployed systems because the two sides
exist at **incompatible resolutions**:

- **Exposure** is surveilled at a **population denominator, county/metro/state** grain
  (AIDSVu, CDC AtlasPlus — PrEP proxy per 100k).
- **Phenotype** (*S. aureus* tetracycline resistance) exists only at **facility grain with
  no population denominator** (hospital antibiograms) — or, where a population denominator
  exists (ABCs/EIP), for the **wrong phenotype** (methicillin) in a handful of catchment
  sites.

There is no geographic level at which both a doxy-PEP exposure denominator and an
*S. aureus* tetracycline-resistance denominator coexist. The mismatch, not indifference,
is why nothing joins.

## Task 4 — the exposure side is concrete; the phenotype side is empty at that resolution

AIDSVu supplies the exposure proxy (PrEP) with a population denominator for **52
geographies** at state grain (plus county/metro tiers). Against that, **zero** geographies
have an *S. aureus* tetracycline-resistance dataset at a population denominator to join.
The metro-grain dilution computation (`dilution_metro.py`) operates on this same AIDSVu
exposure side and is a **linkage/resolution and detectability demonstration, not an effect
estimate** (Contract 1), keyed to *S. aureus* tetracycline resistance as $R_0$ (Contract
2): it shows that even where exposure density is highest, no phenotype counterpart exists
at that resolution to link, and — separately — that the exposed subgroup would be too
dilute to move a population rate (the dilution leg, below).

**Dilution leg (supporting, corrected):** `dilution.py`/`dilution_metro.py` sweep a
parameter grid of favourable assumptions (uptake × enrichment × baseline × isolate
volume); **0 of 135** cells (not the stale "0/81") reach detection at the cross-organism benchmark
RR 1.42, and the metro case requires male-PrEP density far above the densest US geography.
This is a distinct claim from linkage — it says that *if* a linked population-denominator
system existed, the exposed subgroup would still be too dilute — and is reported as
support, not as the linkage denominator.

## Task 5 — scope bound (Contract 3)

The claim is that **no deployed system links** the two — **not** that the linkage is
impossible. It could be built. A system that *could* detect the signal would require, at a
common population denominator: (i) an exposure feed — outpatient doxycycline/doxy-PEP
dispensing or PrEP-linked records at county/metro grain (the exposure side AIDSVu already
approximates); and (ii) a phenotype feed carrying *S. aureus* **tetracycline/doxycycline**
susceptibility with a population denominator — most plausibly by adding tetracycline AST
reporting for *S. aureus* to the existing population-based ABCs/EIP platform (which already
has the denominator and the isolates), or by standing up a sentinel *S. aureus* antibiogram
network with defined catchment denominators, and joining the two on geography. None is
deployed. The cost is going unmeasured because the phenotype-side instrument was never
built, not because the phenomenon is unmeasurable.

## Licenses / not

**Stream C may claim:** no deployed US public-health surveillance system links doxy-PEP
exposure to *S. aureus* tetracycline/doxycycline resistance at a common population
denominator; the failure is specifically **no phenotype-side population-denominator capture (exposure exists; the S. aureus tetracycline unit is surveilled nowhere with a population denominator)**; the exposure and phenotype sides exist
at incompatible resolutions; the surveillance architecture is standardized around the
methicillin axis at every tier and the tetracycline unit is orthogonal to it; facility
*S. aureus* tetracycline capture is **non-standardized per CLSI M39** (methicillin split
mandated, tetracycline suppressible) — captured nowhere consistently, nowhere with a
population denominator; and, separately, even a linked population-denominator system would
face a diluted exposed subgroup (0/135 favourable cells).

**Stream C may NOT claim:** that such linkage is impossible in principle (a system could be
built — deployed-systems only); that **no facility reports** tetracycline for *S. aureus*
(M39 permits it and some labs do — the claim is inconsistency/non-standardization, not
universal absence); any effect size or causal statement (this is
capability/linkage/resolution only); or that the phenotype unit is MRSA (it is *S. aureus*
tetracycline resistance — ABCs/EIP's and NHSN's MRSA surveillance are flagged wrong-unit
near-misses, not the unit).

(Regenerate with `python -m src.analysis.streamc_linkage`.)
