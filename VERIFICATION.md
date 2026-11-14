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
