# Tarasutra continuation — 19 November 2026

## TARA1
119772/factor 2 (DF015-0003/S) is explicitly realized.
A=1089859, C=1627375, D=3121631, Q=2087631, E=2105745.
The states A/Q, C/Q, C/D, 2A/D, A/E have
T=(1,0,3,2,4), S=(4,2,1,0,0); only S at source 3 has defect 2.
The standard-library checker reconstructs all ten maps, primitive gcds,
strong connectivity and the complete CRT base fibre:
B=2720751096305053288157586672376
 +3245172386374697665101193455750*n, n>=0.
This exact proof is independent of search completeness.
T1 found the tuple on (C+A)/Q=82/63; its least signed denominator is 63.

## TARA2
Two levels with the same old readings and different new readings witness
strict refinement: projection proves refinement and that pair proves
strictness. Sound rejection is a separate arithmetic requirement.
For Delta=J^2(aJ^2+b), J!=0, aJ^2+b must be a square. A modular
nonsquare rejects exactly. If s^2 divides a,b, the quotient by s^2
must likewise be a square. J=0 keeps its separate exact treatment.
LOGITS Ridge scores only order queries; they are not existence probabilities.

## TARA3
The snapshot records completed h19..78: 19190 planes, 479685 chunks and
631969933005 level pairs with plane contexts. It does not assert fresh
independent replay of every chunk or new h15..18 coverage.
Comparison h19..40: 21698169219 initial pairs per policy.
Exact root calls: T1=11081465490; T2=4871893206; LOGITS=5068774441.
These are work counters, not universal wall-time speedups.

## Reproduction and scope
Run make tarasutra-verify. The discovery chunk, SHA-256 provenance,
current ledger overlay, coverage reports and independent checker are included.
Current status: 37 excluded / 2 realized-containing / 1 existence-open:
DF015-0007/T = 606897/factor 3.
Uniqueness within either realized type and both global minimum-base questions
remain open. Version RC3.3 and the old DOI/tag are unchanged.
No manuscripts or private diagnostic tools are included.
