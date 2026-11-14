# Transitive-generator rigidity in arbitrary cardinality

**2026-11-13 · PROVED_SYMBOLIC · Claim C017**

Let \(F\subset\mathbb Q\cap(1/2,1)\) be a finite closed strongly connected component of cardinality \(n\).

## Theorem

1. If \(T_B|_F\) is a single \(n\)-cycle, then \(S_B|_F=\mathrm{id}\).
2. If \(S_B|_F\) is a single \(n\)-cycle, then \(T_B|_F=\mathrm{id}\).
3. In either architecture, \(n\le\tau(B-1)\).

## Proof

If \(T_B|_F\) is an \(n\)-cycle, the denominator law cannot decrease strictly and return, so all states have a common reduced denominator \(q\) and \(\gcd(q,B)=1\). For \(x=p/q\in F\), put \(g=\gcd(p,B)\). If \(g>1\), then the numerator of \(S_Bx\) is \(p/g<p/2<q/2\). Every target in \(F\) has denominator \(q\) and is high, hence numerator \(>q/2\), contradiction. Thus \(g=1\) at every state. The \(S_B\)-map preserves the numerator and, since every target denominator is \(q\), fixes each state. The fixed-point condition is equivalent to \(p\mid B-1\) for every numerator in the \(T\)-cycle; the numerators are distinct, so \(n\le\tau(B-1)\).

For the second assertion, if \(S_B|_F\) is an \(n\)-cycle, the numerator law cannot decrease strictly around the cycle, so all states share one numerator \(p\) with \(\gcd(p,B)=1\). A strict \(T_B\)-edge from \(p/q\) would have target denominator at most \(q/2<p\), impossible for a high target with numerator \(p\). Hence every \(T_B\)-edge has defect one, preserves the denominator and fixes the state. Each denominator therefore divides \(B-1\), yielding \(n\le\tau(B-1)\).

## Consequence

Every nonpermutation finite high component is nontransitive under both restricted generators.
