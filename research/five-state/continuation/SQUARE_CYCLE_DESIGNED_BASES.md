# Designed-base experiment

Choose coprime pairs \((U,V)\) away from 2 and 3 and solve
\(B=1\bmod U\), \(B=-1\bmod V\), and \(B=0\bmod 6\).
This ensures that chosen prime powers occur in each of the two sign
classes. The input pairs are `(221375,1583023)`,
`(677875,278369)`, and `(809875,314041)`, and their reverses.
For each orientation use the first two bases strictly above the
known witness base. Exhaust the allowable divisors of \(B^2-1\)
with the existing fixed-base checker.

| Base | Divisors | 119772/2 | 119772/3 | 606897/3 |
| ---: | ---: | ---: | ---: | ---: |
| 89419110501876 | 30720 | 28 | 1 | 41 |
| 91521760801626 | 18432 | 53 | 8 | 38 |
| 89306164976874 | 7680 | 68 | 10 | 19 |
| 91408815276624 | 6144 | 47 | 10 | 22 |
| 88878790900626 | 15360 | 72 | 1 | 19 |
| 90010987215876 | 6144 | 37 | 0 | 19 |
| 88876030593624 | 24576 | 86 | 39 | 98 |
| 90008226908874 | 24576 | 163 | 40 | 252 |
| 88196922213126 | 30720 | 217 | 72 | 223 |
| 89722925942376 | 36864 | 171 | 124 | 332 |
| 88819510379874 | 18432 | 70 | 3 | 114 |
| 90345514109124 | 12288 | 32 | 9 | 9 |

The last three columns count candidates before the full edge tests.
None survives. The twelve fixed-base fibres were exhausted. The
designed sample supports no estimate of the density of realizations.

From the repository root using Python with SymPy and `src` on
`PYTHONPATH`, put `research/five-state/continuation` on the import
path and run:

```python
from sympy.ntheory.modular import crt
from verify_residual_by_base import classify

known_base = 88011536665779
for left, right in ((221375, 1583023), (677875, 278369), (809875, 314041)):
    for plus, minus in ((left, right), (right, left)):
        residue, period = map(int, crt((plus, minus, 6), (1, -1, 0)))
        base = known_base + 1 + (residue - known_base - 1) % period
        for candidate in (base, base + period):
            print(classify(candidate), flush=True)
```
