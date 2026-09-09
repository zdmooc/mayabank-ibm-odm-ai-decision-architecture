#!/usr/bin/env python3
"""Portable MCP-like Decision tool server for governance tests.

This module validates tool catalog, scopes, payloads and audit semantics.
It is intentionally transport-neutral and does not claim to be a full MCP network server.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = ROOT / "mcp" / "tool-policy.json"


@dataclass
class ToolError(Exception):
    code: str
    message: str

    def to_dict(self) -> dict[str, Any]:
        return {"ok": False, "error": {"code": self.code, "message": self.message}}


def load_policy() -> dict[str, Any]:
    return json.loads(POLICY_PATH.read_text(encoding="utf-8"))


def tool_catalog() -> list[dict[str, Any]]:
    return [
        {
            "name": "underwriting_decision",
            "description": "Evaluate a synthetic IARD underwriting request through governed decision policy.",
            "inputSchema": {
                "type": "object",
                "required": ["requestId", "applicantAge", "declaredRiskLevel"],
            },
        },
        {
            "name": "claim_decision",
            "description": "Evaluate a synthetic IARD claim decision without bypassing human review.",
            "inputSchema": {
                "type": "object",
                "required": ["claimId", "policyActive", "coveredEvent", "fraudRisk"],
            },
        },
        {
            "name": "decision_audit_lookup",
            "description": "Read a synthetic decision audit record.",
            "inputSchema": {"type": "object", "required": ["decisionId"]},
        },
    ]


def _authorize(tool: str, granted_scopes: set[str], policy: dict[str, Any]) -> None:
    spec = policy["tools"].get(tool)
    if not spec:
        raise ToolError("TOOL_NOT_FOUND", f"Unknown tool: {tool}")
    required = set(spec.get("requiredScopes", []))
    missing = sorted(required - granted_scopes)
    if missing:
        raise ToolError("FORBIDDEN", f"Missing scopes: {','.join(missing)}")


def _validate_meta(tool_call_id: str, correlation_id: str) -> None:
    if not tool_call_id.strip():
        raise ToolError("INVALID_TOOL_CALL", "toolCallId is required")
    if not correlation_id.strip():
        raise ToolError("INVALID_TOOL_CALL", "correlationId is required")


def _underwriting(payload: dict[str, Any]) -> dict[str, Any]:
    required = {"requestId", "applicantAge", "declaredRiskLevel"}
    if not required.issubset(payload):
        raise ToolError("INVALID_ARGUMENTS", "Missing underwriting fields")
    if int(payload["applicantAge"]) < 18:
        decision, reason = "REJECT", "APPLICANT_UNDER_18"
    elif payload["declaredRiskLevel"] == "HIGH":
        decision, reason = "REVIEW", "HIGH_DECLARED_RISK"
    else:
        decision, reason = "ACCEPT", "ELIGIBLE_STANDARD"
    return {
        "decision": decision,
        "reasonCodes": [reason],
        "humanReviewRequired": decision == "REVIEW",
        "decisionSource": "governed-policy-portable-v1",
    }


def _claim(payload: dict[str, Any]) -> dict[str, Any]:
    required = {"claimId", "policyActive", "coveredEvent", "fraudRisk"}
    if not required.issubset(payload):
        raise ToolError("INVALID_ARGUMENTS", "Missing claim fields")
    if not bool(payload["policyActive"]) or not bool(payload["coveredEvent"]):
        return {
            "decision": "REJECT",
            "reasonCodes": ["NOT_COVERED"],
            "humanReviewRequired": False,
            "decisionSource": "governed-policy-portable-v1",
        }
    if float(payload["fraudRisk"]) >= 0.55:
        return {
            "decision": "REVIEW",
            "reasonCodes": ["FRAUD_SIGNAL_REVIEW"],
            "humanReviewRequired": True,
            "decisionSource": "governed-policy-portable-v1",
        }
    return {
        "decision": "PAY",
        "reasonCodes": ["COVERED_STANDARD"],
        "humanReviewRequired": False,
        "decisionSource": "governed-policy-portable-v1",
    }


def _audit_lookup(payload: dict[str, Any]) -> dict[str, Any]:
    if "decisionId" not in payload:
        raise ToolError("INVALID_ARGUMENTS", "decisionId is required")
    return {
        "decisionId": payload["decisionId"],
        "status": "SYNTHETIC_AUDIT_RECORD",
        "readOnly": True,
    }


def call_tool(
    tool: str,
    payload: dict[str, Any],
    granted_scopes: set[str],
    tool_call_id: str,
    correlation_id: str,
) -> dict[str, Any]:
    policy = load_policy()
    _validate_meta(tool_call_id, correlation_id)
    _authorize(tool, granted_scopes, policy)

    if tool == "underwriting_decision":
        result = _underwriting(payload)
    elif tool == "claim_decision":
        result = _claim(payload)
    elif tool == "decision_audit_lookup":
        result = _audit_lookup(payload)
    else:
        raise ToolError("TOOL_NOT_FOUND", tool)

    return {
        "ok": True,
        "tool": tool,
        "toolCallId": tool_call_id,
        "correlationId": correlation_id,
        "result": result,
        "agentMayOverride": False,
        "auditRequired": True,
    }


def demo() -> list[dict[str, Any]]:
    cases = [
        (
            "underwriting_decision",
            {"requestId": "REQ-9001", "applicantAge": 42, "declaredRiskLevel": "LOW"},
            {"decision:underwriting"},
        ),
        (
            "claim_decision",
            {"claimId": "CLM-9002", "policyActive": True, "coveredEvent": True, "fraudRisk": 0.82},
            {"decision:claim"},
        ),
    ]
    out = []
    for i, (tool, payload, scopes) in enumerate(cases, start=1):
        out.append(call_tool(tool, payload, scopes, f"TC-{i}", "CORR-I9"))
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--list-tools", action="store_true")
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()
    if args.list_tools:
        print(json.dumps(tool_catalog(), indent=2, ensure_ascii=False))
    elif args.demo:
        print(json.dumps(demo(), indent=2, ensure_ascii=False))
    else:
        parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
