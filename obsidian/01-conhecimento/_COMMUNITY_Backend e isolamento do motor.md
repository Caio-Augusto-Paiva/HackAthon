---
type: community
members: 12
---

# Backend e isolamento do motor

**Members:** 12 nodes

## Members
- [[API README (api)]] - document - api/README.md
- [[Arvore da secao 4.3 da especificacao (sessao, validacao, modelos)]] - concept - docs/revisoes/2026-10-21-revisao-motor.md
- [[Backend FastAPI + SQLite (casca fina sobre motor e kb)]] - concept - api/README.md
- [[Compatibilidade com o motor via para_motor (exclude_none)]] - concept - kb/README.md
- [[Decisao deterministica, sem LLM nem rede no caminho]] - rationale - api/README.md
- [[Demonstracao executavel (python -m engine) com base artificial]] - concept - engine/README.md
- [[Divergencias kb x motor (prioridade, layout, operadores ASCII)]] - concept - kb/README.md
- [[Host confiavel (TrustedHostMiddleware contra DNS rebinding)]] - concept - api/README.md
- [[Motor de inferencia README (engine)]] - document - engine/README.md
- [[Motor independente de web, banco, LLM e servicos externos]] - rationale - engine/README.md
- [[Organizacao dos modulos do motor]] - concept - engine/README.md
- [[kb como pacote folha (nao importa engine)]] - rationale - kb/README.md

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Backend_e_isolamento_do_motor
SORT file.name ASC
```

## Connections to other communities
- 3 edges to [[_COMMUNITY_Modelos e validação do kb]]
- 2 edges to [[_COMMUNITY_Sessões, API e motor]]
- 1 edge to [[_COMMUNITY_Demonstração e troca de modo]]
- 1 edge to [[_COMMUNITY_Snapshot e pressupostos do motor]]
- 1 edge to [[_COMMUNITY_Fontes canônicas e revisões]]
- 1 edge to [[_COMMUNITY_Entrega e manutenção documental]]

## Top bridge nodes
- [[Backend FastAPI + SQLite (casca fina sobre motor e kb)]] - degree 6, connects to 2 communities
- [[API README (api)]] - degree 3, connects to 2 communities
- [[Motor de inferencia README (engine)]] - degree 6, connects to 1 community
- [[Organizacao dos modulos do motor]] - degree 4, connects to 1 community
- [[Compatibilidade com o motor via para_motor (exclude_none)]] - degree 4, connects to 1 community