# Fondamentaux IBM ODM — mémo Architecte Solution

## 1. Chaîne de décision

```text
Application appelante
  -> Decision Service
  -> RuleApp
  -> Ruleset
  -> règles / decision tables / ruleflow
  -> résultat explicable
```

## 2. Concepts essentiels

### XOM — Execution Object Model

Modèle technique utilisé à l’exécution. Il peut être basé sur des classes Java ou une représentation structurée équivalente.

Exemple logique :

```text
UnderwritingRequest
- applicantAge
- productType
- drivingLicenseYears
- recentClaims
- incompleteFile
- declaredRiskLevel
```

### BOM — Business Object Model

Vue métier exposée aux auteurs de règles. Le BOM permet de présenter un vocabulaire compréhensible sans obliger l’auteur métier à raisonner directement sur le code Java.

Exemples de vocabulaire :

- « le souscripteur » ;
- « le nombre de sinistres récents » ;
- « le dossier est incomplet » ;
- « le niveau de risque déclaré ».

### BAL — Business Action Language

Langage lisible par le métier pour exprimer les règles.

Exemple pédagogique :

```text
si le dossier est incomplet
alors la décision est REVIEW
et ajouter le motif DOSSIER_INCOMPLET
```

### Decision Table

Appropriée lorsque plusieurs conditions structurées conduisent à des résultats répétitifs et comparables.

### Ruleflow

Orchestre les groupes de règles et l’ordre logique d’évaluation.

Exemple cible :

```text
validation-dossier
   -> exclusions
   -> éligibilité
   -> revue-manuelle
   -> finalisation
```

### Ruleset

Unité exécutable de règles appelée par le moteur de décision.

Cible du lab : `underwritingEligibilityRuleset`.

### RuleApp

Paquet de déploiement contenant un ou plusieurs Rulesets.

Cible du lab : `MayaInsuranceIARD`.

### Decision Center

Espace de gouvernance et de collaboration permettant de gérer les décisions/règles, leur cycle de vie, les versions et la collaboration métier/IT.

### Rule Execution Server — RES

Runtime qui exécute les RuleApps/Rulesets appelés par les applications clientes.

## 3. Répartition des responsabilités

| Responsabilité | Composant |
|---|---|
| modèle technique | XOM |
| vocabulaire métier | BOM |
| règles lisibles | BAL |
| matrice de décision | Decision Table |
| orchestration des règles | Ruleflow |
| unité exécutable | Ruleset |
| unité de déploiement | RuleApp |
| gouvernance | Decision Center |
| exécution | Rule Execution Server |

## 4. Principe d’architecture retenu

IBM ODM porte les **politiques métier déterministes et auditables**.

Plus tard :

- ML fournira des scores/probabilités ;
- GenAI structurera du contenu non structuré ;
- ODM conservera l’autorité sur les politiques métier ;
- l’humain validera les exceptions sensibles.

## 5. Règle de portfolio

Les fichiers de ce dépôt sont des spécifications et artefacts pédagogiques reconstruits proprement. Aucun binaire, export propriétaire, JAR IBM ou contenu décompilé n’est versionné.
