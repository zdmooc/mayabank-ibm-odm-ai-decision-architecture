# I10 — CRC Verification Summary

## Statut

**PASS — validation réellement exécutée sur OpenShift Local / CRC le 2026-09-09.**

## Environnement observé

- OpenShift Server : `4.22.7`
- Kubernetes Server : `v1.35.6`
- `oc` client : `4.19.3`
- utilisateur : `kubeadmin`
- namespace : `mayainsurance-decision-local`
- Route : `decision-api-mayainsurance-decision-local.apps-crc.testing`

## Preuves fonctionnelles

- Build `decision-api-4` : `Complete`
- Deployment `decision-api` : rollout réussi
- Pod applicatif : `1/1 Running`
- `/health/live` : `{"status":"UP"}`
- `/health/ready` : `{"status":"READY","mode":"portable"}`
- E2E Underwriting : `decision=ACCEPT`
- reason code : `ELIGIBLE_STANDARD`
- `correlationId=COR-I10-LOCAL`
- `E2E_ASSERTIONS=PASS`

## Régression embarquée

Suite exécutée dans le pod :

- Decision API
- Eventing
- ML Fraud
- GenAI document extraction
- MCP guardrails

Résultat :

```text
Ran 25 tests in 0.009s
OK
RESULT=PASS
```

## Evidence locale générée

Le script `scripts/local-crc/verify.sh` a généré :

`evidence/iteration-10/verify-20260909-140228.txt`

Le fichier ci-dessus existe dans le clone local ayant exécuté la validation. Ce résumé versionné conserve les résultats essentiels dans le dépôt public.

## Incident résolu pendant la validation

Un build intermédiaire (`decision-api-2`) a échoué car une NetworkPolicy namespace-wide `default-deny` bloquait également l'egress des pods de build OpenShift, notamment DNS, API server et `registry.access.redhat.com`.

Correction appliquée :

- le `default-deny` namespace est limité à l'Ingress ;
- l'egress reste restreint spécifiquement pour le pod `decision-api` ;
- `deploy.sh` supprime l'ancien policy avant le build puis réapplique la configuration corrigée ;
- `deploy.sh` force un `rollout restart` après un build réussi afin de charger la nouvelle image.

## Limite importante

Cette preuve valide la façade Decision API portable et son architecture OpenShift. Elle **ne constitue pas une preuve d'exécution d'un runtime IBM ODM licencié**. L'intégration ODM réelle reste séparée et documentée dans `deploy/openshift/IBM_ODM_RUNTIME.md`.
