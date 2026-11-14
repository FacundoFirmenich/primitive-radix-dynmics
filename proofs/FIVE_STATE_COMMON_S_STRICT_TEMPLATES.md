# Five-state common S-strict templates — symbolic reduction

**Status:** PROVED_SYMBOLIC  
**Date:** 2026-11-14

## Jurisdiction

Consider the four active ordered-map skeletons

- `575722`, `575898` (a T three-cycle plus a T two-cycle),
- `575738`, `576298` (a T two-cycle plus a T three-cycle),

with common `S = [4,1,2,1,0]`, strict source `3`, and strict factor `r in {2,3}`. All T-edges and all other S-edges have defect one.

The two orientations inside each pair are kept distinct at the final CRT stage. The theorem below states that their state-side necessary divisibilities coincide.

## Fibre coordinates

The S-fibre identities give
[
(p_0,p_1,p_2,p_3,p_4)=(A,C,E,rC,A).
]

For `575722/575898`,
[
(q_0,q_1,q_2,q_3,q_4)=(Q,D,Q,Q,D).
]

For `575738/576298`,
[
(q_0,q_1,q_2,q_3,q_4)=(Q,D,D,Q,D).
]

## Common S-strict relation

Every realization satisfies
[
oxed{Q=rD-(r-1)C.}
]

A defect-one fixed S-edge at state 1 gives (Bequiv1pmod C). The strict edge (3	o1), in complementary coordinates, gives
[
B(Q-rC)equiv r(D-C)pmod{rC}.
]
Modulo (C), this yields (Cmid Q-rD).

Write (Q-rD=kC). Highness gives (C<D<2C), (A<D<2A), (A<Q<2A), and (rC<Q<2rC).

- For (r=2), (Q<2A<2D) gives (k<0), while (Q>2C) and (2D<4C) give (k>-2). Hence (k=-1).
- For (r=3), (Q<2A<2D) gives (Q-3D<-D<-C), so (k<-1), while (Q>3C) and (3D<6C) give (k>-3). Hence (k=-2).

Thus (k=-(r-1)).

Put (z=D-C>0), (a=D-A>0). Then
[
Q=D+(r-1)z
]
and the defect-one S two-cycle (0leftrightarrow4) implies
[
oxed{Amid (r-1)zigl(2a+(r-1)zigr).}
]

Highness also gives
[
oxed{rac{r-1}{2r-1}D<z<rac D2},
qquad
oxed{0<2a+(r-1)z<D.}
]

## Two T-cycle templates

### Template I — T three-cycle on Q, T two-cycle on D

For `575722` and `575898`,
[
oxed{Dmid A^2-C^2},
qquad
oxed{Qmid A^3-r^3C^3}.
]

The two orientations of the Q-three-cycle produce the same eliminated state-side divisibility; orientation survives only in the intermediate residue ordering and final CRT compatibility.

### Template II — T two-cycle on Q, T three-cycle on D

For `575738` and `576298`,
[
oxed{Qmid A^2-r^2C^2},
qquad
oxed{Dmid C^3-A^3}.
]

Reversing the D-three-cycle again preserves the eliminated cubic divisibility.

## Consequence

Eight oriented branches are therefore not eight independent state-side problems. Before final CRT orientation, they reduce to four factor-specific arithmetic templates:

- Template I, r=2;
- Template I, r=3;
- Template II, r=2;
- Template II, r=3.

Together with the exceptional ordered skeletons `119772` and `606897`, the eleven-branch continuation is controlled by a much smaller number of arithmetic mechanisms.

This result does **not** claim that any template is impossible or realized.
