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
- compréhension de documents ;
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

**Le ML prédit, le GenAI extrait, IBM ODM applique la politique métier, l’humain traite les exceptions sensibles.**

## Souscription IARD

Validations portables :

```bash
python tools/validate_iteration_01.py
python tools/validate_iteration_03.py
python tools/validate_iteration_04.py
```

## Decision API v1

- `POST /v1/decisions/underwriting` ;
- `POST /v1/decisions/claims` ;
- OpenAPI 3.1 ;
- idempotence ;
- correlation ID ;
- erreurs `ProblemDetails` ;
- OAuth2/OIDC et mTLS documentés en cible.

```bash
python -m unittest tests/test_decision_api.py
```

## Event-Driven v1

- `DecisionRequested` ;
- `DecisionCompleted` ;
- `ReviewRequired` ;
- AsyncAPI 3.1 ;
- Kafka-compatible / Redpanda ;
- replay d’audit sans ré-exécution métier automatique.

```bash
python eventing/replay.py data/synthetic/decision-events.jsonl
python -m unittest tests/test_eventing.py
```

## ML dans la décision v1

L’Itération 7 ajoute un scoring fraude synthétique avec :

- `riskScore` ;
- `confidenceScore` ;
- `modelVersion` ;
- fallback modèle indisponible/faible confiance ;
- politique ODM consommant le score.

```bash
python ml/fraud/scorer.py
python -m unittest tests/test_ml_fraud.py
```

Principe : **aucun score ML ne produit un rejet automatique.**

## GenAI documentaire v1

L’Itération 8 ajoute :

- JSON Schema d’extraction ;
- prompt contract ;
- sorties GenAI synthétiques ;
- validation structurée ;
- `confidenceScore` ;
- fallback fournisseur indisponible ;
- `HUMAN_REVIEW` si confiance insuffisante ;
- `FORWARD_TO_ODM` uniquement si l’extraction est valide.

```bash
python genai/document-extraction/extractor.py
python -m unittest tests/test_genai_document_extraction.py
```

Principe : **le GenAI ne produit jamais une décision métier finale.** Aucun fournisseur LLM externe n’est présenté comme réellement exécuté dans cette itération.

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
- ne pas revendiquer un runtime IBM ODM, LLM ou OpenShift exécuté sans preuve ;
- éviter tout fork fonctionnel entre OpenShift Local et Azure.

## État

- **I0 à I8 : TERMINÉES**
- **Prochaine : Itération 9 — MCP & Agentic AI**

Voir `docs/iteration-08/README.md`, `docs/00-roadmap.md` et `docs/BACKLOG.md`.
