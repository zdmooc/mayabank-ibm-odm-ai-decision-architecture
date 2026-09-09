# Itération 3 — Souscription, éligibilité et offre IARD

## Statut

**TERMINÉE — règles enrichies, tarification simple, garanties, exclusions, franchises, dataset synthétique et tests livrés.**

## Objectif

Faire évoluer le premier Decision Service d’éligibilité vers une décision de souscription IARD plus complète, tout en gardant des responsabilités métier séparées :

```text
Underwriting
  -> ACCEPT / REJECT / REVIEW
        |
        +--> Pricing
        |      -> base premium / coefficient / prime
        |
        +--> Policy configuration
               -> garanties / exclusions / franchise
```

L’objectif n’est pas de modéliser un produit d’assurance réel. Toutes les règles, primes, seuils et garanties sont fictifs.

## Décisions couvertes

### 1. Éligibilité

Réutilise `underwriting-eligibility` de l’Itération 1 :

- mineur -> `REJECT` ;
- dossier incomplet -> `REVIEW` ;
- permis très récent -> `REVIEW` ;
- sinistralité élevée -> `REVIEW` ;
- risque déclaré élevé -> `REVIEW` ;
- sinon -> `ACCEPT`.

### 2. Tarification simple

Pour les dossiers `ACCEPT`, le lab calcule une prime synthétique :

```text
prime = prime_de_base × coefficient_risque × coefficient_sinistres
```

La tarification est volontairement simple et déterministe afin de préparer un futur Decision Service `PremiumDecision` sous IBM ODM.

### 3. Garanties / exclusions / franchise

Le produit fictif `AUTO_STANDARD` possède :

- responsabilité civile : incluse ;
- assistance : incluse ;
- dommages : incluse si niveau de risque LOW ou MEDIUM ;
- exclusion fictive : aucun dommage optionnel pour risque HIGH ;
- franchise synthétique dépendant du niveau de risque.

## Artefacts

- `decision-services/underwriting-offer/README.md` ;
- `decision-services/underwriting-offer/pricing-table.csv` ;
- `decision-services/underwriting-offer/coverage-table.csv` ;
- `data/synthetic/iard-underwriting-cases.csv` ;
- `tools/validate_iteration_03.py`.

## Cas de non-régression

Le dataset inclut au minimum :

- acceptation standard ;
- rejet mineur ;
- revue dossier incomplet ;
- revue permis récent ;
- revue sinistralité ;
- revue risque élevé ;
- calcul d’une prime et d’une franchise pour un dossier accepté.

## Principe DDD / ODM

- **Underwriting** possède la décision d’éligibilité ;
- **Pricing** possède le calcul de prime ;
- **Policy** possède la configuration garanties/exclusions/franchise ;
- **IBM ODM** sera la plateforme d’exécution et de gouvernance de ces décisions, sans devenir propriétaire du sens métier.

## Validation locale portable

```bash
python tools/validate_iteration_03.py
```

Cette validation exécute une implémentation Python de référence afin de verrouiller la sémantique avant le futur lab IBM ODM.

## Critères de sortie

- [x] règles d’éligibilité couvertes ;
- [x] tarification simple déterministe ;
- [x] garanties / exclusions / franchises fictives ;
- [x] cas ACCEPT / REJECT / REVIEW ;
- [x] dataset synthétique versionné ;
- [x] tests de non-régression portables ;
- [x] séparation Underwriting / Pricing / Policy conservée ;
- [x] aucune donnée ni règle d’un assureur réel.

## Prochaine étape

**Itération 4 — Sinistre & fraude : couverture, franchise, score fraude simulé, human review et audit de décision.**
