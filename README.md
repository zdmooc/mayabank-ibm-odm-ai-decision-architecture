# MayaBank IBM ODM & AI Decision Architecture

Référentiel d’architecture et laboratoire pédagogique pour concevoir une plateforme de **Decision Management & AI appliquée à l’assurance IARD**, dans un contexte entièrement fictif et anonymisé.

## Positionnement

**Architecte Solution — IBM ODM / Decision Management / AI — Assurance IARD**

Le dépôt montre comment relier :

```text
Besoin métier IARD
  -> modèle de décision
  -> règles déterministes IBM ODM
  -> scores / prédictions ML
  -> compréhension documentaire GenAI
  -> validation humaine si nécessaire
  -> API / événements
  -> OpenShift / Kubernetes
  -> sécurité / observabilité / HA-PRA / GitOps
```

## Cas d’usage fil rouge

Plateforme fictive **MayaInsurance IARD** :

- souscription et éligibilité ;
- tarification ;
- garanties, exclusions et franchises ;
- traitement de sinistres ;
- détection de fraude ;
- décisions nécessitant une revue humaine.

## Principe architectural

L’IA ne remplace pas la politique métier :

```text
Documents / données
        |
        +--> GenAI : extraction / compréhension
        +--> ML    : score / prédiction
        |
        v
IBM ODM : règles métier versionnées et explicables
        |
        v
ACCEPT / REJECT / REVIEW / PRICE / COVERAGE
```

## Stratégie de déploiement

Le projet doit être **portable et testable sur deux cibles** sans dupliquer la logique métier :

1. **OpenShift Local / CRC — cible prioritaire des labs locaux**
   - exécution sur le poste de développement ;
   - validation des manifests, Routes, Secrets, ConfigMaps, probes, quotas, NetworkPolicy et GitOps ;
   - preuve de fonctionnement conservée dans le dépôt avant de déclarer un lab exécuté.

2. **Azure — cible cloud alternative**
   - **AKS** comme cible Kubernetes Azure de référence pour les labs cloud ;
   - **Azure Red Hat OpenShift (ARO)** documenté comme option entreprise lorsque la cible doit rester OpenShift managé sur Azure ;
   - les services ODM/AI doivent conserver les mêmes contrats API et règles de décision entre local et cloud.

Principe : **OpenShift Local d’abord, Azure ensuite**. Aucun service Azure coûteux ne doit rester déployé inutilement après un lab.

## Périmètre technique cible

- IBM ODM : Decision Center, Decision Server, Decision Services, Rule Designer ;
- XOM / BOM / vocabulaire métier / BAL ;
- Decision Tables et Ruleflows ;
- REST / OpenAPI ;
- ML et GenAI ;
- MCP / agents pour l’accès gouverné aux Decision Services ;
- OAuth2 / OIDC / mTLS ;
- OpenShift Local / CRC ;
- Azure AKS, avec ARO comme option de référence ;
- GitOps / CI-CD ;
- observabilité, audit, SLI/SLO ;
- HA / PRA / RTO / RPO.

## Règles du dépôt

- aucun nom, donnée, architecture interne ou artefact confidentiel d’une entreprise réelle ;
- tous les scénarios métier utilisent **MayaInsurance** ;
- aucune copie de binaire IBM, JAR propriétaire ou contenu décompilé ;
- distinguer systématiquement **architecture cible**, **POC**, **lab exécuté** et **hypothèse** ;
- chaque itération doit être récupérable, documentée et testable indépendamment ;
- éviter tout fork fonctionnel entre la variante OpenShift Local et la variante Azure.

## État

**Itération 0 — Initialisation et cadrage : TERMINÉE**

Voir `docs/iteration-00/README.md`.

## Roadmap

Voir `docs/00-roadmap.md`.
