# MayaBank IBM ODM & AI Decision Architecture

Référentiel d’architecture et laboratoire pédagogique pour concevoir une plateforme de **Decision Management & AI appliquée à l’assurance IARD**, dans un contexte entièrement fictif et anonymisé.

## Positionnement

**Architecte Solution — IBM ODM / Decision Management / AI — Assurance IARD**

Le dépôt montre comment relier :

```text
Besoin métier IARD
  -> DDD / bounded contexts
  -> modèle de décision
  -> règles déterministes IBM ODM
  -> scores / prédictions ML
  -> compréhension documentaire GenAI
  -> validation humaine si nécessaire
  -> API / événements
  -> OpenShift / Kubernetes
  -> sécurité / observabilité / HA-PRA / GitOps
```

## Cas d’usage fil rouge

Plateforme fictive **MayaInsurance IARD** :

- souscription et éligibilité ;
- tarification ;
- garanties, exclusions et franchises ;
- traitement de sinistres ;
- détection de fraude ;
- décisions nécessitant une revue humaine.

## Modèle métier

Bounded contexts cœur :

- **Underwriting** ;
- **Pricing** ;
- **Claim** ;
- **Fraud**.

Supporting domains : **Policy**, **Party**, **Document**.

Principe : **DDD porte les frontières métier ; IBM ODM est la plateforme d’exécution et de gouvernance des politiques de décision. ODM n’est pas un bounded context métier.**

## Principe architectural

L’IA ne remplace pas la politique métier :

```text
Documents / données
        |
        +--> GenAI : extraction / compréhension
        +--> ML    : score / prédiction
        |
        v
IBM ODM : règles métier versionnées et explicables
        |
        v
ACCEPT / REJECT / REVIEW / PRICE / COVERAGE
```

## Souscription IARD v1

Les Itérations 1 à 3 fournissent :

- un Decision Service portable d’éligibilité ;
- un modèle DDD IARD ;
- une tarification simple fictive ;
- une configuration garanties / exclusions / franchises ;
- un dataset synthétique de non-régression.

Validation :

```bash
python tools/validate_iteration_01.py
python tools/validate_iteration_03.py
```

## Sinistre & fraude v1

L’Itération 4 ajoute :

- décision de couverture ;
- calcul de franchise et montant indemnisable ;
- score fraude **simulé** ;
- revue humaine pour les scores sensibles ;
- `decisionId`, `ruleVersion` et reason codes ;
- audit JSONL synthétique.

Validation :

```bash
python tools/validate_iteration_04.py
```

Principe : **un score de fraude simulé ne peut pas rejeter seul une décision sensible ; il déclenche une revue humaine.**

## Decision API v1

L’Itération 5 ajoute une façade API stable devant les Decision Services :

- `POST /v1/decisions/underwriting` ;
- `POST /v1/decisions/claims` ;
- OpenAPI 3.1 ;
- `Idempotency-Key` ;
- `X-Correlation-Id` ;
- erreurs normalisées `ProblemDetails` ;
- timeout/retry documentés ;
- architecture OAuth2/OIDC ;
- mTLS cible entreprise.

Validation portable :

```bash
python -m unittest tests/test_decision_api.py
python api/reference_decision_api.py
python api/sample_client.py
```

Le serveur portable ne remplace pas un API Gateway, un IAM ou un runtime IBM ODM réel.

## Event-Driven v1

L’Itération 6 ajoute :

- `DecisionRequested` ;
- `DecisionCompleted` ;
- `ReviewRequired` ;
- AsyncAPI 3.1 ;
- topics versionnés ;
- `correlationId` / `causationId` ;
- stratégie at-least-once + consommateurs idempotents ;
- journal synthétique et replay d’audit ;
- configuration Redpanda/Kafka-compatible de laboratoire.

Validation portable :

```bash
python eventing/replay.py data/synthetic/decision-events.jsonl
python -m unittest tests/test_eventing.py
```

Principe : **un replay reconstruit audit/projections mais ne ré-exécute jamais automatiquement une décision sensible dans ODM.**

## Stratégie de déploiement

Le projet doit être **portable et testable sur deux cibles** sans dupliquer la logique métier :

1. **OpenShift Local / CRC — cible prioritaire des labs locaux**
   - exécution sur le poste de développement ;
   - validation des manifests, Routes, Secrets, ConfigMaps, probes, quotas, NetworkPolicy et GitOps ;
   - preuve de fonctionnement conservée dans le dépôt avant de déclarer un lab exécuté.

2. **Azure — cible cloud alternative**
   - **AKS** comme cible Kubernetes Azure de référence pour les labs cloud ;
   - **Azure Red Hat OpenShift (ARO)** documenté comme option entreprise lorsque la cible doit rester OpenShift managé sur Azure ;
   - les services ODM/AI doivent conserver les mêmes contrats API et règles de décision entre local et cloud.

Principe : **OpenShift Local d’abord, Azure ensuite**.

## Périmètre technique cible

- IBM ODM : Decision Center, Decision Server, Decision Services, Rule Designer ;
- XOM / BOM / vocabulaire métier / BAL ;
- Decision Tables et Ruleflows ;
- DDD / Context Map / C4 logique ;
- REST / OpenAPI ;
- Event-Driven / AsyncAPI / Kafka-compatible ;
- ML et GenAI ;
- MCP / agents pour l’accès gouverné aux Decision Services ;
- OAuth2 / OIDC / mTLS ;
- OpenShift Local / CRC ;
- Azure AKS, avec ARO comme option de référence ;
- GitOps / CI-CD ;
- observabilité, audit, SLI/SLO ;
- HA / PRA / RTO / RPO.

## Règles du dépôt

- aucun nom, donnée, architecture interne ou artefact confidentiel d’une entreprise réelle ;
- tous les scénarios métier utilisent **MayaInsurance** ;
- aucune copie de binaire IBM, JAR propriétaire ou contenu décompilé ;
- distinguer systématiquement **architecture cible**, **POC**, **lab exécuté** et **hypothèse** ;
- chaque itération doit être récupérable, documentée et testable indépendamment ;
- éviter tout fork fonctionnel entre OpenShift Local et Azure.

## État

- **Itération 0 — Initialisation et cadrage : TERMINÉE**
- **Itération 1 — Fondamentaux ODM & premier Decision Service IARD : TERMINÉE**
- **Itération 2 — DDD / modèle métier IARD : TERMINÉE**
- **Itération 3 — Souscription, tarification et offre IARD : TERMINÉE**
- **Itération 4 — Sinistre & fraude : TERMINÉE**
- **Itération 5 — API-First : TERMINÉE**
- **Itération 6 — Event-Driven : TERMINÉE**
- **Prochaine : Itération 7 — ML dans la décision**

Voir `docs/iteration-06/README.md`.

## Roadmap

Voir `docs/00-roadmap.md` et `docs/BACKLOG.md`.
