# Guideline source checksums + staph keyword-search verification

Generated 2026-08-19. Each negative/near-null coding of `s_aureus_*` is
pinned to a file SHA-256 and a full-text case-insensitive keyword count.
Terms: Staphylococcus/staph/aureus, MRSA, MSSA, methicillin[-resistant],
tet(K), tet(M), skin-and-soft-tissue, SSTI, nasal carriage, nares,
coagulase, USA300.

| File | staph-term hits | chars | SHA-256 | where |
|---|---|---|---|---|
| `guideline_australia_cornelisse_mja_2024.pdf` | 0 | 36992 | `0c6b1e2743b9d6aede5fecf56caba54ce49767184349c5375de0799738b70697` | (none) |
| `guideline_cdc_mmwr_2024_rr7302a1.pdf` | 23 | 44933 | `724a32c1b168de49d57e84a581848ff3b1579d9842f2787970116fb69d7092f3` | staphylococc\w*:3@p[6, 10]; aureus:11@p[6, 9, 10]; methicillin[- ]?resist\w*:1@p[6]; methicillin:3@p[6, 10]; staph\w*:3@p[6, 10]; tet\(?M\)?:1@p[9]; nares:1@p[6] |
| `guideline_chicago_cdph_protocol_2023.pdf` | 0 | 13623 | `c25ad2fd0fa89f1b0db8800f7e7a91155bd9a34f96cb34903812ebe94b89b488` | (none) |
| `guideline_detroit_pubhealth_std_2022.pdf` | 0 | 4835 | `db244a6a9351481642349994985a0935165cca9306f054ab27ed612f66aa9caa` | (none) |
| `guideline_ecdc_mardh_eurosurv_2023.pdf` | 4 | 22489 | `0fcce4015dc3d5105db2580d61a1f1f926926f7c2915a367493116659daea3a2` | staphylococc\w*:1@p[2]; aureus:2@p[2]; staph\w*:1@p[2] |
| `guideline_la_county_factsheet_2023.pdf` | 1 | 2720 | `432716a59307ff3fb62a5558bb8fc684f05af8f98dd8532fd2a742c8a6d16887` | staph\w*:1@p[1] |
| `guideline_maryland_doh_factsheet_2024.pdf` | 0 | 1658 | `131934e5e23feee1e92ee6942a63084ce15889cdfcac734c791ae2b6ad17d226` | (none) |
| `guideline_massachusetts_dph_2024.pdf` | 0 | 4156 | `d3220e9f3d91b844a0770064699d498742431a28313aebbc6a840db6898d8e9a` | (none) |
| `guideline_nyc_dohmh_dearcolleague_2023.pdf` | 1 | 15739 | `63b173b9578d05c2b99edbe941d2621ddaa9b35c5ff5d555442e1b5cdfaaa989` | staph\w*:1@p[4] |
| `guideline_philadelphia_pdph_han_2024.pdf` | 1 | 5609 | `71d91542ca062c5f4493955da99e748762ab88c2956341e3f748acab04878e28` | aureus:1@p[2] |
| `guideline_ri_doh_page_2026.pdf` | 0 | 6565 | `287cdedc499f2cc84477e58b2564ddf01127543202269841a5b23bc96f40bef3` | (none) |
| `guideline_san_diego_cahan_2023.pdf` | 3 | 7751 | `fe3e2afc8945c409b205d510aacf5988f44c5abdeba60ba9de9ffc2617038c22` | staphylococc\w*:1@p[2]; aureus:1@p[2]; staph\w*:1@p[2] |
| `guideline_sf_provider_guide_2026.pdf` | 0 | 6373 | `3540e87916e409b00aab83f857ba02210088c63eab0bab8030124ab1da910a58` | (none) |
| `guideline_who_2026.pdf` | 3 | 34888 | `b4154b68f43e4521d349be04d9362847bbceb7a1469bb06baf3a549c12056e02` | staphylococc\w*:1@p[17]; aureus:1@p[17]; staph\w*:1@p[17] |

## Cross-check vs codings (2026-08-19)

Every coded `s_aureus_*` value matches its keyword count:
- **0 staph hits** (silent/absent): Chicago, Detroit, Maryland, Massachusetts, RI, SF, Australia.
- **named in body_text**: San Diego (p2), CDC (p6/9/10 — 23 hits, the richest discussion), ECDC (p2, pending scope).
- **still_learning_list**: LA County (1 hit, p1, "for example staph").
- **patient_counselling_script**: NYC (1 hit, p4, "staph infections").
- **reference_title_only** (cites the S. aureus evidence, never carries it into text):
  - WHO → Soge et al. citation (p17).
  - Philadelphia → Luetkemeyer CROI 2023 abstract citation (p2).

Correction logged: WHO was initially miscoded `absent`; the exhaustive search found
the single Soge-reference mention a plain grep had missed. That is the reason for
this verification pass.
