---
type: community
cohesion: 0.14
members: 14
---

# Decisões de reprocessamento

**Cohesion:** 0.14 - loosely connected
**Members:** 14 nodes

## Members
- [[Agenda e prioridades (bandeiras 100, urgências 50, evidências 10)]] - concept - docs/entrega/02-arquitetura.md
- [[Bandeira vermelha leva a chamar_agora]] - concept - docs/entrega/02-arquitetura.md
- [[Continuar respondendo após encerrar pelo alerta (R21)]] - concept - docs/entrega/02-arquitetura.md
- [[Correção por reprocessamento de prefixos na ordem real]] - concept - docs/entrega/02-arquitetura.md
- [[Critérios de parada]] - concept - docs/entrega/02-arquitetura.md
- [[Decisão ajustada TPB sem exigir febre (R-TPB-0204)]] - rationale - docs/entrega/01-processo.md
- [[Decisão ajustada grupo derivado max para leitecaneca]] - rationale - docs/entrega/01-processo.md
- [[Decisão ajustada reprocessar lotes na ordem real, não limpar bandeiras]] - rationale - docs/entrega/01-processo.md
- [[Decisão ajustada saída deve conter as inconclusivas esperadas]] - rationale - docs/entrega/01-processo.md
- [[Operador max em derivados positivos]] - concept - docs/entrega/02-arquitetura.md
- [[Seis telas de triagem antes das perguntas dinâmicas]] - concept - docs/entrega/02-arquitetura.md
- [[Seção Diálogo, parada e bandeiras]] - document - docs/entrega/02-arquitetura.md
- [[Seção Julgamento sobre sugestões da IA]] - document - docs/entrega/01-processo.md
- [[inferir(base, fatos) sem estado vs determinismo da sessão]] - concept - docs/entrega/02-arquitetura.md

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Decisões_de_reprocessamento
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_Diário de bordo 20-2110]]
- 2 edges to [[_COMMUNITY_Combinação MYCIN e blocos]]
- 2 edges to [[_COMMUNITY_Processo de desenvolvimento]]
- 1 edge to [[_COMMUNITY_Motor e API FastAPI]]
- 1 edge to [[_COMMUNITY_Decisões de seleção de perguntas]]
- 1 edge to [[_COMMUNITY_Fechamento de interface]]
- 1 edge to [[_COMMUNITY_Decisões rejeitadas e passos]]
- 1 edge to [[_COMMUNITY_Ausência de validação clínica]]

## Top bridge nodes
- [[Seção Julgamento sobre sugestões da IA]] - degree 8, connects to 4 communities
- [[Seção Diálogo, parada e bandeiras]] - degree 6, connects to 1 community
- [[Correção por reprocessamento de prefixos na ordem real]] - degree 3, connects to 1 community
- [[Agenda e prioridades (bandeiras 100, urgências 50, evidências 10)]] - degree 2, connects to 1 community
- [[Continuar respondendo após encerrar pelo alerta (R21)]] - degree 2, connects to 1 community