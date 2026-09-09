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

## I10 — OpenShift Local / CRC

**Statut : PRÊTE POUR EXÉCUTION LOCALE — preuve CRC encore requise avant `DONE`.**

Artefacts :

- `Dockerfile` UBI Python ;
- `BuildConfig` binaire + `ImageStream` ;
- namespace / ServiceAccount ;
- ResourceQuota / LimitRange ;
- ConfigMap / Secret pattern ;
- Deployment / Service / Route TLS ;
- requests/limits ;
- probes ;
- NetworkPolicy default-deny ;
- validation E2E + tests portables exécutés dans le pod ;
- conservation automatique des preuves.

Depuis un clone à jour :

```bash
git pull
bash scripts/local-crc/deploy.sh
bash scripts/local-crc/verify.sh
```

Le résultat de `verify.sh` doit être conservé dans `evidence/iteration-10/` avant de marquer l’itération terminée.

### IBM ODM réel

Le runtime IBM ODM licencié n’est pas embarqué dans le dépôt public. La stratégie d’intégration est documentée dans `deploy/openshift/IBM_ODM_RUNTIME.md`. Le lab CRC actuel exécute la façade portable et conserve les contrats nécessaires au futur adapter ODM.

## Stratégie de déploiement

1. **OpenShift Local / CRC** — cible prioritaire des labs locaux.
2. **Azure AKS** — cible cloud Kubernetes de référence.
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

- **I0 à I9 : TERMINÉES**
- **I10 — OpenShift Local / CRC : PRÊTE À EXÉCUTER, validation locale requise**
- **I11 Azure : après validation I10**

Voir `docs/iteration-10/README.md`, `docs/00-roadmap.md` et `docs/BACKLOG.md`.
