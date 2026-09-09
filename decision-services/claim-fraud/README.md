# Claim & Fraud Decision Service

Service portable de référence pour la gestion fictive d'un sinistre IARD.

## Entrées

- état de la police ;
- présence de la garantie ;
- événement couvert ou non ;
- montant réclamé ;
- franchise ;
- score fraude simulé.

## Sorties

- `PAY` ;
- `REJECT` ;
- `REVIEW`.

## Gouvernance

Le score fraude ne possède pas l'autorité finale. Les scores moyens ou élevés déclenchent une revue humaine. La décision finale reste gouvernée par les règles du domaine Claim/Fraud et la validation humaine quand nécessaire.

## Versioning

- règles sinistre : `claim-rules-v1` ;
- seuils fraude : `fraud-thresholds-v1` ;
- futur Decision Service ODM : `ClaimDecision`.
