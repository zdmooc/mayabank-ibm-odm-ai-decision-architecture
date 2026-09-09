# Itération 10 — OpenShift Local / CRC

## Statut

**TERMINÉE — déploiement CRC, rollout, probes, E2E et régression embarquée réellement validés avec `RESULT=PASS`.**

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
- `scripts/local-crc/verify.sh` ;
- `evidence/iteration-10/verification-summary.md`.

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
- NetworkPolicy ingress default-deny ;
- egress restreint spécifiquement pour le pod applicatif.

## Build

Le lab utilise un `BuildConfig` à source binaire :

```bash
oc start-build decision-api --from-dir=. --follow --wait -n mayainsurance-decision-local
```

Cela évite d'imposer Docker ou Podman sur le poste.

Le script de déploiement supprime temporairement l'ancien `default-deny` avant un rebuild afin de ne pas bloquer les pods OpenShift de build, puis réapplique les policies runtime et force un `rollout restart` pour charger la nouvelle image.

## Exécution validée

Depuis la racine du dépôt :

```bash
bash scripts/local-crc/deploy.sh
bash scripts/local-crc/verify.sh
```

Validation réelle obtenue le **2026-09-09** sur OpenShift Server **4.22.7** :

```text
Build decision-api-4: Complete
Deployment rollout: successful
/health/live: UP
/health/ready: READY
Decision E2E: ACCEPT
E2E_ASSERTIONS=PASS
Ran 25 tests
OK
RESULT=PASS
```

La preuve locale produite par le script :

`evidence/iteration-10/verify-20260909-140228.txt`

Le résumé versionné est disponible dans :

`evidence/iteration-10/verification-summary.md`

## IBM ODM réel

Le runtime IBM ODM n'est volontairement pas inclus dans le dépôt public. Voir `deploy/openshift/IBM_ODM_RUNTIME.md`.

La validation CRC prouve l'exécution de l'architecture portable et du contrat de décision. Elle ne prétend pas prouver l'exécution d'un runtime IBM ODM licencié.

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
- [x] rollout réellement validé sur CRC ;
- [x] test E2E réellement vert sur CRC ;
- [x] 25 tests portables exécutés dans le pod avec `OK` ;
- [x] preuve locale générée et résumé versionné.

## Prochaine étape

**Itération 11 — Azure AKS / ARO : cible cloud, IaC, registry, identité, réseau, secrets, parité fonctionnelle avec CRC et maîtrise des coûts.**
