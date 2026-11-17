# Verification contract

## Fast exact verification

```bash
make verify
```

Checks:

- nonsquare certificate (`j=1..37`);
- exact five-state dynamics for 1,001 bases in the certified arithmetic progression;
- independent C++ replay when a C++17 compiler is available;
- projective content-cocycle/spectral certificate;
- claim/evidence graph closure;
- publication embargo (no manuscript source/PDF);
- machine-readable metadata consistency.

## Full reproducibility

```bash
make reproduce
```

Regenerates:

- traceability report;
- epistemic graph JSON + standalone HTML;
- five deterministic figures and graphical abstract;
- verification report;
- SHA-256 manifest.

## Release validation

A public release additionally requires an independent external clean-room run. Internal CI is not a substitute for that gate.

## Current RC3.3 integration (17 November 2026)

The reproducibility entry point is `make reproduce`. It includes both `rc33-verify` and `recent-verify`; the latter executes ten exact-code scripts on temporary copies and validates the source/data checkpoint manifest before and after. See `research/rc33/recent/RESULTS.md` for all 24 added claims and `outputs/reports/recent/RUN_MANIFEST.json` for execution scope. The complete saved t ≤ 5000 run is checked by its code hash, current finite prefix and all 157 terminal candidates; rerun it with `make recent-full-census`.

`make sync-check` validates repository metadata, evidence paths, graph endpoints and the ten approved bilingual figure hashes. `make integrity` verifies the generated-output manifest. The immutable DOI archive remains the 16 November tagged snapshot, as recorded in `metadata/DOI_STATUS.json`.
