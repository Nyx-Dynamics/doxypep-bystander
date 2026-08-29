Adrian C. Demidont, DO
Nyx Dynamics, LLC, Fairfield, Connecticut, United States of America
Nyx Institute for Computational Medicine, Philadelphia, Pennsylvania, United States of America
ORCID 0000-0002-9216-8569 · acdemidont@nyxdynamics.org

29 August 2026

To the Editors, PLOS ONE

Dear Editors,

I submit **"Measurement inheritance: following a doxy-PEP bystander-resistance signal from
trial to surveillance"** for consideration as a research article.

**Prior submission history, and why PLOS ONE.** This manuscript was previously submitted to
PLOS Biology (PBIOLOGY-D-26-02526) and declined without external review. The editorial decision
rested entirely on fit-of-scope for that journal's general-biology readership, not on the
science. The editor wrote that the study did not provide "the degree of conceptual advance that
PLOS Biology seeks to publish," and that "even if reviewers were to certify the manuscript as
technically correct, we consider that the work does not represent the type of advance that PLOS
Biology seeks to publish" — an assessment, in his words, "based on considerations such as the
degree of advance provided and the breadth of potential interest of the research question to our
broad readership." He added explicitly that the decision "does not represent a criticism of the
quality of your work, nor are we questioning its value to others working in this area."

I am therefore submitting to PLOS ONE because its publication criteria are exactly the axis on
which the work was *not* found wanting. PLOS ONE evaluates whether a study is technically sound,
methodologically rigorous, and reports conclusions supported by the data — not whether it clears
a threshold of general-interest conceptual advance for a broad readership. The reasons PLOS
Biology cited for decline (breadth of interest, degree of advance) are not PLOS ONE criteria; the
qualities PLOS Biology affirmed (technical correctness, value to researchers in the field) are.
The manuscript is unchanged in substance from the version PLOS Biology reviewed for scope, save
for format adjustments to PLOS ONE style, and I address the PLOS ONE criteria directly below.

**What the paper does.** Doxycycline post-exposure prophylaxis (doxy-PEP), built and measured
for gonococcal efficacy, also selects tetracycline resistance in the commensal *Staphylococcus
aureus*, for which doxycycline is one of few oral treatments. The pivotal trial's 2025 final
analysis newly detected this bystander signal — a significant rise in incident
doxycycline-resistant *S. aureus* (hazard ratio 3.89, 95% CI 1.42–10.68) — and its authors
called for surveillance of exactly this. We ask not whether doxy-PEP drives population-level
resistance, but whether the guidance and surveillance now deployed around it could follow such a
signal. Auditing the evidence base in three streams (trials, guidelines, surveillance) against a
single yardstick — the within-exposed effect each could detect — we find that no governmental
guideline requires *S. aureus* measurement (0 of 6 outbreak-matched jurisdictions; 0 of 10
coded), and that none of twelve deployed US surveillance systems links doxy-PEP exposure to the
*S. aureus* tetracycline phenotype at a common population denominator. The upstream instrument
generated information the downstream architecture is not built to receive; we name this
*measurement inheritance*, and its distributive corollary — one side of the benefit–externality
ledger measurable and the other not — *distributive observability*.

**Technical standard and transparency.** The analysis is a fully reproducible public-data audit.
Every figure and table regenerates from a single command (`make all`) over a test-gated
pipeline; each coded value carries a page/section/table locator and the builder fails on a
missing locator rather than emitting a null; all 40+ sources are SHA-256–pinned; guidelines were
double-coded by a blinded second coder with per-field Cohen's κ reported (including the one field
with meaningful disagreement, κ = 0.58, reported rather than rounded up); and analysis decisions
that could go either way were date-logged before results were known. Code, data, and manuscript
are public on GitHub and archived at Zenodo with a citable DOI.

**Conclusions supported by, and bounded to, the data.** We make **no population-level causal
claim**. The individual-level hazard is the trial's own randomised finding, cited as such; our
contribution is the evidentiary-adequacy result — that the deployed guidance and surveillance
cannot inherit that signal — together with a per-source, falsifiable detectability standard and a
pre-registered falsification condition for each stream. Limitations (the ~12-month trial
horizon; unresolved tet(K)/tet(M) mechanism; colonization ≠ infection; our own forced reliance on
the MRSA subset where no *S. aureus*-tetracycline dataset exists) are stated in the text rather
than left to surface in review.

**Ethics and data availability.** No human-subjects, individual-level, or restricted-access data
were used; every input is public. Full data and code availability statements are in the
manuscript.

**Declarations.** Sole author. Former Gilead Sciences employment (2020–2024), all equity divested
by 2024, with no role in this work; the study is unfunded. Generative-AI assistance for writing
and analysis engineering is disclosed, with every numerical value and quotation independently
verified against primary sources by the author, who takes full responsibility. I request no
reviewer exclusions and have no competing interests requiring one.

Thank you for your consideration.

Sincerely,
Adrian C. Demidont, DO
