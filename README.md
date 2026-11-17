# Primitive Radix–Möbius Dynamics · RGΦ

**Scientific edition RC3.3 · integrated continuation: 17 November 2026**

Public software, exact certificates and research records for *Finite Rational Components in Primitive Radix–Möbius Dynamics: Content and a Sharp Threshold*, by Facundo Firmenich.

![The fifth state changes the arithmetic completion](outputs/figures/rc33_visual_EN.png)

## Results and current scope

| Result | Evidence |
| --- | --- |
| Both maps permute every finite high component with at most four states; five states attain the first failure | [Threshold proof](proofs/SHARP_THRESHOLD.md) · [CRT witness](certificates/ARITHMETIC_PROGRESSION.json) |
| Complete forty-case oriented ledger: **37 exclusions / 1 realized-containing row / 2 open rows** | [Oriented ledger](research/five-state/continuation/ORIENTED_STATUS.csv) |
| All-height certificates on specified cofactor strata, including h ≤ 14, and fifth-coordinate restrictions | [RC3.3 checkers](research/rc33/README.md) |
| Exact chamber reduction for 606897/3; saved exhaustive t ≤ 5000 exclusion with current prefix and terminal replay | [Recent result register](research/rc33/recent/RESULTS.md#r17b) |
| Weighted and coupled finite-group covers, deterministic phases and finite recovery records | [Recent modules](research/rc33/recent/RESULTS.md) · [24 claim cards](research/rc33/recent/CLAIMS.json) |

The two existence orientations, unrestricted uniqueness of the known carrier and least-base questions remain open. The [live research dashboard](RESEARCH_STATUS.md) distinguishes these questions from proven finite and conditional statements.

The **FST-11 continuation** adds [five word-observation claims](research/rc33/fst11/RESULTS.md): complete variable-length forms, complementary normalization channels, language-conditioned CRT and a nonregular global fibre. It includes the unchanged received engine and an exact cross-checker.

The **T007 sister-branch continuation** adds [seven scoped records](research/rc33/t007/RESULTS.md): a Q≤5000 six-state hexagon certificate, exact word-tower separation, a checked transfer boundary and a 43-prime elliptic relation sieve with a 172-fold norm improvement.

## Reproduce

```bash
python -m pip install -e '.[dev]'
make reproduce
```

This runs the core verifier, tests, RC3.3 certificate checks, ten recent replay scripts the FST-11 suite and the T007 checks; rebuilds traceability, figures and graphs; audits synchronization; and seals the generated outputs. The expensive complete t ≤ 5000 census is separately available as `make recent-full-census`; the default replay verifies its saved code hash, finite prefix and all 157 terminal candidates.

See the [quick start](QUICKSTART_REPRODUCE.md), [verification guide](VERIFICATION.md), [current replay receipt](outputs/reports/recent/RUN_MANIFEST.json) and [synchronization record](docs/SYNC_2026-11-17.md). GitHub Actions runs only by manual dispatch.

## Figures and HTML

- Standalone maps and visual abstracts: [English viewer](outputs/interactive/rc33_epistemic_EN.html) · [Spanish viewer](outputs/interactive/rc33_epistemic_ES.html).
- Searchable [interactive dependency graph](outputs/interactive/epistemic_graph.html) and its [JSON data](outputs/interactive/epistemic_graph.json).
- [Claim traceability](outputs/reports/claim_traceability.md) and [canonical alignment hashes](metadata/CANONICAL_ALIGNMENT.json).

GitHub's file viewer shows HTML source; download the repository and open the HTML files locally for the rendered interactive editions. [Resumen en castellano](README_ES.md).

## Citation and archive

The registered version DOI is [10.5281/zenodo.24270311](https://doi.org/10.5281/zenodo.24270311); the all-versions DOI is [10.5281/zenodo.24270310](https://doi.org/10.5281/zenodo.24270310). It identifies the immutable 16 November code snapshot tagged [`rc3.3-zenodo`](https://github.com/FacundoFirmenich/primitive-radix-mobius-dynamics/releases/tag/rc3.3-zenodo), commit `7d94e81d06944f36640ab289b87473fc0292c6df`.

Current `main` adds the 17 November integration. This continuation has not been archived under a new DOI; the existing tags and archive remain unchanged. Scientific edition RC3.3 is retained; the installable package version is 0.3.3. See [CITATION.cff](CITATION.cff).

The [pre-arXiv publication boundary](docs/PUBLICATION_BOUNDARY.md) remains active: this repository contains code, certificates, metadata and standalone figures. Complete main, supplementary and companion manuscripts remain in the private A1 delivery. Code is MIT and research records are CC BY 4.0 under the [licensing terms](LICENSE.md).

The **FST12/13 continuation** adds [nine scoped records](research/rc33/fst1213/RESULTS.md) on language complexity, natural boundaries, erasure families, bounded inverse ranks and effective modular resolution. Run `make fst1213-verify`; the two received atlas scripts are replayed in Node with an inert DOM, separately from the new exact Python checks.

### FST14 terminal-inverse continuation

Four scoped records and a reproducible declared-adapter audit extend FST12/13: exact terminal periods, bounded lifting/CRT inversion and logarithmic suffix resolution. Run `make fst14-verify`. The missing historical baselines and browser suites are not represented as replayed. Current combined continuation:49 cards;103 public claim records. Full manuscripts remain private; original DOI/tag unchanged.
