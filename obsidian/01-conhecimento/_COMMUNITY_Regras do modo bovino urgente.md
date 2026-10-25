---
type: community
cohesion: 0.14
members: 23
---

# Regras do modo bovino urgente

**Cohesion:** 0.14 - loosely connected
**Members:** 23 nodes

## Members
- [[Apatia (apatia)]] - concept - docs/entrega/03-regras-de-producao.md
- [[Atendimento Veterinário Imediato (chamar_agora)]] - concept - docs/entrega/03-regras-de-producao.md
- [[Camada 3 - Bandeiras vermelhas]] - concept - docs/entrega/03-regras-de-producao.md
- [[Conteúdo espumoso na sonda (espuma_sonda)]] - concept - docs/entrega/03-regras-de-producao.md
- [[Gás livre na sonda (gas_livre_sonda)]] - concept - docs/entrega/03-regras-de-producao.md
- [[Seção Timpanismo Espumoso (gravidade alta)]] - concept - docs/entrega/03-regras-de-producao.md
- [[Seção Timpanismo Gasoso (gravidade alta)]] - concept - docs/entrega/03-regras-de-producao.md
- [[Timpanismo Espumoso (timpanismo_espumoso)]] - concept - docs/entrega/03-regras-de-producao.md
- [[Timpanismo Gasoso (timpanismo_gasoso)]] - concept - docs/entrega/03-regras-de-producao.md
- [[`R-BV-01` decubito = sim - chamar_agora (CF 0,99)]] - concept - docs/entrega/03-regras-de-producao.md
- [[`R-BV-02` urina_escura = sim - chamar_agora (CF 0,99)]] - concept - docs/entrega/03-regras-de-producao.md
- [[`R-BV-03` apetite = ausente E apatia = sim - chamar_agora (CF 0,99)]] - concept - docs/entrega/03-regras-de-producao.md
- [[`R-BV-04` hipotermia = sim E apatia = sim - chamar_agora (CF 0,99)]] - concept - docs/entrega/03-regras-de-producao.md
- [[`R-BV-05` ubere_inflamado = sim E febre = sim E apatia = sim - chamar_agora (CF 0,99)]] - concept - docs/entrega/03-regras-de-producao.md
- [[`R-BV-06` temperatura_retal ≥ 41 - chamar_agora (CF 0,99)]] - concept - docs/entrega/03-regras-de-producao.md
- [[`R-TES-03` espuma_sonda = sim - timpanismo_espumoso (CF 0,9)]] - concept - docs/entrega/03-regras-de-producao.md
- [[`R-TES-04` apetite = ausente E queda_producao = sim - timpanismo_espumoso (CF 0,05)]] - concept - docs/entrega/03-regras-de-producao.md
- [[`R-TES-05` gas_livre_sonda = sim - timpanismo_espumoso (CF -0,7)]] - concept - docs/entrega/03-regras-de-producao.md
- [[`R-TGA-03` gas_livre_sonda = sim - timpanismo_gasoso (CF 0,9)]] - concept - docs/entrega/03-regras-de-producao.md
- [[`R-TGA-04` apetite = ausente E apatia = sim - timpanismo_gasoso (CF 0,05)]] - concept - docs/entrega/03-regras-de-producao.md
- [[`R-TGA-05` espuma_sonda = sim - timpanismo_gasoso (CF -0,7)]] - concept - docs/entrega/03-regras-de-producao.md
- [[`R-URG-10` timpanismo_espumoso = sim CF ≥ 0,5 - chamar_agora (CF 0,99)]] - concept - docs/entrega/03-regras-de-producao.md
- [[`R-URG-11` timpanismo_gasoso = sim CF ≥ 0,5 - chamar_agora (CF 0,99)]] - concept - docs/entrega/03-regras-de-producao.md

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Regras_do_modo_bovino_urgente
SORT file.name ASC
```

## Connections to other communities
- 14 edges to [[_COMMUNITY_Regras de cetose e deslocamento]]
- 11 edges to [[_COMMUNITY_Regras de produção e CF]]
- 10 edges to [[_COMMUNITY_Camada 2 regras de doença]]
- 8 edges to [[_COMMUNITY_Hipocalcemia e periparto]]
- 4 edges to [[_COMMUNITY_Brucelose, PNCEBT e urgências]]
- 1 edge to [[_COMMUNITY_Regras de IBR e pneumonia]]
- 1 edge to [[_COMMUNITY_Regras de metrite e retenção]]
- 1 edge to [[_COMMUNITY_Regras de acidose e BVD]]
- 1 edge to [[_COMMUNITY_Regras de aborto e leptospirose]]
- 1 edge to [[_COMMUNITY_TPB e derivado febre]]
- 1 edge to [[_COMMUNITY_Reticulopericardite traumática]]

## Top bridge nodes
- [[Atendimento Veterinário Imediato (chamar_agora)]] - degree 21, connects to 10 communities
- [[Apatia (apatia)]] - degree 9, connects to 4 communities
- [[`R-TES-04` apetite = ausente E queda_producao = sim - timpanismo_espumoso (CF 0,05)]] - degree 5, connects to 3 communities
- [[`R-TGA-04` apetite = ausente E apatia = sim - timpanismo_gasoso (CF 0,05)]] - degree 5, connects to 3 communities
- [[Timpanismo Espumoso (timpanismo_espumoso)]] - degree 11, connects to 2 communities