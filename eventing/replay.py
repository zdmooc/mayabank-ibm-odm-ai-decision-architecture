#!/usr/bin/env python3
"""Portable audit replay for MayaInsurance decision events.

This module NEVER re-executes a business decision. It only validates and
reconstructs an audit projection from an event journal.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable

REQUIRED = {
    "eventId",
    "eventType",
    "schemaVersion",
    "occurredAt",
    "correlationId",
    "aggregateType",
    "aggregateId",
    "payload",
}


def load_events(path: Path) -> list[dict]:
    events: list[dict] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSON at line {line_no}: {exc}") from exc
    return events


def replay(events: Iterable[dict]) -> dict:
    seen: dict[str, dict] = {}
    requested_aggregates: set[tuple[str, str]] = set()
    completed_decisions: set[str] = set()
    projection: list[dict] = []

    for index, event in enumerate(events, start=1):
        missing = REQUIRED - event.keys()
        if missing:
            raise ValueError(f"Event #{index} missing fields: {sorted(missing)}")

        event_id = event["eventId"]
        if event_id in seen:
            raise ValueError(f"Duplicate eventId: {event_id}")

        causation_id = event.get("causationId")
        if causation_id:
            cause = seen.get(causation_id)
            if cause is None:
                raise ValueError(f"Unknown causationId {causation_id} for {event_id}")
            if cause["correlationId"] != event["correlationId"]:
                raise ValueError(f"Correlation mismatch between {causation_id} and {event_id}")

        aggregate_key = (event["aggregateType"], event["aggregateId"])
        event_type = event["eventType"]

        if event_type == "DecisionRequested":
            requested_aggregates.add(aggregate_key)
        elif event_type == "DecisionCompleted":
            if aggregate_key not in requested_aggregates:
                raise ValueError(
                    f"DecisionCompleted {event_id} has no prior DecisionRequested for {aggregate_key}"
                )
            decision_id = event.get("decisionId")
            if not decision_id:
                raise ValueError(f"DecisionCompleted {event_id} has no decisionId")
            completed_decisions.add(decision_id)
        elif event_type == "ReviewRequired":
            decision_id = event.get("decisionId")
            if not decision_id or decision_id not in completed_decisions:
                raise ValueError(f"ReviewRequired {event_id} has no prior completed decision")
        else:
            raise ValueError(f"Unsupported eventType: {event_type}")

        seen[event_id] = event
        projection.append(
            {
                "eventId": event_id,
                "eventType": event_type,
                "aggregateId": event["aggregateId"],
                "decisionId": event.get("decisionId"),
                "correlationId": event["correlationId"],
            }
        )

    return {
        "eventCount": len(projection),
        "uniqueEventCount": len(seen),
        "requestedAggregates": len(requested_aggregates),
        "completedDecisions": len(completed_decisions),
        "projection": projection,
        "businessDecisionReexecuted": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("journal", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    result = replay(load_events(args.journal))
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"Replay audit validation: OK ({result['eventCount']} events)")
        print(f"Completed decisions: {result['completedDecisions']}")
        print("Business decision re-executed: false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
