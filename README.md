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

Plateforme fictive **MayaInsurance IARD** :

- souscription et éligibilité ;
- tarification ;
- garanties / exclusions / franchises ;
- sinistre et couverture ;
- fraude ;
- extraction documentaire ;
- audit ;
- human review.

## Modules livrés

### I1–I4 — Decision Management IARD

- XOM/BOM/BAL ;
- Decision Tables / Ruleflows ;
- DDD Underwriting/Pricing/Claim/Fraud ;
- tarification / couverture / franchise ;
- fraude synthétique ;
- Decision ID / audit.

### I5 — Decision API

- REST / OpenAPI 3.1 ;
- idempotence ;
- correlation ID ;
- erreurs normalisées ;
- OAuth2/OIDC et mTLS cible.

```bash
python -m unittest tests/test_decision_api.py
```

### I6 — Event-Driven

- `DecisionRequested` ;
- `DecisionCompleted` ;
- `ReviewRequired` ;
- AsyncAPI 3.1 ;
- Kafka-compatible / Redpanda ;
- replay d’audit sans ré-exécution métier automatique.

```bash
python -m unittest tests/test_eventing.py
```

### I7 — ML dans la décision

- `riskScore` ;
- `confidenceScore` ;
- `modelVersion` ;
- fallback ;
- policy ODM consommant le score.

Principe : **aucun score ML ne produit un rejet automatique.**

### I8 — GenAI documentaire

- JSON Schema ;
- prompt contract ;
- extraction synthétique ;
- confidence gating ;
- fallback provider ;
- `HUMAN_REVIEW` ;
- `FORWARD_TO_ODM` uniquement après validation.

Principe : **le GenAI ne produit jamais une décision métier finale.**

### I9 — MCP & Agentic AI

Le dépôt expose maintenant trois tools gouvernés :

- `underwriting_decision` — scope `decision:underwriting` ;
- `claim_decision` — scope `decision:claim` ;
- `decision_audit_lookup` — scope `decision:audit.read`.

Le lab cible **MCP 2026-07-28** avec une architecture stateless-compatible.

Garde-fous :

- scopes évalués côté serveur ;
- `toolCallId` + `correlationId` ;
- aucun tool d’override de règles ;
- aucun paiement / déploiement / clôture automatique ;
- `REVIEW` reste human-in-the-loop ;
- audit obligatoire.

```bash
python mcp/decision_mcp_server.py --list-tools
python mcp/decision_mcp_server.py --demo
python -m unittest tests/test_mcp_guardrails.py
```

Le serveur portable valide la sémantique et les politiques ; aucun serveur MCP de production n’est revendiqué comme exécuté.

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
- **Prochaine : Itération 10 — OpenShift Local / CRC**

Voir `docs/iteration-09/README.md`, `docs/00-roadmap.md` et `docs/BACKLOG.md`.
