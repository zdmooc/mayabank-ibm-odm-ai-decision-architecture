#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SERVICE = ROOT / "decision-services" / "underwriting-eligibility"
SAMPLES = SERVICE / "samples"
TABLE = SERVICE / "decision-table.csv"


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_rules() -> list[dict[str, str]]:
    with TABLE.open("r", encoding="utf-8", newline="") as handle:
        rules = list(csv.DictReader(handle))
    return sorted(rules, key=lambda row: int(row["priority"]), reverse=True)


def matches(rule: dict[str, str], request: dict) -> bool:
    if rule["incompleteFile"] != "*":
        expected = rule["incompleteFile"].lower() == "true"
        if request["incompleteFile"] is not expected:
            return False

    if rule["applicantAge_lt"] != "*" and not request["applicantAge"] < int(rule["applicantAge_lt"]):
        return False

    if rule["productType"] != "*" and request["productType"] != rule["productType"]:
        return False

    if rule["drivingLicenseYears_lt"] != "*":
        value = request.get("drivingLicenseYears")
        if value is None or not value < int(rule["drivingLicenseYears_lt"]):
            return False

    if rule["recentClaims_gte"] != "*" and not request["recentClaims"] >= int(rule["recentClaims_gte"]):
        return False

    if rule["declaredRiskLevel"] != "*" and request["declaredRiskLevel"] != rule["declaredRiskLevel"]:
        return False

    return True


def decide(request: dict, rules: list[dict[str, str]]) -> dict:
    for rule in rules:
        if matches(rule, request):
            return {
                "requestId": request["requestId"],
                "decision": rule["decision"],
                "reasonCodes": [rule["reasonCode"]],
                "decisionVersion": "iard-underwriting-v1",
            }
    raise RuntimeError(f"No rule matched request {request['requestId']}")


def validate_case(name: str, rules: list[dict[str, str]]) -> None:
    request = load_json(SAMPLES / f"request-{name}.json")
    expected = load_json(SAMPLES / f"expected-{name}.json")
    actual = decide(request, rules)
    if actual != expected:
        raise SystemExit(
            f"ERROR {name}:\nexpected={json.dumps(expected, indent=2)}\nactual={json.dumps(actual, indent=2)}"
        )
    print(f"{name.upper()}: OK -> {actual['decision']} / {actual['reasonCodes'][0]}")


def main() -> None:
    rules = load_rules()
    if not rules:
        raise SystemExit("ERROR: decision table is empty")

    for name in ("accept", "reject", "review"):
        validate_case(name, rules)

    print("Iteration 01 ODM portable validation: OK")
    print("Note: this validates the portable specification, not an IBM ODM runtime deployment.")


if __name__ == "__main__":
    main()
