import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "genai" / "document-extraction" / "extractor.py"
spec = importlib.util.spec_from_file_location("extractor", MODULE)
extractor = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(extractor)


class GenAIDocumentExtractionTests(unittest.TestCase):
    def test_expected_next_steps(self):
        results = extractor.run()
        self.assertEqual([r["nextStep"] for r in results], [
            "FORWARD_TO_ODM", "HUMAN_REVIEW", "HUMAN_REVIEW", "HUMAN_REVIEW"
        ])
        for row in results:
            self.assertEqual(row["nextStep"], row["expectedNextStep"])

    def test_low_confidence_is_review(self):
        row = extractor.run()[1]
        self.assertIn("GENAI_LOW_CONFIDENCE", row["reasonCodes"])

    def test_invalid_schema_is_review(self):
        row = extractor.run()[2]
        self.assertIn("INVALID_CLAIMED_AMOUNT", row["reasonCodes"])

    def test_provider_unavailable_is_review(self):
        row = extractor.run()[3]
        self.assertIn("GENAI_PROVIDER_UNAVAILABLE", row["reasonCodes"])

    def test_genai_never_returns_business_decision(self):
        for row in extractor.run():
            self.assertIsNone(row["businessDecision"])
            self.assertNotIn(row["nextStep"], {"ACCEPT", "REJECT", "PAY"})


if __name__ == "__main__":
    unittest.main()
