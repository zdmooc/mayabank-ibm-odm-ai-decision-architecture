# Backlog — IBM ODM & AI Decision Architecture / Assurance IARD

## Objectif
Construire un POC démontrable d’architecture de décision IARD combinant IBM ODM, AI/ML, GenAI, API, événements, OpenShift Local/CRC puis Azure.

## Priorités
- **P0** : indispensable au fil rouge et à la démonstration.
- **P1** : industrialisation et intégration.
- **P2** : approfondissement expert / entretien.

## Backlog par itération

### I0 — Cadrage et gouvernance — DONE
- [x] Contexte fictif MayaInsurance IARD
- [x] Anonymisation et absence de données client
- [x] Séparation ODM / ML / GenAI / humain
- [x] Architecture logique initiale
- [x] Roadmap
- [x] Cible OpenShift Local/CRC puis Azure AKS/ARO

### I1 — Fondamentaux IBM ODM — P0
- [ ] Documenter Decision Center, Decision Server, Rule Designer
- [ ] Définir XOM, BOM, vocabulaire BAL
- [ ] Créer Decision Table et Ruleflow simples
- [ ] Créer un premier Decision Service IARD
- [ ] Ajouter exemples de requête/réponse
- [ ] Ajouter tests fonctionnels minimaux

**DoD** : un Decision Service simple est documenté, testable et versionné.

### I2 — DDD / modèle métier IARD — P0
- [ ] Définir bounded contexts utiles : Underwriting, Pricing, Claim, Fraud
- [ ] Définir agrégats et objets métier sans sur-découpage
- [ ] Créer dictionnaire métier
- [ ] Relier décisions, règles, événements et API
- [ ] Produire diagramme C4/ArchiMate logique

### I3 — Souscription & éligibilité — P0
- [ ] Règles d’éligibilité
- [ ] Tarification simple
- [ ] Garanties / exclusions / franchises
- [ ] Cas ACCEPT / REJECT / REVIEW
- [ ] Jeu de données synthétique
- [ ] Tests de non-régression de règles

### I4 — Sinistre & fraude — P0
- [ ] Décision de couverture
- [ ] Calcul / contrôle de franchise
- [ ] Score fraude simulé
- [ ] Human review sur seuils sensibles
- [ ] Audit Decision ID + rule version

### I5 — API-First — P0
- [ ] Decision API REST
- [ ] OpenAPI
- [ ] Idempotence
- [ ] Timeouts / retries / erreurs
- [ ] OAuth2/OIDC
- [ ] mTLS documenté pour cible entreprise

### I6 — Event-Driven — P1
- [ ] Événements DecisionRequested / DecisionCompleted / ReviewRequired
- [ ] AsyncAPI
- [ ] Kafka local ou composant compatible
- [ ] Correlation ID
- [ ] Audit et replay maîtrisé

### I7 — ML dans la décision — P0
- [ ] Modèle simple de scoring risque/fraude
- [ ] Version du modèle
- [ ] Confidence score
- [ ] Fallback sans ML
- [ ] Règles ODM exploitant le score
- [ ] Tests sur seuils

### I8 — GenAI documentaire — P1
- [ ] Extraction structurée depuis document synthétique
- [ ] Validation schéma JSON
- [ ] Confidence gating
- [ ] Rejet / human review si confiance faible
- [ ] Interdiction d’une décision sensible par LLM seul

### I9 — MCP & Agentic AI — P1
- [ ] Exposer Decision Services comme tools
- [ ] MCP server de démonstration
- [ ] Permissions et scopes
- [ ] Audit tool calls
- [ ] Garde-fous agentiques

### I10 — OpenShift Local / CRC — P0
- [ ] Namespace/projet
- [ ] Deployments / Services / Routes
- [ ] ConfigMaps / Secrets
- [ ] Requests / limits / quotas
- [ ] NetworkPolicy
- [ ] Probes
- [ ] Test E2E local
- [ ] Script de validation automatisé

**DoD** : le parcours IARD principal fonctionne de bout en bout sur CRC avec preuves reproductibles.

### I11 — Azure AKS / ARO — P1
- [ ] Définir cible AKS
- [ ] Documenter alternative ARO
- [ ] IaC
- [ ] Registry / identité / réseau / secrets
- [ ] Test de parité fonctionnelle avec CRC
- [ ] Script destroy / maîtrise coûts

### I12 — GitOps / CI-CD — P1
- [ ] Argo CD
- [ ] Helm/Kustomize overlays local/Azure
- [ ] Versioning règles + code
- [ ] Quality gates
- [ ] Promotion multi-environnements
- [ ] Rollback

### I13 — Observabilité & audit — P1
- [ ] Metrics
- [ ] Logs
- [ ] Traces
- [ ] Decision ID
- [ ] Rule/model version
- [ ] SLI/SLO
- [ ] Dashboard de démonstration

### I14 — HA / PRA / sécurité — P2
- [ ] RTO/RPO
- [ ] Topologie cible
- [ ] Backup / restore
- [ ] Tests de panne
- [ ] IAM / RBAC
- [ ] Threat model

### I15 — Soutenance Architecte Solution — P2
- [ ] HLD
- [ ] ADR majeurs
- [ ] Matrice risques / arbitrages
- [ ] Diagrammes finaux
- [ ] Demo script
- [ ] Questions/réponses entretien

## 3 passes de revue finale

### Revue R1 — Cohérence architecture
- [ ] DDD / API / Event / Decision cohérents
- [ ] Aucun doublon inutile avec les autres dépôts
- [ ] AI et ODM clairement séparés
- [ ] Anonymisation vérifiée

### Revue R2 — Exécutabilité
- [ ] `git clone` propre
- [ ] Déploiement CRC reproductible
- [ ] Tests E2E verts
- [ ] GitOps opérationnel
- [ ] Parité Azure documentée/testée

### Revue R3 — Niveau Architecte Solution
- [ ] HLD/ADR/NFR complets
- [ ] Sécurité/HA/PRA/observabilité traités
- [ ] README orienté recruteur/architecte
- [ ] Démo de 10–15 min
- [ ] Aucun claim non prouvé
