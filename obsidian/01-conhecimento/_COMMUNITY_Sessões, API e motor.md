---
type: community
members: 18
---

# Sessões, API e motor

**Members:** 18 nodes

## Members
- [[Bandeira vermelha pausa, continuar, ver_parecer]] - concept - engine/README.md
- [[CF MYCIN com Fraction (sem arredondar para +-1)]] - rationale - engine/README.md
- [[Classe Sessao (dialogo, estado, correcao, modo)]] - concept - engine/README.md
- [[Concorrencia BEGIN IMMEDIATE e conferencia de revisao]] - concept - api/README.md
- [[Correcao reprocessa respostas em lotes na ordem real]] - concept - engine/README.md
- [[Correção e alertas respeitam ordem real dos lotes persistida]] - rationale - docs/entrega/05-apresentacao-e-demo.md
- [[D1 snapshot_json como fonte da verdade da sessao]] - rationale - api/README.md
- [[D2 estado() registra perguntas, GET nao sobe revisao]] - rationale - api/README.md
- [[D5 origem importacao reescrita pela API no como e no traco]] - rationale - api/README.md
- [[Explicacao por que e como (porquecomo)]] - concept - engine/README.md
- [[Importacao de animais CSVJSON sem 500]] - concept - api/README.md
- [[Nucleo sem estado inferir() e analisar()]] - concept - engine/README.md
- [[Observacoes com valor, cf e origem (resposta, ficha, importacao)]] - concept - engine/README.md
- [[Potencial conservador com intervalos inferiorsuperior]] - rationale - engine/README.md
- [[Sessao.restaurar  exportar sem replay]] - concept - engine/README.md
- [[Traco de inferencia e eventos (fato_adicionado, regra_disparada)]] - concept - engine/README.md
- [[Triagem obrigatoria por telas antes das perguntas dinamicas]] - concept - engine/README.md
- [[ordem_respostas no snapshot (reprocessar lotes na correcao)]] - concept - api/README.md

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Sessões_API_e_motor
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_Backend e isolamento do motor]]
- 1 edge to [[_COMMUNITY_Casos sintéticos na v0002]]
- 1 edge to [[_COMMUNITY_Demonstração e troca de modo]]
- 1 edge to [[_COMMUNITY_Parecer, retomada e limites]]
- 1 edge to [[_COMMUNITY_Plano histórico frontend implementado]]
- 1 edge to [[_COMMUNITY_Parecer e fatores de certeza]]
- 1 edge to [[_COMMUNITY_Versões e execução de casos]]

## Top bridge nodes
- [[Classe Sessao (dialogo, estado, correcao, modo)]] - degree 10, connects to 3 communities
- [[Correção e alertas respeitam ordem real dos lotes persistida]] - degree 3, connects to 2 communities
- [[Explicacao por que e como (porquecomo)]] - degree 4, connects to 1 community
- [[Bandeira vermelha pausa, continuar, ver_parecer]] - degree 3, connects to 1 community
- [[CF MYCIN com Fraction (sem arredondar para +-1)]] - degree 2, connects to 1 community