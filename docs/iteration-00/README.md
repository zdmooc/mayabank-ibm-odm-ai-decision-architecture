# Itération 0 — Cadrage IBM ODM & AI / Assurance IARD

## Objectif

Définir le cadre du dépôt avant tout développement ou déploiement.

## Contexte fictif

**MayaInsurance** souhaite industrialiser des décisions IARD qui sont aujourd’hui réparties entre applications, procédures métier et traitements manuels.

Les décisions concernent notamment :

- éligibilité d’un contrat ;
- conditions de souscription ;
- tarification ;
- garanties et exclusions ;
- franchise ;
- orientation d’un sinistre ;
- suspicion de fraude ;
- revue humaine des cas sensibles.

## Séparation des responsabilités

| Besoin | Composant privilégié |
|---|---|
| politique métier déterministe | IBM ODM |
| score ou probabilité | ML |
| compréhension de texte/document | GenAI |
| orchestration d’exception | workflow / humain |
| exposition | API |
| diffusion asynchrone | événements |

Principe : **le modèle propose ou enrichit ; le moteur de décision applique les politiques ; l’humain traite les exceptions sensibles.**

## NFR initiaux

- explicabilité ;
- auditabilité ;
- versioning règles et modèles ;
- sécurité by design ;
- séparation des environnements ;
- résilience ;
- observabilité ;
- réversibilité ;
- performance mesurable ;
- absence de données réelles.

## Architecture logique initiale

```text
Channel / Back Office
        |
        v
API Gateway
        |
        v
Decision API
   |         |
   |         +--> ML / GenAI
   |
   +------------> IBM ODM Decision Service
                         |
                         v
            ACCEPT / REJECT / REVIEW
                         |
                         v
                  Events / Workflow
```

## Livrables de l’Itération 0

- README de positionnement ;
- roadmap ;
- contexte fictif ;
- séparation règles / ML / GenAI / humain ;
- principes d’anonymisation ;
- NFR initiaux ;
- architecture logique initiale.

## Critères de sortie

- [x] aucun nom d’entreprise cliente réelle ;
- [x] aucun artefact propriétaire ;
- [x] cas d’usage IARD clairement défini ;
- [x] rôle d’IBM ODM clairement séparé de l’AI ;
- [x] roadmap incrémentale créée ;
- [x] aucune prétention de lab exécuté tant qu’aucune preuve n’existe.

**Statut : TERMINÉE**

Prochaine étape : **Itération 1 — Fondamentaux IBM ODM et premier Decision Service IARD.**
