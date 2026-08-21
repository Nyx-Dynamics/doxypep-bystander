# Response to Anticipated Reviews

Prepared from a six-reviewer adversarial pre-submission panel (ID clinician, molecular-AMR
microbiologist, surveillance epidemiologist, biostatistician, meta-science/ethics, and a
handling editor). Each anticipated objection is stated as a reviewer would raise it, then
answered, with the manuscript location of the change. Load-bearing revisions were made
*before* submission; this document records them so an editor can see the paper already
survives its own panel.

---

### 1. "This is an effect claim wearing a disclaimer."
**Answer.** It is not, and the manuscript is consistent on the point across the abstract,
the framing note, §4, and a dedicated "what we are and are not claiming" box. The analysis
is a *design-based sensitivity analysis*: the benchmark effect is fixed a priori from an
independent source (Soge 2025), never read from the trials' own estimates, and the output is
a detectability threshold, not an effect. We do not dispute the trials' non-significant
between-arm tests; we show the sources could not resolve the question either way. The strong
framing the paper does make is *epistemic* ("the instrument cannot answer this"), not causal.

### 2. "The Stream C headline (0/135) suppresses your own panel-power correction."
**Answer — accepted and fixed (P0).** The manuscript now reports the controlled-panel
correction in §3.3, the abstract, and Figure 1. Under the panel actually under test
(~52 geographies × ~14 years), the single-comparison grid median is retired; ~25/135 cells
become nominally detectable and the best case falls to a required within-exposed RR ≈1.0.
We rest nothing on that best case — it compounds four simultaneous implausibilities (55%
uptake, 5× enrichment, 13% baseline resistance, 100,000 MICs/geography-year) and fails on
any one. The claim is now anchored on the **realistic cell: RR_needed ≈14–64** across the
design-effect range, above Soge's 1.42–2.25 throughout. All figures already computed in
`outputs/feasibility_result.md`.

### 3. "You compute a per-carrier 40% from counts you simultaneously call irreconcilable."
**Answer — accepted and reframed (P0).** §3.1 now presents 8.5%→40% strictly as a bounded
*denominator-sensitivity illustration, not a tested quantity*: it states the 16/40 month-12
numerator, notes it inherits the same withheld-data uncertainty, and identifies the robust
claim as the between-arm *direction* plus a several-fold rise that holds **under either
denominator** (~3× all-swabbed, ~5× per-carrier). The 5/16/28 spread is now a reconciliation
table (venue × numerator × denominator × basis × rate) with an explicit statement that we do
not suggest impropriety — only that the public record cannot resolve it because the
individual-level data are withheld. "The counts do not reconcile" is softened to "cannot be
reconciled from the public record" throughout.

### 4. "'tet(K) confers inducible doxycycline resistance' is not supported."
**Answer — respectfully, the source supports it verbatim.** The IDSA MRSA treatment
guideline (Liu et al., CID 2011), which the sentence cites, states: *"Although the tet(M)
gene confers resistance to all agents in the class, tet(K) confers resistance to
tetracycline and inducible resistance to doxycycline, with no impact on minocycline
susceptibility."* The manuscript attributes the distinction to the guideline and uses it
only to make the clinical point that a "tetracycline-class" endpoint cannot tell a clinician
what the guideline needs to know. We believe the objection conflates this with the separate
*inducible clindamycin* resistance (D-zone test) that also appears in Liu. No change; quote
available for the record.

### 5. "The unit is declared as *S. aureus* but the empirical spine is MRSA."
**Answer — accepted; scope condition promoted up-front (P1).** The §4 reflexive treatment
(the clustering, dispersion, and outbreak-jurisdiction evidence is MRSA because that subset
is the only part any system was built to observe) is now also stated as an explicit scope
condition in the Introduction, framed as an early *instance* of measurement inheritance
rather than a late concession. The manuscript marks every place its own analysis is forced
onto MRSA.

### 6. "The clustering σ̂ is transported from a between-cohort context into a between-visit
simulation, and reported with false precision on a miscounted base."
**Answer — accepted and softened (P1).** §3.1 now states the transfer is "an assumption,
not an identity" — an upper bound on a *different* variance component (cross-cohort spread
absorbs methodological heterogeneity a single trial's repeated visits do not incur) — and
that the load-bearing claim rests on the lower confidence bound, not the point estimate. The
study count is corrected: σ̂ is fit on the **ten colonisation cohorts** (of eighteen
screened), not eighteen; fixed in both the manuscript and the analysis code.

### 7. "'Loss of a whole class' overstates — tet(M) does not remove the glycylcyclines."
**Answer — accepted and recast (P1).** The passage now reads as a stake-sizing counterfactual
("one would expect … a mechanistic expectation, not a dynamic anyone has yet measured"),
speaks of "the loss of the oral tetracyclines as a usable category," and explicitly notes
that the newer glycylcyclines/aminomethylcyclines (tigecycline, eravacycline, omadacycline),
engineered to evade both determinants, remain.

### 8. "The 'closed universe of twelve' zero is partly built into a selection rule that
disqualifies antibiograms, and may omit EIP/ELR isolate-level AST feeds."
**Answer — partially accepted (P2, in progress).** We will (a) state that "0 of 12" is
conditional on requiring a population denominator and name-and-dispose the additional streams
(EIP/ELR isolate-level AST, NSSP/ESSENCE, commercial AST networks) so the universe does not
read as gerrymandered, and (b) narrow "the phenotype half does not exist" to "is not reported
or linked at a population denominator." The underlying claim — that no deployed system
*links* exposure to the *S. aureus* tetracycline unit at a population denominator — is
unaffected.

### 9. "'Measurement inheritance' repackages known biases."
**Answer — the contribution is the unification (P2, in progress).** A short paragraph will
position the construct against its neighbors (post-hoc power, ascertainment/surveillance
bias, construct validity, the McNamara fallacy) and state what it adds: the demonstration
that four distinct-looking failures are one failure — an apparatus reproducing the organism
and question it was built for — rendering a specific question unanswerable *as instrumented*.
Generality is scoped honestly as a worked instance offered for testing elsewhere.

### 10. "The distributive-justice frame ignores doxy-PEP's measured benefit; 'unmeasurable'
is too strong."
**Answer — partially accepted.** "Unmeasurable" is replaced by "unmeasured as instrumented"
(the harm is measurable in principle — §5 gives the instrument — but unpriced by deployed
systems, which is the stronger governance claim). A P2 paragraph will name the normative
premise (the duty to measure attaches to whoever internalizes the benefit) and credit the
benefit side, so the justice claim is about *foreclosed weighing*, not presumed net harm.

### Minor accuracy items (being incorporated)
- NARMS has a gonococcal component; phrasing adjusted so it does not read as enteric-only.
- Confirm CLSI M39 edition designation (5th ed. dropped the "-A" suffix).
- State Soge's own caveat at first use (any-use was *not* associated; RR 1.42 is the
  >3-doses/month contrast).
- Reconcile Figure 2 caption vs text on which is "the load-bearing gap" (denominator vs unit).

---

**Status key.** P0/P1 items are applied in the submitted manuscript. P2 items are
strengthening edits that do not affect any load-bearing claim; they are noted here for
transparency and will be incorporated at revision or on editor request.
