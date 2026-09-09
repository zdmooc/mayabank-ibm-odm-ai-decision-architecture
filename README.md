# MayaBank IBM ODM & AI Decision Architecture

Référentiel d’architecture et laboratoire pédagogique pour concevoir une plateforme de **Decision Management & AI appliquée à l’assurance IARD**, dans un contexte entièrement fictif et anonymisé.

## Positionnement

**Architecte Solution — IBM ODM / Decision Management / AI — Assurance IARD**

Le dépôt relie :

```text
Besoin métier IARD
  -> DDD / bounded contexts
  -> IBM ODM / règles déterministes
  -> ML / scoring
  -> GenAI documentaire
  -> Decision API
  -> Event-Driven
  -> MCP / agents gouvernés
  -> OpenShift / Azure
  -> sécurité / observabilité / HA-PRA / GitOps
```

## Principe architectural

**Le ML prédit, le GenAI extrait, IBM ODM applique la politique métier, MCP expose les capacités comme tools, l’agent orchestre uniquement ce qu’il est autorisé à appeler, et l’humain conserve les décisions sensibles.**

## Cas d’usage fil rouge

Plateforme fictive **MayaInsurance IARD** : souscription, tarification, garanties, sinistre, fraude, extraction documentaire, audit et human review.

## Modules livrés

### I1–I4 — Decision Management IARD

XOM/BOM/BAL, Decision Tables/Ruleflows, DDD Underwriting/Pricing/Claim/Fraud, tarification, couverture, franchise, fraude synthétique et audit.

### I5 — Decision API

REST/OpenAPI 3.1, idempotence, correlation ID, erreurs normalisées, OAuth2/OIDC et mTLS cible.

### I6 — Event-Driven

`DecisionRequested`, `DecisionCompleted`, `ReviewRequired`, AsyncAPI 3.1, Kafka-compatible/Redpanda et replay d’audit sans ré-exécution métier automatique.

### I7 — ML dans la décision

`riskScore`, `confidenceScore`, `modelVersion`, fallback et policy ODM consommant le score. Aucun score ML ne produit un rejet automatique.

### I8 — GenAI documentaire

JSON Schema, prompt contract, extraction synthétique, confidence gating, fallback provider et `FORWARD_TO_ODM` uniquement après validation. Le GenAI ne produit jamais une décision métier finale.

### I9 — MCP & Agentic AI

Tools gouvernés :

- `underwriting_decision` — scope `decision:underwriting` ;
- `claim_decision` — scope `decision:claim` ;
- `decision_audit_lookup` — scope `decision:audit.read`.

Le lab cible MCP `2026-07-28`. Aucun tool d’override, paiement ou déploiement automatique n’est exposé.

## I10 — OpenShift Local / CRC — TERMINÉE

Validation réellement exécutée sur **OpenShift Local / CRC 4.22.7**.

Artefacts :

- `Dockerfile` UBI Python ;
- `BuildConfig` binaire + `ImageStream` ;
- namespace / ServiceAccount ;
- ResourceQuota / LimitRange ;
- ConfigMap / Secret pattern ;
- Deployment / Service / Route TLS ;
- requests/limits ;
- liveness/readiness probes ;
- NetworkPolicy ingress default-deny + egress applicatif restreint ;
- scripts `deploy.sh` / `verify.sh` ;
- preuve versionnée.

Résultat réel :

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

Voir `evidence/iteration-10/verification-summary.md`.

### IBM ODM réel

Le runtime IBM ODM licencié n’est pas embarqué dans le dépôt public. La stratégie d’intégration est documentée dans `deploy/openshift/IBM_ODM_RUNTIME.md`. La preuve I10 concerne la façade portable et ne revendique pas l’exécution d’un runtime ODM licencié.

## Stratégie de déploiement

1. **OpenShift Local / CRC** — validé en I10.
2. **Azure AKS** — cible cloud Kubernetes de référence pour I11.
3. **ARO** — option entreprise si OpenShift managé sur Azure est requis.

Principe : **OpenShift Local d’abord, Azure ensuite**.

## Règles du dépôt

- aucune donnée, architecture interne ou artefact confidentiel d’une entreprise réelle ;
- scénarios fictifs MayaInsurance uniquement ;
- aucun binaire IBM propriétaire ou contenu décompilé ;
- distinguer architecture cible, POC, lab exécuté et hypothèse ;
- ne pas revendiquer un runtime IBM ODM, LLM, MCP ou OpenShift exécuté sans preuve ;
- aucune décision sensible abandonnée au ML, GenAI ou agent seul.

## État

- **I0 à I10 : TERMINÉES**
- **Prochaine : I11 — Azure AKS / ARO**

Voir `docs/iteration-10/README.md`, `docs/00-roadmap.md`, `docs/BACKLOG.md` et `evidence/iteration-10/verification-summary.md`.
