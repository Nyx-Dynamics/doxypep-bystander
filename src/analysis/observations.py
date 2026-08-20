"""Stream A analyses of how results are reported.

`src/analysis/observations.py` (was denominators.py). Three questions:

- `discordance` — where sources disagree on the denominator for one result.
- `mechanism_blindness` — which organisms get an endpoint that resolves tet(K)
  from tet(M), and which get one that cannot.
- `phenotype_relabeling` — where a source names a different drug than was tested.

None of these are data-quality problems to clean away. They are the findings.
"""
from __future__ import annotations

import pandas as pd

GROUP = ["unit", "arm", "timepoint", "organism", "phenotype_measured"]


def observations_frame(records) -> pd.DataFrame:
    """Flatten every coded observation across trials into one tidy frame."""
    rows = []
    for r in records:
        for o in r.observations:
            rows.append({
                "unit": r.unit, "trial_name": r.trial_name,
                "source_type": o.source_type, "source_citation": o.source_citation,
                "arm": o.arm, "timepoint": o.timepoint, "organism": o.organism,
                "phenotype_measured": o.phenotype_measured,
                "phenotype_as_labeled": o.phenotype_as_labeled,
                "relabeled": o.relabeled,
                "mechanism_discriminating": o.mechanism_discriminating,
                "discrimination_method": o.discrimination_method,
                "numerator": o.numerator, "denominator": o.denominator,
                "proportion": o.proportion,
                "denominator_basis": o.denominator_basis,
                "denominator_intervention_affected":
                    o.denominator_intervention_affected,
                "description_denominator_mismatch":
                    o.description_denominator_mismatch,
                "significance_reported": o.significance_reported,
                "p_value": o.p_value, "locator": o.locator,
            })
    return pd.DataFrame(rows)


def discordance(records) -> pd.DataFrame:
    """One row per underlying result; flags where reportings disagree.

    `proportion_ratio` is how far the headline number moves purely on the choice
    of denominator."""
    df = observations_frame(records)
    if df.empty:
        return pd.DataFrame(columns=GROUP)

    out = []
    for key, g in df.groupby(GROUP, dropna=False):
        props = g["proportion"]
        out.append({
            **dict(zip(GROUP, key)),
            "n_reportings": len(g),
            "n_bases": g["denominator_basis"].nunique(),
            "bases": ", ".join(sorted(g["denominator_basis"].unique())),
            "n_distinct_denominators": g["denominator"].nunique(),
            "denominators": ", ".join(str(d) for d in sorted(g["denominator"].unique())),
            "proportion_min": props.min(),
            "proportion_max": props.max(),
            "proportion_ratio": (props.max() / props.min()) if props.min() > 0 else float("nan"),
            "discordant": g["denominator_basis"].nunique() > 1
                          or g["denominator"].nunique() > 1,
            "any_description_mismatch":
                (g["description_denominator_mismatch"] == "yes").any(),
            "any_intervention_affected_denominator":
                (g["denominator_intervention_affected"] == "yes").any(),
            "sources": " | ".join(g["source_citation"]),
        })
    return pd.DataFrame(out).sort_values(
        ["discordant", "proportion_ratio"], ascending=[False, False])


def mechanism_blindness(records) -> pd.DataFrame:
    """Per organism: was the endpoint able to resolve tet(K) from tet(M)?

    The expected asymmetry — mechanism-discriminating assays for the in-category
    organism (gonococcus), mechanism-blind ones for the bystander (S. aureus) — is
    the thesis at the level of the assay. Confirm it here rather than assume it."""
    df = observations_frame(records)
    if df.empty:
        return pd.DataFrame()
    df = df[df["source_type"] == "primary_trial"]
    if df.empty:
        return pd.DataFrame()

    out = []
    for (unit, organism), g in df.groupby(["unit", "organism"]):
        n = len(g)
        n_disc = (g["mechanism_discriminating"] == "yes").sum()
        out.append({
            "unit": unit, "organism": organism,
            "n_observations": n,
            "n_discriminating": int(n_disc),
            "share_discriminating": n_disc / n,
            "methods": ", ".join(sorted(g["discrimination_method"].unique())),
            "blind": n_disc == 0,
        })
    return pd.DataFrame(out).sort_values(["unit", "organism"])


def blindness_asymmetry(records) -> pd.DataFrame:
    """Within each trial, contrast in-category vs bystander organisms.

    `asymmetric` is True where a trial resolved mechanism for gonococcus/commensal
    Neisseria but not for S. aureus — the same laboratory, the same study, two
    standards of measurement."""
    m = mechanism_blindness(records)
    if m.empty:
        return m
    IN_CATEGORY = {"n_gonorrhoeae", "commensal_neisseria", "c_trachomatis"}
    BYSTANDER = {"s_aureus", "mssa", "mrsa", "gas"}

    out = []
    for unit, g in m.groupby("unit"):
        inc = g[g["organism"].isin(IN_CATEGORY)]
        byst = g[g["organism"].isin(BYSTANDER)]
        if inc.empty or byst.empty:
            continue
        out.append({
            "unit": unit,
            "in_category_organisms": ", ".join(inc["organism"]),
            "in_category_any_discriminating": bool((~inc["blind"]).any()),
            "bystander_organisms": ", ".join(byst["organism"]),
            "bystander_any_discriminating": bool((~byst["blind"]).any()),
            "asymmetric": bool((~inc["blind"]).any() and byst["blind"].all()),
        })
    return pd.DataFrame(out)


