# Reviewer quickstart

## Exact verification — no package installation required

Python 3.11+ is enough for the authoritative exact Python checks:

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

## Integrated RC3.3 modules

`make rc33-verify` checks the all-height cofactor strata and fifth coordinate.
`make recent-verify` runs the ten recent scripts in temporary directories.
`make sync-check` audits versions, evidence paths, immutable input hashes and graph consistency.
`make recent-full-census` separately repeats the complete t ≤ 5000 chamber census.
The full figure export uses CairoSVG and its system Cairo library (for example, `libcairo2` on Ubuntu).

The full T007 layer requires a C++17 compiler (`g++`) and the declared NumPy/SymPy dependencies. Run `make t007-verify`; the optional complete hexagon replay is `make t007-full-hexagon`. Default quick runs preserve the original complete Q<=5000 execution receipt and source hashes under `research/rc33/t007/saved/`.
