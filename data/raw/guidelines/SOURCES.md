# Stream B — guideline source documents

Immutable source PDFs for guideline coding. DOIs verified 2026-08-18. Each will
be hand-coded to `data/raw/coding/guideline_*.yaml` with a page/section locator
per field (no locator → the builder raises).

| File | Unit | Citation | DOI |
|---|---|---|---|
| `guideline_cdc_mmwr_2024_rr7302a1.pdf` | CDC (US) | Bachmann et al. MMWR Recomm Rep 2024;73(RR-2):1–8 | 10.15585/mmwr.rr7302a1 |
| `guideline_australia_cornelisse_mja_2024.pdf` | Australia | Cornelisse et al. Med J Aust 2024;220:381–6 | 10.5694/mja2.52258 |
| `guideline_germany_dstig_werner_jddg_2024.pdf` | Germany (DSTIG) | Werner et al. J Dtsch Dermatol Ges 2024;22(3):466–78 | 10.1111/ddg.15282 |
| `guideline_ecdc_mardh_eurosurv_2023.pdf` | EU/EEA (ECDC) | Mårdh & Plachouras. Euro Surveill 2023;28(46):2300621 | 10.2807/1560-7917.ES.2023.28.46.2300621 |
| `guideline_sf_provider_guide_2026.pdf` | San Francisco | SFDPH "Doxy-PEP prescribing guide for SF providers" (May 2026) | — (gray literature) |
| `guideline_iusti_europe_2024.pdf` | IUSTI Europe | IUSTI Europe position statement on DoxyPEP, 26 Jun 2024 (Marks et al.) | 10.1177/09564624241273801 (journal ver.); this PDF is the free primary statement |

## Caveats (carry into coding)

- **SF is the May-2026 provider guide, not the Oct-2022 citywide guidance.** Valid
  for guideline-*content* coding (what it requires re: staph monitoring, grading).
  Do NOT use it as the source for the "Oct 2022 exogenous interruption date" —
  that identification claim needs the original 2022 document.
- **IUSTI**: coded from the free IUSTI-hosted PDF, not the paywalled SAGE article
  (same content; the SAGE piece is the journal write-up).
