# Citation verification pass — claim-support against the corpus (2026-08-21)

Method: for each cited source, verify that it actually says what the manuscript uses it
for ("treat the citation as a lead"), against the hashed source text (or PubMed/DOI for
off-corpus entries). 2 off-corpus (diep2008, sfdph2022) resolved via web. Verdicts:
**supported** / **partial** (substance holds, a detail is off) / **fix**.

**Reference-list reconciliation (2026-08-21):** 7 entries were stripped from the bib —
6 that belonged to the *separate* ITS/Spinelli editor correspondence (a gonococcal/STI
work, not this S. aureus manuscript): `harrison1979`, `lopezbernal2018`, `miko2012`,
`schroder2025`, `spinelli2026`, `demidont2026cid`; and the companion `demidont2026metaarxiv`
"150-journal audit" (removed with its §2.6 in-text citation). The bib was **closed** at that
point at **16 entries** (later 19; see the 2026-08-23 addendum below). A stale "cite the CID
letter" instruction and the bib header's "verified against the companion CID correspondence"
line were removed.

**Addendum — final conceptual-literature pass (2026-08-23).** For the PLoS Meta-Research
submission the manuscript was positioned against its intellectual neighbours, adding **five**
meta-research sources (all verified against source PDF or PubMed metadata; see
`references.bib`):

| key | source | supports | placement |
|---|---|---|---|
| `montoya2025estimand` | Renson, Montoya et al., *Am J Epidemiol* 2025;194(12):3566–71 (doi 10.1093/aje/kwaf169) | estimand specification — the quantity estimated is part of the scientific question | Discussion, neighbours ¶ |
| `tancredi2024surveillance` | Tancredi et al., *Public Health* 2024;234:98–104 (doi 10.1016/j.puhe.2024.06.006) | surveillance/ascertainment bias, indicator dependence | Discussion, neighbours ¶ |
| `treem2023visibility` | Treem et al., *J Comput-Mediat Commun* 2023;28(4):zmad023 (doi 10.1093/jcmc/zmad023) | Goodhart-type metric/visibility decoupling | Discussion, neighbours ¶ |
| `montoya2025affected` | Montoya et al., *Stat Med* 2025;44(28–30):e70353 (doi 10.1002/sim.70353) | estimand defined on the *affected* (non-treated) population | Methods, B≠H schema |
| `armond2024integrity` | Armond, Cobey, Moher, *J Clin Epidemiol* 2024;171:111367 (doi 10.1016/j.jclinepi.2024.111367) | research integrity / reproducibility; research-to-policy "domino effect" | Methods (Reproducibility) + Discussion (generalisation) |

Two previously-listed but **uncited** records were removed from the bib: `vanderlinden1998`
and `molina2023croi`. The bib is again **closed: 19 entries, every one cited, every citation
resolved, no undefined citations** (bibtex/plos2015 clean; the manuscript is now the PLoS
LaTeX source `paper/manuscript.tex`, compiled with `plos2015.bst`).

## Summary

| key | claims checked | verdict | action |
|---|---|---|---|
| luetkemeyer2023 (NEJM) | efficacy; 5-of-31 appendix count; data withheld; doxycycline assay | **supported** (4/4) | none |
| **luetkemeyer2025 (Lancet ID, FINAL)** | randomised incident doxy-R *S. aureus* **HR 3.89 (95% CI 1.42–10.68), p=0.0044** (68/393 vs 5/163, Fig 4B, p.880); colonisation-clearance **HR 1.01 (0.69–1.46), p=0.98** (Fig 4A); MRSA unchanged; "mixed" effect + call for *S. aureus* AMR surveillance (Discussion/Conclusion, p.881–882) | **supported** (verified verbatim against the PDF; coded in `luetkemeyer2025_saureus_final.yaml`) | none |
| cdc2024doxypep | recommends; "monitored" quote; "tetracycline resistance in S. aureus"; 5%→13% [20/428→28/222]; names S. aureus | **supported** (5/5) | bib title fuller (below) |
| soge2025 | 18% vs 8% P<.0001; RR 1.42 (>3 doses GC); any-use RR 1.14/1.16; median 3 (IQR 2–6) | **supported** | none — see note |
| dejong2025 | 18 studies; 0–54%; 3 clusters SF/Tokyo/Chicago; MSM not itself a risk factor | **supported** (4/4) | none |
| liu2011 | tetracycline A-II oral CA-MRSA option; tet(K) **inducible** doxy-R / tet(M) whole-class | **supported** (4/4) | none |
| stevens2014 | doxycycline among oral MRSA SSTI options | **supported** | none |
| vanbaelen2024c | within-arm chi-square trend p<0.0001 (doxy) / p=0.0139 (no-PEP) | **supported** | none |
| dona2026 | n=36; MRSA selection 91.7%, tied-highest with GC resistance | **supported** | none |
| vanderlinden1998 | IDR 4.4 co-trimoxazole vs tetracyclines, highest of classes | **supported** | none |
| molina2023croi | DOXYVAC MRSA carriage 1.8/3.6/6.4/5.7/9.9 & 1.2/2.7/7.1/2.1/5.1, cross at M6 | **supported** | none (transcript-sourced) |
| luetkemeyer2023croi | doxy-R MRSA low/unchanged; 16/137 at M12; "surveillance…needed" | **supported** (resolved 2026-08-22) | "~6%" wording corrected to MRSA carriage prevalence |
| diep2008 | USA300 MDR MRSA in MSM, SF (RR 13.2 male-male sex) | **supported** (PubMed) | bib-note nit |
| grossman2016 | tet(K) efflux / tet(M) ribosomal; tetracycline-scored phenotype ambiguous | **supported** (resolved 2026-08-22) | "does not wash back out" recast as inference from tet(M) stability |
| sfdph2022 | SF issued municipal doxy-PEP guidance | **fix** (real doc, wrong title) | update bib entry |
| aidsvu | PrEP density exposure proxy | **supported** | none |
| ~~demidont2026metaarxiv~~ | 150-journal audit | **removed** | stripped (§2.6 clause + cite) |

