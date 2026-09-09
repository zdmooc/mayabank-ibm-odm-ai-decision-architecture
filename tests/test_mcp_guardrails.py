import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
import sys
sys.path.insert(0, str(ROOT))

from mcp.decision_mcp_server import ToolError, call_tool, tool_catalog


class McpGuardrailTests(unittest.TestCase):
    def test_catalog_has_only_expected_tools(self):
        names = {item["name"] for item in tool_catalog()}
        self.assertEqual(
            names,
            {"underwriting_decision", "claim_decision", "decision_audit_lookup"},
        )

    def test_underwriting_scope_allows_call(self):
        result = call_tool(
            "underwriting_decision",
            {"requestId": "REQ-T1", "applicantAge": 34, "declaredRiskLevel": "LOW"},
            {"decision:underwriting"},
            "TC-T1",
            "CORR-T1",
        )
        self.assertEqual(result["result"]["decision"], "ACCEPT")
        self.assertFalse(result["agentMayOverride"])

    def test_wrong_scope_is_forbidden(self):
        with self.assertRaises(ToolError) as ctx:
            call_tool(
                "claim_decision",
                {"claimId": "CLM-T2", "policyActive": True, "coveredEvent": True, "fraudRisk": 0.1},
                {"decision:underwriting"},
                "TC-T2",
                "CORR-T2",
            )
        self.assertEqual(ctx.exception.code, "FORBIDDEN")

    def test_review_stays_human_review(self):
        result = call_tool(
            "claim_decision",
            {"claimId": "CLM-T3", "policyActive": True, "coveredEvent": True, "fraudRisk": 0.9},
            {"decision:claim"},
            "TC-T3",
            "CORR-T3",
        )
        self.assertEqual(result["result"]["decision"], "REVIEW")
        self.assertTrue(result["result"]["humanReviewRequired"])
        self.assertFalse(result["agentMayOverride"])

    def test_unknown_tool_rejected(self):
        with self.assertRaises(ToolError) as ctx:
            call_tool(
                "override_rule",
                {},
                {"decision:underwriting", "decision:claim"},
                "TC-T4",
                "CORR-T4",
            )
        self.assertEqual(ctx.exception.code, "TOOL_NOT_FOUND")

    def test_meta_required(self):
        with self.assertRaises(ToolError) as ctx:
            call_tool(
                "decision_audit_lookup",
                {"decisionId": "DEC-T5"},
                {"decision:audit.read"},
                "",
                "CORR-T5",
            )
        self.assertEqual(ctx.exception.code, "INVALID_TOOL_CALL")


if __name__ == "__main__":
    unittest.main()
