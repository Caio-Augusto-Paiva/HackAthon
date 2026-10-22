---
type: community
members: 26
---

# Sessões, API e motor

**Members:** 26 nodes

## Members
- [[Bandeira vermelha pausa, continuar, ver_parecer]] - concept - engine/README.md
- [[Classe Sessao (dialogo, estado, correcao, modo)]] - concept - engine/README.md
- [[Comparacao de casos com a versao pai]] - concept - api/README.md
- [[Concorrencia BEGIN IMMEDIATE e conferencia de revisao]] - concept - api/README.md
- [[Correcao reprocessa respostas em lotes na ordem real]] - concept - engine/README.md
- [[Correção e alertas respeitam ordem real dos lotes persistida]] - rationale - docs/entrega/05-apresentacao-e-demo.md
- [[Cortes de bloco nao lidos de meta.limiares]] - concept - docs/revisoes/2026-10-21-revisao-motor.md
- [[D1 snapshot_json como fonte da verdade da sessao]] - rationale - api/README.md
- [[D2 estado() registra perguntas, GET nao sobe revisao]] - rationale - api/README.md
- [[D5 origem importacao reescrita pela API no como e no traco]] - rationale - api/README.md
- [[Explicacao por que e como (porquecomo)]] - concept - engine/README.md
- [[Importacao de animais CSVJSON sem 500]] - concept - api/README.md
- [[Intervalo neutro -0,2; 0,2 aparece como 0% sem evidencia]] - rationale - docs/superpowers/plans/2026-10-20-motor-secao-1.md
- [[Nucleo sem estado inferir() e analisar()]] - concept - engine/README.md
- [[Observacoes com valor, cf e origem (resposta, ficha, importacao)]] - concept - engine/README.md
- [[Percentual do parecer max(0, CF) x 100 (divergencia)]] - concept - docs/revisoes/2026-10-21-revisao-motor.md
- [[Percentual max(0,CF)100 e cortes de bloco por meta.limiares]] - concept - engine/README.md
- [[Portao de ativacao de versao (casos_falhando, confirmar_falhas)]] - concept - api/README.md
- [[Potencial conservador com intervalos inferiorsuperior]] - rationale - engine/README.md
- [[Sessao.restaurar  exportar sem replay]] - concept - engine/README.md
- [[Traco de inferencia e eventos (fato_adicionado, regra_disparada)]] - concept - engine/README.md
- [[Triagem obrigatoria por telas antes das perguntas dinamicas]] - concept - engine/README.md
- [[engine.casos.executar_caso (casos de teste reproduziveis)]] - concept - engine/README.md
- [[hipóteses desde segunda pergunta e explicação Por quê]] - concept - docs/superpowers/plans/2026-10-22-frontend-web.md
- [[ordem_respostas no snapshot (reprocessar lotes na correcao)]] - concept - api/README.md
- [[parecer() tres blocos, CF, percentuais, urgencia]] - concept - engine/README.md

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Sessões_API_e_motor
SORT file.name ASC
```

## Connections to other communities
- 3 edges to [[_COMMUNITY_Persistência e validação da base]]
- 2 edges to [[_COMMUNITY_Plano histórico frontend implementado]]
- 2 edges to [[_COMMUNITY_Parecer, alerta e retomada]]
- 1 edge to [[_COMMUNITY_Demonstração e troca de modo]]
- 1 edge to [[_COMMUNITY_Hipocalcemia e mobilidade]]

## Top bridge nodes
- [[Correção e alertas respeitam ordem real dos lotes persistida]] - degree 3, connects to 2 communities
- [[Classe Sessao (dialogo, estado, correcao, modo)]] - degree 10, connects to 1 community
- [[parecer() tres blocos, CF, percentuais, urgencia]] - degree 6, connects to 1 community
- [[Nucleo sem estado inferir() e analisar()]] - degree 4, connects to 1 community
- [[hipóteses desde segunda pergunta e explicação Por quê]] - degree 3, connects to 1 community