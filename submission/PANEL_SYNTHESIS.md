# Adversarial Panel — Synthesis & Revision Punch-List

Six independent reviewers, each briefed to attack a different flank: ID clinician,
molecular-AMR microbiologist, surveillance epidemiologist, biostatistician,
meta-science/ethics, and a handling editor (triage + venue). None saw the others.

## Convergence

**Recommendation — unanimous (6/6):** publishable, *not* as Original Research but as a
**Perspective / Analysis / Methodological Critique**. Severity ranged from "accept with
minor revision" (ID, meta-science, AMR) through "minor-to-moderate" (surveillance) to
"major revision" (biostatistician) and "send for review, major revision expected"
(editor). No reviewer recommended reject. The reproducibility, the pre-registered
locators/hashing, and — repeatedly cited as the paper's shield — the disciplined refusal
of any causal claim are what keep it out of desk-reject territory.

**The one structural strength every reviewer credited independently:** the "one yardstick
across three streams" instrument, and the surveillance seam (CLSI M39 methicillin axis,
NARMS excluding *S. aureus*, ABCs reporting the MRSA split) — named by the editor as "the
paper's most bulletproof and most transferable result," by meta-science as "genuinely new
in its *unification*," and by surveillance as "real structural observation, not rhetoric."
Two reviewers say the same thing: **lead with the instrument, demote the trial autopsy.**

## Revision punch-list, by priority

