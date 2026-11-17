# Repository instructions

Read `PROJECT_CHARTER.md` first. `RESEARCH_STATUS.md` is the only live status dashboard.

When sister-branch material is provided, apply `USER_SISTER_BRANCH_INTEGRATION.md`: integrate its relevant verified value and prepare return annexes for the origin threads. The publication boundary below remains in force.

## Authority order

1. Exact symbolic proof or deterministic certificate.
2. Independent exact checker output.
3. Machine-readable claim/evidence ledgers.
4. Narrative documentation.

Do not promote finite scans to global theorems. Do not add a new mathematical claim without updating `data/claims.csv`, its dependencies and verification route.

## Protected boundary

The manuscript and supplementary manuscript are embargoed from this repository until the owner explicitly changes `docs/PUBLICATION_BOUNDARY.md` after arXiv release. Do not add `.tex` manuscript files or manuscript PDFs.

## Routine verification

- Fast: `make verify`
- Full generated layer: `make reproduce`
- Tests: `make test`
- Integrity: `make seal && make integrity`

No project-local copy of external workflow skills is permitted under `skills/`.
