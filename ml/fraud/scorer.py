#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MODEL_PATH = ROOT / "ml" / "fraud" / "model-v1.json"
CASES_PATH = ROOT / "data" / "synthetic" / "ml-fraud-cases.csv"


def load_model() -> dict:
    return json.loads(MODEL_PATH.read_text(encoding="utf-8"))


def as_bool(value: str) -> bool:
    return str(value).strip().lower() == "true"


def sigmoid(value: float) -> float:
    return 1.0 / (1.0 + math.exp(-value))


def score_case(row: dict, model: dict) -> dict:
    if not as_bool(row.get("model_available", "true")):
        return {
            "caseId": row["case_id"],
            "modelStatus": "UNAVAILABLE",
            "modelVersion": model["modelVersion"],
            "riskScore": None,
            "confidenceScore": 0.0,
            "policyDecision": "REVIEW",
            "reasonCode": "MODEL_UNAVAILABLE",
        }

    missing = 0
    claim_amount = float(row["claim_amount_eur"]) if row.get("claim_amount_eur") else 0.0
    recent_claims = None if row.get("recent_claims", "") == "" else float(row["recent_claims"])
    if recent_claims is None:
        missing += 1
        recent_claims = 0.0

    features = {
        "claimAmountNormalized": min(max(claim_amount / 25000.0, 0.0), 1.0),
        "recentClaimsNormalized": min(max(recent_claims / 3.0, 0.0), 1.0),
        "lateReporting": 1.0 if as_bool(row.get("late_reporting", "false")) else 0.0,
        "documentInconsistency": 1.0 if as_bool(row.get("document_inconsistency", "false")) else 0.0,
    }

    z = float(model["intercept"])
    for name, weight in model["features"].items():
        z += float(weight) * float(features[name])

    risk_score = round(sigmoid(z), 4)
    confidence = max(
        0.0,
        float(model["confidence"]["base"])
        - missing * float(model["confidence"]["missingFeaturePenalty"]),
    )
    confidence = round(confidence, 2)

    if confidence < float(model["confidence"]["minimumForPolicyUse"]):
        policy_decision, reason = "REVIEW", "MODEL_LOW_CONFIDENCE"
    elif risk_score >= 0.80:
        policy_decision, reason = "REVIEW", "FRAUD_HIGH_RISK"
    elif risk_score >= 0.55:
        policy_decision, reason = "REVIEW", "FRAUD_MEDIUM_RISK"
    else:
        policy_decision, reason = "STANDARD", "FRAUD_LOW_RISK"

    return {
        "caseId": row["case_id"],
        "modelStatus": "AVAILABLE",
        "modelVersion": model["modelVersion"],
        "riskScore": risk_score,
        "confidenceScore": confidence,
        "policyDecision": policy_decision,
        "reasonCode": reason,
        "features": features,
    }


def load_cases() -> list[dict]:
    with CASES_PATH.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def evaluate_all() -> list[dict]:
    model = load_model()
    return [score_case(row, model) for row in load_cases()]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    results = evaluate_all()
    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        for result in results:
            print(
                f"{result['caseId']}: {result['policyDecision']} | "
                f"score={result['riskScore']} confidence={result['confidenceScore']} "
                f"reason={result['reasonCode']}"
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
