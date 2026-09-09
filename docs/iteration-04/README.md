# Itération 4 — Sinistre, couverture & fraude

## Statut

**TERMINÉE — décision de couverture, franchise, score fraude simulé, human review et audit portable livrés.**

## Objectif

Construire un parcours de décision sinistre fictif en séparant clairement les responsabilités :

```text
Claim
  -> vérifie police / garantie / événement couvert
  -> calcule franchise et montant indemnisable
        |
        +--> Fraud
               -> score simulé
               -> ACCEPT / REVIEW / REJECT FRAUD CHECK
        |
        v
Decision Outcome
  -> PAY / REJECT / REVIEW
  -> Decision ID + rule version + reason codes
```

Toutes les règles, seuils, montants et scores sont synthétiques.

## Règles v1

### Couverture

- police inactive -> `REJECT` ;
- garantie absente -> `REJECT` ;
- événement non couvert -> `REJECT` ;
- sinon la demande est éligible au calcul d'indemnisation.

### Franchise

```text
indemnisation = max(montant_reclame - franchise, 0)
```

### Fraude simulée

Le score est fourni comme donnée synthétique d'entrée. Aucun modèle ML n'est encore entraîné dans cette itération.

- score < 0.55 -> traitement standard ;
- 0.55 <= score < 0.80 -> `REVIEW` ;
- score >= 0.80 -> `REVIEW` renforcée avec reason code `FRAUD_HIGH_SCORE`.

Une décision sensible n'est jamais rejetée automatiquement par un score ML simulé seul : les cas de fraude élevés restent orientés vers une revue humaine.

## Audit

Chaque décision expose :

- `decisionId` ;
- `claimId` ;
- `decision` ;
- `reasonCodes` ;
- `ruleVersion` ;
- `fraudScoreVersion` ;
- `humanReviewRequired`.

## Livrables

- `decision-services/claim-fraud/README.md` ;
- `decision-services/claim-fraud/coverage-table.csv` ;
- `decision-services/claim-fraud/fraud-thresholds.csv` ;
- `data/synthetic/iard-claim-cases.csv` ;
- `audit/sample-decision-audit.jsonl` ;
- `tools/validate_iteration_04.py`.

## Validation locale portable

```bash
python tools/validate_iteration_04.py
```

Cette validation vérifie la sémantique métier portable. Elle ne constitue pas encore un déploiement IBM ODM réel.

## Critères de sortie

- [x] décision de couverture ;
- [x] calcul de franchise ;
- [x] score fraude simulé ;
- [x] human review sur seuils sensibles ;
- [x] Decision ID + rule version ;
- [x] dataset synthétique ;
- [x] tests de non-régression ;
- [x] aucun rejet sensible décidé par un score ML seul.

## Prochaine étape

**Itération 5 — API-First : Decision API REST, OpenAPI, idempotence, erreurs, OAuth2/OIDC et mTLS cible entreprise.**
