# Itération 10 — OpenShift Local / CRC

## Statut

**PRÊTE POUR EXÉCUTION LOCALE — artefacts de build/déploiement/validation livrés ; preuve CRC encore requise avant `DONE`.**

## Objectif

Déployer sur OpenShift Local / CRC la façade Decision API portable construite aux itérations précédentes et vérifier un parcours IARD E2E reproductible.

```text
Git repository
    ↓ binary build
OpenShift BuildConfig
    ↓
ImageStream decision-api:latest
    ↓
Deployment decision-api
    ↓
Service
    ↓
Route TLS edge
    ↓
POST /v1/decisions/underwriting
    ↓
ACCEPT / REJECT / REVIEW
```

## Ressources livrées

- `Dockerfile` ;
- `deploy/openshift/00-platform.yaml` ;
- `deploy/openshift/10-workload.yaml` ;
- `deploy/openshift/IBM_ODM_RUNTIME.md` ;
- `scripts/local-crc/deploy.sh` ;
- `scripts/local-crc/verify.sh`.

## Sécurité / exploitation du lab

- namespace dédié `mayainsurance-decision-local` ;
- ServiceAccount dédié ;
- ResourceQuota ;
- LimitRange ;
- requests/limits ;
- container non-root ;
- seccomp `RuntimeDefault` ;
- capabilities Linux supprimées ;
- ConfigMap ;
- Secret local non versionné en clair dans les manifests ;
- readiness/liveness probes ;
- Route TLS edge ;
- NetworkPolicy default-deny + règles minimales.

## Build

Le lab utilise un `BuildConfig` à source binaire. Le contenu du clone local courant est envoyé au cluster :

```bash
oc start-build decision-api --from-dir=. --follow --wait -n mayainsurance-decision-local
```

Cela évite d'imposer Docker ou Podman sur le poste.

## Exécution

Depuis la racine du dépôt :

```bash
bash scripts/local-crc/deploy.sh
bash scripts/local-crc/verify.sh
```

Optionnel :

```bash
export LAB_BEARER_TOKEN='un-token-local-different'
bash scripts/local-crc/deploy.sh
bash scripts/local-crc/verify.sh
```

## Ce que `verify.sh` contrôle

- connexion `oc` ;
- ressources Kubernetes/OpenShift ;
- rollout du Deployment ;
- build ;
- Route ;
- `/health/live` ;
- `/health/ready` ;
- décision Underwriting E2E ;
- `decision=ACCEPT` attendu ;
- propagation du `correlationId` ;
- tests portables API/Event/ML/GenAI/MCP exécutés dans le pod.

Une preuve est écrite dans :

`evidence/iteration-10/verify-<timestamp>.txt`

## IBM ODM réel

Le runtime IBM ODM n'est volontairement pas inclus dans le dépôt public. Voir `deploy/openshift/IBM_ODM_RUNTIME.md`.

Le lab CRC de cette itération valide l'architecture portable et le contrat de décision. Un futur overlay privé/licencié pourra substituer un adapter ODM réel.

## Critères de sortie

- [x] namespace/projet défini ;
- [x] BuildConfig/ImageStream ;
- [x] Deployment / Service / Route ;
- [x] ConfigMap / Secret pattern ;
- [x] requests / limits / quota / LimitRange ;
- [x] NetworkPolicy ;
- [x] probes ;
- [x] script de déploiement ;
- [x] script de validation automatisé ;
- [ ] rollout réellement validé sur le CRC de l'utilisateur ;
- [ ] test E2E réellement vert sur CRC ;
- [ ] preuve `evidence/iteration-10/...` conservée.

## Gate

**Ne pas marquer I10 `DONE` avant obtention de la preuve CRC.**