### P0 — load-bearing; a knowledgeable referee *will* catch these
1. **Restore the panel-power correction to Stream C.** Flagged independently and forcefully
   by BOTH the biostatistician and the surveillance epidemiologist as the single most
   exposed number in the paper — and it is the exact vulnerability the repo's own
   `feasibility_result.md` flags. The manuscript prints only the single-comparison
   dilution figures (0/135; RR_needed 2.9–53) while the code shows that under the panel
   design actually under test (≈52 geographies × 14 yr, DEFF=1) the median RR_needed
   collapses to ≈2.94, 25/135 cells become nominally detectable, and the best case flips
   to RR_needed ≈1.07. **Fix:** report the panel numbers in-text; anchor the claim on the
   *realistic* cell (RR_needed ≈14–64 across DEFF, robustly above Soge's 1.42); explicitly
   disown the best case as a compound of four implausibilities that fails on any one.
2. **Reframe the per-carrier 8.5%→40% figure and the 5/16/28 "discordance."** Named the
   "single most attackable move" by the editor and touched by ID, biostat, and
   meta-science. You cannot in one paper say the counts don't reconcile *and* foreground a
   specific per-carrier rate computed from those counts. **Fix:** present 8.5→40% strictly
   as a bounded denominator-sensitivity illustration (state the 16/40 numerator, the tiny
   denominator, and that it inherits the same withheld-data uncertainty); add a
   reconciliation table showing which denominator/timepoint/venue each of 5/16/28 uses;
   soften "the counts do not reconcile" to "are reported over differing/undocumented
   denominators and cannot be reconciled from the public record" — no implication of
   impropriety.

### P1 — substantive; fixable without new analysis
3. **Soften the clustering "measured property" claim and fix the study count.** The
   biostatistician: σ̂≈2.7 is a between-*cohort* dispersion transported into a
   between-*visit* simulation — an upper bound on a *different* variance component, not a
   measured property of the trial endpoint. Also: σ̂ is fit on **10** cohorts, but §2.3 and
   the docstrings say "18 studies," and 4 zero-count cohorts make the upper CI unstable.
   **Fix:** reconcile the count; report σ̂ as "≈2.7 (large; lower bound ~1.7)" without the
   two-sig-fig precision; reframe the Type-I claim as explicitly conditional/illustrative
   ("*if* between-visit dispersion reached even the low end…"), and drop "not an impression
   but a measured property."
4. **Fix the tet(K) "inducible doxycycline resistance" wording.** The molecular-AMR
   reviewer: "inducible" in the cited Liu 2011 context describes clindamycin/MLS_B, not
   tet(K); tet(K) is efflux and constitutive/regulated but not the "inducible doxycycline
   resistance" the sentence implies. This **adjudicates the open citation tension** — the
   specialist reading wins; verify against Liu 2011 and correct the clause. Also relax
   "doxycycline pressure shifts the population toward tet(M)" to a guarded statement, and
   acknowledge tet(L)/tet(38)/tigecycline so the mechanism section isn't over-tidy.
5. **"Loss of a whole class" → "oral tetracyclines," and cast as stake-sizing.** ID,
   molecular-AMR, and meta-science all flag it as the chief rhetorical over-reach. tet(M)
   does not remove tigecycline/omadacycline/eravacycline. **Fix:** "the oral tetracycline
   option"; frame the passage as *what is at stake if a signal accrues*, not a prediction.
6. **Make the *S. aureus*-vs-MRSA reliance an up-front scope condition.** Editor,
   surveillance, biostat: the empirical spine (clustering, denominator, sampling frame) is
   MRSA, so the unit choice currently reads as rhetorical. The §4 reflexive move ("we are
   forced onto MRSA… that absence *is* the argument") is the right defense — **promote it
   to the Introduction** as a stated scope condition and an exhibit of measurement
   inheritance, so it reads as operational, not a late concession.
7. **"unmeasurable" → "unmeasured as currently instrumented," consistently.** Meta-science
   and surveillance: the abstract/intro say "unmeasurable" while §4/§5 give the recipe to
   measure it. The externality claim is *stronger* as an unpriced-but-priceable one. Global
   find-and-replace with care.

### P2 — strengthens; lower urgency
8. **Own the frame-dependence of the Stream C zero** (surveillance): state that "0/12" is
   conditional on requiring a population denominator, which disqualifies antibiograms
   before coding; name-and-dispose ELR/EIP isolate-level AST feeds, NSSP/ESSENCE, and
   commercial AST networks so "12" doesn't read as gerrymandered; narrow "the phenotype
   half does not exist" to "is not reported/linked at a population denominator."
9. **Position "measurement inheritance" against its neighbors** (meta-science): one
   paragraph distinguishing it from post-hoc power, ascertainment/surveillance bias,
   construct validity, the McNamara fallacy — the contribution is the *unification*. Scope
   generality honestly as "a worked instance offered for testing elsewhere."
10. **Credit the benefit side of the distributive-justice ledger** (meta-science): name the
    normative premise (the duty to measure attaches to whoever internalizes the benefit)
    and acknowledge doxy-PEP's measured benefit, so the justice claim is about *foreclosed
    weighing*, not presumed net harm.
11. **Tone pass to the "quiet" register** (editor): a few passages ("the concern is reported
    in the one place the exposure did not move it," "keeps the same signal out of the
    headline") edge back toward the prosecutorial turn the author's own notes disavow.
12. Minor accuracy: NARMS has a gonococcal arm (don't imply enteric-only); confirm CLSI
    M39 edition designation (5th ed. dropped the "-A"); state Soge's own caveat (any-use was
    *not* associated; 1.42 is the >3-doses/month contrast) at first use; Fig 2 caption vs
    text disagree on which is "the load-bearing gap" (denominator vs unit) — pick one.

## Per-reviewer one-line
- **ID clinician** — minor revision; "loss of a class" overreach, colonization→infection gap, 5/16/28 framing.
- **Molecular-AMR** — minor-moderate; "inducible" unsupported, tet(M)-shift overstated, tet(L)/38/tigecycline, "whole class"→"oral tetracyclines."
- **Surveillance epidemiologist** — minor-moderate; panel-power omission, frame-dependent zero, closed-universe completeness (EIP/ELR), reframe "phenotype half does not exist."
- **Biostatistician** — major; panel-power omission (selective reporting), σ between-cohort→between-visit + "18 vs 10" + false precision.
- **Meta-science/ethics** — accept, minor-moderate; position the construct vs neighbors, scope generality, "unmeasurable"→"unmeasured," credit benefit side.
- **Handling editor** — send for review; disclaimer-vs-payload tension, per-carrier 40% flashpoint, lead with the instrument. Venue: PLOS Biology Meta-Research → JAC-AMR → EID; medRxiv now.
