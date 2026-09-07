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

## Stratégie de déploiement

Deux cibles sont obligatoires dans la trajectoire du dépôt :

### Cible A — OpenShift Local / CRC

- cible prioritaire pour apprendre, développer et tester localement ;
- validation des workloads ODM, API, ML/GenAI et composants d’intégration ;
- usage de Routes, Services, ConfigMaps, Secrets, quotas, probes et NetworkPolicy ;
- GitOps introduit après stabilisation des workloads ;
- un lab n’est marqué `EXÉCUTÉ` qu’avec une preuve reproductible.

### Cible B — Azure

- **AKS** comme cible Kubernetes Azure pour reproduire le même système dans le cloud ;
- **ARO** comme option d’architecture entreprise lorsque le besoin impose OpenShift managé sur Azure ;
- aucune divergence de logique métier ODM entre OpenShift Local et Azure ;
- configuration et déploiement différenciés par overlays/values/IaC, pas par fork applicatif ;
- destruction des ressources Azure de lab après validation lorsque cela est possible afin de maîtriser les coûts.

Ordre de travail retenu : **Local/CRC -> validation -> Azure**.

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
- portabilité OpenShift Local / Azure ;
- maîtrise du coût des labs cloud ;
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
                         |
            +------------+------------+
            |                         |
            v                         v
 OpenShift Local / CRC          Azure AKS / ARO
```

## Livrables de l’Itération 0

- README de positionnement ;
- roadmap ;
- contexte fictif ;
- séparation règles / ML / GenAI / humain ;
- principes d’anonymisation ;
- NFR initiaux ;
- architecture logique initiale ;
- stratégie de déploiement OpenShift Local + Azure.

## Critères de sortie

- [x] aucun nom d’entreprise cliente réelle ;
- [x] aucun artefact propriétaire ;
- [x] cas d’usage IARD clairement défini ;
- [x] rôle d’IBM ODM clairement séparé de l’AI ;
- [x] OpenShift Local / CRC défini comme cible prioritaire de lab ;
- [x] Azure AKS défini comme cible cloud et ARO comme option entreprise ;
- [x] principe de portabilité sans fork applicatif défini ;
- [x] roadmap incrémentale créée ;
- [x] aucune prétention de lab exécuté tant qu’aucune preuve n’existe.

**Statut : TERMINÉE**

Prochaine étape : **Itération 1 — Fondamentaux IBM ODM et premier Decision Service IARD.**
