# Eventing architecture

## Objectif

Fournir un backbone événementiel découplé autour des Decision Services IARD.

## Topics

| Topic | Producteur | Consommateurs typiques |
|---|---|---|
| `mayainsurance.decision.requested.v1` | Decision API | audit, orchestration |
| `mayainsurance.decision.completed.v1` | Decision Service | audit, notification, analytics |
| `mayainsurance.review.required.v1` | Decision Service | workflow humain |

## Partitionnement

Clé recommandée : `aggregateId`.

Cela préserve l’ordre des événements d’un même agrégat dans une partition sans imposer un ordre global.

## Delivery

- modèle : at-least-once ;
- consommateurs idempotents ;
- déduplication par `eventId` ;
- retry borné ;
- DLQ pour poison messages ;
- journalisation de `correlationId` et `causationId`.

## Replay

Le replay v1 reconstruit une projection d’audit et détecte :

- doublons `eventId` ;
- événement sans événement causal lorsque `causationId` est fourni ;
- incohérence `correlationId` dans une chaîne ;
- `DecisionCompleted` sans `DecisionRequested` préalable pour le même agrégat.

Le replay **n’appelle aucun Decision Service**.

## Local Kafka-compatible

`docker-compose.redpanda.yml` fournit une configuration légère de laboratoire compatible avec les API Kafka.

Cette configuration est un artefact de déploiement local à tester ultérieurement. Le dépôt ne marque pas le broker comme exécuté tant qu’une preuve locale n’est pas conservée.
