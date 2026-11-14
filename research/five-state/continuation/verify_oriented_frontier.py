"""Compose the oriented status ledger from explicit proof jurisdictions."""

import csv
import sys

from verify_catalogue_crosswalk import rows as crosswalk
from verify_oriented_predecessors import audit


def ledger():
    verified_shared = {
        (row["form_id"], row["strict_letter"])
        for row in crosswalk() if row["ordered_code"] not in {606897, 119772}
    }
    for row in audit()["rows"]:
        form, letter, factor = row["form"], row["strict_letter"], row["factor"]
        key = form, letter
        status, evidence = "OPEN", ""
        if row["status"] != "HIGH_FEASIBLE":
            status, evidence = "EXCLUDED", "ORIENTED_PREDECESSOR_CERTIFICATES.json"
        elif key in verified_shared:
            status, evidence = "EXCLUDED", "SHARED_SYSTEMS_EXCLUSION.md"
        elif letter == "S" and form in {"DF015-0004","DF015-0008","DF015-0012","DF015-0018"}:
            status, evidence = "EXCLUDED", "SPARSE_S_STRICT_CERTIFICATES.json"
        elif key == ("DF015-0015", "T"):
            status, evidence = "EXCLUDED", "../../df015-0015/CERTIFICATE.md"
        elif key == ("DF015-0016", "T"):
            status, evidence = "ARCHIVED_EXCLUSION", "Round 016 FORM_ADJUDICATION_20.csv, R3_PARTIAL_RECTANGLE_NO_GO"
        elif key == ("DF015-0007", "S"):
            status, evidence = "REALIZED_CONTAINING", "../../../certificates/ARITHMETIC_PROGRESSION.json"
        yield form, letter, factor, status, evidence


if __name__ == "__main__":
    writer = csv.writer(sys.stdout, lineterminator="\n")
    writer.writerow(("form", "strict_letter", "factor", "status", "evidence"))
    writer.writerows(sorted(ledger()))
