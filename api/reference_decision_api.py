#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

IDEMPOTENCY_STORE: dict[str, tuple[str, dict[str, Any]]] = {}


def canonical_hash(payload: dict[str, Any]) -> str:
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def problem(status: int, code: str, title: str, correlation_id: str, detail: str = "") -> dict[str, Any]:
    return {
        "type": f"urn:mayainsurance:problem:{code.lower()}",
        "title": title,
        "status": status,
        "code": code,
        "detail": detail,
        "correlationId": correlation_id,
    }


def decide_underwriting(payload: dict[str, Any], correlation_id: str) -> dict[str, Any]:
    if payload.get("applicantAge", 0) < 18:
        decision, reasons = "REJECT", ["APPLICANT_UNDER_18"]
    elif payload.get("incompleteFile"):
        decision, reasons = "REVIEW", ["DOSSIER_INCOMPLET"]
    elif payload.get("productType") == "AUTO" and payload.get("drivingLicenseYears", 0) < 1:
        decision, reasons = "REVIEW", ["PERMIS_TROP_RECENT"]
    elif payload.get("recentClaims", 0) >= 3:
        decision, reasons = "REVIEW", ["SINISTRALITE_ELEVEE"]
    elif payload.get("declaredRiskLevel") == "HIGH":
        decision, reasons = "REVIEW", ["RISQUE_ELEVE"]
    else:
        decision, reasons = "ACCEPT", ["ELIGIBLE_STANDARD"]
    return {
        "decisionId": f"DEC-{uuid.uuid4()}",
        "decision": decision,
        "reasonCodes": reasons,
        "decisionVersion": "iard-underwriting-v1",
        "correlationId": correlation_id,
        "humanReviewRequired": decision == "REVIEW",
    }


def decide_claim(payload: dict[str, Any], correlation_id: str) -> dict[str, Any]:
    if not payload.get("policyActive"):
        decision, reasons = "REJECT", ["POLICY_INACTIVE"]
    elif not payload.get("coveragePresent"):
        decision, reasons = "REJECT", ["COVERAGE_MISSING"]
    elif not payload.get("eventCovered"):
        decision, reasons = "REJECT", ["EVENT_NOT_COVERED"]
    elif float(payload.get("fraudScore", 0.0)) >= 0.80:
        decision, reasons = "REVIEW", ["FRAUD_HIGH_SCORE"]
    elif float(payload.get("fraudScore", 0.0)) >= 0.55:
        decision, reasons = "REVIEW", ["FRAUD_REVIEW_SCORE"]
    else:
        decision, reasons = "PAY", ["CLAIM_COVERED"]
    return {
        "decisionId": f"DEC-{uuid.uuid4()}",
        "decision": decision,
        "reasonCodes": reasons,
        "decisionVersion": "iard-claim-v1",
        "correlationId": correlation_id,
        "humanReviewRequired": decision == "REVIEW",
    }


def _authorized(auth_header: str) -> bool:
    if not auth_header.startswith("Bearer "):
        return False
    expected = os.getenv("LAB_BEARER_TOKEN", "").strip()
    if not expected:
        return True
    return auth_header == f"Bearer {expected}"


def process_decision(path: str, payload: dict[str, Any], headers: dict[str, str]) -> tuple[int, dict[str, Any], str]:
    correlation_id = headers.get("X-Correlation-Id") or f"COR-{uuid.uuid4()}"
    auth = headers.get("Authorization", "")
    if not _authorized(auth):
        return 401, problem(401, "UNAUTHORIZED", "Valid Bearer token required", correlation_id), correlation_id

    idem_key = headers.get("Idempotency-Key", "")
    if len(idem_key) < 8:
        return 400, problem(400, "INVALID_REQUEST", "Idempotency-Key required", correlation_id), correlation_id

    payload_hash = canonical_hash(payload)
    cached = IDEMPOTENCY_STORE.get(idem_key)
    if cached:
        cached_hash, cached_response = cached
        if cached_hash != payload_hash:
            return 409, problem(409, "IDEMPOTENCY_CONFLICT", "Idempotency key reused with different payload", correlation_id), correlation_id
        response = dict(cached_response)
        response["correlationId"] = correlation_id
        return 200, response, correlation_id

    try:
        if path == "/v1/decisions/underwriting":
            response = decide_underwriting(payload, correlation_id)
        elif path == "/v1/decisions/claims":
            response = decide_claim(payload, correlation_id)
        else:
            return 404, problem(404, "NOT_FOUND", "Endpoint not found", correlation_id), correlation_id
    except (TypeError, ValueError, KeyError) as exc:
        return 400, problem(400, "INVALID_REQUEST", "Invalid payload", correlation_id, str(exc)), correlation_id

    IDEMPOTENCY_STORE[idem_key] = (payload_hash, dict(response))
    return 200, response, correlation_id


class Handler(BaseHTTPRequestHandler):
    server_version = "MayaInsuranceDecisionAPI/0.2"

    def _write(self, status: int, body: dict[str, Any], correlation_id: str, content_type: str = "application/json") -> None:
        raw = json.dumps(body, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("X-Correlation-Id", correlation_id)
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self) -> None:
        correlation_id = self.headers.get("X-Correlation-Id") or f"COR-{uuid.uuid4()}"
        if self.path == "/health/live":
            self._write(200, {"status": "UP"}, correlation_id)
        elif self.path == "/health/ready":
            self._write(200, {"status": "READY", "mode": os.getenv("DECISION_MODE", "portable")}, correlation_id)
        else:
            self._write(404, problem(404, "NOT_FOUND", "Endpoint not found", correlation_id), correlation_id, "application/problem+json")

    def do_POST(self) -> None:
        correlation_id = self.headers.get("X-Correlation-Id") or f"COR-{uuid.uuid4()}"
        try:
            size = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(size) or b"{}")
        except (ValueError, json.JSONDecodeError):
            self._write(400, problem(400, "INVALID_REQUEST", "Invalid JSON", correlation_id), correlation_id, "application/problem+json")
            return

        headers = {
            "Authorization": self.headers.get("Authorization", ""),
            "Idempotency-Key": self.headers.get("Idempotency-Key", ""),
            "X-Correlation-Id": correlation_id,
        }
        status, body, cid = process_decision(self.path, payload, headers)
        ctype = "application/json" if status < 400 else "application/problem+json"
        self._write(status, body, cid, ctype)

    def log_message(self, fmt: str, *args: Any) -> None:
        return


def main() -> None:
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8080"))
    server = ThreadingHTTPServer((host, port), Handler)
    print(f"MayaInsurance Decision API reference listening on http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    main()
