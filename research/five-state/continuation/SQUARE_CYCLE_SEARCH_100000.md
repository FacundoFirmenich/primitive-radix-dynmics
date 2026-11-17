# Exact bounded search of the remaining square-cycle systems

The PowerShell command below uses the local C# compiler supplied by
PowerShell and enumerates square roots of unity by prime powers and
CRT. It performs the state and overlap incidence tests of the two
exact CRT criteria. The output columns are A,C,D,Q,E in checker order.
The displayed case 2 denotes 119772 with factor two, case 3 denotes
119772 with factor three, and case 606897 uses its fixed factor three.

    Add-Type -Path research/five-state/continuation/square_cycle_search.cs
    [RgphiSquareSearch]::Search(100000,2)
    [RgphiSquareSearch]::Search(100000,3)
    [RgphiSquareSearch]::Search(100000,606897)

At coordinate bound 5000 the independent C# search reproduced the
Python filtered candidate counts for the two open cases. The
factor-three 119772 tuple was checked by the original ten-edge
verifier, giving residue 88011536665779 and period 223336848698040.

| Case | Coordinate bound | Candidates after generation | Realizations |
| --- | --- | ---: | --- |
| 119772 factor 2 | A <= 100000 | 78,167,178 | none |
| 119772 factor 3 | A <= 100000 | 64,836,054 | (406,712,1265,731,557) |
| 606897 factor 3 | Q <= 100000 | 6,510,940 | none |

The ranges are exhaustive because the prescribed linear shifts give
the fifth coordinate or the strict modulus. The two ordinary cycle
congruences then give modular square roots, and the chamber intervals
contain at most one representative for the dependent coordinate.
The subsequent filters are the remaining cycle conditions and
pairwise CRT checks. These numerical ranges place no bound on a
primitive state of unbounded coordinate.
