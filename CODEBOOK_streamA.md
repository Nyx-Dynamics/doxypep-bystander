# CODEBOOK — Stream A (trials)

Replaces the Stream A section in `CODEBOOK.md`. Same contract as Stream B: every
coded value carries a locator, the builder raises on a missing one, `partial`
requires a note.

Unit = one trial. Metadata: `unit`, `trial_name`, `citation`, `doi`,
`registry_id`, `source_file`, `coder`, `code_date`.

---

## Why this schema is shaped the way it is

Three findings drove the design. Read this before coding or the fields will look
over-engineered.

**1. Mechanism determines whether a phenotype means anything.** Grossman
(Cold Spring Harb Perspect Med 2016;6:a025387), Table 1 — isogenic *E. coli*
MICs, µg/mL:

| | control | tet(M) | tet(K) |
|---|---|---|---|
| Tetracycline | 2 | 128 | 128 |
| Doxycycline | 2 | 64 | 4 |
| Minocycline | 0.5 | 64 | 1 |

tet(K) — among the most common tetracycline-specific efflux pumps in Gram-positive
clinical isolates — raises tetracycline MIC 64-fold and doxycycline MIC 2-fold.
tet(M) (ribosomal protection) raises both. So an isolate reported
"tetracycline-resistant" may be fully doxycycline-susceptible.

This explains Mittelstaedt (J Infect Dis 2025;231:e708–12): 13.2%
tetracycline-nonsusceptible vs 2.0% doxycycline-nonsusceptible, same isolates.

**Directional consequence.** Doxycycline exerts little selective advantage on
tet(K) strains (MIC 4 vs 2) but strong advantage on tet(M). Doxy-PEP is therefore
predicted to shift *mechanism composition* toward tet(M) within the
tetracycline-resistant fraction. Total tetracycline-resistance prevalence can stay
flat while clinically meaningful doxycycline resistance rises. An endpoint scored
S/I/R at the standard tetracycline breakpoint is **structurally blind** to that
shift — not underpowered, blind. This is why `mechanism_discriminating` exists.

**2. The same trial's result is reported with different denominators.** Worked
case, DoxyPEP *S. aureus*, doxy arm, month 12:

| source | n/N | basis |
|---|---|---|
| NEJM Fig 4B | 5/31 | colonized participants |
| NEJM Fig 4B | 5/111 | all participants swabbed |
| CDC MMWR 2024 | 28/222 | all participants swabbed |
| Szondy 2024 Table 2 (MSSA) | 15/71 | isolates cultured |

CDC's numbers do not reconcile with the primary publication; CDC cites both the
NEJM paper and a CROI 2023 abstract. Code each reported instance separately — the
multiplicity is the finding, not noise to resolve.

Note also that the denominator here is **intervention-affected**: *S. aureus*
carriage was 40% lower in the doxy arm at month 12 (28% vs 47%, P = .03). Dividing
resistant isolates by all swabbed mixes a carriage effect with a resistance effect.

**3. Sources relabel the phenotype.** NEJM Methods state nares/oropharyngeal swabs
were cultured for *S. aureus* with **doxycycline**-resistance testing (ETEST, MIC
≥16 µg/mL). CDC MMWR describes the same trial as evaluating **tetracycline**
resistance in *S. aureus*. Given finding 1, those are not interchangeable labels.
Hence `phenotype_measured` and `phenotype_as_labeled` are separate fields.

---

## Trial-level coded fields (y/n/partial + locator)

1. **`s_aureus_measured`** — sampled at all? `partial` if only a subset, substudy,
   or one arm.
2. **`powered_for_resistance_endpoint`** — is a power calculation stated for the
   resistance outcome? `no` covers "not stated"; distinguish in the note.
