#!/usr/bin/env bash
set -euo pipefail

NS="${NS:-mayainsurance-decision-local}"
LAB_BEARER_TOKEN="${LAB_BEARER_TOKEN:-maya-local-lab-token}"

if ! command -v oc >/dev/null 2>&1; then
  echo "ERROR: oc introuvable dans PATH" >&2
  exit 1
fi

oc whoami >/dev/null

echo "[1/6] Platform resources"
oc apply -f deploy/openshift/00-platform.yaml

echo "[2/6] Local lab secret"
oc -n "$NS" create secret generic decision-api-secret \
  --from-literal=LAB_BEARER_TOKEN="$LAB_BEARER_TOKEN" \
  --dry-run=client -o yaml | oc apply -f -

echo "[3/6] Prepare build networking"
# On reruns, an existing namespace-wide default-deny egress policy would also
# select OpenShift build pods and block DNS, the API server and the external
# base-image registry. Remove that policy before the binary build; the corrected
# ingress-only default-deny is reapplied with runtime resources after the build.
oc -n "$NS" delete networkpolicy default-deny --ignore-not-found=true

echo "[4/6] Binary build from current repository"
oc -n "$NS" start-build decision-api --from-dir=. --follow --wait

echo "[5/6] Runtime resources"
oc apply -f deploy/openshift/10-workload.yaml

# The Deployment references the mutable :latest ImageStream tag. Re-applying the
# same manifest does not change the pod template, so explicitly restart the
# Deployment after each successful build to force a fresh image pull.
oc -n "$NS" rollout restart deployment/decision-api

echo "[6/6] Rollout"
oc -n "$NS" rollout status deployment/decision-api --timeout=180s

HOST="$(oc -n "$NS" get route decision-api -o jsonpath='{.spec.host}')"
echo "Decision API deployed: https://${HOST}"
echo "Next: bash scripts/local-crc/verify.sh"
