"""Defined literature search — the measurement gap in the research literature.

The three streams show trials, guidelines, and surveillance each fail to MEASURE
the bystander signal. This extends the same question one level out: of the doxy-PEP
research literature itself, what fraction so much as NAMES a bystander staphylococcal
organism — and of those, how many actually measure it?

Method. Two NCBI E-utilities `esearch` queries with stated date bounds:
  * DENOMINATOR — doxy-PEP (STI post-exposure prophylaxis) papers.
  * NUMERATOR   — those that ALSO name S. aureus / MRSA / MSSA / staphylococc*.
The fraction is the reportable number. Naming is a GENEROUS proxy for measuring, so
the numerator over-counts; a hand classification of the numerator (below, each with
a PMID) separates "measures with a doxy-PEP exposure contrast" from "measures with
no contrast" from "names only" (review / survey / in-silico / in-category / case).

PubMed grows, so counts drift. This module FREEZES the retrieved PMIDs + counts into
`data/raw/literature_search/snapshot.json` stamped with the run date; the reportable
number in the manuscript cites that frozen snapshot, and re-running refreshes it.
No network at analysis time if the snapshot exists (pass refresh=True to re-query).
"""
from __future__ import annotations

import json
from datetime import date
from pathlib import Path

ESEARCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"

DATE_BOUNDS = ('"2015"[dp]', '"2026"[dp]')  # doxy-PEP era; Bolan pilot was 2015

DENOMINATOR = (
    '("doxy-PEP"[tiab] OR "doxyPEP"[tiab] OR "doxycycline postexposure prophylaxis"[tiab] '
    'OR "doxycycline post-exposure prophylaxis"[tiab] OR ("doxycycline"[tiab] AND '
    '"prophylaxis"[tiab] AND ("sexually transmitted"[tiab] OR STI[tiab] OR STIs[tiab] '
    'OR gonorrhea[tiab] OR gonorrhoea[tiab] OR chlamydia[tiab] OR syphilis[tiab]))) '
    f'AND ({DATE_BOUNDS[0]} : {DATE_BOUNDS[1]})'
)
BYSTANDER_CLAUSE = (
    ' AND ("Staphylococcus aureus"[tiab] OR "S. aureus"[tiab] OR MRSA[tiab] '
    'OR MSSA[tiab] OR staphylococc*[tiab])'
)

# Hand classification of the numerator, PMID->(tier, note), verified against an
# authoritative esummary PMID<->title pairing (not position-based). PMIDs are stable.
# tier: measures_with_contrast | measures_no_contrast | names_only
NUMERATOR_CLASSIFICATION = {
    "40036749": ("measures_with_contrast", "Soge CID 2025 — tetR S. aureus colonization 18% vs 8%, doxy-PEP vs none"),
    "39882974": ("measures_with_contrast", "DuDHS pilot RCT (Grennan), Clin Infect Dis 2026 — measures resistance, pilot n"),
    "42342442": ("measures_no_contrast", "Gaspari STI 2026 — nasal S. aureus macrolide/tet resistance, MSM on PrEP, cross-sectional"),
    "39718967": ("measures_no_contrast", "J Infect Dis 2025 — tetR S. aureus in doxy-PEP-ELIGIBLE population, no exposure contrast"),
    "39228717": ("measures_no_contrast", "medRxiv 2024 — preprint of 39718967 (same study)"),
    "41974008": ("names_only", "Ann Intern Med 2026 — 'what you may have missed' review"),
    "41891836": ("names_only", "Dona Ital J Dermatol Venerol 2026 — KAP survey of clinicians"),
    "41366180": ("names_only", "Infect Dis Ther 2026 — narrative review, AMR/microbiome"),
    "39766573": ("names_only", "Antibiotics (Basel) 2024 — 'From Cure to Prevention' narrative review"),
    "39657948": ("names_only", "Int J STD AIDS 2025 — LGV diagnosis case series (incidental)"),
    "38575877": ("names_only", "BMC Infect Dis 2024 — Truong SR/MA (secondary synthesis)"),
    "38517444": ("names_only", "JAC 2024 — tetR N. gonorrhoeae England (in-category; staph incidental)"),
    "37466467": ("names_only", "Int J STD AIDS 2023 — Kenyon in-silico cross-resistance"),
}
# Unclassified retrieved PMIDs default to names_only (see write_report caveat).


def _count(term: str, timeout: float = 30.0) -> tuple[int, list[str]]:
    """esearch via curl — the sandbox's TLS proxy uses a self-signed cert that
    urllib rejects; curl is available everywhere this runs and is reproducible."""
    import subprocess
    out = subprocess.run(
        ["curl", "-s", ESEARCH,
         "--data-urlencode", "db=pubmed",
         "--data-urlencode", f"term={term}",
         "--data-urlencode", "retmax=100"],
        capture_output=True, text=True, timeout=timeout, check=True).stdout
    count = int(out.split("<Count>")[1].split("</Count>")[0])
    ids = [s.split("</Id>")[0] for s in out.split("<Id>")[1:]]
    return count, ids


