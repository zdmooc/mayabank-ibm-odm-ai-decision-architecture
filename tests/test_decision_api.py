import importlib.util
import os
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("decision_api", ROOT / "api" / "reference_decision_api.py")
MOD = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(MOD)


class DecisionApiTests(unittest.TestCase):
    def setUp(self):
        MOD.IDEMPOTENCY_STORE.clear()
        bearer_token = os.getenv("LAB_BEARER_TOKEN", "synthetic-token")
        self.headers = {
            "Authorization": f"Bearer {bearer_token}",
            "Idempotency-Key": "idem-key-0001",
            "X-Correlation-Id": "COR-TEST-001",
        }
        self.underwriting = {
            "requestId": "REQ-001",
            "applicantAge": 35,
            "productType": "AUTO",
            "drivingLicenseYears": 10,
            "recentClaims": 0,
            "incompleteFile": False,
            "declaredRiskLevel": "LOW",
        }

    def test_underwriting_accept(self):
        status, body, _ = MOD.process_decision("/v1/decisions/underwriting", self.underwriting, self.headers)
        self.assertEqual(200, status)
        self.assertEqual("ACCEPT", body["decision"])
        self.assertEqual("COR-TEST-001", body["correlationId"])

    def test_idempotent_replay_keeps_decision_id(self):
        status1, body1, _ = MOD.process_decision("/v1/decisions/underwriting", self.underwriting, self.headers)
        status2, body2, _ = MOD.process_decision("/v1/decisions/underwriting", self.underwriting, self.headers)
        self.assertEqual(200, status1)
        self.assertEqual(200, status2)
        self.assertEqual(body1["decisionId"], body2["decisionId"])

    def test_idempotency_conflict(self):
        MOD.process_decision("/v1/decisions/underwriting", self.underwriting, self.headers)
        modified = dict(self.underwriting)
        modified["applicantAge"] = 17
        status, body, _ = MOD.process_decision("/v1/decisions/underwriting", modified, self.headers)
        self.assertEqual(409, status)
        self.assertEqual("IDEMPOTENCY_CONFLICT", body["code"])

    def test_missing_bearer_token(self):
        headers = dict(self.headers)
        headers["Authorization"] = ""
        status, body, _ = MOD.process_decision("/v1/decisions/underwriting", self.underwriting, headers)
        self.assertEqual(401, status)
        self.assertEqual("UNAUTHORIZED", body["code"])

    def test_claim_high_fraud_requires_human_review(self):
        headers = dict(self.headers)
        headers["Idempotency-Key"] = "idem-key-claim-1"
        claim = {
            "claimId": "CLM-001",
            "policyActive": True,
            "coveragePresent": True,
            "eventCovered": True,
            "claimedAmount": 1500.0,
            "deductible": 200.0,
            "fraudScore": 0.91,
        }
        status, body, _ = MOD.process_decision("/v1/decisions/claims", claim, headers)
        self.assertEqual(200, status)
        self.assertEqual("REVIEW", body["decision"])
        self.assertTrue(body["humanReviewRequired"])
        self.assertIn("FRAUD_HIGH_SCORE", body["reasonCodes"])


if __name__ == "__main__":
    unittest.main()
