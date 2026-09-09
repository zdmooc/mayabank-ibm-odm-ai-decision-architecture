# Itération 5 — API-First / Decision API

## Statut

**TERMINÉE — contrat API, référence portable, idempotence, erreurs et architecture sécurité livrés.**

## Objectif

Exposer les décisions IARD à travers une façade API stable sans coupler les consommateurs au runtime IBM ODM.

```text
Canal / Back Office / Partenaire
            ↓
     API Gateway / IAM
            ↓
        Decision API
   correlation / idempotence
   validation / erreurs
            ↓
     Decision Services
 Underwriting / Claim / Pricing
            ↓
         IBM ODM
```

## Principes API

- contrat REST versionné indépendamment de l'implémentation ODM ;
- `Idempotency-Key` obligatoire pour les POST de décision ;
- `X-Correlation-Id` propagé de bout en bout ;
- erreurs normalisées au format `ProblemDetails` ;
- timeout explicite côté appelant ;
- retry limité aux erreurs transitoires et jamais aveugle ;
- authentification OAuth2/OIDC en cible ;
- mTLS entre composants sensibles en cible entreprise ;
- aucune information sensible dans les reason codes ou logs.

## Endpoints v1

- `POST /v1/decisions/underwriting` ;
- `POST /v1/decisions/claims` ;
- `GET /health/live` ;
- `GET /health/ready`.

## Idempotence

Deux requêtes strictement équivalentes portant la même `Idempotency-Key` retournent la même décision logique.

Une réutilisation de la même clé avec un payload différent doit retourner `409 IDEMPOTENCY_CONFLICT`.

La persistance utilisée dans le POC portable est en mémoire uniquement. La cible réelle utilisera un store partagé et durable avec TTL.

## Erreurs

| HTTP | Code | Usage |
|---:|---|---|
| 400 | `INVALID_REQUEST` | payload invalide |
| 401 | `UNAUTHORIZED` | token absent/invalide |
| 403 | `FORBIDDEN` | scope insuffisant |
| 409 | `IDEMPOTENCY_CONFLICT` | même clé, payload différent |
| 422 | `DECISION_INPUT_REJECTED` | entrée métier non exploitable |
| 429 | `RATE_LIMITED` | limitation API Gateway |
| 503 | `DECISION_SERVICE_UNAVAILABLE` | backend décision indisponible |
| 504 | `DECISION_TIMEOUT` | timeout backend |

## Sécurité cible

### OAuth2 / OIDC

Scopes proposés :

- `decision:underwriting` ;
- `decision:claim` ;
- `decision:audit.read`.

Le POC portable vérifie uniquement la présence d'un Bearer token fictif ; la validation cryptographique JWT/JWKS sera réalisée avec l'IAM de la plateforme lors des itérations de déploiement.

### mTLS

Cible entreprise :

```text
Client -> API Gateway : TLS
API Gateway -> Decision API : mTLS
Decision API -> ODM / services : mTLS ou service mesh selon cible
```

## Timeouts / retries

Recommandation de référence :

- timeout appel Decision Service : 2 s dans le lab ;
- 1 retry maximum pour erreur transitoire avant toute réponse au client ;
- aucun retry automatique sur erreur métier ou `4xx` ;
- idempotence obligatoire avant retry d'un `POST`.

## Livrables

- `api/decision-api.openapi.yaml` ;
- `api/reference_decision_api.py` ;
- `api/sample_client.py` ;
- `docs/iteration-05/security.md` ;
- `tests/test_decision_api.py`.

## Validation portable

```bash
python -m unittest tests/test_decision_api.py
python api/reference_decision_api.py
```

Le serveur portable sert uniquement à valider le contrat et les comportements transverses. Il ne remplace ni un API Gateway réel, ni un IAM, ni un runtime IBM ODM.

## Critères de sortie

- [x] Decision API REST définie ;
- [x] OpenAPI versionné ;
- [x] idempotence définie et testée ;
- [x] erreurs normalisées ;
- [x] correlation ID ;
- [x] timeouts / retries documentés ;
- [x] OAuth2/OIDC cible documenté ;
- [x] mTLS cible entreprise documenté ;
- [x] aucune dépendance propriétaire IBM ajoutée.

## Prochaine étape

**Itération 6 — Event-Driven : événements de décision, AsyncAPI, Kafka-compatible local, corrélation, audit et replay maîtrisé.**
