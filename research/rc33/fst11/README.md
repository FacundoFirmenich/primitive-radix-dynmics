# FST-11 · exact word-observation contracts

Run `make fst11-verify` from the repository root. The source engine is byte-identical to the received `fst11.py`. Its 25 embedded atlas tables are preserved as JSON. `audit_fst11.py` uses direct arithmetic and enumerations to cross-check the implementation; `replay.py` runs it in a temporary copy and preserves inputs.

See [RESULTS.md](RESULTS.md), [CLAIMS.json](CLAIMS.json) and [current replay](../../../outputs/reports/fst11/RUN_MANIFEST.json). The received 47/29 historical test suites were not supplied; those are not claimed as rerun. Full manuscripts and the received PDF remain private.
