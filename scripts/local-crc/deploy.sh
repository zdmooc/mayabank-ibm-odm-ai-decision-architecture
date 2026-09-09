#!/usr/bin/env bash
set -euo pipefail

NS="${NS:-mayainsurance-decision-local}"
LAB_BEARER_TOKEN="${LAB_BEARER_TOKEN:-maya-local-lab-token}"

if ! command -v oc >/dev/null 2>&1; then
  echo "ERROR: oc introuvable dans PATH" >&2
  exit 1
fi

oc whoami >/dev/null

echo "[1/5] Platform resources"
oc apply -f deploy/openshift/00-platform.yaml

echo "[2/5] Local lab secret"
oc -n "$NS" create secret generic decision-api-secret \
  --from-literal=LAB_BEARER_TOKEN="$LAB_BEARER_TOKEN" \
  --dry-run=client -o yaml | oc apply -f -

echo "[3/5] Binary build from current repository"
oc -n "$NS" start-build decision-api --from-dir=. --follow --wait

echo "[4/5] Runtime resources"
oc apply -f deploy/openshift/10-workload.yaml

echo "[5/5] Rollout"
oc -n "$NS" rollout status deployment/decision-api --timeout=180s

HOST="$(oc -n "$NS" get route decision-api -o jsonpath='{.spec.host}')"
echo "Decision API deployed: https://${HOST}"
echo "Next: bash scripts/local-crc/verify.sh"
