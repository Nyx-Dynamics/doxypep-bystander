Adrian C. Demidont, DO
Nyx Dynamics, LLC, Fairfield, CT, USA
Nyx Institute for Computational Medicine, Philadelphia, PA, USA
ORCID 0000-0002-9216-8569 · acdemidont@nyxdynamics.org

21 August 2026

To the Editors, PLOS Biology — Meta-Research Section

Dear Editors,

I am submitting an Analysis for consideration in the Meta-Research section:
**"Monitoring That the Instrument Cannot Provide: Measurement Inheritance and
Tetracycline-Resistant *Staphylococcus aureus* in Doxycycline Post-Exposure
Prophylaxis."**

**What it argues, and what it does not.** The paper makes no population-level causal claim.
Its starting point is a fact the pivotal trial's final analysis has now established: in its
randomised, participant-level analysis, doxycycline post-exposure prophylaxis (doxy-PEP) was
associated with a significant increase in incident doxycycline-resistant *Staphylococcus
aureus* (hazard ratio 3.89, 95% CI 1.42–10.68), with no matching effect on carriage — and
its authors call for public-health surveillance of exactly this. The paper asks the question
that fact raises: can the systems built around doxy-PEP *follow* the signal the trial
resolved? Working from public data alone, it audits the three sources any answer would have
to come from — the trials, the governing guidelines, and the deployed surveillance systems —
and finds that the upstream instrument generated information the downstream systems cannot
receive. The guidelines counsel patients about the harm while mandating no measurement of it;
and no deployed US surveillance system links doxy-PEP exposure to the *S. aureus* tetracycline
phenotype at a common population denominator. The signal is individual-level and real; whether
it propagates into a population externality is precisely what no deployed system can determine.

**Why Meta-Research.** The durable contribution is not about one drug. It is a
meta-scientific one — *measurement inheritance*: an evidence apparatus carries, in its
sampling frame, cadence, coding, and denominator, the organism and question it was built
for, and so cannot answer an orthogonal question about a bystander. Doxy-PEP is the worked
instance; the apparatus was built to measure gonococcal efficacy and, applied to a
commensal *S. aureus*, inherits a denominator the intervention itself moves, a phenotype
label that spans two resistance mechanisms, and a surveillance architecture standardised
around the methicillin axis while the tetracycline unit falls orthogonally through it. The
claim is that the trial's newly-resolved individual-level signal is *uninheritable as
instrumented* — the population question it raises cannot be followed by the deployed systems —
an epistemological finding established with data science, not an effect estimate. The
timeliness is unusual: the enabling trial result appeared in 2025, and the surveillance gap
it exposes is live.

**Reproducibility.** Every number, table, and figure regenerates from public data by one
command (`make all`) over a test-gated pipeline (116 unit tests). Each coded value carries a
page or table locator, and the builder fails rather than emit an unlocated value. Analysis
decisions were logged, with dates, before results were known. The full repository — code,
coded source data, and this manuscript — is openly available on GitHub and archived at
Zenodo with a citable DOI; a reviewer guide mapping every claim to its regenerable artifact
accompanies the submission.

**Disclosures.** I am the sole author. I report former employment at Gilead Sciences
(01/2020–11/2024) with prior ownership of corporate stock, all divested by 12/2024; Gilead
played no role in this work, which was completed independently of any funding. A large
language model was used for writing and analysis-engineering assistance; the scientific
argument, the reading of primary sources, the model specification, and all conclusions are
my own, I verified every value and quotation against primary sources, and no AI tool is
credited as an author. These statements appear in full in the manuscript's Declarations.

The work has not been published elsewhere and is not under consideration by another journal.
A preprint is being posted to medRxiv concurrently, with the repository attached. I suggest
that reviewers with expertise in AMR surveillance methodology, biostatistics (design-based
sensitivity analysis), and meta-research would be well matched to the manuscript; I have no
competing-interest exclusions to request.

Thank you for your consideration.

Sincerely,
Adrian C. Demidont, DO
