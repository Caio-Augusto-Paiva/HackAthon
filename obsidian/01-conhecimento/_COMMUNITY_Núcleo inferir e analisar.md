---
type: community
cohesion: 0.09
members: 31
---

# Núcleo inferir e analisar

**Cohesion:** 0.09 - loosely connected
**Members:** 31 nodes

## Members
- [[API, persistencia, interface e base clinica fora desta entrega]] - concept - engine/README.md
- [[CF internos Fraction (evita arredondar para +-1)]] - concept - engine/README.md
- [[Custo maior com muitos caminhos compartilhados; nao e otimizador global]] - concept - engine/README.md
- [[Decisoes e limites]] - concept - engine/README.md
- [[Doencas confirmadas nao se bloqueiam na parada por comorbidade]] - concept - engine/README.md
- [[Especificacao canonica prevalece sobre plano historico]] - concept - engine/README.md
- [[Eventos fato_adicionado com correcao e anterior; fatos origem regra]] - concept - engine/README.md
- [[Folhas compartilhadas particionadas para rejeitar contradicoes]] - concept - engine/README.md
- [[Guardas rejeitam camadas invalidas, referencias, pesos extremos, observacoes invalidas]] - concept - engine/README.md
- [[Inferencia so conta urgenciabandeira com CF final  0]] - concept - engine/README.md
- [[Modulo engine.avaliacao]] - code - engine/README.md
- [[Modulo engine.cf]] - code - engine/README.md
- [[Modulo engine.explicacao]] - code - engine/README.md
- [[Modulo engine.inferencia]] - code - engine/README.md
- [[Modulo engine.memoria]] - code - engine/README.md
- [[Modulo engine.modelos]] - code - engine/README.md
- [[Modulo engine.parada]] - code - engine/README.md
- [[Modulo engine.parecer]] - code - engine/README.md
- [[Modulo engine.selecao]] - code - engine/README.md
- [[Modulo engine.sessao]] - code - engine/README.md
- [[Modulo engine.traco]] - code - engine/README.md
- [[Modulo engine.validacao]] - code - engine/README.md
- [[Organizacao de modulos]] - concept - engine/README.md
- [[Perguntas que confirmam bandeiras pendentes tem precedencia]] - concept - engine/README.md
- [[Potencial regra uma vez, intervalos inferiorsuperior, conservador]] - concept - engine/README.md
- [[Urgenciabandeira exigem CF  0 (ValueError)]] - concept - engine/README.md
- [[Validacao editorial completa em kb]] - concept - engine/README.md
- [[analisar(base, fatos, modo)]] - concept - docs/entrega/02-arquitetura.md
- [[analisar(base, fatos, modo) potencial, viabilidade, escolha de perguntas]] - concept - engine/README.md
- [[inferir(base, fatos)]] - concept - docs/entrega/02-arquitetura.md
- [[inferir(base, fatos) sem estado; recalcula sem reaplicar evidencias]] - concept - engine/README.md

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Núcleo_inferir_e_analisar
SORT file.name ASC
```

## Connections to other communities
- 5 edges to [[_COMMUNITY_Contratos Python e restauração]]
- 4 edges to [[_COMMUNITY_Agenda e propagação MYCIN]]
- 3 edges to [[_COMMUNITY_API da sessão do motor]]
- 3 edges to [[_COMMUNITY_Testes e evidências]]
- 2 edges to [[_COMMUNITY_Diálogo, parada e bandeiras]]

## Top bridge nodes
- [[Decisoes e limites]] - degree 16, connects to 3 communities
- [[Organizacao de modulos]] - degree 15, connects to 2 communities
- [[CF internos Fraction (evita arredondar para +-1)]] - degree 4, connects to 2 communities
- [[analisar(base, fatos, modo)]] - degree 3, connects to 2 communities
- [[inferir(base, fatos)]] - degree 3, connects to 2 communities