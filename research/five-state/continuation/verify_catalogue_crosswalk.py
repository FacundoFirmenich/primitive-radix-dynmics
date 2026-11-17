"""Match the published directed graphs to the Round 015 normal forms."""

import argparse
import ast
import csv
import itertools
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OUTPUT = HERE / "ORIENTED_TO_ROUND015.csv"


def representative(t, s, generator, source, factor):
    variants = []
    for perm in itertools.permutations(range(5)):
        inverse = tuple(perm.index(i) for i in range(5))
        left = tuple(perm[t[i]] for i in inverse)
        right = tuple(perm[s[i]] for i in inverse)
        variants.append(((left, right, generator, perm[source], factor), False))
        variants.append(((right, left, 1 - generator, perm[source], factor), True))
    return min(variants)


def rows():
    source = (HERE / "ROUND015_CLASS_TO_NORMAL_FORM.csv").read_text(encoding="utf-8")
    lines = source.splitlines()
    header = next(i for i, line in enumerate(lines) if line.startswith("index,canonical_key,"))
    normal_forms = {}
    for row in csv.DictReader(lines[header:]):
        key, exchanged = representative(*ast.literal_eval(row["canonical_key"]))
        if key in normal_forms:
            raise ValueError("Duplicate archived normal form")
        normal_forms[key] = row["normal_form"], exchanged, row["strict_generator_original"]
    if len(normal_forms) != 20:
        raise ValueError("Expected 20 archived forms")
    checker = ROOT / "src/rmr/check_open_branch_local_moduli.py"
    tables = {}
    for statement in ast.parse(checker.read_text(encoding="utf-8")).body:
        if isinstance(statement, ast.Assign) and isinstance(statement.targets[0], ast.Name):
            name = statement.targets[0].id
            if name in {"CASES", "FACTORS"}:
                tables[name] = ast.literal_eval(statement.value)
    for code, (t, s, letter, strict) in tables["CASES"].items():
        for factor in tables["FACTORS"][code]:
            key, exchanged = representative(t, s, "TS".index(letter), strict, factor)
            form, archived_exchange, archived_letter = normal_forms[key]
            yield {
                "ordered_code": code,
                "factor": factor,
                "strict_letter": letter,
                "form_id": form,
                "exchanges_generators_vs_canonical_key": str(exchanged != archived_exchange).lower(),
                "archived_original_strict_letter": archived_letter,
                "same_orientation_as_archived_original": str(archived_letter == letter).lower(),
            }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    result = list(rows())
    if len(result) != 11 or len({row["form_id"] for row in result}) != 10:
        raise ValueError("Unexpected crosswalk multiplicity")
    if args.write:
        with OUTPUT.open("x", encoding="utf-8", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=list(result[0]), lineterminator="\n")
            writer.writeheader()
            writer.writerows(result)
    else:
        with OUTPUT.open(encoding="utf-8", newline="") as stream:
            recorded = list(csv.DictReader(stream))
        if recorded != [{key: str(value) for key, value in row.items()} for row in result]:
            raise ValueError("Crosswalk differs from the archived inputs")
    print("Crosswalk verified: 11 oriented rows, 10 archived form IDs")


if __name__ == "__main__":
    main()
