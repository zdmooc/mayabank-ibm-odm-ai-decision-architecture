#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "data" / "synthetic" / "iard-claim-cases.csv"


def as_bool(value: str) -> bool:
    return value.lower() == "true"


def decide(row: dict[str, str]) -> dict:
    claim_id = row["claimId"]
    policy_active = as_bool(row["policyActive"])
    coverage_present = as_bool(row["coveragePresent"])
    event_covered = as_bool(row["eventCovered"])
    claimed_amount = float(row["claimedAmount"])
    deductible = float(row["deductible"])
    fraud_score = float(row["fraudScore"])

    indemnity = max(claimed_amount - deductible, 0.0)
    human_review = False

    if not policy_active:
        decision, reason, indemnity = "REJECT", "POLICY_INACTIVE", 0.0
    elif not coverage_present:
        decision, reason, indemnity = "REJECT", "COVERAGE_NOT_PRESENT", 0.0
    elif not event_covered:
        decision, reason, indemnity = "REJECT", "EVENT_NOT_COVERED", 0.0
    elif fraud_score >= 0.80:
        decision, reason, human_review = "REVIEW", "FRAUD_HIGH_SCORE", True
    elif fraud_score >= 0.55:
        decision, reason, human_review = "REVIEW", "FRAUD_MEDIUM_SCORE", True
    else:
        decision, reason = "PAY", "COVERAGE_CONFIRMED"

    return {
        "decisionId": f"DEC-{claim_id}",
        "claimId": claim_id,
        "decision": decision,
        "reason": reason,
        "humanReviewRequired": human_review,
        "indemnity": round(indemnity, 2),
        "ruleVersion": "claim-rules-v1",
        "fraudScoreVersion": "fraud-score-simulated-v1",
    }


def main() -> None:
    with CASES.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    if not rows:
        raise SystemExit("ERROR: no claim cases")

    for row in rows:
        actual = decide(row)
        expected = {
            "decision": row["expectedDecision"],
            "reason": row["expectedReason"],
            "humanReviewRequired": as_bool(row["expectedHumanReview"]),
            "indemnity": round(float(row["expectedIndemnity"]), 2),
        }
        for key, value in expected.items():
            if actual[key] != value:
                raise SystemExit(f"ERROR {row['claimId']} {key}: expected={value} actual={actual[key]}")
        print(f"{row['claimId']}: OK -> {actual['decision']} / {actual['reason']} / indemnity={actual['indemnity']}")

    print("Iteration 04 claim/fraud portable validation: OK")
    print("Note: fraud scores are synthetic inputs; this is not an ML model nor an IBM ODM runtime execution.")


if __name__ == "__main__":
    main()