**No cited source failed claim-support.** Every load-bearing number verified verbatim
against source: the NEJM 5-of-31, the CDC 20/428→28/222, the CROI 16/137, the DOXYVAC
series, Soge's 18%/8% and RR 1.42, Vanbaelen's p<0.0001/p=0.0139, Donà's 91.7%, van der
Linden's 4.4.

## Items needing action

1. **sfdph2022 — DONE.** The bib entry now carries the verified title *"Health Update:
   Doxycycline Post-Exposure Prophylaxis Reduces Incidence of Sexually Transmitted
   Infections"* (SFDPH, Oct 20 2022, first US municipal doxy-PEP guidance) + the sf.gov
   URL; `TODO-verify` dropped. Kept distinct from the on-disk 2026 provider guide (gl_sf).

2. **grossman2016 — one over-attribution.** The standalone cite at the "once tet(M) is
   selected … it does not wash back out the way a colonisation proportion does"
   [@grossman2016] sentence: Grossman supports tet(M)'s **stability/mobility** (transposon-
   borne, heritable) but makes **no population-persistence / "washing out" claim** — that
   inference is the manuscript's. Reframe as an inference from Grossman's stability (e.g.
   "because tet(M) is a stable, mobile determinant [@grossman2016], it does not wash back
   out…"), so Grossman carries the mechanism and the population reading is ours. (The
   "inducible doxycycline resistance" co-cite at the tet(K)/tet(M) sentence is **sound** —
   liu2011 states "inducible" verbatim; Grossman carries the efflux-vs-ribosomal mechanism.
   Minor: Grossman's "whole class" excludes tigecycline/omadacycline, but the manuscript's
   context is "doxycycline and minocycline alike," which is correct.)

3. **luetkemeyer2023croi — tighten the "~6%" wording (clarity, not error).** "Doxycycline
   resistance within the MRSA subset (~6% of isolates) stayed low…" is easily misread: the
   ~6% is **MRSA carriage prevalence**, while doxy-R *within* MRSA was ~0–3% (near zero).
   The sentence parses correctly (the ~6% modifies the subset size) but reads ambiguously;
   suggest "the MRSA subset — ~6% of isolates — within which doxycycline resistance stayed
   low and, if anything, declined." Appears at two places (intro and §3.1).

4. **cdc2024doxypep — DONE.** Bib title corrected to the document's actual title, *"CDC
   clinical guidelines on the use of doxycycline postexposure prophylaxis for bacterial
   sexually transmitted infection prevention, United States, 2024."*

5. **diep2008 — DONE.** Bib note corrected: Chambers is the **second** author (senior
   author is Perdreau-Remington); "verified via PubMed PMID 18283202." Metadata exact.

6. **demidont2026metaarxiv — REMOVED.** The "150-journal audit" self-citation (with its
   `[coauthor]` placeholder) was stripped from the bib and its §2.6 in-text clause removed,
   per PI direction.

## Confirmed non-issues

- **`@nyxdynamics`** — not a citation; it is the corresponding-author email
  `acdemidont@nyxdynamics.org` in the title footnote. Pandoc citeproc emits no warning and
  does not parse it as a key. No action.
- **Soge benchmark exposure definitions** — the manuscript describes the RR 2.25 S. aureus
  benchmark as "doxy-PEP users versus non-users" (any recent use), which **matches** the
  source (18% vs 8%, any use); the RR 1.42 GC benchmark is correctly the ">3 doses/month"
  figure. The two exposure definitions differ but are not conflated in text or code. The
  2.25 is a derived ratio (18/8), which the code/Methods already present as such.

## Uncited bib entries — RESOLVED (stripped)

`harrison1979`, `lopezbernal2018`, `miko2012`, `schroder2025`, `spinelli2026`,
`demidont2026cid` were never cited in this manuscript because they belong to a **separate
work** — the PI's ITS "time zero" correspondence to the CID editor about the Spinelli
doxy-PEP ITS paper (a gonococcal/STI-focused piece: minocycline-PEP-for-gonorrhea,
gonococcal tetracycline resistance, the ITS methods reference, and the Spinelli paper
itself). `demidont2026cid` is that correspondence (submitted, not published). They bled
into this bib and have been **removed** — this manuscript's unit is *S. aureus*, and its
reference list is now scoped accordingly. (Two inconsistent IDs — CID-S-26-03420 vs
CID-132517 — had appeared for the correspondence; both are now out of this repo.)

## Remaining open items (manuscript prose)

Both claim-support tightenings **RESOLVED 2026-08-21** (pre-Zenodo freeze):
- **grossman2016** — the "does not wash back out" sentence is now cast as an explicit
  inference from tet(M) molecular stability/mobility ("an inference from the determinant's
  biology, not a measured population dynamic"), which is what Grossman supports.
- **luetkemeyer2023croi** — the "~6% of isolates" wording is corrected at both spots to
  "MRSA colonisation about 6% of sampled participants" (carriage prevalence, not the
  doxy-R-within-MRSA rate).

No open claim-support items remain.
