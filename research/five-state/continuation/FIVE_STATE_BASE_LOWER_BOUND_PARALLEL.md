# Updated lower bounds from the two parallel local searches

The oriented ledger has 37 exclusions, one realization-containing
row and two open rows. The two open rows were searched again by
extending the contiguous coordinate ranges in the
[first census](SQUARE_CYCLE_SEARCH_100000.md). Use coordinates
in the order (A,C,D,Q,E).

| Row | Coordinate range | Additional filtered candidates | New realizations |
| --- | --- | ---: | ---: |
| 119772 at factor 2 | (100001\le A\le150000) | 111,701,038 | 0 |
| 606897 at factor 3 | (100001\le Q\le270000) | 53,826,511 | 0 |

The [frozen block records](SQUARE_CYCLE_PARALLEL_CENSUS.json) end at
those limits. Candidate counts are after generation filters and
before the final square congruences and overlap checks. No candidate
in the extension reached the ten-edge check. The known realization
of 119772 at factor three was independently recovered at its base,
and its original coordinate census through (A=100000) remains
the bound used here.

The [previous height argument](FIVE_STATE_BASE_LOWER_BOUND.md)
gives the strict bounds below for any new realization:

| Row | Strict lower bound for (B^2-1) | Integer lower bound on (B) |
| --- | --- | ---: |
| 119772 at factor 2 | (2\cdot150001^4) | 31,820,229,419 |
| 119772 at factor 3 | ((27/8)\cdot100001^4) | 18,371,540,497 |
| 606897 at factor 3 | ((27/32)\cdot270001^4) | 66,963,421,866 |

The known tuple has least realizing base (88,011,536,665,779).
Taking the minimum over it and the three rows gives
(B^{(5)}_{\min}\ge18,371,540,497).

The range search derives two coordinates from roots of unity and
the exact high-chamber shifts. The accompanying C# source is the
range version used for these blocks. From the repository root:

    Add-Type -Path research/five-state/continuation/square_cycle_search_range.cs
    [RgphiSquareSearchRange]::Search(100001,150000,2)
    [RgphiSquareSearchRange]::Search(100001,270000,606897)

The range implementation reproduced the earlier implementation
through 5000 for all three systems. These bounds concern absence of
realizations below the indicated bases in the specified rows.
Neither open orientation changes status.
