# Exceptional ordered cases and the direct quartic construction

The structured quotient search was applied to both remaining ordered rows.
The table lists the four necessary cycle numerators after elimination of
the fifth-state coordinate from the indicated congruences.

| Ordered case | modulo A | modulo C | modulo D | modulo Q |
| --- | --- | --- | --- | --- |
| 119772, factor 2 | 4Q²−D² | Q²−D² | C²−4A² | C²−A² |
| 606897, factor 3 | Q²−D² | 9Q²−D² | C²−A² | C²−9A² |

For 119772, the displayed state coordinates are those in the known-shape
criterion: the strict edge gives D congruent to 2E modulo A, and the
two-cycle at numerator A gives A dividing Q²−E². Combining them gives
the first entry. The other three entries come from the defect-one cycles.

For 606897, in the order in the local-moduli checker, use numerators
(A,C,E,C,A) and denominators (Q,D,Q,3Q,D). The S cycles on the numerators
A and C yield the first two entries. The T cycle at denominator D gives
the third entry. On the T cycle modulo Q, B² is 1 modulo Q. The strict
edge requires BC congruent to 3A modulo 3Q. Reducing modulo Q and squaring
gives the fourth entry.

For each row, consider a homogeneous quartic P in A,C,D,Q. Require its
restriction to each coordinate hyperplane to be a polynomial multiple
of the corresponding restricted cycle numerator. Polynomial division
gives linear conditions on the 35 coefficients. In both cases the rank
is 34 over the rationals, with kernel spanned by A C D Q. Thus this
direct ansatz yields only constant quotients P/(A C D Q).

    python research/five-state/continuation/verify_exceptional_quartics.py

The calculation is exhaustive for this ansatz. Additional conditions
involving E, the linear strict shifts when available, or other
denominators can change the quotient problem. Neither ordered case is
adjudicated here.
