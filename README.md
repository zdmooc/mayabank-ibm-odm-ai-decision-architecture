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

Bounded contexts cœur : **Underwriting**, **Pricing**, **Claim**, **Fraud**.
Supporting domains : **Policy**, **Party**, **Document**.

Principe : **DDD porte les frontières métier ; IBM ODM est la plateforme d’exécution et de gouvernance des politiques de décision. ODM n’est pas un bounded context métier.**

## Principe architectural

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

L’IA ne remplace pas la politique métier.

## Souscription IARD v1

Les Itérations 1 à 3 fournissent :

- Decision Service portable d’éligibilité ;
- modèle DDD IARD ;
- tarification simple fictive ;
- garanties / exclusions / franchises ;
- dataset synthétique de non-régression.

```bash
python tools/validate_iteration_01.py
python tools/validate_iteration_03.py
```

## Sinistre & fraude v1

L’Itération 4 ajoute couverture, franchise, indemnisation, score fraude simulé, human review et audit versionné.

```bash
python tools/validate_iteration_04.py
```

Principe : **un score de fraude ne peut pas rejeter seul une décision sensible.**

## Decision API v1

L’Itération 5 ajoute : REST/OpenAPI 3.1, idempotence, correlation ID, erreurs normalisées, timeout/retry, OAuth2/OIDC cible et mTLS entreprise.

```bash
python -m unittest tests/test_decision_api.py
python api/reference_decision_api.py
```

## Event-Driven v1

L’Itération 6 ajoute `DecisionRequested`, `DecisionCompleted`, `ReviewRequired`, AsyncAPI 3.1, topics versionnés, correlation/causation IDs, at-least-once + idempotence et replay d’audit.

```bash
python eventing/replay.py data/synthetic/decision-events.jsonl
python -m unittest tests/test_eventing.py
```

Principe : **le replay ne ré-exécute jamais automatiquement une décision sensible dans ODM.**

## ML Decision v1

L’Itération 7 ajoute un scoring fraude synthétique gouverné :

- `riskScore` ;
- `confidenceScore` ;
- `modelVersion` ;
- fallback modèle indisponible/faible confiance ;
- politique ODM qui consomme le score ;
- aucun `REJECT` automatique piloté par le ML seul.

```bash
python ml/fraud/scorer.py
python ml/fraud/scorer.py --json
python -m unittest tests/test_ml_fraud.py
```

Principe : **le ML prédit ; IBM ODM applique la politique métier.**

## Stratégie de déploiement

1. **OpenShift Local / CRC — cible prioritaire des labs locaux** ;
2. **Azure AKS — cible Kubernetes cloud de référence** ;
3. **ARO — option entreprise OpenShift managé sur Azure**.

Principe : **OpenShift Local d’abord, Azure ensuite**, sans fork fonctionnel entre les plateformes.

## Périmètre technique cible

- IBM ODM : Decision Center, Decision Server, Decision Services, Rule Designer ;
- XOM / BOM / BAL / Decision Tables / Ruleflows ;
- DDD / Context Map / C4 ;
- REST / OpenAPI ;
- Event-Driven / AsyncAPI / Kafka-compatible ;
- ML / GenAI / MCP / agents ;
- OAuth2 / OIDC / mTLS ;
- OpenShift Local / CRC ;
- Azure AKS / ARO ;
- GitOps / CI-CD ;
- observabilité / audit / SLI-SLO ;
- HA / PRA / RTO / RPO.

## Règles du dépôt

- aucun nom, donnée ou architecture interne d’une entreprise réelle ;
- aucune copie de binaire IBM/JAR propriétaire/contenu décompilé ;
- distinguer architecture cible, POC, lab exécuté et hypothèse ;
- chaque itération doit rester documentée et testable indépendamment.

## État

- **I0 : TERMINÉE**
- **I1 : TERMINÉE**
- **I2 : TERMINÉE**
- **I3 : TERMINÉE**
- **I4 : TERMINÉE**
- **I5 : TERMINÉE**
- **I6 : TERMINÉE**
- **I7 : TERMINÉE**
- **Prochaine : Itération 8 — GenAI documentaire**

Voir `docs/iteration-07/README.md`.

## Roadmap

Voir `docs/00-roadmap.md` et `docs/BACKLOG.md`.
