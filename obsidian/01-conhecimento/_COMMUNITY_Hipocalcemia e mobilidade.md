---
type: community
members: 15
---

# Hipocalcemia e mobilidade

**Members:** 15 nodes

## Members
- [[Cálcio sérico total (calcio_serico)]] - concept - docs/entrega/03-regras-de-producao.md
- [[DEV-BV-01 passou, chamar_agora, hipocalcemia]] - concept - docs/entrega/04-casos-de-teste.md
- [[DEV-MAS-01 passou, observar, mastite]] - concept - docs/entrega/04-casos-de-teste.md
- [[Decúbito (decubito)]] - concept - docs/entrega/03-regras-de-producao.md
- [[Desvio cervical em S (pescoco_em_s)]] - concept - docs/entrega/03-regras-de-producao.md
- [[Exemplos sintéticos de alerta e sinais mamários pela CLI]] - concept - base/desenvolvimento/LEIA-ME.txt
- [[Hipocalcemia Puerperal (hipocalcemia)]] - concept - docs/entrega/03-regras-de-producao.md
- [[Periparto imediato (periparto_imediato)]] - concept - docs/entrega/03-regras-de-producao.md
- [[R-BV-01 chamar_agora (CF 0,99)]] - concept - docs/entrega/03-regras-de-producao.md
- [[R-DER-01 periparto_imediato (CF 0,99)]] - concept - docs/entrega/03-regras-de-producao.md
- [[R-HIP-01 hipocalcemia (CF 0,65)]] - concept - docs/entrega/03-regras-de-producao.md
- [[R-HIP-02 hipocalcemia (CF 0,8)]] - concept - docs/entrega/03-regras-de-producao.md
- [[R-HIP-03 hipocalcemia (CF 0,9)]] - concept - docs/entrega/03-regras-de-producao.md
- [[R-URG-01 chamar_agora (CF 0,99)]] - concept - docs/entrega/03-regras-de-producao.md
- [[Reserva CLI estimada alerta, explicação, troca e snapshot sem banco]] - concept - docs/entrega/05-apresentacao-e-demo.md

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Hipocalcemia_e_mobilidade
SORT file.name ASC
```

## Connections to other communities
- 12 edges to [[_COMMUNITY_Regras e símbolos da v0002]]
- 9 edges to [[_COMMUNITY_Casos sintéticos na v0002]]
- 3 edges to [[_COMMUNITY_Integração e proveniência da base]]
- 2 edges to [[_COMMUNITY_Arquitetura do motor e base]]
- 2 edges to [[_COMMUNITY_Sinais térmicos e urgência]]
- 2 edges to [[_COMMUNITY_Bandeiras de urgência]]
- 1 edge to [[_COMMUNITY_Metrite e puerpério]]
- 1 edge to [[_COMMUNITY_Demonstração e troca de modo]]
- 1 edge to [[_COMMUNITY_Sessões, API e motor]]

## Top bridge nodes
- [[Reserva CLI estimada alerta, explicação, troca e snapshot sem banco]] - degree 6, connects to 4 communities
- [[Hipocalcemia Puerperal (hipocalcemia)]] - degree 9, connects to 3 communities
- [[R-BV-01 chamar_agora (CF 0,99)]] - degree 6, connects to 3 communities
- [[DEV-BV-01 passou, chamar_agora, hipocalcemia]] - degree 7, connects to 2 communities
- [[DEV-MAS-01 passou, observar, mastite]] - degree 6, connects to 2 communities