3. **`authors_concede_underpowering`** — in text?
4. **`conclusion_contested`** — has a published reanalysis reached a different
   conclusion from this trial's data? `yes` requires the contesting citation in the
   note. DOXYVAC is `yes` (Vanbaelen 2024c, Lancet Infect Dis 2024;24:e606–7:
   MRSA carriage 2%→12% in the doxy-PEP arm, against the trial's own null).
5. **`selection_level_tested`** — `individual` | `population` | `both` | `na`, with
   its own locator. An individual-level test cannot detect cross-arm selection when
   arms share a sexual network; that is the mechanism of the DOXYVAC disagreement.
   If most trials tested only individual-level selection, that is a finding
   independent of sample size.

## Assay descriptors (free text + locator)

`body_site`, `identification_method`, `susceptibility_method`,
`breakpoint_standard` (CLSI/EUCAST + year), `breakpoint_value` verbatim.

Record breakpoints verbatim. Szondy Table 2 shows the same endpoint at MIC ≥2 mg/L
(CLSI, DoxyPEP gonococcus), >0.5 mg/L (EUCAST 2023, DOXYVAC), ≥1 mg/L (EUCAST
2018, IPERGAY), and ≥16 µg/mL (DoxyPEP *S. aureus*). Pooling across these without
recording them is not meaningful.

## Resistance observations — one record per *reported instance*

Fields:

- `source_type` — `primary_trial` | `guideline` | `meta_analysis` | `reanalysis` |
  `registry`
- `source_citation`
- `arm` — `doxy` | `control` | `combined`
- `timepoint` — verbatim (`baseline`, `month12`, `week48`)
- `organism` — `s_aureus` | `mssa` | `mrsa` | `n_gonorrhoeae` | `commensal_neisseria`
  | `c_trachomatis` | `gas` | `other`
- **`phenotype_measured`** — the drug the assay actually tested: `doxycycline` |
  `tetracycline` | `methicillin` | `minocycline` | `not_stated`
- **`phenotype_as_labeled`** — how *this source* describes it. If it differs from
  `phenotype_measured`, a note is required quoting both.
- **`mechanism_discriminating`** — `yes` | `no` | `unclear`. Does the endpoint
  distinguish efflux (tetK) from ribosomal protection (tetM)? `yes` requires a
  `discrimination_method` other than `none`.
- **`discrimination_method`** — `standard_breakpoint` (blind) |
  `high_level_breakpoint` | `tetM_pcr` | `wgs` | `none`
- `numerator`, `denominator` — integers as printed
- `denominator_basis` — `all_participants_swabbed` | `colonized_participants` |
  `isolates_cultured` | `unclear` (note required)
- `denominator_intervention_affected` — `yes`/`no`. `yes` where the intervention
  moved the denominator itself (DoxyPEP carriage 47%→28%). Note required.
- `description_denominator_mismatch` — `yes` where the prose describes a different
  basis than the printed denominator implies. Note required, quoting both. CDC's
  sentence is the motivating case: it describes patients with *S. aureus* in their
  nares, then prints 428 and 222, which are totals swabbed. Record that the
  description and denominator disagree; do not assert an error.
- `significance_reported` — `within_arm` | `between_arm` | `both` | `none`, plus
  `p_value`. DoxyPEP forces this: Vanbaelen 2024a reports that Luetkemeyer found a
  significant within-arm increase (5%→13%) while the between-arm difference at
  month 12 was not significant. Reporting either alone changes the conclusion.
- `locator`, `quote`, `note`

## The asymmetry this is built to measure

Expected pattern, to be confirmed by coding rather than assumed:

| organism | discrimination method | discriminating? |
|---|---|---|
| *N. gonorrhoeae* (DOXYVAC) | tetM PCR, WGS, national reference lab | yes |
| *N. gonorrhoeae* (Soge) | high-level tetR breakpoint | yes |
| *S. aureus* (DoxyPEP) | ETEST, standard breakpoint | no |
| *S. aureus* (DuDHS) | Kirby-Bauer disc diffusion | no |

The mechanism-discriminating endpoint for the in-category organism, the
mechanism-blind endpoint for the bystander. If the coding bears this out, it is the
thesis at the level of the assay rather than the study design.

## Detectability inputs

`src/analysis/detectability.py` uses observations with
`source_type == "primary_trial"`, `denominator` as n. Where bases differ, compute
per basis and report the range; the coder does not choose. Exact binomial or
Fisher — these n are small and the normal approximation Stream C used at large N
will mislead. Document why the methods differ.

Start with MRSA. Szondy Table 2 gives DoxyPEP month-12 MRSA tetracycline resistance
as 1/11 (doxy) and 2/6 (control) — the entire basis for the CDC statement that MRSA
colonization trends did not differ between arms. Note that the NEJM paper contains
no MRSA breakdown, so those rows trace to the CROI abstract; code `source_type`
accordingly.

## Gate

If any trial codes `powered_for_resistance_endpoint: yes` with adequate n, stop and
report — the Stream A leg weakens and the framing needs revision.
