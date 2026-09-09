# Dictionnaire métier IARD — Ubiquitous Language

| Terme | Définition dans MayaInsurance |
|---|---|
| Application | Demande de souscription soumise pour décision. |
| Applicant | Personne ou entité portant la demande. |
| Risk Profile | Données métier utilisées pour caractériser le risque. |
| Coverage Request | Garanties demandées lors de la souscription. |
| Underwriting Decision | Résultat ACCEPT, REJECT ou REVIEW sur une demande. |
| Quote | Proposition tarifaire liée à une demande. |
| Base Premium | Prime de référence avant ajustements. |
| Adjustment | Majoration ou réduction justifiée par une politique métier. |
| Policy | Contrat d'assurance en vigueur ou en préparation. |
| Coverage | Garantie attachée au contrat. |
| Exclusion | Situation explicitement non couverte par une garantie. |
| Deductible | Part restant à charge selon la politique applicable. |
| Claim Case | Dossier de sinistre. |
| Loss Event | Événement déclaré à l'origine du sinistre. |
| Claim Decision | Décision de couverture/orientation du dossier. |
| Fraud Signal | Indicateur contribuant à une suspicion de fraude. |
| Risk Score | Score probabiliste produit par un modèle ou une méthode de scoring. |
| Human Review | Revue humaine imposée par une règle, un faible niveau de confiance ou une sensibilité particulière. |
| Decision Version | Version de la politique/ruleset ayant produit la décision. |
| Reason Code | Code explicite expliquant un résultat de décision. |

## Convention

Les termes métier ci-dessus doivent être préférés dans :
- les modèles ;
- les API ;
- les règles ODM ;
- les événements ;
- les tests ;
- la documentation.

Les termes techniques IBM (`RuleApp`, `Ruleset`, `BOM`, `XOM`, etc.) ne remplacent jamais le vocabulaire métier.
