# Stream B — sampling frame, scope, and retrieval log

*Written 2026-08-19, while the corpus was fresh. This is the methods-section
provenance for the guideline coding.*

## Sampling frame

The frame was assembled from a third-party compilation plus a fixed set of
authoritative bodies — **not** an ad-hoc search:

- **NCSD "Doxy and STI PEP Sample Policies" compilation** (National Coalition of
  STD Directors) — the base list of US jurisdictional doxy-PEP policies.
- Plus, by design, four apex/anchor bodies: **WHO** (global), **CDC** (US
  national), the **Australian** consensus statement, and the **UK BASHH** position
  (international contrast).

## Scope filter (governmental authorities only)

The unit of analysis is a **governmental public-health authority** — city, county,
state, national, or global. Rationale: these bodies both (a) set doxy-PEP policy
and (b) hold the local surveillance / outbreak record, and that pairing is what
makes the institutional-memory comparison meaningful. This is a scope decision,
not a finding.

## Exclusions (with reasons)

Excluded documents are retained in `data/raw/guidelines/excluded/` with per-file
reasons (`excluded/README.md`). Categories excluded and why:

- **FQHCs / community health centers** — relay their health department's language
  rather than making the policy decision under study: Howard Brown Health
  (Chicago), Open Door Health (Providence RI; note RI DOH↔Open Door is a
  *collaboration*, entangled — see DECISIONS), Callen-Lorde (NYC), Fenway Health
  (Boston).
- **Patient-navigation / outreach** — VOISES (Johns Hopkins/Baltimore).
- **Nonprofit advocacy / patient education** — American Sexual Health Association
  (ASHA, national).
- **Professional societies** — German STI Society (DSTIG), IUSTI Europe.
- **Advocacy comments** — Fenway Health's public *comment to CDC* (a submission,
  not a jurisdictional policy).

Coding these would grade safety-net providers / advocacy bodies on a policy
judgement they do not own and dilute the monitoring column with documents that
were never going to specify monitoring.

`ECDC` (EU/EEA considerations) is left pending a PI call — an EU agency document
but a meeting report, not a jurisdictional policy with a matched surveillance
record.

## Retrieval log (as of 2026-08-19)

**Obtained and in corpus (14 governmental units):**
WHO (global); CDC (US national); Australia (national consensus); and city/county/
state: NYC DOHMH, Chicago CDPH, Philadelphia PDPH, Detroit Public Health, San
Diego County, Los Angeles County, San Francisco DPH, Maryland DOH, Massachusetts
DPH, Rhode Island DOH (pointer stub — substantive guidance entangled with Open
Door / RI PHI). *v2-coded: 9; CDC / SF / Australia / RI in hand, coding pending.*

**Attempted but NOT retrieved (flagged; a corpus of public documents should log
which stopped being public):**

| Jurisdiction | Status (2026-08-19) |
|---|---|
| **Seattle–King County** | Landing page **errors** on access; the PDF is reportedly reachable via `cdn.kingcounty.gov`. Access failure recorded; retrieval outstanding. |
| **UK BASHH** (international contrast) | Named in the frame; position document not yet retrieved. |
| California DPH (statewide) | Not retrieved; check whether a CDPH v2.0 post-dates the June-2024 CDC guidance. |
| Alameda, Santa Clara (CA) | Not retrieved. |
| Multnomah / Oregon | Not retrieved. |
| Minnesota | Not retrieved. |
| New Mexico | Not retrieved. |
| Michigan (state) | Detroit (city) obtained; state-level not retrieved. |
| Jefferson County | Not retrieved. |

Absence in this corpus means "not retrieved under the stated attempts as of the
date above," never "does not exist." Re-attempts and any further access failures
should be appended here with dates.
