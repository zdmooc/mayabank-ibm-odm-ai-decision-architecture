# Matrice décisions / événements / domaines

| Domaine | Commande / entrée | Décision | Événement principal | Consommateurs possibles |
|---|---|---|---|---|
| Underwriting | EvaluateApplication | UnderwritingEligibility | UnderwritingDecisionMade | Pricing, Policy, Audit |
| Pricing | CalculatePremium | PremiumDecision | PremiumCalculated | Underwriting, Policy, Audit |
| Claim | EvaluateClaim | ClaimCoverageDecision | ClaimDecisionMade | Policy, Workflow, Audit |
| Fraud | AssessFraud | FraudReviewDecision | FraudAssessmentCompleted | Claim, Underwriting, Workflow |

## Événements de revue humaine

`ReviewRequired` est un événement transverse émis lorsqu'une décision ne doit pas être automatisée jusqu'au bout.

Attributs minimaux :

```json
{
  "eventType": "ReviewRequired",
  "decisionId": "DEC-...",
  "domain": "UNDERWRITING|PRICING|CLAIM|FRAUD",
  "reasonCodes": ["..."],
  "decisionVersion": "...",
  "occurredAt": "2026-09-09T00:00:00Z"
}
```

## Traçabilité minimale d'une décision

Chaque décision métier devra progressivement transporter :
- `decisionId` ;
- `correlationId` ;
- domaine propriétaire ;
- type de décision ;
- résultat ;
- `reasonCodes` ;
- version de règles ;
- version de modèle ML si utilisée ;
- niveau de confiance si AI/ML ;
- horodatage ;
- indicateur de revue humaine.

## Règle

Un événement décrit un **fait passé**. Une décision ODM ne publie donc pas `ApproveClaim`, mais par exemple `ClaimDecisionMade` avec le résultat de la décision.
