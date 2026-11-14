# Exact five-state counterfamily

Use the canonical primitive states
[
x_0=406/731,;x_1=712/731,;x_2=712/1265,;x_3=1218/1265,;x_4=406/557.
]

For
[
B_t=88{,}011{,}536{,}665{,}779+t,223{,}336{,}848{,}698{,}040,qquad tge0,
]
the generalized CRT constraints in `certificates/CRT_CONGRUENCES.csv` force the exact maps
[
T=[1,0,3,2,4],qquad S=[4,2,1,0,0].
]

All (T)-edges and all (S)-edges except (x_3	o x_0) have defect one; that edge has exact factor three. The directed graph is strongly connected and (S) is noninjective.

The CRT modulus is the least common multiple of the local moduli, so the construction holds for the complete infinite arithmetic progression, not merely for the 1,001 regression bases checked by software.

Supports C011.
