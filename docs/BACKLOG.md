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

### I1 — Fondamentaux IBM ODM — DONE
- [x] Documenter Decision Center, Decision Server, Rule Designer
- [x] Définir XOM, BOM, vocabulaire BAL
- [x] Créer Decision Table et Ruleflow simples
- [x] Créer un premier Decision Service IARD
- [x] Ajouter exemples de requête/réponse
- [x] Ajouter tests fonctionnels minimaux

**DoD atteint** : Decision Service simple documenté, versionné et validable via `python tools/validate_iteration_01.py`. Le validateur contrôle la spécification portable ; l’exécution IBM ODM réelle viendra dans les itérations de lab.

### I2 — DDD / modèle métier IARD — DONE
- [x] Définir bounded contexts utiles : Underwriting, Pricing, Claim, Fraud
- [x] Définir agrégats et objets métier sans sur-découpage
- [x] Créer dictionnaire métier
- [x] Relier décisions, règles, événements et API
- [x] Produire diagramme C4 logique

**DoD atteint** : context map, modèle de domaine, ubiquitous language, matrice décisions/événements et vue C4 logique livrés. IBM ODM reste une plateforme de décision et non un bounded context métier.

### I3 — Souscription & éligibilité — DONE
- [x] Règles d’éligibilité
- [x] Tarification simple
- [x] Garanties / exclusions / franchises
- [x] Cas ACCEPT / REJECT / REVIEW
- [x] Jeu de données synthétique
- [x] Tests de non-régression de règles

**DoD atteint** : service logique `underwriting-offer`, tables Pricing/Policy, dataset synthétique et validateur `python tools/validate_iteration_03.py`. Les règles restent fictives et la validation est portable ; le runtime IBM ODM sera traité dans les itérations de lab.

### I4 — Sinistre & fraude — DONE
- [x] Décision de couverture
- [x] Calcul / contrôle de franchise
- [x] Score fraude simulé
- [x] Human review sur seuils sensibles
- [x] Audit Decision ID + rule version

**DoD atteint** : service logique Claim/Fraud, règles de couverture, seuils de fraude synthétiques, dataset sinistre, audit JSONL et validateur `python tools/validate_iteration_04.py`. Aucun score simulé n’a autorité pour rejeter seul une décision sensible.

### I5 — API-First — DONE
- [x] Decision API REST
- [x] OpenAPI
- [x] Idempotence
- [x] Timeouts / retries / erreurs
- [x] OAuth2/OIDC
- [x] mTLS documenté pour cible entreprise

**DoD atteint** : façade Decision API v1, OpenAPI 3.1, idempotence, correlation ID, erreurs `ProblemDetails`, client et serveur de référence portables, tests fonctionnels, architecture OAuth2/OIDC et mTLS documentée. Aucun IAM réel ni runtime IBM ODM n’est revendiqué comme exécuté à ce stade.

### I6 — Event-Driven — DONE
- [x] Événements DecisionRequested / DecisionCompleted / ReviewRequired
- [x] AsyncAPI
- [x] Kafka local ou composant compatible
- [x] Correlation ID
- [x] Audit et replay maîtrisé

**DoD atteint** : AsyncAPI 3.1, topics versionnés, configuration Redpanda/Kafka-compatible locale, journal synthétique, correlation/causation IDs, stratégie at-least-once/idempotence, replay d’audit et tests de non-régression. Le replay ne ré-exécute jamais automatiquement une décision sensible.

### I7 — ML dans la décision — DONE
- [x] Modèle simple de scoring risque/fraude
- [x] Version du modèle
- [x] Confidence score
- [x] Fallback sans ML
- [x] Règles ODM exploitant le score
- [x] Tests sur seuils

**DoD atteint** : scoring fraude synthétique versionné, `confidenceScore`, fallback faible confiance/modèle indisponible, politique ODM consommant le score et tests. Aucun rejet automatique n’est piloté par le ML seul.

### I8 — GenAI documentaire — DONE
- [x] Extraction structurée depuis document synthétique
- [x] Validation schéma JSON
- [x] Confidence gating
- [x] Rejet / human review si confiance faible
- [x] Interdiction d’une décision sensible par LLM seul

**DoD atteint** : JSON Schema, prompt contract, adapter portable sur sorties GenAI synthétiques, seuil de confiance, fallback fournisseur indisponible, human review et tests. Seules les extractions validées sont transmises à ODM ; aucun fournisseur LLM réel n’est revendiqué comme exécuté.

### I9 — MCP & Agentic AI — DONE
- [x] Exposer Decision Services comme tools
- [x] MCP server de démonstration portable
- [x] Permissions et scopes
- [x] Audit tool calls
- [x] Garde-fous agentiques

**DoD atteint** : cible MCP `2026-07-28`, catalogue de tools Underwriting/Claim/Audit, policies de scopes, serveur portable stateless-compatible, correlation/toolCall IDs, refus explicite des tools/scopes interdits, audit synthétique et tests. Aucun agent ne peut override une règle, convertir `REVIEW` en décision finale, déclencher un paiement ou déployer une RuleApp.

### I10 — OpenShift Local / CRC — DONE
- [x] Namespace/projet
- [x] Deployments / Services / Routes
- [x] ConfigMaps / Secrets
- [x] Requests / limits / quotas
- [x] NetworkPolicy
- [x] Probes
- [x] Test E2E local
- [x] Script de validation automatisé
- [x] Build CRC réellement validé
- [x] Rollout réellement validé
- [x] 25 tests portables exécutés dans le pod avec `OK`
- [x] Preuve locale générée + résumé versionné

**DoD atteint** : façade Decision API réellement déployée sur OpenShift Local/CRC 4.22.7, build binaire OpenShift, Route TLS, health checks, décision Underwriting `ACCEPT`, correlation ID, régression embarquée 25/25 et `RESULT=PASS`. Cette preuve concerne le runtime portable ; elle ne revendique pas l’exécution d’un runtime IBM ODM licencié.

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
- [x] `git clone` propre
- [x] Déploiement CRC reproductible
- [x] Tests E2E verts
- [ ] GitOps opérationnel
- [ ] Parité Azure documentée/testée

### Revue R3 — Niveau Architecte Solution
- [ ] HLD/ADR/NFR complets
- [ ] Sécurité/HA/PRA/observabilité traités
- [ ] README orienté recruteur/architecte
- [ ] Démo de 10–15 min
- [ ] Aucun claim non prouvé
