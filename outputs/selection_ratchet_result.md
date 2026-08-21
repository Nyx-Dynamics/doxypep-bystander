# The selection ratchet — S. aureus within US DoxyPEP (S. aureus-scoped)

The clean single-trial, single-assay test of whether doxycycline resistance in
*S. aureus* accumulates under selection. Colonization, doxy-R, and susceptible carriage
share the same cultures, timepoints, and denominators (CROI 2023 OA-3 published abstract
table — the same source §3.1 cites; M0 and M12 only). **No cross-trial pooling.
Directional confirmatory tests only — two endpoints cannot support shape discovery. No
causal claim.**

**Arithmetic base (verified).** The reported resistance figure (3.6% → 11.7%) is over the
WHOLE COHORT (all-swabbed), not carriers — in the abstract table every doxy-R cell shares
its denominator with the isolation cell beside it. Per carrier (dividing by colonization)
it is **8.5% → 40%** (12/141 → 16/40). The manuscript's stated "fraction-of-carriers"
reading applies to that *derived* per-carrier series, not the raw all-swabbed figure.

## Doxy-PEP arm — the ratchet

| quantity (of all swabbed) | baseline | month 12 |
|---|---|---|
| colonization | 42% | 29% |
| doxy-R (reported, all-swabbed) | 3.6% | 11.7% |
| **susceptible carriage** | **38.6%** | **17.5%** |
| per-carrier doxy-R | 8.5% | 40.0% |

- **Susceptible carriage depletes**, consistent with the decline selection predicts:
  one-sided trend test **p = 4.5e-06**
  (39% → 18% of all swabbed).
- **Per-carrier resistance rises**: 12/141
  (8.5%) → 16/40
  (40.0%), one-sided Fisher **p = 9.6e-06**.
- **Conservation-of-carriers / selection vs neutral suppression.** Resistant carriage
  *rose* absolutely (3.6% →
  11.7% of all swabbed) *even though* total
  colonization *fell* (42% →
  29%). Neutral suppression — clearing carriage
  regardless of resistance — predicts resistant carriage should fall in proportion, to an
  expected ~3 resistant carriers at M12; **16**
  were observed (one-sided Poisson **p = 6.4e-07**). The susceptible loss
  decomposes as (total-carriage loss) + (resistant expansion): susceptibles are cleared
  while resistants expand — the ratchet.

## SOC arm — uninformative (as expected)

| quantity (of all swabbed) | baseline | month 12 |
|---|---|---|
| colonization | 48% | 45% |
| susceptible carriage | 36.6% | 40.3% |
| per-carrier doxy-R | 24.4% | 10.7% |

The SOC susceptible series does not deplete (it rises, 37% → 40%;
decline p = 0.69, not significant) and per-carrier resistance
*falls* (24.4% → 10.7%; increase Fisher
p = 0.97). With 62 swabbed at M12 this arm is
**underpowered and uninformative**, not a contrasting shape — stated as such.

**Licenses.** S. aureus susceptible carriage depletes consistent with selection and the
resistant fraction rises — the ratchet — in the doxy-PEP arm; the SOC arm is
uninformative. This is a directional, hypothesis-confirming result on the S. aureus unit,
not a fitted model and not a causal claim.

(Regenerate with `python -m src.analysis.selection_ratchet`.)
