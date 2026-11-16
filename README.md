# Primitive Radix Dynamics · RGΦ

## Archived reproducibility release — RC3.3

**[DOI: 10.5281/zenodo.24270311](https://doi.org/10.5281/zenodo.24270311)** · [GitHub release](https://github.com/FacundoFirmenich/primitive-radix-mobius-dynamics/releases/tag/rc3.3-zenodo) · [Zenodo record](https://zenodo.org/records/24270311).

The DOI identifies the RC3.3 verification software and exact certificates. The archived source is pinned to [commit `7d94e81`](https://github.com/FacundoFirmenich/primitive-radix-mobius-dynamics/commit/7d94e81d06944f36640ab289b87473fc0292c6df). Cite this version when reproducing the RC3.3 results. The all-versions DOI is [10.5281/zenodo.24270310](https://doi.org/10.5281/zenodo.24270310).


A research and reproducibility companion for finite rational components of the radix map and its Möbius conjugate. The project tracks the common integer factor removed at each primitive projective step and uses that content to study which finite labelled graphs can be realized in a common radix.

## Results and evidence

| Result | Evidence |
| --- | --- |
| Permutation rigidity through four states and an explicit five-state nonpermutation family | [Threshold](proofs/SHARP_THRESHOLD.md) · [CRT witness](certificates/ARITHMETIC_PROGRESSION.json) |
| Bounds from projective width for two unimodular charts | [Two-chart theorem](proofs/TWO_CHART_PROJECTIVE_WIDTH.md) |
| Exact decision procedure at fixed radix and bounded cardinality | [Divisor universe](proofs/FIXED_BASE_DECIDABILITY.md) |
| Exclusion of the oriented form DF015-0015-B1 | [Proof and exact replay](research/df015-0015/CERTIFICATE.md) |

The full five-state arithmetic classification remains open. The oriented and generator-unoriented enumerations use different conventions. See the [research status](RESEARCH_STATUS.md), [catalogue reconciliation](research/five-state/DF015_0015_RECONCILIATION.md), and [claim ledger](data/claims.csv).

## Reproduce locally

    python -m pip install -e ".[dev]"
    make reproduce

GitHub-hosted execution is disabled for this repository. Use the [quick start](QUICKSTART_REPRODUCE.md) for Windows and individual checks. The [verification guide](VERIFICATION.md) explains the scope of each calculation. Scientific claims and their dependencies are recorded in the [traceability report](outputs/reports/claim_traceability.md).

Citation metadata is in [CITATION.cff](CITATION.cff). Code is MIT and research records are CC BY 4.0, subject to the [licensing terms](LICENSE.md). The article and supplementary manuscript remain under [publication embargo](docs/PUBLICATION_BOUNDARY.md).
