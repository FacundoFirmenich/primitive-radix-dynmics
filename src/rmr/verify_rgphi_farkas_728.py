"""Check the exact two-strict high-cone Farkas certificate identities."""

import argparse
import json
from collections import deque
from fractions import Fraction
from pathlib import Path


def fibre_weights(mapping, factors):
    adjacent = [[] for _ in mapping]
    for source, target in enumerate(mapping):
        adjacent[source].append((target, 1 / factors[source]))
        adjacent[target].append((source, factors[source]))
    weights = {}
    for index in range(len(mapping)):
        if index in weights:
            continue
        weights[index] = index, Fraction(1)
        pending = deque([index])
        while pending:
            current = pending.popleft()
            root, weight = weights[current]
            for neighbour, ratio in adjacent[current]:
                value = root, weight * ratio
                if neighbour in weights:
                    if weights[neighbour] != value:
                        raise ArithmeticError("Inconsistent fibre equations")
                else:
                    weights[neighbour] = value
                    pending.append(neighbour)
    return weights


def check(row):
    factors = {letter: [Fraction(1)] * 5 for letter in "TS"}
    for edge in row["strict_edges"].split("|"):
        source, factor = edge[1:].split(":r")
        factors[edge[0]][int(source)] = Fraction(factor)
    p = fibre_weights([int(x) for x in row["S"].split(",")], factors["S"])
    q = fibre_weights([int(x) for x in row["T"].split(",")], factors["T"])

    constraints = {}
    for i in range(5):
        p_root, p_weight = p[i]
        q_root, q_weight = q[i]
        p_key, q_key = ("p", p_root), ("q", q_root)
        constraints[f"p{i}>=1"] = [(p_key, p_weight)]
        constraints[f"q{i}-p{i}>=1"] = [(p_key, -p_weight), (q_key, q_weight)]
        constraints[f"2p{i}-q{i}>=1"] = [(p_key, 2 * p_weight), (q_key, -q_weight)]

    total = {}
    bound = Fraction()
    for label, raw_multiplier in row["terms"]:
        multiplier = Fraction(raw_multiplier)
        if multiplier <= 0:
            raise ArithmeticError((row["id"], "Nonpositive multiplier"))
        bound += multiplier
        for coordinate, coefficient in constraints[label]:
            total[coordinate] = total.get(coordinate, Fraction()) + multiplier * coefficient
    if any(total.values()) or bound <= 0 or bound != -Fraction(row["rhs"]):
        raise ArithmeticError((row["id"], "Invalid contradiction"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("certificate", type=Path)
    entries = json.loads(parser.parse_args().certificate.read_bytes())
    if len(entries) != 728 or len({row["id"] for row in entries}) != 728:
        raise ValueError("Expected 728 different profiles")
    for entry in entries:
        check(entry)
    print("Exact Farkas identities:", len(entries))
