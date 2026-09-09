# Itération 2 — Modèle métier IARD / DDD

## Statut

**TERMINÉE — modèle de domaine, bounded contexts, dictionnaire et traçabilité livrés.**

## Objectif

Structurer le domaine **MayaInsurance IARD** avant d'ajouter davantage de règles, d'AI ou d'intégrations.

Le principe retenu est volontairement simple : **DDD structure le métier ; IBM ODM exécute les politiques de décision.**

IBM ODM n'est donc pas un bounded context métier. Il constitue une capacité de plateforme partagée qui héberge et exécute des décisions appartenant aux domaines métier.

## Bounded contexts retenus

### Core domains

- **Underwriting** — éligibilité, acceptation, rejet, revue ;
- **Pricing** — prime, majoration, remise et paramètres tarifaires ;
- **Claim** — couverture, franchise, orientation et décision de sinistre ;
- **Fraud** — évaluation de suspicion et orientation vers revue.

### Supporting domains

- **Policy** — contrat, garanties et état de police ;
- **Party** — assuré, conducteur, bénéficiaire et identité métier ;
- **Document** — pièces justificatives et données structurées extraites.

### Generic capabilities

- IAM / sécurité ;
- notifications ;
- audit / observabilité ;
- workflow de revue humaine.

## Principe de propriété des décisions

| Décision | Domaine propriétaire | Exécution cible |
|---|---|---|
| UnderwritingEligibility | Underwriting | IBM ODM |
| PremiumDecision | Pricing | IBM ODM |
| ClaimCoverageDecision | Claim | IBM ODM |
| FraudReviewDecision | Fraud | IBM ODM + score ML futur |

La plateforme ODM fournit l'exécution, la gouvernance et le versioning, mais **la règle reste sémantiquement la propriété du domaine métier**.

## Livrables

- `docs/iteration-02/domain-model.md` ;
- `docs/iteration-02/glossary.md` ;
- `docs/iteration-02/decision-event-matrix.md` ;
- `architecture/iard-context-map.md`.

## Critères de sortie

- [x] bounded contexts principaux identifiés ;
- [x] absence de sur-découpage microservices ;
- [x] propriété des décisions définie ;
- [x] objets métier essentiels identifiés ;
- [x] événements métier principaux définis ;
- [x] relation DDD / ODM clarifiée ;
- [x] aucune donnée ou terminologie client réelle.

## Prochaine étape

**Itération 3 — Souscription & éligibilité : règles complètes, garanties/exclusions/franchises, jeux de données synthétiques et tests de non-régression.**
