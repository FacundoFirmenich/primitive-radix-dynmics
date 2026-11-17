# FST-11 public result register · RC3.3

This is a concise code-and-certificate scope record. Full proofs are integrated in the private companion; the supplement records execution and source preservation.

## F11K

**Exact prefix-eight kernel and complete two-axis word normal form.** For literal decimal words including the empty word, K(w)=8*10^len(w)-9*val(w). Its exact kernel is prefixing eights. The image of Pi7(K) is h with 7 not dividing h and h mod9 in {2,5,8}; every word has unique coordinates (h,j,t), with scaling 7^(a0(h)+3j) and leading-eight count t. This extends the fixed-length contract without discarding literal length.

Scope: All finite decimal words, including empty and leading zeros; a set bijection, not a monoid isomorphism.

Evidence: [source engine](src/fst11.py), [exact checker](audit_fst11.py), [current receipt](../../../outputs/reports/fst11/RUN_MANIFEST.json).

## F11H

**Prime-erasure lattice fusion and bounded regular-language ambiguity witness.** Prime-erasure channels fuse by lcm into erasure of the intersection and by gcd into erasure of the union. Signed Pi7 and Pi2 recover K. On a regular language L they identify a word without length exactly when L intersects 8+L trivially; a q-state DFA gives ambiguity witnesses t<=q and word length<=q^2-1.

Scope: Sign preserved; exact complementary units recover K; literal recovery requires length or prefix-separating language.

Evidence: [source engine](src/fst11.py), [exact checker](audit_fst11.py), [current receipt](../../../outputs/reports/fst11/RUN_MANIFEST.json).

## F11C

**Language-conditioned finite-precision CRT identification.** For known length and distinct primes other than three, exact valuations and positive unit precisions define one CRT class. A DFA/modular-counter product counts all compatible words. For 002, K=7982 and combined modulus 56 yield eighteen unrestricted three-digit candidates, but one under the ending-02 restriction. The implementation tests 376 observed signature classes and 1111 guaranteed decodings.

Scope: Distinct primes other than three; valuations known, unit precisions positive; uniqueness requires exact candidate count.

Evidence: [source engine](src/fst11.py), [exact checker](audit_fst11.py), [current receipt](../../../outputs/reports/fst11/RUN_MANIFEST.json).

## F11R

**Fixed-scaling regular relation and nonregular unrestricted h=8 fibre.** For fixed j, decimal multiplication by 343^j with the specified final carry is a synchronous regular relation. The unbounded h=8 fibre is nonregular: its canonical word lengths are ceil(j log10(343)), with irrational length-set density. The finite language {888889,901961} has a j=2 pair and no j=1 pair; neighbor-only chain counts do not transfer to arbitrary sublanguages.

Scope: Fixed j synchronous regularity; no global arbitrary-language normalized-injectivity decision claimed.

Evidence: [source engine](src/fst11.py), [exact checker](audit_fst11.py), [current receipt](../../../outputs/reports/fst11/RUN_MANIFEST.json).

## F11V

**Replayed supplied FST11 source, atlas tables and finite direct checks.** Current exact checks cover all 11111 words of lengths zero through four, 2223 lattice inverse keys in the stated interval, all 25 embedded atlas records, five DFA language families, 376 observed finite-signature classes, 1111 guaranteed finite decodings and 7200 prime-set lattice comparisons. The unchanged documented CLI also passes. These are finite checks and assisted self-review, not a new global RGphi exclusion or external independent review.

Scope: Current exact checks only; unattached historical 47/29 suites and FST10 archive not reproduced.

Evidence: [source engine](src/fst11.py), [exact checker](audit_fst11.py), [current receipt](../../../outputs/reports/fst11/RUN_MANIFEST.json).
