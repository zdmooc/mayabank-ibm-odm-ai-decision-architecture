# Roadmap — IBM ODM & AI Decision Architecture

## Objectif global

Construire progressivement une architecture de décision IARD moderne, gouvernée et explicable, combinant IBM ODM, ML, GenAI, API, événements et une trajectoire de déploiement **OpenShift Local / CRC -> Azure**.

## Stratégie de déploiement transverse

- **OpenShift Local / CRC** : cible prioritaire des labs et validations locales.
- **Azure AKS** : cible cloud Kubernetes de référence.
- **Azure Red Hat OpenShift (ARO)** : option entreprise lorsque le besoin impose OpenShift managé sur Azure.
- Même logique métier, mêmes contrats API et mêmes Decision Services sur toutes les cibles.
- Différences de plateforme gérées par manifests, Helm/Kustomize, overlays, secrets et IaC.

## Itérations

### Itération 0 — Cadrage et gouvernance — TERMINÉE
- positionnement Architecte Solution ; domaine fictif ; anonymisation ; NFR ; stratégie CRC -> Azure.

### Itération 1 — Fondamentaux ODM — TERMINÉE
- Decision Center / Decision Server / Rule Designer ; XOM/BOM/BAL ; Decision Table ; Ruleflow ; premier Decision Service.

### Itération 2 — Modèle métier IARD / DDD — TERMINÉE
- bounded contexts Underwriting/Pricing/Claim/Fraud ; context map ; ubiquitous language ; décisions/événements ; vue C4.

### Itération 3 — Souscription & éligibilité — TERMINÉE
- éligibilité ; tarification ; garanties/exclusions/franchises ; tests de non-régression.

### Itération 4 — Sinistre & fraude — TERMINÉE
- couverture ; franchise ; score fraude simulé ; human review ; audit/versioning.

### Itération 5 — API & intégration — TERMINÉE
- Decision API REST ; OpenAPI 3.1 ; idempotence ; correlation ID ; erreurs ; OAuth2/OIDC ; mTLS cible.

### Itération 6 — Event-Driven — TERMINÉE
- DecisionRequested / DecisionCompleted / ReviewRequired ; AsyncAPI 3.1 ; Kafka-compatible ; audit ; replay maîtrisé.

### Itération 7 — ML dans la décision — TERMINÉE
- score risque/fraude ; `modelVersion` ; `confidenceScore` ; fallback ; politique ODM consommant le score ; tests sur seuils ; aucun rejet automatique par ML seul.

### Itération 8 — GenAI documentaire
- extraction de pièces ;
- structuration JSON ;
- validation de schéma ;
- confidence gating ;
- human review si confiance faible ;
- passage à ODM pour décision gouvernée.

### Itération 9 — MCP & Agents
- Decision Services comme outils ; agent contrôlé ; permissions ; audit ; garde-fous.

### Itération 10 — Déploiement OpenShift Local / CRC
- namespace ; workloads ODM/services ; Services/Routes ; ConfigMaps/Secrets ; NetworkPolicy ; quotas/requests/limits ; probes ; E2E local.

### Itération 11 — Azure
- AKS ; ARO alternatif ; registry ; identité ; réseau ; secrets ; observabilité ; IaC ; parité fonctionnelle.

### Itération 12 — GitOps / CI-CD
- promotion multi-environnements ; versioning règles/code ; overlays ; rollback ; quality gates.

### Itération 13 — Observabilité & audit
- métriques ; traces ; decision ID ; rule/model version ; SLI/SLO.

### Itération 14 — HA / PRA / sécurité
- RTO/RPO ; topologie ; sauvegarde/reprise ; tests de panne ; IAM/RBAC ; différences lab/cible entreprise.

### Itération 15 — Soutenance Architecte Solution
- HLD ; ADR ; risques ; arbitrages ; comparaison CRC/AKS/ARO ; scénario entretien.
