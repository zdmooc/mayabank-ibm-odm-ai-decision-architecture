#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "decision-services" / "underwriting-offer"
DATASET = ROOT / "data" / "synthetic" / "iard-underwriting-cases.csv"
PRICING = BASE / "pricing-table.csv"
COVERAGE = BASE / "coverage-table.csv"


def rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def eligibility(case: dict[str, str]) -> tuple[str, str]:
    age = int(case["applicant_age"])
    incomplete = case["incomplete_file"].lower() == "true"
    license_years = int(case["driving_license_years"])
    claims = int(case["recent_claims"])
    risk = case["declared_risk_level"]

    if age < 18:
        return "REJECT", "APPLICANT_UNDER_18"
    if incomplete:
        return "REVIEW", "DOSSIER_INCOMPLET"
    if case["product_type"] == "AUTO" and license_years < 1:
        return "REVIEW", "PERMIS_TROP_RECENT"
    if claims >= 3:
        return "REVIEW", "SINISTRALITE_ELEVEE"
    if risk == "HIGH":
        return "REVIEW", "RISQUE_ELEVE"
    return "ACCEPT", "ELIGIBLE_STANDARD"


def pricing(case: dict[str, str], pricing_by_risk: dict[str, dict[str, str]]) -> float:
    row = pricing_by_risk[case["declared_risk_level"]]
    claims = min(int(case["recent_claims"]), 2)
    amount = (
        float(row["base_premium_eur"])
        * float(row["risk_coefficient"])
        * float(row[f"claims_coefficient_{claims}"])
    )
    return round(amount, 2)


def main() -> int:
    pricing_by_risk = {r["risk_level"]: r for r in rows(PRICING)}
    coverage_by_risk = {r["risk_level"]: r for r in rows(COVERAGE)}
    cases = rows(DATASET)

    if not cases:
        raise SystemExit("ERROR: no IARD cases")

    for case in cases:
        decision, reason = eligibility(case)
        premium = 0.0
        deductible = 0.0
        if decision == "ACCEPT":
            premium = pricing(case, pricing_by_risk)
            deductible = float(coverage_by_risk[case["declared_risk_level"]]["deductible_eur"])

        expected = (
            case["expected_decision"],
            case["expected_reason"],
            round(float(case["expected_premium_eur"]), 2),
            round(float(case["expected_deductible_eur"]), 2),
        )
        actual = (decision, reason, round(premium, 2), round(deductible, 2))
        if actual != expected:
            raise SystemExit(f"ERROR {case['case_id']}: expected={expected} actual={actual}")
        print(f"{case['case_id']}: OK -> {decision} / premium={premium:.2f} / deductible={deductible:.2f}")

    print(f"Iteration 03 IARD regression: OK ({len(cases)} cases)")
    print("Note: portable semantic validation only; IBM ODM runtime deployment comes later.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
