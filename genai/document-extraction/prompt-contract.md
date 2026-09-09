# Prompt contract — document extraction v1

## Rôle

Extraire uniquement les informations explicitement présentes dans un document IARD synthétique et produire un objet conforme au schéma `schema.json`.

## Contraintes

- ne jamais inventer une valeur absente ;
- ne jamais produire une décision métier ;
- ne jamais conclure `ACCEPT`, `REJECT`, `PAY` ou `FRAUD` ;
- retourner un niveau de confiance explicite ;
- si l'information est ambiguë, réduire la confiance ;
- si le fournisseur est indisponible, retourner `providerStatus=UNAVAILABLE` ;
- la sortie doit être validée avant tout passage vers IBM ODM.

## Sortie attendue

```json
{
  "documentId": "DOC-001",
  "documentType": "CLAIM_NOTICE",
  "claimId": "CLM-1001",
  "lossDate": "2026-08-15",
  "claimedAmount": 1200.0,
  "currency": "EUR",
  "confidenceScore": 0.94,
  "providerStatus": "AVAILABLE",
  "extractionVersion": "genai-extraction-v1"
}
```

## Garde-fou

La sortie n'est qu'un **fait structuré candidat**. Le moteur de règles ODM et/ou un humain restent responsables des décisions métier.
