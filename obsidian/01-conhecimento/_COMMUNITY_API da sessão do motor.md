---
type: community
cohesion: 0.09
members: 24
---

# API da sessão do motor

**Cohesion:** 0.09 - loosely connected
**Members:** 24 nodes

## Members
- [[Campos null da ficha sao ausentes e perguntaveis]] - concept - engine/README.md
- [[Correcao nao consome outra pergunta]] - concept - engine/README.md
- [[Formato {doenca, nome, gravidade, cf_atual, regras}]] - concept - engine/README.md
- [[Limite opcional substitui so o desta sessao]] - concept - engine/README.md
- [[Nao implementa por que nao e a doenca X]] - concept - engine/README.md
- [[Nao se pode injetar doencasderivados como fatos]] - concept - engine/README.md
- [[Observacao {valor, cf, origem}; origens resposta, ficha, importacao]] - concept - engine/README.md
- [[Reconhecimento mantido so para ativas; reativada pausa de novo]] - concept - engine/README.md
- [[Repetir responder() seria incorreto (correcao altera selecao)]] - concept - engine/README.md
- [[Selecao multipla lista de ids ou mapa de booleanos]] - concept - engine/README.md
- [[Sessao(base, modo, ficha, limite_dinamico)]] - concept - engine/README.md
- [[acao_bandeira('continuar''ver_parecer')]] - concept - engine/README.md
- [[como(simbolo)]] - concept - engine/README.md
- [[como evidencias disparadas, derivados e origem]] - concept - engine/README.md
- [[estado()]] - concept - engine/README.md
- [[estado, responder_triagem, responder, trocar_modo, acao_bandeira]] - concept - docs/entrega/02-arquitetura.md
- [[limite_dinamico=0 nos dois exemplos (so triagem)]] - concept - docs/entrega/02-arquitetura.md
- [[nao_sei  None  nao sei = desconhecimento (CF 0, conta como respondida)]] - concept - engine/README.md
- [[porque na triagem origem triagem, motivo, serve_a]] - concept - engine/README.md
- [[porque(simbolo)]] - concept - engine/README.md
- [[responder(simbolo, valor, corrigir)]] - concept - engine/README.md
- [[responder_triagem(id, resposta, corrigir)]] - concept - engine/README.md
- [[trocar_modo preserva fatos, contagem e motivos]] - concept - engine/README.md
- [[trocar_modo('veterinario')]] - concept - engine/README.md

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/API_da_sessão_do_motor
SORT file.name ASC
```

## Connections to other communities
- 5 edges to [[_COMMUNITY_Contratos Python e restauração]]
- 3 edges to [[_COMMUNITY_Núcleo inferir e analisar]]
- 2 edges to [[_COMMUNITY_Diálogo, parada e bandeiras]]
- 1 edge to [[_COMMUNITY_Agenda e propagação MYCIN]]

## Top bridge nodes
- [[Sessao(base, modo, ficha, limite_dinamico)]] - degree 15, connects to 3 communities
- [[acao_bandeira('continuar''ver_parecer')]] - degree 4, connects to 2 communities
- [[como(simbolo)]] - degree 4, connects to 1 community
- [[limite_dinamico=0 nos dois exemplos (so triagem)]] - degree 3, connects to 1 community
- [[porque(simbolo)]] - degree 3, connects to 1 community