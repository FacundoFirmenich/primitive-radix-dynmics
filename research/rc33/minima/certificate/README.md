# Three research objectives, fixed certificates

Facundo Firmenich · RGΦ RC3.3 · 20 November 2026.

This package contains four scoped results:

- The finite-survivor criterion, with no prior rational-height or cardinality
  cutoff, and explicit interval/graph certificates for every base 2 through 53.
- A separate cut-point reconstruction and finite-closure checker for those 52
  bases. It finds 23 singleton and two two-state components, all permutational.
- Complete all-height index strata 1 through 12: 117,093,402 integral-level pairs,
  no primitive candidates of the necessary five-chamber system.
- The finite necessary search window below B*=88011536665779:
  H<=11750908 and 13<=lambda<=523225, for nonpermutation five-state components.

The written proofs distinguish these domains from global uniqueness and both
minimum-base questions. No global minimum or global uniqueness is claimed.

From the canonical project root run `make minima-check`. Its default mode checks
the archive, exact geometry, complete tile coverage, saved independent receipts,
the integer/GMP filter and positive controls, and small exact interval replays.
`python3 code/check_minima.py --full` additionally replays all 117,093,402 level
pairs and reconstructs all 52 interval certificates from cut points in a separate
work directory. Full mode can take several minutes. It does not modify inputs.

Requirements: Python 3, SymPy, a C++17 compiler and GMP C++ development headers
and libraries (`libgmp-dev` on Debian/Ubuntu). `BUILD_ENVIRONMENT.json` records
the actual compiler, GMP version, flags and original executable hash. The
archived executable is the original Linux build; the checker rebuilds it from
source for the execution environment.

The index and cardinality supervisors are also preserved as research software.
Their live databases, source-specific queues and changing logs are outside this
fixed certificate. A resource limit is recorded as inconclusive and supplies
no exclusion. New carriers are checked against their own base objective, and
large-base carriers remain relevant to uniqueness.
