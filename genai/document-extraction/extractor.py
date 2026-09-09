#!/usr/bin/env python3
"""Portable GenAI extraction gate using synthetic provider outputs only."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "synthetic" / "genai-documents.jsonl"
MIN_CONFIDENCE = 0.85


def load_cases(path: Path = DATA) -> list[dict]:
    with path.open("r", encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def validate_extraction(payload: dict) -> list[str]:
    errors: list[str] = []
    required = {
        "documentId", "documentType", "claimId", "lossDate", "claimedAmount",
        "currency", "confidenceScore", "providerStatus", "extractionVersion",
    }
    missing = sorted(required - set(payload))
    if missing:
        errors.append("MISSING_FIELDS:" + ",".join(missing))
        return errors

    if payload["documentType"] not in {"CLAIM_NOTICE", "INVOICE", "SUPPORTING_DOCUMENT"}:
        errors.append("INVALID_DOCUMENT_TYPE")
    if not isinstance(payload["claimedAmount"], (int, float)) or payload["claimedAmount"] < 0:
        errors.append("INVALID_CLAIMED_AMOUNT")
    if payload["currency"] != "EUR":
        errors.append("INVALID_CURRENCY")
    if not isinstance(payload["confidenceScore"], (int, float)) or not 0 <= payload["confidenceScore"] <= 1:
        errors.append("INVALID_CONFIDENCE")
    if payload["providerStatus"] not in {"AVAILABLE", "UNAVAILABLE"}:
        errors.append("INVALID_PROVIDER_STATUS")
    if payload["extractionVersion"] != "genai-extraction-v1":
        errors.append("INVALID_EXTRACTION_VERSION")
    if not isinstance(payload["lossDate"], str) or len(payload["lossDate"]) != 10:
        errors.append("INVALID_LOSS_DATE")
    return errors


def gate(payload: dict) -> dict:
    errors = validate_extraction(payload)
    reasons: list[str] = []

    if errors:
        reasons.extend(errors)
        next_step = "HUMAN_REVIEW"
    elif payload["providerStatus"] != "AVAILABLE":
        reasons.append("GENAI_PROVIDER_UNAVAILABLE")
        next_step = "HUMAN_REVIEW"
    elif float(payload["confidenceScore"]) < MIN_CONFIDENCE:
        reasons.append("GENAI_LOW_CONFIDENCE")
        next_step = "HUMAN_REVIEW"
    else:
        reasons.append("GENAI_EXTRACTION_VALIDATED")
        next_step = "FORWARD_TO_ODM"

    return {
        "documentId": payload.get("documentId"),
        "nextStep": next_step,
        "reasonCodes": reasons,
        "confidenceScore": payload.get("confidenceScore"),
        "extractionVersion": payload.get("extractionVersion"),
        "businessDecision": None,
    }


def run() -> list[dict]:
    results = []
    for case in load_cases():
        result = gate(case["simulatedExtraction"])
        result["expectedNextStep"] = case["expectedNextStep"]
        results.append(result)
    return results


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    results = run()
    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        for row in results:
            print(f"{row['documentId']}: {row['nextStep']} / {','.join(row['reasonCodes'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
