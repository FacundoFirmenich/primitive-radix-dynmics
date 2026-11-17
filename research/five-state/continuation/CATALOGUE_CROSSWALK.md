# Oriented graphs and Round 015

The archived source is `ROUND015_CLASS_TO_NORMAL_FORM.csv`, copied byte for byte
from the research repository at commit `c25857e53eea8585a4f10e0a5a42295a315151ec`
and Git blob `f7ed9272fbe850d3fd59df680046cfb36e4da59c`.

Run `python research/five-state/continuation/verify_catalogue_crosswalk.py`.
The checker conjugates both endomaps by all 120 vertex permutations and carries
the strict source and its factor through each conjugation. It also tests generator
exchange to identify the archived *combinatorial* classes. The generated CSV
records both the orientation relative to the canonical key and the orientation
relative to the original generator recorded in the archive.

The 11 oriented rows map to 10 archived form IDs. The two rows over DF015-0007
are 119772 and 606897, both with factor three and opposite strict letters.
The known CRT realization certifies 119772 alone. The strict-S graph 575738
at factor three lies over DF015-0015, whereas the chamber exclusion
DF015-0015-B1 applies to the strict-T representative from Round 017.

The oriented checker also includes graphs over DF015-0009, DF015-0010 and
DF015-0016 with a strict letter opposite to the original strict-T representative.
The corresponding historical exclusions cannot be imported by exchanging
the two formal letters. These findings constrain any aggregate count that
mixes the two catalogues.

The new [shared-system exclusion](SHARED_SYSTEMS_EXCLUSION.md) closes all eight shared rows in their stated orientations. The marked strict-T and strict-S representatives of DF015-0015 now both have an exclusion certificate.
