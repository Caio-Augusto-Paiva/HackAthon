---
type: community
cohesion: 0.17
members: 16
---

# Diálogo, parada e bandeiras

**Cohesion:** 0.17 - loosely connected
**Members:** 16 nodes

## Members
- [[Bandeira ativa - chamar_agora]] - concept - docs/entrega/02-arquitetura.md
- [[Correcao por reprocessamento de prefixos de lotes na ordem real de entrada]] - concept - docs/entrega/02-arquitetura.md
- [[Correcao testada em Sessao (kb.Caso nao codifica)]] - concept - docs/entrega/02-arquitetura.md
- [[Criterios de parada (confirmacao, concorrentes, potencial, bandeiras, sem perguntas, limite)]] - concept - docs/entrega/02-arquitetura.md
- [[Determinismo da sessao mesma base, valores, ordem e acoes]] - concept - docs/entrega/02-arquitetura.md
- [[Dialogo, parada e bandeiras]] - concept - docs/entrega/02-arquitetura.md
- [[Fase dinamica limitada a 1225 perguntas]] - concept - docs/entrega/02-arquitetura.md
- [[Preferencia a perguntas que confirmam bandeira pendente]] - concept - docs/entrega/02-arquitetura.md
- [[Produtor recebe pausa; veterinario nao]] - concept - docs/entrega/02-arquitetura.md
- [[R15R16 do registro de riscos (desvios do caso de abomaso)]] - concept - docs/entrega/02-arquitetura.md
- [[Reconhecimento vale so para bandeiras ativas]] - concept - docs/entrega/02-arquitetura.md
- [[Respostas novas nao reduzem urgencia travada]] - concept - docs/entrega/02-arquitetura.md
- [[Seis telas de triagem antes das perguntas dinamicas]] - concept - docs/entrega/02-arquitetura.md
- [[Selecao e parada]] - concept - docs/entrega/02-arquitetura.md
- [[Veterinarios nao sao pausados]] - concept - engine/README.md
- [[inferir(base, fatos) sem estado]] - concept - docs/entrega/02-arquitetura.md

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Diálogo_parada_e_bandeiras
SORT file.name ASC
```

## Connections to other communities
- 3 edges to [[_COMMUNITY_Componentes do modelo conceitual]]
- 2 edges to [[_COMMUNITY_Núcleo inferir e analisar]]
- 2 edges to [[_COMMUNITY_Contratos Python e restauração]]
- 2 edges to [[_COMMUNITY_API da sessão do motor]]
- 2 edges to [[_COMMUNITY_Base v0005 e validação]]
- 1 edge to [[_COMMUNITY_API, explicação e camada web]]

## Top bridge nodes
- [[Dialogo, parada e bandeiras]] - degree 13, connects to 2 communities
- [[Selecao e parada]] - degree 5, connects to 2 communities
- [[Correcao por reprocessamento de prefixos de lotes na ordem real de entrada]] - degree 5, connects to 1 community
- [[Produtor recebe pausa; veterinario nao]] - degree 4, connects to 1 community
- [[Correcao testada em Sessao (kb.Caso nao codifica)]] - degree 3, connects to 1 community