def cross_trial_blindness(records) -> pd.DataFrame:
    """The mechanism asymmetry is CROSS-trial. In-category organisms get
    mechanism-discriminating assays (tetM PCR / WGS / high-level breakpoint), the
    bystander S. aureus gets mechanism-blind ones (standard breakpoint / disc
    diffusion) — but largely in DIFFERENT trials, so the within-trial
    `blindness_asymmetry()` is empty. This contrasts across the whole corpus."""
    m = mechanism_blindness(records)
    if m.empty:
        return pd.DataFrame()
    IN_CATEGORY = {"n_gonorrhoeae", "commensal_neisseria", "c_trachomatis"}
    BYSTANDER = {"s_aureus", "mssa", "mrsa", "gas"}
    out = []
    for cat, members in [("in_category", IN_CATEGORY), ("bystander", BYSTANDER)]:
        g = m[m["organism"].isin(members)]
        if g.empty:
            continue
        methods = sorted({x for row in g["methods"] for x in row.split(", ")})
        out.append({
            "category": cat,
            "units_organisms": ", ".join(f"{u}:{o}" for u, o in zip(g["unit"], g["organism"])),
            "any_discriminating": bool((~g["blind"]).any()),
            "all_blind": bool(g["blind"].all()),
            "methods": ", ".join(methods),
        })
    return pd.DataFrame(out)


def phenotype_relabeling(records) -> pd.DataFrame:
    """Reportings that name a different drug than the assay tested.

    Motivating case: NEJM measured doxycycline resistance in S. aureus (ETEST,
    MIC >=16 ug/mL); CDC MMWR describes the same trial as evaluating tetracycline
    resistance. Given tet(K), those labels are not interchangeable."""
    df = observations_frame(records)
    if df.empty:
        return df
    cols = ["unit", "source_type", "source_citation", "organism",
            "phenotype_measured", "phenotype_as_labeled", "locator"]
    return df[df["relabeled"]][cols].reset_index(drop=True)


def significance_asymmetry(records) -> pd.DataFrame:
    """Results where only one level of comparison's significance was reported.

    DoxyPEP: a significant within-arm increase alongside a non-significant
    between-arm difference. Reporting either alone changes the conclusion."""
    df = observations_frame(records)
    if df.empty:
        return pd.DataFrame()
    g = (df.groupby(GROUP)["significance_reported"]
           .agg(lambda s: set(s) - {"none"}).reset_index())
    g["levels_reported"] = g["significance_reported"].apply(
        lambda s: ", ".join(sorted(s)) if s else "none")
    g["one_sided_only"] = g["significance_reported"].apply(
        lambda s: s in ({"within_arm"}, {"between_arm"}))
    return g.drop(columns=["significance_reported"])


def saureus_measurement_heterogeneity(records) -> pd.DataFrame:
    """Per trial: how was *S. aureus* measured? The columns are the axes on which the
    trials differ — assay, body site, denominator basis, phenotype axis, mechanism
    discrimination. The claim it evidences (manuscript S3.1) is that they differ
    enough to resist pooling: one trial measures doxycycline resistance *within*
    S. aureus by E-test over an all-swabbed denominator, another by disc diffusion in
    a handful of carriers, a third measures MRSA *carriage prevalence* — a different
    axis entirely. None resolves mechanism (tet(K) vs tet(M))."""
    RESISTANCE_PHENO = {"doxycycline", "tetracycline", "minocycline"}
    SA_ORGS = {"s_aureus", "mssa", "mrsa"}
    rows = []
    for r in records:
        sa = [o for o in r.observations if o.organism in SA_ORGS]
        # first-party observations only (primary trial or the trial's own abstract)
        prim = [o for o in sa
                if o.source_type in {"primary_trial", "conference_abstract"}]
        measures_resistance = any(o.phenotype_measured in RESISTANCE_PHENO
                                  for o in prim)
        if measures_resistance:
            axis = "resistance-within-S.aureus"
        elif sa:
            axis = "carriage/other"
        else:
            axis = "not coded (see trial note)"
        methods = sorted({o.discrimination_method for o in prim} - {"none"})
        rows.append({
            "trial": r.trial_name,
            "s_aureus_measured": r.s_aureus_measured.value,
            "assay": (r.susceptibility_method.quote
                      if r.susceptibility_method else None),
            "body_site": r.body_site.quote if r.body_site else None,
            "phenotype_axis": axis,
            "organisms_coded": ", ".join(sorted({o.organism for o in sa})) or "(none)",
            "phenotypes": ", ".join(sorted({o.phenotype_measured for o in prim})) or "-",
            "denominator_bases": ", ".join(sorted({o.denominator_basis for o in prim})) or "-",
            "discriminating_method": ", ".join(methods) or "none",
            "any_mechanism_discriminating": any(o.mechanism_discriminating == "yes"
                                                for o in prim),
            "n_firstparty_obs": len(prim),
        })
    df = pd.DataFrame(rows)
    # a crude poolability flag: pooling needs a shared axis AND a shared denominator
    if not df.empty:
        df["shared_axis"] = df["phenotype_axis"].nunique() == 1
        df["shared_denominator_basis"] = (
            df["denominator_bases"].nunique() == 1
            and "-" not in set(df["denominator_bases"]))
    return df.sort_values("trial").reset_index(drop=True)


def primary_trial_denominators(records) -> pd.DataFrame:
    """Detectability inputs: primary-trial observations only, per basis.

    Where a result carries more than one basis, detectability is computed for each
    and reported as a range — the coder does not choose."""
    df = observations_frame(records)
    if df.empty:
        return df
    return (df[df["source_type"] == "primary_trial"]
            .sort_values(GROUP + ["denominator_basis"])
            .reset_index(drop=True))
