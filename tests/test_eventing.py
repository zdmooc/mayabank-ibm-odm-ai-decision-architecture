import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "eventing" / "replay.py"
SPEC = importlib.util.spec_from_file_location("event_replay", MODULE_PATH)
replay_module = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(replay_module)

JOURNAL = ROOT / "data" / "synthetic" / "decision-events.jsonl"


class EventReplayTests(unittest.TestCase):
    def setUp(self):
        self.events = replay_module.load_events(JOURNAL)

    def test_sample_replay_is_valid_and_non_executing(self):
        result = replay_module.replay(self.events)
        self.assertEqual(result["eventCount"], 5)
        self.assertEqual(result["completedDecisions"], 2)
        self.assertFalse(result["businessDecisionReexecuted"])

    def test_duplicate_event_is_rejected(self):
        events = self.events + [copy.deepcopy(self.events[0])]
        with self.assertRaisesRegex(ValueError, "Duplicate eventId"):
            replay_module.replay(events)

    def test_correlation_mismatch_is_rejected(self):
        events = copy.deepcopy(self.events)
        events[1]["correlationId"] = "OTHER"
        with self.assertRaisesRegex(ValueError, "Correlation mismatch"):
            replay_module.replay(events)

    def test_completed_without_requested_is_rejected(self):
        events = [copy.deepcopy(self.events[1])]
        events[0]["causationId"] = None
        with self.assertRaisesRegex(ValueError, "no prior DecisionRequested"):
            replay_module.replay(events)

    def test_review_without_completed_decision_is_rejected(self):
        event = copy.deepcopy(self.events[4])
        event["causationId"] = None
        with self.assertRaisesRegex(ValueError, "no prior completed decision"):
            replay_module.replay([event])


if __name__ == "__main__":
    unittest.main()
