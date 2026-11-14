# Primitive Radix Dynamics · RGΦ


A research and reproducibility companion for finite rational components of the radix map and its Möbius conjugate. The project tracks the common integer factor removed at each primitive projective step and uses that content to study which finite labelled graphs can be realized in a common radix.

## Results and evidence

| Result | Evidence |
| --- | --- |
| Permutation rigidity through four states and an explicit five-state nonpermutation family | [Threshold](proofs/SHARP_THRESHOLD.md) · [CRT witness](certificates/ARITHMETIC_PROGRESSION.json) |
| Bounds from projective width for two unimodular charts | [Two-chart theorem](proofs/TWO_CHART_PROJECTIVE_WIDTH.md) |
| Exact decision procedure at fixed radix and bounded cardinality | [Divisor universe](proofs/FIXED_BASE_DECIDABILITY.md) |
| Exclusion of the oriented form DF015-0015-B1 | [Proof and exact replay](research/df015-0015/CERTIFICATE.md) |
| Exclusion of both shared strict-S systems at factors 2 and 3 | [Bounded quotients and exact replay](research/five-state/continuation/SHARED_SYSTEMS_EXCLUSION.md) |
| Strict-T factor-two obstruction and four sparse strict-S exclusions | [Predecessor congruence and exact resultant certificates](research/five-state/continuation/PREDECESSOR_AND_SPARSE_EXCLUSIONS.md) |

The full five-state arithmetic classification remains open. See the [research status](RESEARCH_STATUS.md), [40-row oriented ledger](research/five-state/continuation/ORIENTED_STATUS.csv), and [claim ledger](data/claims.csv).

## Reproduce locally

    python -m pip install -e ".[dev]"
    make reproduce

GitHub-hosted execution is disabled for this repository. Use the [quick start](QUICKSTART_REPRODUCE.md) for Windows and individual checks. The [verification guide](VERIFICATION.md) explains the scope of each calculation. Scientific claims and their dependencies are recorded in the [traceability report](outputs/reports/claim_traceability.md).

Citation metadata is in [CITATION.cff](CITATION.cff). Code is MIT and research records are CC BY 4.0, subject to the [licensing terms](LICENSE.md). The article and supplementary manuscript remain under [publication embargo](docs/PUBLICATION_BOUNDARY.md).
