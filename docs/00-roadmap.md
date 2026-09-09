# Roadmap — IBM ODM & AI Decision Architecture

## Objectif global

Construire progressivement une architecture de décision IARD moderne, gouvernée et explicable, combinant IBM ODM, ML, GenAI, API, événements, MCP/agents et une trajectoire de déploiement **OpenShift Local / CRC -> Azure**.

## Stratégie de déploiement transverse

- **OpenShift Local / CRC** : cible prioritaire des labs et validations locales.
- **Azure AKS** : cible cloud Kubernetes de référence.
- **Azure Red Hat OpenShift (ARO)** : option entreprise lorsque le besoin impose OpenShift managé sur Azure.
- Même logique métier, mêmes contrats API et mêmes Decision Services sur toutes les cibles.
- Aucun lab n’est déclaré exécuté sans preuve reproductible.

## Itérations

### I0 — Cadrage et gouvernance — TERMINÉE
Positionnement, anonymisation, séparation règles/ML/GenAI/humain, NFR et stratégie CRC -> Azure.

### I1 — Fondamentaux ODM — TERMINÉE
Decision Center/Server/Rule Designer, XOM/BOM/BAL, Decision Table, Ruleflow, RuleApp, Ruleset et premier Decision Service.

### I2 — Modèle métier IARD / DDD — TERMINÉE
Bounded contexts, agrégats, ubiquitous language, context map, décisions/événements et vue C4 logique.

### I3 — Souscription & éligibilité — TERMINÉE
Éligibilité, tarification simple, garanties/exclusions/franchises et tests de non-régression.

### I4 — Sinistre & fraude — TERMINÉE
Couverture, franchise, score fraude simulé, human review et audit.

### I5 — API & intégration — TERMINÉE
Decision API REST, OpenAPI 3.1, idempotence, correlation ID, erreurs, OAuth2/OIDC et mTLS cible.

### I6 — Event-Driven — TERMINÉE
DecisionRequested/Completed/ReviewRequired, AsyncAPI 3.1, Kafka-compatible, correlation/causation IDs, audit et replay.

### I7 — ML dans la décision — TERMINÉE
Scoring fraude synthétique, `modelVersion`, `confidenceScore`, fallback et règles ODM consommant le score.

### I8 — GenAI documentaire — TERMINÉE
Extraction structurée, JSON Schema, prompt contract, confidence gating, fallback fournisseur et passage contrôlé vers ODM.

### I9 — MCP & Agentic AI — TERMINÉE
Cible MCP `2026-07-28`, tools Underwriting/Claim/Audit, scopes, serveur portable stateless-compatible, audit et garde-fous agentiques.

### I10 — OpenShift Local / CRC — PRÊTE POUR EXÉCUTION
- Dockerfile portable ;
- BuildConfig binaire + ImageStream ;
- namespace / ServiceAccount ;
- Deployment / Service / Route TLS ;
- ConfigMap / Secret pattern ;
- ResourceQuota / LimitRange ;
- requests / limits ;
- NetworkPolicy ;
- liveness/readiness probes ;
- scripts `deploy.sh` et `verify.sh` ;
- génération de preuve `evidence/iteration-10/` ;
- runtime IBM ODM licencié documenté comme intégration future séparée.

**Gate restant** : exécuter sur le CRC de l'utilisateur, obtenir rollout + E2E verts et conserver la preuve avant `DONE`.

### I11 — Azure
Ne démarre qu'après validation I10. Portage AKS, ARO comme alternative, registry/identité/réseau/secrets, IaC, parité CRC/Azure et destroy contrôlé.

### I12 — GitOps / CI-CD
Promotion multi-environnements, versioning règles/code, overlays local/Azure, rollback et quality gates.

### I13 — Observabilité & audit
Métriques, logs, traces, Decision ID, versions règles/modèles, SLI/SLO et dashboard.

### I14 — HA / PRA / sécurité
RTO/RPO, topologie, sauvegarde/reprise, tests de panne, IAM/RBAC et threat model.

### I15 — Soutenance Architecte Solution
HLD, ADR, risques, arbitrages, diagrammes finaux, démonstration et questions/réponses entretien.
