# Roadmap — IBM ODM & AI Decision Architecture

## Objectif global

Construire progressivement une architecture de décision IARD moderne, gouvernée et explicable, combinant IBM ODM, ML, GenAI, API, événements et OpenShift.

## Itérations

### Itération 0 — Cadrage et gouvernance
Statut : **TERMINÉE**

- définir le positionnement Architecte Solution ;
- définir le domaine fictif MayaInsurance IARD ;
- fixer les règles d’anonymisation ;
- distinguer règle / ML / GenAI / humain ;
- définir les NFR et principes d’architecture ;
- créer la roadmap.

### Itération 1 — Fondamentaux ODM
- Decision Center / Decision Server / Rule Designer ;
- XOM, BOM, vocabulaire, BAL ;
- Decision Table, Ruleflow, RuleApp, Ruleset ;
- premier Decision Service IARD.

### Itération 2 — Modèle métier IARD
- bounded contexts utiles ;
- underwriting, pricing, claim, fraud ;
- dictionnaire métier ;
- modèle de décision et traçabilité.

### Itération 3 — Souscription & éligibilité
- règles d’éligibilité ;
- tarification simple ;
- exceptions ;
- tests unitaires et scénarios métier.

### Itération 4 — Sinistre & fraude
- règles de couverture ;
- franchise ;
- score fraude ;
- human review.

### Itération 5 — API & intégration
- REST/OpenAPI ;
- idempotence ;
- timeouts/retries ;
- sécurité OAuth2/OIDC/mTLS.

### Itération 6 — Event-Driven
- événements de décision ;
- Kafka/AsyncAPI ;
- audit et corrélation.

### Itération 7 — ML dans la décision
- score de risque/fraude ;
- seuils ;
- gouvernance de version de modèle ;
- fallback sans ML.

### Itération 8 — GenAI documentaire
- extraction de pièces ;
- structuration des informations ;
- confidence gating ;
- passage à ODM pour décision gouvernée.

### Itération 9 — MCP & Agents
- Decision Services comme outils ;
- agent contrôlé ;
- permissions, audit, garde-fous ;
- aucune décision sensible laissée au LLM seul.

### Itération 10 — OpenShift
- déploiement ;
- configuration ;
- secrets ;
- NetworkPolicy ;
- quotas ;
- probes ;
- scaling.

### Itération 11 — GitOps / CI-CD
- promotion multi-environnements ;
- versioning règles/code ;
- rollback ;
- quality gates.

### Itération 12 — Observabilité & audit
- métriques ;
- traces ;
- décision ID ;
- rule/model version ;
- SLI/SLO.

### Itération 13 — HA / PRA / sécurité
- RTO/RPO ;
- topologie cible ;
- sauvegarde/reprise ;
- tests de panne.

### Itération 14 — Soutenance Architecte Solution
- HLD ;
- ADR ;
- risques ;
- arbitrages ;
- scénario entretien banque/assurance.
