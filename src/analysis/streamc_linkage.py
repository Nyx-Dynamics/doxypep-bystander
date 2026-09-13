"""Stream C — the linkage decomposition (intro ¶6, third leg).

Re-anchored 2026-08-20. The prior Stream C "0/81" was a dilution PARAMETER GRID, not a
denominator of surveillance systems (see DECISIONS.md Stream C CHECKPOINT). This module
answers the actual linkage claim against a principled, closed universe of established US
public-health surveillance systems (`data/raw/coding/streamc_surveillance_systems.yaml`):
does any DEPLOYED system link doxy-PEP exposure to S. aureus tetracycline/doxycycline
resistance at a common population denominator?

The claim is decomposed into three capabilities, coded per system, so the failure is
specific rather than a bare count:
  (1) exposure-side capture — doxy-PEP/doxycycline exposure at a population denominator;
  (2) phenotype-side capture — S. AUREUS TETRACYCLINE resistance at a population
      denominator (the analytic unit; MRSA/methicillin systems are a wrong-unit near-miss,
      Contract 2, flagged not counted);
  (3) the join — any system linking the two at a common denominator.

Contract 1: capability/linkage/resolution, never an effect. Contract 3: DEPLOYED systems,
not measurement in principle. The dilution leg (`dilution.py`/`dilution_metro.py`, now
0/135 not 0/81) is a separate, supporting finding — even a linked population-denominator
system would face a diluted exposed subgroup — and is referenced, not merged.
"""
from __future__ import annotations

from pathlib import Path

import yaml


# capability classifiers (strict to the S. aureus tetracycline unit) ---------- #
EXPOSURE_POP = {"proxy_pop", "specific_pop"}       # exposure at a population denominator
PHENO_POP = {"pop_denom"}                          # S. aureus tetR at a population denominator


def load_systems(root: Path):
    data = yaml.safe_load(
        (root / "data/raw/coding/streamc_surveillance_systems.yaml").read_text())
    return data


def _included(systems):
    return [s for s in systems["systems"] if s.get("included", False)]


def classify(systems):
    inc = _included(systems)
    rows = []
    for s in inc:
        exp = s.get("exposure_capture", "not_captured") in EXPOSURE_POP
        phe = s.get("phenotype_capture", "not_captured") in PHENO_POP
        rows.append({
            "id": s["id"], "name": s["name"], "tier": s["tier"],
            "exposure_pop": exp, "phenotype_pop": phe,
            "links": bool(s.get("links", False)),
            "exposure_capture": s.get("exposure_capture", "not_captured"),
            "phenotype_capture": s.get("phenotype_capture", "not_captured"),
            "unit_flag": s.get("unit_flag", "none"),
            "exposure_resolution": s.get("exposure_resolution", "none"),
            "phenotype_resolution": s.get("phenotype_resolution", "none"),
        })
    dec = {
        "n_systems": len(inc),
        "exposure_only": sum(r["exposure_pop"] and not r["phenotype_pop"] for r in rows),
        "phenotype_only": sum(r["phenotype_pop"] and not r["exposure_pop"] for r in rows),
        "both_unlinked": sum(r["exposure_pop"] and r["phenotype_pop"] and not r["links"] for r in rows),
        "linked": sum(r["links"] for r in rows),
        # near-misses that explain WHY phenotype-side is what it is
        "mrsa_wrong_unit": [r["name"] for r in rows if r["unit_flag"] == "mrsa"],
        "pheno_right_unit_nonstandard": [r["name"] for r in rows
                                         if r["phenotype_capture"] == "facility_nonstandard_no_denom"],
        "wrong_organism": [r["name"] for r in rows if r["phenotype_capture"] == "wrong_organism"],
    }
    return rows, dec


