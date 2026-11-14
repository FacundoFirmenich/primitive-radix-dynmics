# Oriented five-state frontier map — 2026-11-14

## Live oriented continuation

The eleven active arithmetic branches are not eleven independent state-side problems.

### Shared S-strict family: eight branches -> four factor-specific templates

Common S-map: `[4,1,2,1,0]`, strict source 3.

**Template I — T three-cycle on Q + T two-cycle on D**

- ordered skeleton `575722`, factors 2 and 3;
- ordered skeleton `575898`, factors 2 and 3.

State-side necessary system:
[
Q=rD-(r-1)C,
quad
Dmid A^2-C^2,
quad
Qmid A^3-r^3C^3,
]
plus the common S-cycle divisibility recorded in `proofs/FIVE_STATE_COMMON_S_STRICT_TEMPLATES.md`.

**Template II — T two-cycle on Q + T three-cycle on D**

- ordered skeleton `575738`, factors 2 and 3;
- ordered skeleton `576298`, factors 2 and 3.

State-side necessary system:
[
Q=rD-(r-1)C,
quad
Qmid A^2-r^2C^2,
quad
Dmid C^3-A^3,
]
plus the same common S-cycle divisibility.

Within each pair, orientation changes residue order at the CRT layer but not the eliminated state-side divisibilities. No dynamical equivalence is claimed.

### Exceptional oriented skeletons

- `119772`, strict S, factor 2: open;
- `119772`, strict S, factor 3: contains the exact realized counterfamily;
- `606897`, strict T, factor 3: open.

Thus the live eleven-branch continuation is controlled by **seven factor-specific mechanisms**:

- four shared S-strict templates;
- two factor-specific cases of `119772`;
- one factor-specific case of `606897`.

One mechanism is realized; six remain arithmetically unresolved.

## Generator-unoriented catalogue

The separate normalized catalogue still has twenty rows:

- 7 globally impossible;
- 1 realized-containing;
- 12 open in the stored generator-unoriented normalization.

These counts and the oriented continuation use different quotient conventions and must not be compared row by row.

## Further exact reductions

- four dense normalized forms have near-coprime divisor splitting;
- `DF015-0015` reduces to nineteen smooth elliptic cubics with Siegel-finite coprime locus;
- all eleven oriented open branches survive the natural local mod-8/mod-9 gate, so no blanket local no-go is valid.

## Remaining closure mechanisms

The correct global targets are:

1. divisor-allocation / S-unit closure of the shared dense templates;
2. effective relative-integral enumeration on the nineteen elliptic curves;
3. exact adjudication of the two exceptional oriented skeletons;
4. final CRT reconstruction for every surviving state tuple.
