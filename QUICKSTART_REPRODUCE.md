# Reviewer quickstart

## Exact verification — no package installation required

Python 3.10+ is enough for the authoritative exact Python checks:

```bash
make verify
```

If a C++17 compiler is available, the verifier automatically compiles and runs the independent C++ replay.

## Windows exact checks

From PowerShell, run:

    $env:PYTHONPATH = 'src'
    python -m rmr.verify
    python research/df015-0015/verify_rgphi_df015_0015.py
    python src/rmr/verify_rgphi_farkas_728.py research/five-state/certificates/HIGH_INFEASIBILITY_FARKAS_728.json

## Full generated layer

For tests plus SVG/PNG/PDF figures:

```bash
python -m pip install -e '.[dev]'
make reproduce
```

Expected generated outputs:

- `outputs/reports/claim_traceability.md`
- `outputs/reports/verification_report.json`
- `outputs/interactive/epistemic_graph.json`
- `outputs/interactive/epistemic_graph.html`
- `outputs/figures/*.svg`
- `outputs/figures/*.png`
- `outputs/figures/*.pdf`
- `outputs/checksums/SHA256SUMS.txt`

No manuscript is generated: the manuscript is deliberately outside this repository during the pre-arXiv embargo.
