# Itération 7 — ML dans la décision IARD

## Statut

**TERMINÉE — scoring fraude synthétique, version de modèle, confiance, fallback et intégration aux règles livrés.**

## Objectif

Introduire un composant ML dans la décision IARD sans lui donner l’autorité de décision métier.

```text
Claim / Underwriting Data
        ↓
   ML Scoring Service
 riskScore + confidence
 modelVersion
        ↓
   IBM ODM / Policy Rules
 seuils + garde-fous
        ↓
 STANDARD / REVIEW
        ↓
 Human Review si nécessaire
```

## Principe d’architecture

**Le ML prédit ; IBM ODM applique la politique métier.**

Le modèle fournit :

- `riskScore` entre 0 et 1 ;
- `confidenceScore` entre 0 et 1 ;
- `modelVersion` ;
- `modelStatus` ;
- facteurs explicatifs simples de lab.

Le moteur de règles décide ensuite comment exploiter ce signal.

## Politique v1

- modèle indisponible -> `REVIEW` avec `MODEL_UNAVAILABLE` ;
- confiance < 0.70 -> `REVIEW` avec `MODEL_LOW_CONFIDENCE` ;
- score >= 0.80 -> `REVIEW` renforcée ;
- 0.55 <= score < 0.80 -> `REVIEW` ;
- score < 0.55 et confiance suffisante -> traitement standard.

**Aucun score ML ne produit un rejet automatique.**

## Modèle de laboratoire

Le modèle est volontairement simple, déterministe et sans dépendance externe. Il utilise des poids synthétiques pour démontrer :

- features versionnées ;
- modèle versionné ;
- score ;
- confiance ;
- fallback ;
- intégration règles/ML.

Il ne prétend pas représenter un modèle actuariel ou antifraude réel.

## Livrables

- `ml/fraud/model-v1.json` ;
- `ml/fraud/scorer.py` ;
- `ml/fraud/odm-score-policy.csv` ;
- `data/synthetic/ml-fraud-cases.csv` ;
- `tests/test_ml_fraud.py`.

## Exécution

```bash
python ml/fraud/scorer.py
python ml/fraud/scorer.py --json
python -m unittest tests/test_ml_fraud.py
```

## Gouvernance

Chaque score doit transporter :

- version du modèle ;
- timestamp logique ;
- score ;
- confiance ;
- statut du modèle ;
- reason codes de politique après passage dans les règles.

Le fallback doit être explicite et auditable.

## Critères de sortie

- [x] score fraude synthétique ;
- [x] `modelVersion` ;
- [x] `confidenceScore` ;
- [x] fallback modèle indisponible/faible confiance ;
- [x] politique ODM consommant le score ;
- [x] tests sur seuils ;
- [x] aucun rejet automatique piloté par le ML seul.

## Prochaine étape

**Itération 8 — GenAI documentaire : extraction structurée, validation JSON, confidence gating et passage vers ODM.**
