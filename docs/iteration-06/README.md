# Itération 6 — Event-Driven / Kafka / AsyncAPI

## Statut

**TERMINÉE — contrats d’événements, AsyncAPI 3.1, replay portable, audit et configuration Kafka-compatible livrés.**

## Objectif

Découpler les consommateurs des Decision Services synchrones en publiant des événements métier gouvernés et traçables.

```text
Canal / Back Office / API
          ↓
   Decision API
          ↓
    IBM ODM / Rules
          ↓
DecisionCompleted / ReviewRequired
          ↓
Kafka-compatible Event Backbone
          ↓
Audit / Workflow / Notification / Analytics
```

## Événements v1

- `DecisionRequested` ;
- `DecisionCompleted` ;
- `ReviewRequired`.

Tous les événements possèdent un envelope commun :

- `eventId` ;
- `eventType` ;
- `schemaVersion` ;
- `occurredAt` ;
- `correlationId` ;
- `causationId` ;
- `decisionId` lorsque disponible ;
- `aggregateType` ;
- `aggregateId` ;
- `payload`.

## Topics logiques

- `mayainsurance.decision.requested.v1` ;
- `mayainsurance.decision.completed.v1` ;
- `mayainsurance.review.required.v1`.

La convention de version est portée dans le nom du topic et dans `schemaVersion`.

## Delivery semantics

Le POC retient une approche **at-least-once + consommateurs idempotents** :

- clé de partition recommandée : `aggregateId` ;
- déduplication par `eventId` ;
- ordre garanti uniquement à l’intérieur d’une partition ;
- pas de dépendance à un ordre global ;
- DLQ prévue pour les erreurs non récupérables ;
- retries bornés et observables.

## Replay

Le replay fourni dans cette itération sert à :

- reconstruire un audit ;
- reconstruire une projection ;
- vérifier la cohérence d’un flux événementiel.

**Il ne relance jamais automatiquement une décision sensible dans ODM.** Une ré-exécution métier doit être une action explicite, auditée et contrôlée.

## Livrables

- `api/decision-events.asyncapi.yaml` ;
- `eventing/README.md` ;
- `eventing/replay.py` ;
- `eventing/docker-compose.redpanda.yml` ;
- `data/synthetic/decision-events.jsonl` ;
- `tests/test_eventing.py`.

## Validation portable

```bash
python eventing/replay.py data/synthetic/decision-events.jsonl
python -m unittest tests/test_eventing.py
```

La configuration Redpanda/Kafka-compatible est fournie comme cible locale, mais cette itération ne prétend pas qu’un broker local a été démarré dans cet environnement.

## Critères de sortie

- [x] événements de décision définis ;
- [x] AsyncAPI 3.1 versionné ;
- [x] topics et règles de partitionnement définis ;
- [x] correlation/causation IDs ;
- [x] stratégie at-least-once + idempotence ;
- [x] audit et replay portable ;
- [x] configuration Kafka-compatible locale ;
- [x] replay sans ré-exécution automatique de décision sensible.

## Prochaine étape

**Itération 7 — ML dans la décision : score risque/fraude, version de modèle, confidence score, fallback et règles ODM exploitant le score.**