def failure_mode(dec):
    """Which of the three canonical linkage failures the decomposition supports."""
    if dec["linked"]:
        return "linked (unexpected — investigate)"
    if dec["exposure_only"] and not dec["phenotype_only"] and not dec["both_unlinked"]:
        return "no phenotype-side population-denominator capture (exposure exists; the S. aureus tetracycline unit is surveilled nowhere with a population denominator)"
    if dec["phenotype_only"] and not dec["exposure_only"]:
        return "no exposure-side capture"
    if dec["both_unlinked"]:
        return "both exist separately but nothing joins them"
    return "neither side captured"


def aidsvu_exposure_geographies(root: Path):
    """The exposure-side resolution the project actually holds (Task 4): how many
    geographies AIDSVu supplies PrEP (exposure proxy) for. The phenotype side has zero
    geographies with S. aureus tetracycline resistance at a population denominator."""
    try:
        from src.loaders.aidsvu import load_aidsvu
        df = load_aidsvu(root / "data/raw/aidsvu")
        return int(df["state"].nunique())
    except Exception:
        return None


def run(root: Path | str = None):
    root = Path(root) if root else Path(__file__).resolve().parents[2]
    systems = load_systems(root)
    rows, dec = classify(systems)
    n_exposure_geo = aidsvu_exposure_geographies(root)
    _write_report(root, systems, rows, dec, n_exposure_geo)
    return rows, dec


def _yn(b):
    return "yes" if b else "—"


