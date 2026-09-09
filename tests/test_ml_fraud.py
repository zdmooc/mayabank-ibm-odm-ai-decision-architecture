import csv
import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "ml" / "fraud" / "scorer.py"
SPEC = importlib.util.spec_from_file_location("fraud_scorer", MODULE_PATH)
SCORER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SCORER)


class FraudMLTests(unittest.TestCase):
    def test_expected_policy(self):
        model = SCORER.load_model()
        with (ROOT / "data" / "synthetic" / "ml-fraud-cases.csv").open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        for row in rows:
            result = SCORER.score_case(row, model)
            self.assertEqual(result["policyDecision"], row["expected_policy"], row["case_id"])

    def test_unavailable_model_falls_back_to_review(self):
        model = SCORER.load_model()
        row = {
            "case_id": "X",
            "claim_amount_eur": "1000",
            "recent_claims": "0",
            "late_reporting": "false",
            "document_inconsistency": "false",
            "model_available": "false",
        }
        result = SCORER.score_case(row, model)
        self.assertEqual(result["reasonCode"], "MODEL_UNAVAILABLE")
        self.assertEqual(result["policyDecision"], "REVIEW")

    def test_missing_feature_lowers_confidence(self):
        model = SCORER.load_model()
        row = {
            "case_id": "Y",
            "claim_amount_eur": "6000",
            "recent_claims": "",
            "late_reporting": "false",
            "document_inconsistency": "true",
            "model_available": "true",
        }
        result = SCORER.score_case(row, model)
        self.assertLess(result["confidenceScore"], 0.70)
        self.assertEqual(result["reasonCode"], "MODEL_LOW_CONFIDENCE")

    def test_ml_never_auto_rejects(self):
        for result in SCORER.evaluate_all():
            self.assertNotEqual(result["policyDecision"], "REJECT")


if __name__ == "__main__":
    unittest.main()
