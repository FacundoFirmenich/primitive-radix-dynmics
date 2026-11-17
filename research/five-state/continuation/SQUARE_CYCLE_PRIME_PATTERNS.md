# Exact local state counts and prime-power realizability

For each of the five strict-shift charts, let a state residue at
\(p>3\) be the residue of its four independent integer coordinates.
Count a residue once when it admits a local base for the ten edge
congruences and has locally reduced states. Real inequalities and
global distinctness are external to this local count. The exact
number is
\[
F(p)=p^4-4p^3+14p^2-22p+11 .
\]

Adjacent reducedness and the two opposite overlap constraints imply
that at most one core modulus is divisible by \(p\). The fifth-state
modulus \(E\) may vanish on its own or alongside a core modulus.
If a core modulus vanishes, its two ordinary edges compose to
\(B^2=1\) modulo that modulus, and on each admissible residue the
sign is forced because the edge coefficients are units. If \(E\)
vanishes its ordinary fixed edge forces the positive sign. If
no core modulus vanishes the positive sign suffices. These rules
keep the counts over signs disjoint when the sign is forced.

For each choice of vanishing moduli and sign, the checker substitutes
that sign into the raw edge congruences and adds the resulting
linear forms for the vanishing source moduli. The forms for every
other core modulus and for \(E\), when nonvanishing, are required
to be units by inclusion-exclusion. Local reductions of all five
fractions are checked. Every rank calculation uses an integral
minor supported on 2 and 3, so the ranks agree over \(\mathbb Q\)
and \(\mathbb F_p\) for all \(p>3\). The count with no vanishing form
is \((p-1)^3(p-2)\). With only \(E\) vanishing it is \((p-1)^3\).
The singleton core counts for either sign are \((p-1)^2\) at
two positions and \((p-1)(p-2)\) at the other two. Exactly two
overlaps with \(E\) contribute \(p-1\) each at the positive sign.
These terms sum to \(F(p)\).

For a core modulus marked as vanishing, the first ordinary edge
remainder at that modulus and the marked modulus forms are a basis
for the imposed row space. The checker certifies their independence
modulo every \(p>3\), and expresses the other active remainders using
the first remainder and the same source modulus, with denominators
units at \(p\). The strict source uses the same core form scaled
by the strict factor, also a unit there. An active \(E\) edge has
identically zero remainder at the positive sign. A unit minor
now solves the independent linear forms over \(\mathbb Z_p\) while
preserving the initial residue. Prescribe any positive valuation
at each marked modulus, and at the first remainder prescribe zero
or any value with valuation at least that of its core modulus.
All localized ten-edge constraints then hold with the chosen base
sign. With no marked core, only the optional valuation of \(E\)
needs to be prescribed.

Modulo an active core form, that first remainder is the selected
signed factor of the corresponding square numerator up to a unit.
The other signed factor is a unit. In particular, both sign
patterns with a single marked core and \(E\) a unit survive at
arbitrary valuations. No cyclic valuation obstruction at a single
generic prime follows from these constraints alone.

The mod-\(p\) normalized factor is
\[
\frac{F(p)}{(p-1)^4}
 =1+\frac{8}{(p-1)^2}-\frac{2}{(p-1)^3}.
\]
There is also an exact Haar measure on \(\mathbb Z_p^4\). In a
locally admissible class with a single marked core, the first
remainder and that modulus are independent uniform coordinates
inside \(p\mathbb Z_p\), by the unit minor. Conditional on the core
having valuation \(k\ge1\), the remainder is divisible by \(p^k\)
with probability \(p^{-(k-1)}\). Summing over the geometric law of
\(k\) gives \(p/(p+1)\). This calculation includes the optional
overlap with \(E\), since the fixed edge allows the chosen positive
base exactly. All admissible classes with no marked core lift
without any density loss. Thus the local density at all powers is
\[
\mu_p=p^{-4}\left((p-1)^4+
\frac{p}{p+1}\big(8(p-1)^2-2(p-1)\big)\right).
\]
In particular \(\prod_{p>3}\mu_p/(1-1/p)^4\) converges absolutely
and is common to the five charts. At the strict prime \(p=r\),
every coordinate must be a unit. The dependent coordinate is
automatically a unit with the other four, and \(B=0\bmod r\)
meets the only strict-prime edge condition. Its local measure is
\((1-1/r)^4\). A global counting asymptotic or a prediction of first
witness height would require further estimates, since the active
primes depend on the unknown coordinates.

At the prime two in the factor-three charts the checker finds seven
classes modulo two in each chart. Modulo four it finds 100, 102 and
100 classes for 119772 with shifts 1 and 2, and 606897, respectively.
These are truncated counts, since modulus four leaves deeper valuation
classes unresolved.

    PYTHONPATH=src python -B research/five-state/continuation/verify_square_prime_patterns.py
