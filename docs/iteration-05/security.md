# Sécurité cible — Decision API

## Objectif

Définir une sécurité portable entre OpenShift Local/CRC et Azure, sans coder en dur un fournisseur IAM.

## Cible d'authentification

- OAuth 2.0 / OpenID Connect ;
- flux machine-to-machine : Client Credentials ;
- validation JWT par issuer/audience/expiry/signature ;
- JWKS récupéré depuis l'IAM ;
- scopes minimum par type de décision.

Scopes de référence :

- `decision:underwriting` ;
- `decision:claim` ;
- `decision:audit.read`.

## Autorisation

Le scope ne remplace pas l'autorisation métier. L'API devra également pouvoir appliquer :

- le type de client ;
- l'environnement ;
- la catégorie de décision ;
- la sensibilité des données ;
- les politiques RBAC/ABAC de l'organisation.

## TLS / mTLS

### Lab local

Le serveur Python portable reste en HTTP local et ne prétend pas implémenter le niveau de sécurité entreprise.

### Cible OpenShift / Azure

- TLS entrant au niveau Route/Ingress/API Gateway ;
- mTLS recommandé entre API Gateway et Decision API ;
- mTLS ou service mesh entre Decision API et runtime de décision selon contraintes de plateforme ;
- rotation automatique des certificats ;
- secrets hors Git.

## Secrets

Interdit :

- token réel dans Git ;
- mot de passe en ConfigMap ;
- clé privée dans le dépôt ;
- secret dans une image de conteneur.

Cibles :

- OpenShift Secret + gestionnaire de secrets externe si disponible ;
- Azure Key Vault sur cible Azure ;
- identité managée/workload identity quand applicable.

## Audit

Tracer :

- correlation ID ;
- decision ID ;
- client/service principal logique ;
- endpoint ;
- statut ;
- version de Decision Service ;
- durée.

Ne pas tracer :

- token ;
- données personnelles inutiles ;
- documents bruts ;
- secrets ;
- payload complet par défaut.

## Threats à traiter lors du hardening

- replay de requête ;
- vol de token ;
- confusion d'audience JWT ;
- abus de scope ;
- déni de service ;
- fuite de données dans les logs ;
- contournement d'idempotence ;
- appel direct du runtime ODM en bypassant la façade gouvernée.
