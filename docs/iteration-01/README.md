# Itération 1 — Fondamentaux IBM ODM & premier Decision Service IARD

## Statut

**TERMINÉE — conception et artefacts portables prêts.**

> Important : cette itération ne prétend pas qu’un RuleApp IBM propriétaire a été compilé ou déployé. Elle construit le modèle, le vocabulaire, le contrat et les règles de référence qui seront importés/implémentés dans ODM lors des itérations de lab.

## Objectif

Construire le premier bloc de décision de **MayaInsurance IARD** en séparant clairement :

- modèle d’exécution (XOM) ;
- modèle métier/vocabulaire (BOM) ;
- règles métier (BAL / Decision Table) ;
- orchestration (Ruleflow) ;
- unité de déploiement (RuleApp / Ruleset) ;
- contrat d’appel du Decision Service.

## Baseline technique

Référence de travail : **IBM Operational Decision Manager 9.6 / Java 21**.

Composants à maîtriser :

- Rule Designer ;
- Decision Center / Business Console ;
- Rule Execution Server (RES) ;
- Decision Service ;
- RuleApp ;
- Ruleset.

## Premier Decision Service

Nom logique : `underwriting-eligibility`

Finalité : décider si une demande de souscription IARD est :

- `ACCEPT` ;
- `REJECT` ;
- `REVIEW`.

Le service ne réalise pas encore de tarification avancée, de ML ou de GenAI. Ces éléments arriveront dans les itérations suivantes.

## Entrées principales

- âge du souscripteur ;
- type de produit ;
- ancienneté du permis pour l’auto ;
- nombre de sinistres récents ;
- indicateur de dossier incomplet ;
- niveau de risque déclaré.

Toutes les valeurs et règles sont **fictives** et servent uniquement au laboratoire.

## Sortie

```json
{
  "decision": "ACCEPT|REJECT|REVIEW",
  "reasonCodes": ["..."],
  "decisionVersion": "iard-underwriting-v1"
}
```

## Artefacts livrés

- `docs/iteration-01/odm-fundamentals.md` ;
- `decision-services/underwriting-eligibility/README.md` ;
- `decision-services/underwriting-eligibility/decision-table.csv` ;
- `decision-services/underwriting-eligibility/samples/request-*.json` ;
- `decision-services/underwriting-eligibility/samples/expected-*.json` ;
- `api/underwriting-eligibility.openapi.yaml`.

## Mapping ODM cible

```text
Java / JSON model
      ↓
XOM
      ↓
BOM + vocabulaire métier
      ↓
BAL / Decision Table
      ↓
Ruleflow
      ↓
Ruleset: underwritingEligibilityRuleset
      ↓
RuleApp: MayaInsuranceIARD
      ↓
Rule Execution Server
      ↓
Decision Service API
```

## Critères de sortie

- [x] rôle de XOM/BOM/BAL clarifié ;
- [x] premier Decision Service cadré ;
- [x] contrat d’entrée/sortie défini ;
- [x] règles fictives déterministes définies ;
- [x] cas ACCEPT / REJECT / REVIEW fournis ;
- [x] contrat OpenAPI fourni ;
- [x] aucun artefact IBM propriétaire ajouté ;
- [x] aucune donnée d’une entreprise réelle.

## Prochaine étape

**Itération 2 — Modèle métier IARD / DDD / bounded contexts / dictionnaire métier / traçabilité de décision.**
