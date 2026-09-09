# Itération 8 — GenAI documentaire gouvernée

## Statut

**TERMINÉE — extraction structurée synthétique, JSON Schema, confidence gating, fallback et passage contrôlé vers ODM livrés.**

## Objectif

Introduire une capacité GenAI pour comprendre des documents IARD sans lui donner l'autorité de prendre une décision métier.

```text
Document synthétique
       ↓
GenAI Extraction Adapter
       ↓
JSON structuré + confidence
       ↓
Schema Validation
       ↓
Confidence Gating
   ├─ valide + confiance suffisante -> FORWARD_TO_ODM
   └─ sinon -> HUMAN_REVIEW
       ↓
IBM ODM / règles métier gouvernées
```

## Principe d'architecture

**Le GenAI extrait et structure ; IBM ODM décide selon des règles gouvernées.**

Le composant GenAI ne produit jamais `ACCEPT`, `REJECT`, `PAY` ou une autre décision métier finale.

## Contrat d'extraction v1

Champs structurés :

- `documentId` ;
- `documentType` ;
- `claimId` ;
- `lossDate` ;
- `claimedAmount` ;
- `currency` ;
- `confidenceScore` ;
- `providerStatus` ;
- `extractionVersion`.

## Confidence gating

- schéma invalide -> `HUMAN_REVIEW` ;
- provider indisponible -> `HUMAN_REVIEW` ;
- confiance < 0.85 -> `HUMAN_REVIEW` ;
- schéma valide + confiance >= 0.85 -> `FORWARD_TO_ODM`.

Le seuil est synthétique et sert uniquement au laboratoire.

## Implémentation portable

Cette itération n'appelle volontairement aucun fournisseur LLM externe. Le dataset contient des sorties GenAI synthétiques qui permettent de tester :

- contrat d'extraction ;
- validation de schéma ;
- niveau de confiance ;
- provider indisponible ;
- fallback humain ;
- frontière GenAI -> ODM.

Un futur adapter pourra appeler un fournisseur GenAI sans modifier les politiques de gating.

## Livrables

- `genai/document-extraction/schema.json` ;
- `genai/document-extraction/prompt-contract.md` ;
- `genai/document-extraction/extractor.py` ;
- `data/synthetic/genai-documents.jsonl` ;
- `tests/test_genai_document_extraction.py`.

## Validation portable

```bash
python genai/document-extraction/extractor.py
python genai/document-extraction/extractor.py --json
python -m unittest tests/test_genai_document_extraction.py
```

## Critères de sortie

- [x] extraction structurée depuis documents synthétiques ;
- [x] JSON Schema versionné ;
- [x] confidence gating ;
- [x] fallback si provider indisponible ;
- [x] human review si confiance faible ;
- [x] passage vers ODM uniquement après validation ;
- [x] aucune décision sensible laissée au GenAI seul ;
- [x] aucun appel fournisseur GenAI présenté comme réellement exécuté.

## Prochaine étape

**Itération 9 — MCP & Agentic AI : Decision Services comme tools, permissions/scopes, audit des tool calls et garde-fous agentiques.**
