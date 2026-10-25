---
type: community
cohesion: 0.50
members: 4
---

# Concorrência e snapshot de sessão

**Cohesion:** 0.50 - moderately connected
**Members:** 4 nodes

## Members
- [[Concorrencia BEGIN IMMEDIATE e conferencia de revisao]] - concept - api/README.md
- [[D1 snapshot_json como fonte da verdade da sessao]] - rationale - api/README.md
- [[D2 estado() registra perguntas, GET nao sobe revisao]] - rationale - api/README.md
- [[ordem_respostas no snapshot (reprocessar lotes na correcao)]] - concept - api/README.md

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Concorrência_e_snapshot_de_sessão
SORT file.name ASC
```
