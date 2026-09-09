# Vue C4 logique — MayaInsurance IARD Decision Platform

## System Context

```mermaid
flowchart LR
    USER[Gestionnaire / Souscripteur / Back Office]
    EXT[SI Assurance / Partenaires]
    PLATFORM[MayaInsurance IARD Decision Platform]
    HUMAN[Workflow de revue humaine]

    USER --> PLATFORM
    EXT --> PLATFORM
    PLATFORM --> HUMAN
```

## Container View

```mermaid
flowchart LR
    CH[Canaux / Back Office] --> API[Decision API]

    subgraph DOMAIN[Application métier IARD]
      UW[Underwriting Module]
      PR[Pricing Module]
      CL[Claim Module]
      FR[Fraud Module]
    end

    API --> UW
    API --> PR
    API --> CL
    API --> FR

    UW --> DEC[IBM ODM Decision Services]
    PR --> DEC
    CL --> DEC
    FR --> DEC

    FR --> ML[ML Scoring - futur]
    DOC[Document / GenAI - futur] --> UW

    DEC --> EVT[Event Publisher]
    DEC --> WF[Human Review]
    DEC --> AUD[Audit / Observability]
```

## Mapping DDD -> composants

| Bounded Context | Composant logique | Décision principale |
|---|---|---|
| Underwriting | Underwriting Module | UnderwritingEligibility |
| Pricing | Pricing Module | PremiumDecision |
| Claim | Claim Module | ClaimCoverageDecision |
| Fraud | Fraud Module | FraudReviewDecision |

## Point d'architecture

Cette vue C4 est **logique** : elle ne préjuge pas du nombre final de déploiements ou de microservices. Les frontières DDD sont conservées même si plusieurs modules sont empaquetés ensemble dans le POC local.
