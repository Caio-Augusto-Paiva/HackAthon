---
type: community
cohesion: 0.18
members: 13
---

# Regras de IBR e pneumonia

**Cohesion:** 0.18 - loosely connected
**Members:** 13 nodes

## Members
- [[BoHV-1 detectado (pcr_bohv1)]] - concept - docs/entrega/03-regras-de-producao.md
- [[Crepitações à auscultação pulmonar (ausculta_crepitacoes)]] - concept - docs/entrega/03-regras-de-producao.md
- [[Olhos lacrimejando (olhos_lacrimejando)]] - concept - docs/entrega/03-regras-de-producao.md
- [[Pneumonia (pneumonia)]] - concept - docs/entrega/03-regras-de-producao.md
- [[Rinotraqueíte Infecciosa Bovina (IBR) (ibr)]] - concept - docs/entrega/03-regras-de-producao.md
- [[Seção Pneumonia (gravidade media)]] - concept - docs/entrega/03-regras-de-producao.md
- [[Seção Rinotraqueíte Infecciosa Bovina (IBR) (gravidade media)]] - concept - docs/entrega/03-regras-de-producao.md
- [[`R-IBR-02` olhos_lacrimejando = sim E febre = sim - ibr (CF 0,4)]] - concept - docs/entrega/03-regras-de-producao.md
- [[`R-IBR-03` pcr_bohv1 = sim - ibr (CF 0,9)]] - concept - docs/entrega/03-regras-de-producao.md
- [[`R-IBR-04` febre = sim E queda_producao = sim - ibr (CF 0,05)]] - concept - docs/entrega/03-regras-de-producao.md
- [[`R-IBR-05` ausculta_crepitacoes = sim - ibr (CF -0,3)]] - concept - docs/entrega/03-regras-de-producao.md
- [[`R-PNE-03` ausculta_crepitacoes = sim - pneumonia (CF 0,8)]] - concept - docs/entrega/03-regras-de-producao.md
- [[`R-PNE-05` febre = sim E apatia = sim - pneumonia (CF 0,1)]] - concept - docs/entrega/03-regras-de-producao.md

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Regras_de_IBR_e_pneumonia
SORT file.name ASC
```

## Connections to other communities
- 9 edges to [[_COMMUNITY_Regras de cetose e deslocamento]]
- 8 edges to [[_COMMUNITY_Camada 2 regras de doença]]
- 7 edges to [[_COMMUNITY_Regras de produção e CF]]
- 5 edges to [[_COMMUNITY_Hipocalcemia e periparto]]
- 2 edges to [[_COMMUNITY_Brucelose, PNCEBT e urgências]]
- 1 edge to [[_COMMUNITY_Regras do modo bovino urgente]]

## Top bridge nodes
- [[Rinotraqueíte Infecciosa Bovina (IBR) (ibr)]] - degree 10, connects to 4 communities
- [[Pneumonia (pneumonia)]] - degree 12, connects to 3 communities
- [[`R-PNE-05` febre = sim E apatia = sim - pneumonia (CF 0,1)]] - degree 5, connects to 3 communities
- [[`R-IBR-04` febre = sim E queda_producao = sim - ibr (CF 0,05)]] - degree 5, connects to 2 communities
- [[`R-IBR-02` olhos_lacrimejando = sim E febre = sim - ibr (CF 0,4)]] - degree 4, connects to 2 communities