# IBM ODM runtime — intégration cible, non incluse

Le lab OpenShift Local de l'Itération 10 déploie uniquement les composants portables du dépôt.

## Pourquoi le runtime IBM ODM n'est pas embarqué

- l'image/runtime IBM ODM est soumise aux droits de licence et d'accès IBM ;
- aucun binaire, JAR propriétaire, image privée ou contenu décompilé n'est publié dans ce dépôt ;
- un déploiement ODM réel ne doit être déclaré exécuté qu'après obtention d'une image autorisée et conservation de preuves de lab.

## Point d'intégration cible

```text
Route / API Gateway
        ↓
Decision API portable
        ↓
ODM Decision Service adapter
        ↓
IBM ODM Decision Server / Rule Execution Server
        ↓
Decision Center pour gouvernance des règles
```

Le contrat public REST et les reason codes restent stables. L'implémentation portable utilisée par CRC peut donc être remplacée par un adapter ODM sans modifier les consommateurs.

## Futur overlay entreprise

Un futur overlay privé pourra apporter :

- référence d'image IBM autorisée ;
- imagePullSecret ;
- configuration Decision Server / Decision Center ;
- secrets et certificats ;
- persistence si requise ;
- mTLS ;
- probes spécifiques IBM ;
- sizing ;
- licence ;
- tests de RuleApp/Ruleset réels.

**Ce fichier ne constitue pas une preuve de déploiement IBM ODM.**