def _write_report(root, systems, rows, dec, n_exposure_geo):
    excluded = [s for s in systems["systems"] if not s.get("included", False)]
    fm = failure_mode(dec)
    geo = f"{n_exposure_geo}" if n_exposure_geo is not None else "the AIDSVu"
    md = f"""# Stream C — the linkage decomposition (deployed surveillance systems)

Backing intro ¶6's third leg: **does any deployed US public-health surveillance system
link doxy-PEP exposure to *S. aureus* tetracycline/doxycycline resistance at a common
population denominator?** Answer, decomposed rather than counted. **Capability/linkage,
not effect (Contract 1). Deployed systems, not in principle (Contract 3). Unit is
*S. aureus* tetracycline resistance; MRSA/methicillin systems are a flagged wrong-unit
near-miss (Contract 2).**

## Denominator (re-anchored — see the checkpoint note)

The prior Stream C figure ("0/81") was a **dilution parameter grid**, not a systems
denominator, and was stale (the grid is 135 cells). It is retained below only as a
separate *dilution* finding. The linkage denominator is a **closed universe of established
US public-health surveillance systems** under the stated rule:

> {systems['selection_rule'].strip()}

**{dec['n_systems']} systems** meet the rule and are coded on their own terms (blind to
the expected 0-linked answer). Excluded, with reason: """
    md += "; ".join(f"**{s['name']}** ({s['exclusion_reason']})" for s in excluded)
    md += f""".

## Task 2 — three-way decomposition

| system | tier | exposure @ pop-denom | phenotype (S. aureus tetR) @ pop-denom | links | note |
|---|---|---|---|---|---|
"""
    for r in rows:
        flag = " ⚠ MRSA (wrong unit)" if r["unit_flag"] == "mrsa" else ""
        pheno = _yn(r["phenotype_pop"])
        if not r["phenotype_pop"] and r["phenotype_capture"] != "not_captured":
            pheno = f"— ({r['phenotype_capture']})"
        md += (f"| {r['name']} | {r['tier']} | {_yn(r['exposure_pop'])} "
               f"({r['exposure_capture']}) | {pheno}{flag} | {_yn(r['links'])} | "
               f"{r['exposure_resolution']} / {r['phenotype_resolution']} |\n")
    md += f"""
**Decomposed result:** of {dec['n_systems']} systems — **{dec['exposure_only']} capture
exposure only** (at a population denominator, as a PrEP *proxy*), **{dec['phenotype_only']}
capture *S. aureus* tetracycline phenotype only** at a population denominator,
**{dec['both_unlinked']} capture both but unlinked**, and **{dec['linked']} link the two.**

**The failure is specific:** {fm}. It is *not* "both halves exist and nobody joined them."
The exposure half exists (PrEP density at county/metro); the phenotype half — *S. aureus*
tetracycline/doxycycline resistance at a population denominator — **does not exist in any
deployed system.** Two near-misses explain why:

- **Wrong unit, right denominator:** {", ".join(dec['mrsa_wrong_unit'])} — the one
  population-based *S. aureus* surveillance platform (ABCs/EIP) reports the **methicillin**
  subset (invasive MRSA), not tetracycline/doxycycline susceptibility. The platform that
  *could* carry the unit exists but is not instrumented for it.
- **Right unit, non-standardized, no denominator:** {", ".join(dec['pheno_right_unit_nonstandard'])}
  — the only routine source of *S. aureus* tetracycline/doxycycline susceptibility is the
  facility cumulative antibiogram, and it is inconsistent even at facility level. **CLSI
  M39 (5th ed., 2022)**, the national standard for antibiogram presentation, (a) **requires**
  *S. aureus* to be split into MRSA and MSSA — the methicillin axis is mandated — and (b)
  treats non-primary agents as **selectively reportable/suppressible** (supplemental agents
  tested only on resistant isolates are not reported; cascade rules may suppress agents).
  Tetracycline/doxycycline for *S. aureus* is such a supplemental agent — not in the
  required presentation and suppressible — so facility tetracycline data are
  **non-standardized and patchy across labs**, and carry no population base regardless.
  The claim is inconsistency, not universal absence: some labs report it; a single one does
  not falsify a claim about the standard and the resulting patchwork.
- NARMS, the closest-named federal AR system, excludes *S. aureus* entirely (enteric
  bacteria only); *S. aureus* is not NNDSS-notifiable (only VISA/VRSA).

## The methicillin axis at every tier — the codified seam (cross-tier synthesis)

At each tier where *S. aureus* is surveilled at all, the **reported axis is methicillin**,
not tetracycline:

- **Population denominator:** ABCs/EIP surveils invasive **MRSA/MSSA** (the methicillin
  split) in its catchment sites.
- **Facility, administrative:** NHSN AR Option / LabID reports **MRSA** events.
- **Facility, cumulative antibiogram:** CLSI M39 **mandates** the **MRSA/MSSA** split and
  makes tetracycline suppressible.

The surveillance architecture is **standardized around the methicillin axis at every
level**, and *S. aureus* tetracycline/doxycycline resistance is **orthogonal to that axis**
— so it falls through at each tier: absent where the denominator exists (methicillin
instead), suppressible and non-standardized where the unit is nominally reportable. This is
the Stream C analogue of the endpoint-substitution seam already found in Stream A (the
tet(K)/tet(M) mislabel and the narrowing from *S. aureus* to its methicillin subset) and
Stream B (efficacy graded, harms un-graded): the same measurement-inheritance seam, here
**codified in a national laboratory standard**. The phenotype half is not merely un-built;
the standard that governs it is organised around a different axis.

## Task 3 — resolution analysis (the mechanism)

The linkage cannot be made even in principle with deployed systems because the two sides
exist at **incompatible resolutions**:

- **Exposure** is surveilled at a **population denominator, county/metro/state** grain
  (AIDSVu, CDC AtlasPlus — PrEP proxy per 100k).
- **Phenotype** (*S. aureus* tetracycline resistance) exists only at **facility grain with
  no population denominator** (hospital antibiograms) — or, where a population denominator
  exists (ABCs/EIP), for the **wrong phenotype** (methicillin) in a handful of catchment
  sites.

There is no geographic level at which both a doxy-PEP exposure denominator and an
*S. aureus* tetracycline-resistance denominator coexist. The mismatch, not indifference,
is why nothing joins.

## Task 4 — the exposure side is concrete; the phenotype side is empty at that resolution

AIDSVu supplies the exposure proxy (PrEP) with a population denominator for **{geo}
geographies** at state grain (plus county/metro tiers). Against that, **zero** geographies
have an *S. aureus* tetracycline-resistance dataset at a population denominator to join.
The metro-grain dilution computation (`dilution_metro.py`) operates on this same AIDSVu
exposure side and is a **linkage/resolution and detectability demonstration, not an effect
estimate** (Contract 1), keyed to *S. aureus* tetracycline resistance as $R_0$ (Contract
2): it shows that even where exposure density is highest, no phenotype counterpart exists
at that resolution to link, and — separately — that the exposed subgroup would be too
dilute to move a population rate (the dilution leg, below).

**Dilution leg (supporting, corrected):** `dilution.py`/`dilution_metro.py` sweep a
parameter grid of favourable assumptions (uptake × enrichment × baseline × isolate
volume); **0 of 135** cells (not the stale "0/81") reach detection at the cross-organism benchmark
RR 1.42, and the metro case requires male-PrEP density far above the densest US geography.
This is a distinct claim from linkage — it says that *if* a linked population-denominator
system existed, the exposed subgroup would still be too dilute — and is reported as
support, not as the linkage denominator.

## Task 5 — scope bound (Contract 3)

The claim is that **no deployed system links** the two — **not** that the linkage is
impossible. It could be built. A system that *could* detect the signal would require, at a
common population denominator: (i) an exposure feed — outpatient doxycycline/doxy-PEP
dispensing or PrEP-linked records at county/metro grain (the exposure side AIDSVu already
approximates); and (ii) a phenotype feed carrying *S. aureus* **tetracycline/doxycycline**
susceptibility with a population denominator — most plausibly by adding tetracycline AST
reporting for *S. aureus* to the existing population-based ABCs/EIP platform (which already
has the denominator and the isolates), or by standing up a sentinel *S. aureus* antibiogram
network with defined catchment denominators, and joining the two on geography. None is
deployed. The cost is going unmeasured because the phenotype-side instrument was never
built, not because the phenomenon is unmeasurable.

## Licenses / not

**Stream C may claim:** no deployed US public-health surveillance system links doxy-PEP
exposure to *S. aureus* tetracycline/doxycycline resistance at a common population
denominator; the failure is specifically **{fm}**; the exposure and phenotype sides exist
at incompatible resolutions; the surveillance architecture is standardized around the
methicillin axis at every tier and the tetracycline unit is orthogonal to it; facility
*S. aureus* tetracycline capture is **non-standardized per CLSI M39** (methicillin split
mandated, tetracycline suppressible) — captured nowhere consistently, nowhere with a
population denominator; and, separately, even a linked population-denominator system would
face a diluted exposed subgroup (0/135 favourable cells).

**Stream C may NOT claim:** that such linkage is impossible in principle (a system could be
built — deployed-systems only); that **no facility reports** tetracycline for *S. aureus*
(M39 permits it and some labs do — the claim is inconsistency/non-standardization, not
universal absence); any effect size or causal statement (this is
capability/linkage/resolution only); or that the phenotype unit is MRSA (it is *S. aureus*
tetracycline resistance — ABCs/EIP's and NHSN's MRSA surveillance are flagged wrong-unit
near-misses, not the unit).

(Regenerate with `python -m src.analysis.streamc_linkage`.)
"""
    (root / "outputs").mkdir(exist_ok=True)
    (root / "outputs/streamc_linkage_result.md").write_text(md)


if __name__ == "__main__":
    rows, dec = run()
    print(f"systems in denominator: {dec['n_systems']}")
    print(f"  exposure-only: {dec['exposure_only']}  phenotype-only: {dec['phenotype_only']}"
          f"  both-unlinked: {dec['both_unlinked']}  linked: {dec['linked']}")
    print(f"  failure mode: {failure_mode(dec)}")
    print(f"  MRSA wrong-unit near-miss: {dec['mrsa_wrong_unit']}")
    print("wrote outputs/streamc_linkage_result.md")
