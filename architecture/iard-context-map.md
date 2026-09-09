# Context Map — MayaInsurance IARD

```mermaid
flowchart TB
    subgraph CORE[Core Domains]
      UW[Underwriting]
      PR[Pricing]
      CL[Claim]
      FR[Fraud]
    end

    subgraph SUPPORT[Supporting Domains]
      PA[Party]
      PO[Policy]
      DO[Document]
    end

    subgraph PLATFORM[Decision & Integration Platform]
      API[Decision API]
      ODM[IBM ODM]
      EVT[Events]
      WF[Human Review]
    end

    PA --> UW
    DO --> UW
    UW --> PR
    UW --> PO
    PO --> CL
    CL --> FR
    FR --> CL

    UW -. decision policy .-> API
    PR -. decision policy .-> API
    CL -. decision policy .-> API
    FR -. decision policy .-> API
    API --> ODM
    ODM --> EVT
    ODM --> WF
```

## Relations principales

- **Party -> Underwriting** : fournit l'identité et les informations utiles à la demande.
- **Document -> Underwriting** : fournit des données structurées issues des pièces ; GenAI pourra enrichir ce flux ultérieurement.
- **Underwriting -> Pricing** : une demande éligible peut déclencher un calcul de prime.
- **Underwriting -> Policy** : une acceptation permet la préparation/création d'un contrat.
- **Policy -> Claim** : Claim consulte le contexte de couverture nécessaire à la décision de sinistre.
- **Claim <-> Fraud** : Claim demande une évaluation ; Fraud retourne un résultat/score, sans devenir propriétaire de la décision de couverture.

## Anti-pattern évité

Ne pas créer un bounded context `ODM` ou `Rules` : ce sont des capacités techniques. La responsabilité métier reste dans Underwriting, Pricing, Claim ou Fraud.
