#!/usr/bin/env python3
from __future__ import annotations

import json
import urllib.error
import urllib.request

URL = "http://127.0.0.1:8080/v1/decisions/underwriting"
PAYLOAD = {
    "requestId": "REQ-DEMO-001",
    "applicantAge": 35,
    "productType": "AUTO",
    "drivingLicenseYears": 10,
    "recentClaims": 0,
    "incompleteFile": False,
    "declaredRiskLevel": "LOW",
}


def call() -> None:
    raw = json.dumps(PAYLOAD).encode("utf-8")
    request = urllib.request.Request(
        URL,
        data=raw,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer synthetic-token",
            "Idempotency-Key": "demo-idem-0001",
            "X-Correlation-Id": "COR-DEMO-001",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=2.0) as response:
            print(response.status)
            print(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        print(exc.code)
        print(exc.read().decode("utf-8"))


if __name__ == "__main__":
    call()
