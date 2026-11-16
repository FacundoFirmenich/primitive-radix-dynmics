"""Exact prime-power packing and a replay of the historical 500,000-base sieve.

The new-carrier implications consume the all-height h<=14 certificate from
NEST-ATTACK-001.  This program does not prove that certificate, classify
carriers, or test all ten transitions.  See PROOF_EN.md for the implications.
No third-party packages or network access are used.
"""
from array import array
from collections import Counter
from functools import lru_cache
from hashlib import sha256
from math import gcd, isqrt, prod
from pathlib import Path
import json
import time

HERE = Path(__file__).resolve().parent
LOWER = 9_185_770_249
UPPER = 9_186_270_248
KNOWN_R = 88_011_536_665_779
KNOWN_M = 223_336_848_698_040


def primes_through(n):
    sieve = bytearray(b"\x01") * (n + 1)
    sieve[:2] = b"\x00\x00"
    for p in range(2, isqrt(n) + 1):
        if sieve[p]:
            sieve[p * p:n + 1:p] = b"\x00" * (((n - p * p) // p) + 1)
    return [p for p in range(2, n + 1) if sieve[p]]


def factor(n):
    out = {}
    for p in primes_through(isqrt(n)):
        if p * p > n:
            break
        while n % p == 0:
            out[p] = out.get(p, 0) + 1
            n //= p
    if n > 1:
        out[n] = 1
    return out


def atoms_from_factors(factors):
    return [p ** e for p, e in factors.items() if p != 2]


def capacity(atoms):
    big = sum(a >= 15 for a in atoms)
    return big + (len(atoms) - big) // 2


def brute_capacity(atoms):
    """Maximum number of disjoint groups with product >=15, by all subsets."""
    size = 1 << len(atoms)
    products = [1] * size
    for mask in range(1, size):
        bit = mask & -mask
        products[mask] = products[mask ^ bit] * atoms[bit.bit_length() - 1]

    @lru_cache(None)
    def solve(mask):
        best = 0
        sub = mask
        while sub:
            if products[sub] >= 15:
                best = max(best, 1 + solve(mask ^ sub))
            sub = (sub - 1) & mask
        return best

    return solve(size - 1)


def segmented_features(lo, hi):
    """Factor all integers in a closed interval using exact division."""
    size = hi - lo + 1
    remaining = array("Q", range(lo, hi + 1))
    omega = bytearray(size)
    odd_omega = bytearray(size)
    big = bytearray(size)
    small = bytearray(size)
    for p in primes_through(isqrt(hi)):
        for i in range((-lo) % p, size, p):
            if remaining[i] % p:
                continue
            omega[i] += 1
            power = 1
            while remaining[i] % p == 0:
                remaining[i] //= p
                power *= p
            if p != 2:
                odd_omega[i] += 1
                if power >= 15:
                    big[i] += 1
                else:
                    small[i] += 1
    for i, rem in enumerate(remaining):
        if rem > 1:
            assert rem > isqrt(hi)
            omega[i] += 1
            odd_omega[i] += 1
            big[i] += 1
    caps = bytearray(big[i] + small[i] // 2 for i in range(size))
    return omega, odd_omega, caps


def run():
    started = time.time()
    # Local two-adic control: a<=b+1 is the needed implication, not a=b+1.
    # This is not asserted to be a realized RGPHI core or a global base example.
    local_base, local_modulus = 33, 32*17
    assert (local_base*local_base-1)%local_modulus == 0
    local_cofactors = [local_modulus//gcd(local_modulus,local_base-1),
                       local_modulus//gcd(local_modulus,local_base+1)]
    assert local_cofactors == [17,16]  # a=b=5 is allowed locally
    # Check the closed packing formula against exhaustive subset partitioning.
    atom_tests = 0
    for n in range(1, 20_002, 2):
        atoms = atoms_from_factors(factor(n))
        assert capacity(atoms) == brute_capacity(atoms), (n, atoms)
        atom_tests += 1

    assert UPPER < KNOWN_R  # no known-carrier CRT base in this window
    omega, odd_omega, caps = segmented_features(LOWER - 1, UPPER + 1)
    counts = Counter()
    rejected_examples = {}
    survivors = {"factor_two": [], "factor_three": [], "606897_factor_three": []}
    for base in range(LOWER, UPPER + 1):
        i = base - LOWER  # index of B-1 in the segmented interval
        om, op = omega[i], omega[i + 2]
        qm, qp = odd_omega[i], odd_omega[i + 2]
        cm, cp = caps[i], caps[i + 2]
        old = om >= 4 and op >= 4
        counts["bases"] += 1

        if base % 2 == 0:
            counts["even_bases"] += 1
            if old:
                counts["old_factor_two"] += 1
                if min(cm, cp) >= 4:
                    counts["new_factor_two"] += 1
                    survivors["factor_two"].append(base)
                else:
                    rejected_examples.setdefault("factor_two_packing", base)

        if base % 3 == 0:
            counts["multiples_of_three"] += 1
            if base % 2:
                counts["odd_multiples_of_three"] += 1
            if old:
                counts["old_factor_three"] += 1
                accepted = True
                if base % 2:
                    counts["old_odd_factor_three"] += 1
                    if qm == qp == 3:
                        counts["odd_removed_3_plus_3"] += 1
                        accepted = False
                    if accepted:
                        counts["odd_after_3_plus_3"] += 1
                        if min(cm, cp) < 3:
                            counts["odd_removed_packing"] += 1
                            rejected_examples.setdefault("odd_packing", base)
                            accepted = False
                    if accepted:
                        counts["odd_after_packing"] += 1
                        if ((qm == 3 and base % 48 != 33) or
                                (qp == 3 and base % 48 != 15)):
                            counts["odd_removed_mod48"] += 1
                            rejected_examples.setdefault("odd_mod48", base)
                            accepted = False
                elif min(cm, cp) < 4:
                    counts["even_factor_three_removed_packing"] += 1
                    accepted = False
                if accepted:
                    counts["new_factor_three"] += 1
                    survivors["factor_three"].append(base)
                    if base % 2:
                        counts["new_odd_factor_three"] += 1
                        survivors["606897_factor_three"].append(base)

        if base % 2 == 0 or base % 3 == 0:
            counts["old_domain_union"] += 1
            if old:
                counts["old_union_pass"] += 1

    assert counts["even_bases"] == 250_000
    assert counts["multiples_of_three"] == 166_666
    assert counts["odd_multiples_of_three"] == 83_333
    assert counts["old_factor_two"] == 17_518
    assert counts["old_factor_three"] == 23_081
    assert counts["old_odd_factor_three"] == 20_499
    assert counts["old_union_pass"] == 38_017
    assert counts["odd_removed_3_plus_3"] == 9_064

    all_survivors = sorted(set(survivors["factor_two"]) |
                           set(survivors["factor_three"]))
    counts["new_union_pass"] = len(all_survivors)
    counts["new_union_removed"] = counts["old_union_pass"] - len(all_survivors)

    # Independent trial division of a deterministic sample of segment features.
    sample_bases = sorted(set([LOWER, UPPER] + list(rejected_examples.values()) +
                             [LOWER + (UPPER - LOWER) * j // 1000
                              for j in range(1001)]))
    for base in sample_bases:
        for n in (base - 1, base + 1):
            fs = factor(n)
            j = n - (LOWER - 1)
            assert prod(p ** e for p, e in fs.items()) == n
            assert (omega[j], odd_omega[j], caps[j]) == (
                len(fs), len(atoms_from_factors(fs)),
                capacity(atoms_from_factors(fs)))

    # The known carrier must remain a separate alternative, at every CRT base.
    witness = (406, 712, 1265, 731)
    A, C, D, Q = witness
    signed = {
        "A": [A // gcd(A, D - 3 * Q), A // gcd(A, D + 3 * Q)],
        "C": [C // gcd(C, D - Q), C // gcd(C, D + Q)],
        "D": [D // gcd(D, C - 3 * A), D // gcd(D, C + 3 * A)],
        "Q": [Q // gcd(Q, C - A), Q // gcd(Q, C + A)],
    }
    assert any(h <= 14 for pair in signed.values() for h in pair)
    for t in range(1001):
        base = KNOWN_R + t * KNOWN_M
        for mod, hs in zip(witness, signed.values()):
            assert sorted(hs) == sorted(
                [mod // gcd(mod, base - 1), mod // gcd(mod, base + 1)])

    example_records = {}
    for label, base in rejected_examples.items():
        neighbors = []
        for n in (base - 1, base + 1):
            fs = factor(n)
            neighbors.append({"n": n, "factors": fs,
                              "omega": len(fs),
                              "odd_omega": len(atoms_from_factors(fs)),
                              "packing_capacity_15": capacity(atoms_from_factors(fs))})
        example_records[label] = {"base": base, "neighbors": neighbors}

    out = {
        "checkpoint": "NEST-ATTACK-002-PRIME-PACKING",
        "status": "PASS_SCOPED_NECESSARY_FILTERS_NOT_REALIZATION_CENSUS",
        "window_inclusive": [LOWER, UPPER],
        "counts": dict(sorted(counts.items())),
        "packing_formula_exhaustive_controls": atom_tests,
        "segment_trial_division_sample_bases": len(sample_bases),
        "known_carrier_CRT_positive_controls": 1001,
        "two_adic_local_inequality_control": {
            "B":local_base,"modulus":local_modulus,"a":5,"b":5,
            "signed_denominators":local_cofactors,
            "scope":"local root/cofactor control, not a realized RGPHI core"},
        "known_carrier_signed_denominators": signed,
        "new_carrier_assumption": "all eight signed cofactor denominators exceed 14",
        "source_of_assumption": "NEST-ATTACK-001 scoped all-height certificate",
        "rejected_examples": example_records,
        "seconds": time.time() - started,
        "script_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "review": "self-review; trial-division control is a separate implementation, not independent review",
        "scope": "No state realization is asserted. Window below known CRT residue and below latest conditional base bound.",
    }
    (HERE / "RESULTS.json").write_text(json.dumps(out, indent=2) + "\n")
    (HERE / "SURVIVING_BASES.json").write_text(json.dumps(survivors, separators=(",", ":")) + "\n")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    run()
