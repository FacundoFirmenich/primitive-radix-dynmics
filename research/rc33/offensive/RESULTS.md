# Opposite fibres and half inversion · 20 November 2026

Author: Facundo Firmenich. Scientific version RC3.3.

Run `make offensive-verify`. Inputs, exact proofs and saved results are in
[`certificate/`](certificate/); the wrapper checks their SHA-256 manifest and
replays in a temporary build directory. Python 3 and SymPy are required.

## OPP1

Use common coordinates `(A,C,D,Q)` and retain the original chamber and gcd
conditions. With `(D,Q)` fixed, enumerate

`A | abs(D^2-r^2 Q^2)`, `C | abs(D^2-Q^2)`.

The two remaining square conditions hold exactly when

`(r^2 A^2 mod D, A^2 mod Q) = (C^2 mod D, C^2 mod Q)`.

With `(A,C)` fixed, enumerate

`D | abs(C^2-r^2 A^2)`, `Q | abs(C^2-A^2)`

and match `(D^2 mod A,D^2 mod C) = (r^2 Q^2 mod A,Q^2 mod C)`.
All four numerators are nonzero in the declared chambers. Thus each fixed-pair
fibre is finite without a coordinate-height cutoff. Fifth-coordinate completion,
CRT and all ten edges remain mandatory. See
[the proof and a constructed gcd barrier](certificate/PAIRED_COMPLETION_PROOF_ES.md).

## OPP2

Set `Psi(x)=1/(2x)` and `epsilon_B(x)=floor(B/x) mod 2`. Direct fractional-part
identities give

`T_B(Psi x)=Psi(S_B x)-(1-epsilon_B(x))/2`;

if `T_B x` is high, `S_B(Psi x)=Psi(T_B x)`.

Consequently a high component transfers with T and S exchanged exactly when
every epsilon is one. At odd base the exact defects are preserved and denominator
parity is uniform. If all denominators are even, admissibility is automatic.
[Full proof](certificate/HALF_INVERSION_PROOF_ES.md).

## OPP3

In a normal carrier with `D=rE-jA`, the two S-branch digits at sources 3 and 4
satisfy `r(b4-b3)=jB`. For `r=3,j=1`, the required odd base makes that difference
odd, so this branch cannot transfer by Psi. This explains the failure of the
known factor-three carrier under this particular change of chart.

A normal factor-three carrier with all five coordinates odd must instead have
`j=2`. Its CRT period is odd, so an odd realizing base can be chosen; all S-digits
then are even. Psi is admissible and gives reflected coordinates
`(2A,2C,D,Q,E)`, realizing 606897. Any normal factor-three carrier at even base
would supply such an all-odd tuple. This is a conditional existence reduction;
no new j=2 carrier is asserted.

## OPP4

The hashed input contains 128,058 distinct fixed opposite pairs from 96,127
recorded vertices with at least two square conditions. Completing those fibres
leaves 138,985 candidate pairs after individual gates: six match the first
remainder, four the second, none both. Hence none of these fibres contains a
quadratic core. The earlier context-generation history was not independently
replayed; this result does not cover all possible fixed pairs.

Other regression controls compare 1,536 small contexts with direct integer
enumeration, recover both hidden opposite pairs of each known carrier, verify
8,400 and 4,095 exact rational identities, and check checkpoint equivalence on
a naturally closed 112-context static fixture.

## Research and publication boundary

The persistent explorer alternates whole opposite-coordinate fibres, retaining
partial cores, provenance and deferred arithmetic. Its live reachability closure
is discovery computation. SymPy factor proposals receive exact prime proofs;
unresolved arithmetic is deferred. Query priority is not an existence probability.

The classification remains **37 excluded / 2 realized-containing / 1
existence-open**. Global uniqueness and both least-base problems remain open.
No inference about arithmetic existence is made from the decimal location of
the graph code in pi. Full manuscripts remain private; the original DOI/tag is
unchanged.
