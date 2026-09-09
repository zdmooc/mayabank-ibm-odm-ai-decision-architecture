# Decision Service — underwriting-eligibility

## But

Premier Decision Service pédagogique du domaine **MayaInsurance IARD**.

Il évalue une demande de souscription et produit une décision déterministe :

- `ACCEPT` ;
- `REJECT` ;
- `REVIEW`.

## Contrat logique

### Entrée

```json
{
  "requestId": "REQ-0001",
  "applicantAge": 35,
  "productType": "AUTO",
  "drivingLicenseYears": 12,
  "recentClaims": 0,
  "incompleteFile": false,
  "declaredRiskLevel": "LOW"
}
```

### Sortie

```json
{
  "requestId": "REQ-0001",
  "decision": "ACCEPT",
  "reasonCodes": ["ELIGIBLE_STANDARD"],
  "decisionVersion": "iard-underwriting-v1"
}
```

## Règles fictives v1

1. Un dossier incomplet entraîne `REVIEW`.
2. Un souscripteur âgé de moins de 18 ans entraîne `REJECT`.
3. Pour `AUTO`, moins d’un an de permis entraîne `REVIEW`.
4. Trois sinistres récents ou plus entraînent `REVIEW`.
5. Un risque déclaré `HIGH` entraîne `REVIEW`.
6. En l’absence de règle bloquante ou de revue, la décision est `ACCEPT`.

## Priorité

```text
REJECT > REVIEW > ACCEPT
```

Les règles de rejet ont donc priorité sur les règles de revue.

## Mapping ODM cible

- RuleApp : `MayaInsuranceIARD`
- Ruleset : `underwritingEligibilityRuleset`
- Ruleflow : `underwritingEligibilityFlow`
- Decision Service : `underwriting-eligibility`

## Important

Ces règles sont entièrement fictives. Elles ne représentent aucune politique de souscription d’une compagnie réelle.
