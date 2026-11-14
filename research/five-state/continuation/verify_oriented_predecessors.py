"""Exact linear feasibility replay for both orientations of the Round 015 forms."""

import argparse
import ast
import csv
import json
from collections import Counter
from math import gcd
from pathlib import Path


HERE = Path(__file__).resolve().parent


def fibre_coordinates(mapping, strict, factor, offset):
    ordinary = set(range(5)) - {strict}
    if set(mapping[i] for i in ordinary) != ordinary:
        raise ValueError("Ordinary edges must form a permutation")
    coords = {}
    count = offset
    for start in sorted(ordinary):
        if start in coords:
            continue
        node = start
        while node not in coords:
            coords[node] = (count, 1)
            node = mapping[node]
        count += 1
    if strict is not None:
        coords[strict] = (coords[mapping[strict]][0], factor)
    return coords, count


def combine(left, right, a=1, b=1):
    return tuple(a*x + b*y for x, y in zip(left, right, strict=True))


def contradiction(rows):
    """Eliminate a variable at a time, retaining exact positive combinations."""
    size = len(rows)
    width = len(rows[0])
    system = {row: tuple(int(i == j) for j in range(size)) for i, row in enumerate(rows)}
    for slot in range(width + 1):
        if (0,)*width in system:
            weights = system[(0,)*width]
            if not any(weights) or min(weights) < 0:
                raise ArithmeticError("Invalid infeasibility certificate")
            if any(sum(weight*row[i] for weight, row in zip(weights, rows, strict=True))
                   for i in range(width)):
                raise ArithmeticError("Invalid weighted sum")
            return weights
        if slot == width:
            return None
        lower = [(row, w) for row, w in system.items() if row[slot] > 0]
        upper = [(row, w) for row, w in system.items() if row[slot] < 0]
        system = {row: w for row, w in system.items() if not row[slot]}
        for row1, w1 in lower:
            for row2, w2 in upper:
                divisor = gcd(row1[slot], row2[slot])
                a, b = -row2[slot]//divisor, row1[slot]//divisor
                system.setdefault(combine(row1, row2, a, b), combine(w1, w2, a, b))
    raise ArithmeticError("Elimination did not terminate")


def eliminate_equality(rows, equation):
    pivot = next((i for i, value in enumerate(equation) if value), None)
    if pivot is None:
        return rows
    scale = abs(equation[pivot])
    sign = equation[pivot] // scale
    return [combine(row, equation, scale, -sign*row[pivot]) for row in rows]


def analyze(t, s, letter, strict, factor):
    p, dim = fibre_coordinates(s, strict if letter else None, factor, 0)
    q, dim = fibre_coordinates(t, strict if not letter else None, factor, dim)
    if len({(p[i], q[i]) for i in range(5)}) != 5:
        return {"status": "FORCED_STATE_COLLISION"}

    def linear(*terms):
        row = [0]*dim
        for (variable, multiplier), coefficient in terms:
            row[variable] += multiplier*coefficient
        return tuple(row)

    high = []
    for i in range(5):
        high.extend((linear((q[i], 1), (p[i], -1)), linear((p[i], 2), (q[i], -1))))
    mapping, shifted, modulus = (s, q, p) if letter else (t, p, q)
    target = mapping[strict]
    predecessor, = (i for i in range(5) if i != strict and mapping[i] == target)
    # Strictness and reducedness exclude shift zero in both charts.
    j_bound = factor - 1 if letter else (factor - 1)//2
    branches = {}
    for j in range(-j_bound, j_bound + 1):
        if j == 0:
            continue
        shift = linear((shifted[strict], 1), (shifted[predecessor], -factor), (modulus[target], -j))
        proof = contradiction(eliminate_equality(high, shift))
        branches[j] = {"infeasibility_weights": proof} if proof else {"high_feasible": True}
    return {"status": "HIGH_FEASIBLE" if any("high_feasible" in row for row in branches.values())
            else "NO_HIGH_PREDECESSOR_BRANCH", "branches": branches}


def records():
    lines = (HERE / "ROUND015_CLASS_TO_NORMAL_FORM.csv").read_text(encoding="utf-8").splitlines()
    start = next(i for i, line in enumerate(lines) if line.startswith("index,canonical_key,"))
    for record in csv.DictReader(lines[start:]):
        yield {**record, "graph": ast.literal_eval(record["canonical_key"])}


def audit():
    rows = []
    for record in records():
        t, s, letter, source, factor = record["graph"]
        for first, second, direction in ((t, s, letter), (s, t, 1-letter)):
            rows.append({"form": record["normal_form"], "strict_letter": "TS"[direction],
                         "factor": factor, **analyze(first, second, direction, source, factor)})
    if len(rows) != 40 or len({(r["form"], r["strict_letter"]) for r in rows}) != 40:
        raise ValueError("Expected two distinct orientations for each of twenty forms")
    return {"counts": dict(sorted(Counter(row["status"] for row in rows).items())), "rows": rows}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--compact", action="store_true")
    args = parser.parse_args()
    report = audit()
    print(json.dumps(report["counts"] if args.compact else report, indent=2))


if __name__ == "__main__":
    main()
