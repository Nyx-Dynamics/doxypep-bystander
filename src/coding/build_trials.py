"""Build the Stream A trial corpus and run the reporting analyses.

Loads every `trial_*.yaml` under the coding dir into validated TrialRecords
(each raising if any observation lacks a locator), then runs the observations
analyses (discordance, mechanism blindness, phenotype relabeling, significance
asymmetry) and the Phase C gate. Writes tidy CSVs + `outputs/streamA_result.md`.

`make` target: `python -m src.coding.build_trials`.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.coding.schema_trial import load_trial
from src.analysis import observations as O


def build_trial_corpus(coding_dir: Path | str):
    coding_dir = Path(coding_dir)
    paths = sorted(coding_dir.glob("trial_*.yaml"))
    if not paths:
        raise FileNotFoundError(f"no trial_*.yaml under {coding_dir}")
    return [load_trial(p) for p in paths]


def powered_gate(records) -> list[str]:
    """Phase C gate: trials powered for the resistance endpoint. Non-empty =>
    the Stream A leg weakens; stop and report."""
    return [r.unit for r in records
            if r.powered_for_resistance_endpoint.value == "yes"]


def _write_report(records, obs, disc, relab, mech, prim, root):
    n_trials = len(records)
    n_obs = len(obs)
    # MRSA has primary-trial denominators?
    mrsa_primary = prim[prim["organism"] == "mrsa"] if not prim.empty else prim
    disc_flagged = disc[disc["discordant"]] if not disc.empty else disc
    md = f"""# Stream A result — the same result, reported many ways

{n_trials} trial(s) coded; {n_obs} resistance observations (one per *reported
instance*). First-pass coding (`claude-firstpass`); needs PI verification +
double-coding (Phase F). See `data/processed/trial_observations.csv`.

## Denominator discordance

The same underlying result is reported with different denominators, and the choice
alone moves the headline. Discordant result-groups: **{len(disc_flagged)}**.
"""
    if not disc_flagged.empty:
        for _, r in disc_flagged.iterrows():
            md += (f"\n- **{r['organism']} / {r['arm']} / {r['timepoint']}** — "
                   f"denominators {{{r['denominators']}}} across bases "
                   f"({r['bases']}); the rate moves {r['proportion_ratio']:.1f}x "
                   f"on basis choice alone"
                   f"{'; a source description disagrees with its printed denominator' if r['any_description_mismatch'] else ''}"
                   f"{'; an intervention-affected denominator is in the mix' if r['any_intervention_affected_denominator'] else ''}.")
    md += f"""

## Phenotype relabeling

Reportings that name a different drug than the assay tested: **{len(relab)}**.
NEJM measured *doxycycline* resistance in *S. aureus* (ETEST, MIC >=16); sources
that relabel it "tetracycline" are, per Grossman 2016, not interchangeable —
tet(K) efflux raises tetracycline MIC 64x but doxycycline only 2x.
"""
    if not relab.empty:
        for _, r in relab.iterrows():
            md += (f"\n- {r['source_citation']} ({r['organism']}): measured "
                   f"`{r['phenotype_measured']}`, labeled `{r['phenotype_as_labeled']}` "
                   f"[{r['locator']}]")
    md += f"""

## Mechanism blindness

Can the endpoint separate tet(K) efflux from tet(M) ribosomal protection?
Per-organism (primary-trial observations):
"""
    if not mech.empty:
        for _, r in mech.iterrows():
            md += (f"\n- {r['organism']}: {'BLIND' if r['blind'] else 'discriminating'} "
                   f"({r['methods']})")
    md += f"""

## Detectability input — and a structural gap

Primary-trial denominators feed `detectability.py`. **MRSA has no primary-trial
denominator**: NEJM reports no methicillin breakdown, so the only MRSA numbers
(1/11 doxy, 2/6 control) come from a meta-analysis/CROI restatement. That is a
finding — the endpoint CDC leans on to say "MRSA did not differ between arms" is
not in the primary publication — not a gap to be filled. MRSA rows in the
primary-trial detectability set: **{len(mrsa_primary)}**.

## Gate

{'TRIPPED — a trial is powered for the resistance endpoint; stop and report.' if powered_gate(records) else 'CLEAR — no trial states a power calculation for its resistance endpoint.'}
"""
    (root / "outputs" / "streamA_result.md").write_text(md)


def run(root: Path | str = None):
    root = Path(root) if root else Path(__file__).resolve().parents[2]
    records = build_trial_corpus(root / "data" / "raw" / "coding")
    obs = O.observations_frame(records)
    disc = O.discordance(records)
    relab = O.phenotype_relabeling(records)
    mech = O.mechanism_blindness(records)
    prim = O.primary_trial_denominators(records)

    proc = root / "data" / "processed"
    proc.mkdir(parents=True, exist_ok=True)
    obs.to_csv(proc / "trial_observations.csv", index=False)
    disc.to_csv(proc / "trial_discordance.csv", index=False)
    _write_report(records, obs, disc, relab, mech, prim, root)
    return records, obs, disc, relab, mech, prim


if __name__ == "__main__":
    records, obs, disc, relab, mech, prim = run()
    print(f"coded {len(records)} trial(s); {len(obs)} observations")
    print(f"discordant result-groups: {int(disc['discordant'].sum()) if not disc.empty else 0}")
    print(f"phenotype relabelings: {len(relab)}")
    print(f"MRSA primary-trial denominators: {len(prim[prim['organism']=='mrsa']) if not prim.empty else 0}")
    print("GATE:", "TRIPPED" if powered_gate(records) else "clear")
    print("wrote outputs/streamA_result.md")
