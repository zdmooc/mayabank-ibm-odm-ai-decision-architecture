# Decision Service — underwriting-offer

Service logique composite de démonstration pour **MayaInsurance IARD**.

## Responsabilités

1. appeler/appliquer la décision d’éligibilité Underwriting ;
2. si `ACCEPT`, calculer une prime synthétique Pricing ;
3. déterminer garanties et franchise via Policy configuration ;
4. retourner une offre explicable et versionnée.

## Entrée simplifiée

- âge ;
- type de produit ;
- ancienneté permis ;
- sinistres récents ;
- dossier incomplet ;
- niveau de risque.

## Sortie simplifiée

```json
{
  "decision": "ACCEPT|REJECT|REVIEW",
  "reasonCode": "...",
  "premiumEur": 0.0,
  "deductibleEur": 0.0,
  "coverages": [],
  "decisionVersion": "iard-underwriting-offer-v1"
}
```

Pour `REJECT` et `REVIEW`, aucune prime commerciale n’est calculée.

## Tables

- `pricing-table.csv` : prime de base et coefficients fictifs ;
- `coverage-table.csv` : garanties, exclusions et franchise fictives.

## Gouvernance

Les valeurs sont exclusivement pédagogiques. Elles n’ont aucune valeur actuarielle ou contractuelle.
