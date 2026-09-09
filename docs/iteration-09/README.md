# Itération 9 — MCP & Agentic AI gouvernés

## Statut

**TERMINÉE — catalogue de tools MCP, politiques de scopes, serveur portable, audit et garde-fous agentiques livrés.**

## Objectif

Permettre à un agent d'accéder aux Decision Services IARD via des tools gouvernés sans lui donner l'autorité de prendre ou d'exécuter seul une décision sensible.

```text
Agent / Copilot
      ↓
MCP Client
      ↓
MCP Decision Server
 tools/list + tools/call
 scopes + policy + audit
      ↓
Decision API
      ↓
IBM ODM / Decision Services
      ↓
Decision résultat
      ↓
Agent présente / explique / route
```

## Référence protocole

Le lab cible **MCP 2026-07-28** et retient les principes utiles à une architecture entreprise :

- cœur stateless ;
- requêtes auto-descriptives ;
- autorisation explicite ;
- tools listables et appelables ;
- contrôles d'accès indépendants du raisonnement de l'agent ;
- audit de chaque appel.

Le serveur portable de cette itération ne prétend pas implémenter l'intégralité du protocole réseau MCP. Il verrouille la sémantique des tools, permissions et garde-fous avant le futur déploiement.

## Tools v1

- `underwriting_decision` — scope `decision:underwriting` ;
- `claim_decision` — scope `decision:claim` ;
- `decision_audit_lookup` — scope `decision:audit.read`.

## Garde-fous

- aucun tool ne permet `approve`, `pay`, `reject-final`, `override-rule` ou `deploy` ;
- un agent ne peut pas contourner ODM ou le Decision Engine ;
- scopes vérifiés côté serveur ;
- payloads validés ;
- correlation ID et toolCall ID obligatoires ;
- audit append-only de laboratoire ;
- aucune chaîne de tools ne transforme automatiquement un résultat `REVIEW` en décision finale ;
- les opérations sensibles restent human-in-the-loop.

## Livrables

- `mcp/tool-policy.json` ;
- `mcp/decision_mcp_server.py` ;
- `data/synthetic/mcp-tool-calls.jsonl` ;
- `tests/test_mcp_guardrails.py` ;
- `architecture/mcp-agentic-ai.md`.

## Validation portable

```bash
python mcp/decision_mcp_server.py --list-tools
python mcp/decision_mcp_server.py --demo
python -m unittest tests/test_mcp_guardrails.py
```

## Critères de sortie

- [x] Decision Services exposés comme tools ;
- [x] permissions/scopes explicites ;
- [x] audit des tool calls ;
- [x] correlation ID / toolCall ID ;
- [x] refus d'un scope insuffisant ;
- [x] aucun tool d'override ou d'exécution sensible ;
- [x] human review conservée ;
- [x] architecture compatible avec une cible MCP stateless ;
- [x] aucun serveur MCP de production revendiqué comme exécuté.

## Prochaine étape

**Itération 10 — OpenShift Local / CRC : déploiement des composants portables, Services/Routes, ConfigMaps/Secrets, policies, probes et tests E2E locaux avec preuves.**
