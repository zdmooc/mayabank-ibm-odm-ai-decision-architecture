# Roadmap — IBM ODM & AI Decision Architecture

## Objectif global

Construire progressivement une architecture de décision IARD moderne, gouvernée et explicable, combinant IBM ODM, ML, GenAI, API, événements et une trajectoire de déploiement **OpenShift Local / CRC -> Azure**.

## Stratégie de déploiement transverse

- **OpenShift Local / CRC** : cible prioritaire des labs et validations locales.
- **Azure AKS** : cible cloud Kubernetes de référence.
- **Azure Red Hat OpenShift (ARO)** : option entreprise lorsque le besoin impose OpenShift managé sur Azure.
- Même logique métier, mêmes contrats API et mêmes Decision Services sur toutes les cibles.
- Différences de plateforme gérées par manifests, Helm/Kustomize, overlays, secrets et IaC.
- Aucun lab cloud coûteux ne reste déployé inutilement après validation.

## Itérations

### Itération 0 — Cadrage et gouvernance — TERMINÉE
- positionnement Architecte Solution ;
- domaine fictif MayaInsurance IARD ;
- anonymisation ;
- séparation règle / ML / GenAI / humain ;
- NFR ;
- stratégie CRC -> Azure.

### Itération 1 — Fondamentaux ODM — TERMINÉE
- Decision Center / Decision Server / Rule Designer ;
- XOM, BOM, vocabulaire, BAL ;
- Decision Table, Ruleflow, RuleApp, Ruleset ;
- premier Decision Service IARD.

### Itération 2 — Modèle métier IARD / DDD — TERMINÉE
- bounded contexts Underwriting, Pricing, Claim, Fraud ;
- agrégats et objets métier ;
- ubiquitous language ;
- context map ;
- décisions / événements ;
- vue C4 logique.

### Itération 3 — Souscription & éligibilité — TERMINÉE
- règles d’éligibilité ;
- tarification simple ;
- garanties / exclusions / franchises ;
- exceptions ;
- tests de non-régression.

### Itération 4 — Sinistre & fraude — TERMINÉE
- règles de couverture ;
- franchise ;
- score fraude simulé ;
- human review ;
- audit Decision ID + versions.

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

### Itération 10 — Déploiement OpenShift Local / CRC
- namespace/projet ;
- workloads ODM et services applicatifs ;
- Services / Routes ;
- ConfigMaps / Secrets ;
- NetworkPolicy ;
- quotas / requests / limits ;
- probes ;
- scaling ;
- validation E2E locale avec preuves.

### Itération 11 — Azure
- portage vers AKS ;
- ARO documenté comme alternative OpenShift managée ;
- registry, identité, réseau, secrets et observabilité Azure ;
- IaC et destruction contrôlée du lab ;
- test de parité fonctionnelle Local/CRC vs Azure.

### Itération 12 — GitOps / CI-CD
- promotion multi-environnements ;
- versioning règles/code ;
- overlays local/Azure ;
- rollback ;
- quality gates.

### Itération 13 — Observabilité & audit
- métriques ;
- traces ;
- décision ID ;
- rule/model version ;
- SLI/SLO.

### Itération 14 — HA / PRA / sécurité
- RTO/RPO ;
- topologie cible ;
- sauvegarde/reprise ;
- tests de panne ;
- différences entre lab local et cible entreprise.

### Itération 15 — Soutenance Architecte Solution
- HLD ;
- ADR ;
- risques ;
- arbitrages ;
- comparaison OpenShift Local / AKS / ARO ;
- scénario entretien banque/assurance.
