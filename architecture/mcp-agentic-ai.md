# Architecture MCP & Agentic AI — MayaInsurance IARD

## But

Exposer les capacités de décision IARD à des assistants/agents via MCP tout en conservant l'autorité métier dans les Decision Services gouvernés.

```text
Agent / Copilot
      |
      v
MCP Client
      |
      v
MCP Decision Server
  - tools/list
  - tools/call
  - scopes
  - policy
  - audit
      |
      v
Decision API
      |
      +--> Underwriting Decision Service
      +--> Claim Decision Service
      +--> Audit Read Service
      |
      v
IBM ODM / règles / workflow humain
```

## Frontières de responsabilité

### Agent

Peut :
- choisir un tool autorisé ;
- fournir les paramètres ;
- présenter le résultat ;
- demander une explication ou une revue.

Ne peut pas :
- modifier une règle ;
- contourner une décision ;
- convertir `REVIEW` en acceptation/rejet ;
- déclencher un paiement ;
- déployer une RuleApp ;
- modifier une policy.

### MCP Decision Server

Responsable de :
- catalogue de tools ;
- validation des scopes ;
- validation des métadonnées ;
- validation des payloads ;
- audit ;
- propagation des correlation IDs ;
- refus explicite des capabilities interdites.

### Decision API / IBM ODM

Responsables de :
- contrat métier ;
- règles gouvernées ;
- versioning ;
- décisions déterministes ;
- human review ;
- traçabilité.

## Autorisation

Les permissions sont évaluées côté serveur, jamais déduites du prompt de l'agent.

Scopes v1 :
- `decision:underwriting` ;
- `decision:claim` ;
- `decision:audit.read`.

Une identité dotée du mauvais scope reçoit `FORBIDDEN` même si l'agent demande explicitement l'action.

## Audit

Chaque appel doit transporter :
- `toolCallId` ;
- `correlationId` ;
- identité applicative/utilisateur en cible ;
- nom du tool ;
- scopes accordés ;
- hash ou référence du payload selon exigences de confidentialité ;
- résultat / erreur ;
- version de policy ;
- version de décision/règles lorsque disponible.

## Stateless MCP

La cible MCP 2026-07-28 permet de concevoir le serveur comme une façade stateless horizontalement scalable. Les états métier, idempotency stores, audits et workflows restent dans des composants dédiés ; ils ne doivent pas dépendre d'une session agent locale.

## Cible OpenShift

À partir de l'Itération 10 :

```text
Route / Gateway
      ↓
MCP Decision Server pods
      ↓
Decision API pods
      ↓
ODM / portable decision adapters
```

Avec :
- ServiceAccount/RBAC ;
- NetworkPolicy ;
- secrets externalisés ;
- probes ;
- requests/limits ;
- audit centralisé ;
- mTLS cible entreprise.
