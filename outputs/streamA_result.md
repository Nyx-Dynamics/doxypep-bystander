# Stream A result — the same result, reported many ways

1 trial(s) coded; 20 resistance observations (one per *reported
instance*). First-pass coding (`claude-firstpass`); needs PI verification +
double-coding (Phase F). See `data/processed/trial_observations.csv`.

## Denominator discordance

The same underlying result is reported with different denominators, and the choice
alone moves the headline. Discordant result-groups: **5**.

- **s_aureus / doxy / month6** — denominators {51, 192} across bases (all_participants_swabbed, colonized_participants); the rate moves 3.8x on basis choice alone.
- **s_aureus / doxy / month12** — denominators {31, 111} across bases (all_participants_swabbed, colonized_participants); the rate moves 3.6x on basis choice alone; an intervention-affected denominator is in the mix.
- **s_aureus / control / month6** — denominators {29, 75} across bases (all_participants_swabbed, colonized_participants); the rate moves 2.6x on basis choice alone.
- **s_aureus / combined / baseline** — denominators {215, 483} across bases (all_participants_swabbed, colonized_participants); the rate moves 2.2x on basis choice alone.
- **s_aureus / control / month12** — denominators {24, 51} across bases (all_participants_swabbed, colonized_participants); the rate moves 2.1x on basis choice alone.

## Phenotype relabeling

Reportings that name a different drug than the assay tested: **10**.
NEJM measured *doxycycline* resistance in *S. aureus* (ETEST, MIC >=16); sources
that relabel it "tetracycline" are, per Grossman 2016, not interchangeable —
tet(K) efflux raises tetracycline MIC 64x but doxycycline only 2x.

- Szondy 2024 Table 2 (Int J Infect Dis 147:107186) (mssa): measured `doxycycline`, labeled `tetracycline` [Szondy Table 2, p. 6 (DoxyPEP, S. aureus MSSA)]
- Szondy 2024 Table 2 (mrsa): measured `doxycycline`, labeled `tetracycline` [Szondy Table 2, p. 6 (DoxyPEP, S. aureus MRSA)]
- Szondy 2024 Table 2 (mssa): measured `doxycycline`, labeled `tetracycline` [Szondy Table 2, p. 6]
- Szondy 2024 Table 2 (mrsa): measured `doxycycline`, labeled `tetracycline` [Szondy Table 2, p. 6]
- Szondy 2024 Table 2 (mssa): measured `doxycycline`, labeled `tetracycline` [Szondy Table 2, p. 6]
- Szondy 2024 Table 2 (mrsa): measured `doxycycline`, labeled `tetracycline` [Szondy Table 2, p. 6]
- Szondy 2024 Table 2 (mssa): measured `doxycycline`, labeled `tetracycline` [Szondy Table 2, p. 6]
- Szondy 2024 Table 2 (mrsa): measured `doxycycline`, labeled `tetracycline` [Szondy Table 2, p. 6]
- CDC MMWR 2024 (Bachmann) (s_aureus): measured `not_stated`, labeled `tetracycline` [CDC MMWR p. 6 (Potential Resistance in Commensals)]
- CDC MMWR 2024 (Bachmann) (s_aureus): measured `not_stated`, labeled `tetracycline` [CDC MMWR p. 6]

## Mechanism blindness

Can the endpoint separate tet(K) efflux from tet(M) ribosomal protection?
Per-organism (primary-trial observations):

- s_aureus: BLIND (standard_breakpoint)

## Detectability input — and a structural gap

Primary-trial denominators feed `detectability.py`. **MRSA has no primary-trial
denominator**: NEJM reports no methicillin breakdown, so the only MRSA numbers
(1/11 doxy, 2/6 control) come from a secondary synthesis (Szondy SR/MA, a
re-tabulation of the same data) / the CROI 2023 abstract — not the primary
publication. MRSA rows in the primary-trial detectability set: **0**.

Note (high-scrutiny): the CDC MMWR S. aureus figures (20/428 -> 28/222) are coded
as UNRESOLVED, not as a reconciliation failure — the assay/provenance
(NEJM doxycycline ETEST vs CROI) and the analysis population behind those
denominators are not yet established. See the CDC observations' notes; resolve
before any manuscript use.

## Gate

CLEAR — no trial states a power calculation for its resistance endpoint.
