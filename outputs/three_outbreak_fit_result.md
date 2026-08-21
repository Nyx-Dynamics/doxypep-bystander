# Three-model fit — what shape can the trial MRSA series actually resolve?

Companion to `coverage_null_result.md`; the **MRSA** single-cohort illustration (not the
S. aureus unit — see `selection_ratchet_result.md`). For each observed MRSA carriage
series we fit three nested models by maximum binomial likelihood —

- **flat** `logit p = a` (no change),
- **trend** `logit p = a + b·v` (monotone selection),
- **wave** `logit p = a + b·v + c·v²` (an outbreak: rise then fall) —

compare by AIC (a model is only named "best" when it clears the next by ΔAIC ≥ 2;
otherwise the models are **indistinguishable** and naming one is noise-mining), and
calibrate two likelihood-ratio tests with a parametric bootstrap of 2000 draws (χ² is
unreliable at these counts): **trend-vs-flat** (is there *any* rise?) and **wave-vs-trend**
(is the non-monotone *outbreak curvature* — the clustering signature — real beyond a plain
monotone rise?). A bootstrap p shown as `<0.0005` means no draw reached the
observed statistic. **Detectability, not effect estimation. No causal claim.**

| series | flat / trend / wave AIC | AIC verdict | trend-vs-flat (is there a rise?) | wave-vs-trend (is it an outbreak?) |
|---|---|---|---|---|
| DOXYVAC doxy-PEP arm (MRSA throat carriage) | 454.6 / 442.4 / 443.8 | **trend** | p=<0.0005 | p=0.434 |
| DOXYVAC no-PEP arm (MRSA throat carriage) | 177.2 / 176.7 / 176.4 | indistinguishable (ΔAIC 0.8) | p=0.107 | p=0.146 |

**Reading.** The two bootstrap columns separate two questions the trials' non-monotone
series conflate:

- **Is there a rise?** In the doxy-PEP arm, yes — the monotone trend beats flat
  (bootstrap p <0.0005, no null draw reached it),
  consistent with Vanbaelen's within-arm p<0.0001. In the no-PEP arm the rise is not
  resolved (p=0.107), and all three models sit within
  0.8 AIC unit — **indistinguishable**; the earlier "best=wave"
  reading was a 0.8-AIC artifact and is struck.
- **Is it an outbreak?** In *neither* arm does the wave earn its curvature parameter over
  a monotone trend (wave-vs-trend bootstrap p=0.43
  doxy, 0.15 no-PEP; wave never lowers AIC by the ~2
  units that would mark a real improvement). The non-monotonicity — the M6 crossover, the
  M9 dip, the "up-up-up-down-up" lurch — is **within noise**.

So the data can, at most and in one arm, establish *that* carriage rose; they cannot
identify *how*. A monotone selection trend and a clustered, wave-like transmission
process fit the series equally well. The mechanism is unidentifiable from these
endpoints at these denominators.

This is the disciplined form of the ¶4 claim, and it holds the line the manuscript
already draws: the non-monotonicity is **illustration, not proof**. The trajectories
*are* what clustered, cross-sectionally sampled transmission would produce; they are
*also* statistically indistinguishable from a plain trend or from noise at n≈120–330/
visit with single-to-low-double-digit counts. Both halves are true, and together they
indict the instrument, not establish an outbreak. The DoxyPEP resistance series is
sparser still (2–3 post-baseline points per arm) and cannot even be brought to this
test — a further instance of the same gap.

Paired with `coverage_null_result.md` — which shows a mean-based MRSA endpoint *would* be
blind to clustering it did contain, misreading a flat process as a trend the large
majority of the time at the empirically anchored between-cohort σ̂≈2.7
(`dejong_sigma_result.md`) — this closes the loop: the design cannot see the clustering
*shape* in principle, and cannot rule it out in these data. (MRSA-scoped throughout; the
S. aureus selection question is `selection_ratchet_result.md`.)

(`SEED=20260820`, `N_BOOT=2000`; regenerate with `python -m src.analysis.three_outbreak_fit`.)
