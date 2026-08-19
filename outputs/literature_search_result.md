# Defined literature search — the measurement gap in the literature itself

*Run 2026-08-19 against PubMed via NCBI E-utilities `esearch`. Counts drift
as PubMed grows; this reports the frozen snapshot in
`data/raw/literature_search/snapshot.json`. Re-run `python -m src.analysis.literature_search --refresh`.*

**Date bounds:** "2015"[dp] : "2026"[dp] (the doxy-PEP era).

## Queries (verbatim)

Denominator — doxy-PEP (STI post-exposure prophylaxis) papers:

```
("doxy-PEP"[tiab] OR "doxyPEP"[tiab] OR "doxycycline postexposure prophylaxis"[tiab] OR "doxycycline post-exposure prophylaxis"[tiab] OR ("doxycycline"[tiab] AND "prophylaxis"[tiab] AND ("sexually transmitted"[tiab] OR STI[tiab] OR STIs[tiab] OR gonorrhea[tiab] OR gonorrhoea[tiab] OR chlamydia[tiab] OR syphilis[tiab]))) AND ("2015"[dp] : "2026"[dp])
```

Numerator — the denominator ALSO naming a bystander staphylococcal organism:

```
("doxy-PEP"[tiab] OR "doxyPEP"[tiab] OR "doxycycline postexposure prophylaxis"[tiab] OR "doxycycline post-exposure prophylaxis"[tiab] OR ("doxycycline"[tiab] AND "prophylaxis"[tiab] AND ("sexually transmitted"[tiab] OR STI[tiab] OR STIs[tiab] OR gonorrhea[tiab] OR gonorrhoea[tiab] OR chlamydia[tiab] OR syphilis[tiab]))) AND ("2015"[dp] : "2026"[dp]) AND ("Staphylococcus aureus"[tiab] OR "S. aureus"[tiab] OR MRSA[tiab] OR MSSA[tiab] OR staphylococc*[tiab])
```

## Result

| | count |
|---|---|
| Denominator — doxy-PEP papers | **361** |
| Numerator — those naming *S. aureus* / MRSA / MSSA / staphylococc* | **13** |
| **Fraction naming a bystander organism** | **3.6%** |

**13 of 361 (3.6%)** doxy-PEP papers so much as name a bystander staphylococcal
organism. Naming is a generous proxy for measuring — so this over-counts.

## The numerator, classified (naming ≠ measuring)

Hand classification of the 13 numerator records, each with its PMID:

- **Measures tetR S. aureus against a doxy-PEP EXPOSURE contrast** (2):
  - `40036749` — Soge CID 2025 — tetR S. aureus colonization 18% vs 8%, doxy-PEP vs none
  - `39882974` — DuDHS pilot RCT (Grennan), Clin Infect Dis 2026 — measures resistance, pilot n
- **Measures tetR S. aureus, NO exposure contrast (eligible-population / cross-sectional)** (3):
  - `42342442` — Gaspari STI 2026 — nasal S. aureus macrolide/tet resistance, MSM on PrEP, cross-sectional
  - `39718967` — J Infect Dis 2025 — tetR S. aureus in doxy-PEP-ELIGIBLE population, no exposure contrast
  - `39228717` — medRxiv 2024 — preprint of 39718967 (same study)
- **Names only — review / survey / in-silico / in-category / case report** (8):
  - `41974008` — Ann Intern Med 2026 — 'what you may have missed' review
  - `41891836` — Dona Ital J Dermatol Venerol 2026 — KAP survey of clinicians
  - `41366180` — Infect Dis Ther 2026 — narrative review, AMR/microbiome
  - `39766573` — Antibiotics (Basel) 2024 — 'From Cure to Prevention' narrative review
  - `39657948` — Int J STD AIDS 2025 — LGV diagnosis case series (incidental)
  - `38575877` — BMC Infect Dis 2024 — Truong SR/MA (secondary synthesis)
  - `38517444` — JAC 2024 — tetR N. gonorrhoeae England (in-category; staph incidental)
  - `37466467` — Int J STD AIDS 2023 — Kenyon in-silico cross-resistance


**Second-order finding.** Of 361 doxy-PEP papers, 13 (3.6%) name a bystander
staph organism; only **5 (1.4%)** *measure* tetracycline-resistant
*S. aureus* at all, and only **2** measure it against a doxy-PEP
exposure contrast (Soge; arguably DuDHS at a pilot's sample size). The measurement
gap the three streams document inside trials, guidelines, and surveillance is
reproduced in the research literature that surrounds them: the bystander is almost
never named, and when named, almost never measured.

*Caveat — no silent cap:* the classification is a hand reading of the 13 abstracts,
listed by PMID so it is checkable; unclassified retrieved PMIDs default to
`names_only`. The counts are PubMed as of 2026-08-19 and will rise over time.