def refresh_snapshot(root: Path, today: str) -> dict:
    d_count, _ = _count(DENOMINATOR)
    n_count, n_ids = _count(DENOMINATOR + BYSTANDER_CLAUSE)
    snap = {
        "run_date": today,
        "date_bounds": list(DATE_BOUNDS),
        "denominator_query": DENOMINATOR,
        "numerator_query": DENOMINATOR + BYSTANDER_CLAUSE,
        "denominator_count": d_count,
        "numerator_count": n_count,
        "numerator_pmids": n_ids,
    }
    out = root / "data/raw/literature_search"
    out.mkdir(parents=True, exist_ok=True)
    (out / "snapshot.json").write_text(json.dumps(snap, indent=2))
    return snap


def load_snapshot(root: Path) -> dict:
    return json.loads((root / "data/raw/literature_search/snapshot.json").read_text())


def _tiers(pmids: list[str]) -> dict:
    tiers = {"measures_with_contrast": [], "measures_no_contrast": [], "names_only": []}
    for pmid in pmids:
        tier, desc = NUMERATOR_CLASSIFICATION.get(pmid, ("names_only", f"PMID {pmid} (unclassified)"))
        tiers[tier].append((pmid, desc))
    return tiers


def write_report(root: Path, snap: dict) -> None:
    d, n = snap["denominator_count"], snap["numerator_count"]
    pct = 100 * n / d if d else float("nan")
    tiers = _tiers(snap["numerator_pmids"])
    n_meas_contrast = len(tiers["measures_with_contrast"])
    n_meas = n_meas_contrast + len(tiers["measures_no_contrast"])
    pct_meas = 100 * n_meas / d if d else float("nan")

    def _block(key, label):
        rows = tiers[key]
        if not rows:
            return f"- **{label}:** none\n"
        return f"- **{label}** ({len(rows)}):\n" + "".join(
            f"  - `{pmid}` — {desc}\n" for pmid, desc in rows)

    md = f"""# Defined literature search — the measurement gap in the literature itself

*Run {snap['run_date']} against PubMed via NCBI E-utilities `esearch`. Counts drift
as PubMed grows; this reports the frozen snapshot in
`data/raw/literature_search/snapshot.json`. Re-run `python -m src.analysis.literature_search --refresh`.*

**Date bounds:** {snap['date_bounds'][0]} : {snap['date_bounds'][1]} (the doxy-PEP era).

## Queries (verbatim)

Denominator — doxy-PEP (STI post-exposure prophylaxis) papers:

```
{snap['denominator_query']}
```

Numerator — the denominator ALSO naming a bystander staphylococcal organism:

```
{snap['numerator_query']}
```

## Result

| | count |
|---|---|
| Denominator — doxy-PEP papers | **{d}** |
| Numerator — those naming *S. aureus* / MRSA / MSSA / staphylococc* | **{n}** |
| **Fraction naming a bystander organism** | **{pct:.1f}%** |

**{n} of {d} ({pct:.1f}%)** doxy-PEP papers so much as name a bystander staphylococcal
organism. Naming is a generous proxy for measuring — so this over-counts.

## The numerator, classified (naming ≠ measuring)

Hand classification of the {n} numerator records, each with its PMID:

{_block("measures_with_contrast", "Measures tetR S. aureus against a doxy-PEP EXPOSURE contrast")}{_block("measures_no_contrast", "Measures tetR S. aureus, NO exposure contrast (eligible-population / cross-sectional)")}{_block("names_only", "Names only — review / survey / in-silico / in-category / case report")}

**Second-order finding.** Of {d} doxy-PEP papers, {n} ({pct:.1f}%) name a bystander
staph organism; only **{n_meas} ({pct_meas:.1f}%)** *measure* tetracycline-resistant
*S. aureus* at all, and only **{n_meas_contrast}** measure it against a doxy-PEP
exposure contrast (Soge; arguably DuDHS at a pilot's sample size). The measurement
gap the three streams document inside trials, guidelines, and surveillance is
reproduced in the research literature that surrounds them: the bystander is almost
never named, and when named, almost never measured.

*Caveat — no silent cap:* the classification is a hand reading of the {n} abstracts,
listed by PMID so it is checkable; unclassified retrieved PMIDs default to
`names_only`. The counts are PubMed as of {snap['run_date']} and will rise over time.
"""
    (root / "outputs").mkdir(exist_ok=True)
    (root / "outputs/literature_search_result.md").write_text(md)


def run(root: Path | str = None, refresh: bool = False, today: str = None) -> dict:
    root = Path(root) if root else Path(__file__).resolve().parents[2]
    snap_path = root / "data/raw/literature_search/snapshot.json"
    if refresh or not snap_path.exists():
        snap = refresh_snapshot(root, today or date.today().isoformat())
    else:
        snap = load_snapshot(root)
    write_report(root, snap)
    return snap


if __name__ == "__main__":
    import sys
    snap = run(refresh="--refresh" in sys.argv)
    d, n = snap["denominator_count"], snap["numerator_count"]
    print(f"denominator (doxy-PEP papers): {d}")
    print(f"numerator (names bystander staph): {n}  ({100*n/d:.1f}%)")
    print("wrote outputs/literature_search_result.md")
