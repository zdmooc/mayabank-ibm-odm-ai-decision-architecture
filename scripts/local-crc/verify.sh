#!/usr/bin/env bash
set -euo pipefail

NS="${NS:-mayainsurance-decision-local}"
LAB_BEARER_TOKEN="${LAB_BEARER_TOKEN:-maya-local-lab-token}"
STAMP="$(date +%Y%m%d-%H%M%S)"
EVIDENCE_DIR="evidence/iteration-10"
EVIDENCE_FILE="${EVIDENCE_DIR}/verify-${STAMP}.txt"
mkdir -p "$EVIDENCE_DIR"

exec > >(tee "$EVIDENCE_FILE") 2>&1

echo "=== MayaInsurance I10 CRC verification ==="
date -Iseconds || true

echo "\n[Cluster]"
oc version
oc whoami

echo "\n[Resources]"
oc -n "$NS" get pods,svc,route,quota,limitrange,networkpolicy

echo "\n[Deployment rollout]"
oc -n "$NS" rollout status deployment/decision-api --timeout=30s

echo "\n[Build]"
oc -n "$NS" get builds --sort-by=.metadata.creationTimestamp | tail -n 3

HOST="$(oc -n "$NS" get route decision-api -o jsonpath='{.spec.host}')"
BASE="https://${HOST}"

echo "\n[Health live]"
curl -ksS --fail "${BASE}/health/live"
echo

echo "\n[Health ready]"
curl -ksS --fail "${BASE}/health/ready"
echo

echo "\n[Decision E2E]"
RESPONSE="$(curl -ksS --fail \
  -X POST "${BASE}/v1/decisions/underwriting" \
  -H "Authorization: Bearer ${LAB_BEARER_TOKEN}" \
  -H "Idempotency-Key: i10-local-0001" \
  -H "X-Correlation-Id: COR-I10-LOCAL" \
  -H "Content-Type: application/json" \
  -d '{"requestId":"REQ-I10-1","applicantAge":42,"productType":"HOME","recentClaims":0,"incompleteFile":false,"declaredRiskLevel":"LOW"}')"
echo "$RESPONSE"

python - "$RESPONSE" <<'PY'
import json, sys
payload = json.loads(sys.argv[1])
assert payload["decision"] == "ACCEPT", payload
assert payload["correlationId"] == "COR-I10-LOCAL", payload
assert payload["decisionVersion"] == "iard-underwriting-v1", payload
print("E2E_ASSERTIONS=PASS")
PY

echo "\n[Portable regression tests inside pod]"
POD="$(oc -n "$NS" get pod -l app=decision-api -o jsonpath='{.items[0].metadata.name}')"
oc -n "$NS" exec "$POD" -- python -m unittest \
  tests/test_decision_api.py \
  tests/test_eventing.py \
  tests/test_ml_fraud.py \
  tests/test_genai_document_extraction.py \
  tests/test_mcp_guardrails.py

echo "\nRESULT=PASS"
echo "Evidence: ${EVIDENCE_FILE}"
