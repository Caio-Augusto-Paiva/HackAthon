---
type: community
cohesion: 0.12
members: 24
---

# Regras de metrite e retenção

**Cohesion:** 0.12 - loosely connected
**Members:** 24 nodes

## Members
- [[Aumento uterino à palpação (utero_aumentado_palpacao)]] - concept - docs/entrega/03-regras-de-producao.md
- [[Corrimento vaginal (corrimento_vaginal)]] - concept - docs/entrega/03-regras-de-producao.md
- [[Corrimento vaginal fétido (corrimento_fetido)]] - concept - docs/entrega/03-regras-de-producao.md
- [[Histórico de retenção de placenta (historico_retencao_placenta)]] - concept - docs/entrega/03-regras-de-producao.md
- [[Membranas retidas ao exame (palpacao_membranas_retidas)]] - concept - docs/entrega/03-regras-de-producao.md
- [[Metrite Puerperal (metrite)]] - concept - docs/entrega/03-regras-de-producao.md
- [[Placenta não saiu em 24 horas (placenta_nao_expulsa_24h)]] - concept - docs/entrega/03-regras-de-producao.md
- [[Puerpério (puerperio)]] - concept - docs/entrega/03-regras-de-producao.md
- [[Restos de placenta na vulva (membranas_expostas_vulva)]] - concept - docs/entrega/03-regras-de-producao.md
- [[Retenção de Placenta (retencao_placenta)]] - concept - docs/entrega/03-regras-de-producao.md
- [[Seção Metrite Puerperal (gravidade alta)]] - concept - docs/entrega/03-regras-de-producao.md
- [[Seção Retenção de Placenta (gravidade media)]] - concept - docs/entrega/03-regras-de-producao.md
- [[Tela de triagem 6 excrecoes (multipla)]] - concept - docs/entrega/03-regras-de-producao.md
- [[`R-MET-01` puerperio = sim E corrimento_fetido = sim - metrite (CF 0,75)]] - concept - docs/entrega/03-regras-de-producao.md
- [[`R-MET-02` corrimento_vaginal = sim E puerperio = sim E febre = sim - metrite (CF 0,45)]] - concept - docs/entrega/03-regras-de-producao.md
- [[`R-MET-03` puerperio = sim E utero_aumentado_palpacao = sim E corrimento_vaginal = sim - metrite (CF 0,35)]] - concept - docs/entrega/03-regras-de-producao.md
- [[`R-MET-04` historico_retencao_placenta = sim E puerperio = sim - metrite (CF 0,25)]] - concept - docs/entrega/03-regras-de-producao.md
- [[`R-RPL-01` puerperio = sim E membranas_expostas_vulva = sim - retencao_placenta (CF 0,8)]] - concept - docs/entrega/03-regras-de-producao.md
- [[`R-RPL-02` puerperio = sim E placenta_nao_expulsa_24h = sim - retencao_placenta (CF 0,7)]] - concept - docs/entrega/03-regras-de-producao.md
- [[`R-RPL-03` palpacao_membranas_retidas = sim - retencao_placenta (CF 0,9)]] - concept - docs/entrega/03-regras-de-producao.md
- [[`R-RPL-04` historico_retencao_placenta = sim E puerperio = sim - retencao_placenta (CF 0,35)]] - concept - docs/entrega/03-regras-de-producao.md
- [[`R-RPL-05` corrimento_vaginal = sim E puerperio = sim - retencao_placenta (CF 0,1)]] - concept - docs/entrega/03-regras-de-producao.md
- [[`R-RPL-06` dias_em_lactacao  7 - retencao_placenta (CF -0,5)]] - concept - docs/entrega/03-regras-de-producao.md
- [[`R-URG-04` metrite = sim CF ≥ 0,5 - chamar_agora (CF 0,99)]] - concept - docs/entrega/03-regras-de-producao.md

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Regras_de_metrite_e_retenção
SORT file.name ASC
```

## Connections to other communities
- 13 edges to [[_COMMUNITY_Regras de produção e CF]]
- 10 edges to [[_COMMUNITY_Camada 2 regras de doença]]
- 10 edges to [[_COMMUNITY_Regras de cetose e deslocamento]]
- 5 edges to [[_COMMUNITY_Hipocalcemia e periparto]]
- 3 edges to [[_COMMUNITY_Brucelose, PNCEBT e urgências]]
- 1 edge to [[_COMMUNITY_Regras de aborto e leptospirose]]
- 1 edge to [[_COMMUNITY_Regras do modo bovino urgente]]
- 1 edge to [[_COMMUNITY_Regras de acidose e BVD]]

## Top bridge nodes
- [[Puerpério (puerperio)]] - degree 11, connects to 3 communities
- [[Retenção de Placenta (retencao_placenta)]] - degree 11, connects to 3 communities
- [[Corrimento vaginal (corrimento_vaginal)]] - degree 7, connects to 3 communities
- [[Histórico de retenção de placenta (historico_retencao_placenta)]] - degree 5, connects to 3 communities
- [[Tela de triagem 6 excrecoes (multipla)]] - degree 4, connects to 3 communities