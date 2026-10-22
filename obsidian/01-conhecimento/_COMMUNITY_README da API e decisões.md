---
type: community
cohesion: 0.06
members: 42
---

# README da API e decisões

**Cohesion:** 0.06 - loosely connected
**Members:** 42 nodes

## Members
- [[API README (api)]] - document - api/README.md
- [[Arvore da secao 4.3 da especificacao (sessao, validacao, modelos)]] - concept - docs/revisoes/2026-10-21-revisao-motor.md
- [[Backend FastAPI + SQLite (casca fina sobre motor e kb)]] - concept - api/README.md
- [[Bandeira vermelha pausa, continuar, ver_parecer]] - concept - engine/README.md
- [[CF MYCIN com Fraction (sem arredondar para +-1)]] - rationale - engine/README.md
- [[Classe Sessao (dialogo, estado, correcao, modo)]] - concept - engine/README.md
- [[Compatibilidade com o motor via para_motor (exclude_none)]] - concept - kb/README.md
- [[Concorrencia BEGIN IMMEDIATE e conferencia de revisao]] - concept - api/README.md
- [[Correcao reprocessa respostas em lotes na ordem real]] - concept - engine/README.md
- [[Cortes de bloco nao lidos de meta.limiares]] - concept - docs/revisoes/2026-10-21-revisao-motor.md
- [[D1 snapshot_json como fonte da verdade da sessao]] - rationale - api/README.md
- [[D2 estado() registra perguntas, GET nao sobe revisao]] - rationale - api/README.md
- [[D5 origem importacao reescrita pela API no como e no traco]] - rationale - api/README.md
- [[Decisao deterministica, sem LLM nem rede no caminho]] - rationale - api/README.md
- [[Demonstracao executavel (python -m engine) com base artificial]] - concept - engine/README.md
- [[Divergencias kb x motor (prioridade, layout, operadores ASCII)]] - concept - kb/README.md
- [[Especificacao autorizada da secao 1 (docspromptssecao-1.md)]] - document - docs/superpowers/plans/2026-10-20-motor-secao-1.md
- [[Especificacao canonica do projeto (anamnese bovinos)]] - document - docs/revisoes/2026-10-21-revisao-motor.md
- [[Evidencia final 56 testes sem falhas]] - concept - docs/superpowers/plans/2026-10-20-motor-secao-1.md
- [[Explicacao por que e como (porquecomo)]] - concept - engine/README.md
- [[Ficha com null tratada como nao sei (deve ser ausente)]] - concept - docs/revisoes/2026-10-21-revisao-motor.md
- [[Focos da revisao (sem valor, contradicoes, loops, bandeiras)]] - concept - docs/superpowers/plans/2026-10-20-motor-secao-1.md
- [[Host confiavel (TrustedHostMiddleware contra DNS rebinding)]] - concept - api/README.md
- [[Importacao de animais CSVJSON sem 500]] - concept - api/README.md
- [[Intervalo neutro -0,2; 0,2 aparece como 0% sem evidencia]] - rationale - docs/superpowers/plans/2026-10-20-motor-secao-1.md
- [[Motor de inferencia README (engine)]] - document - engine/README.md
- [[Motor independente de web, banco, LLM e servicos externos]] - rationale - engine/README.md
- [[Nucleo sem estado inferir() e analisar()]] - concept - engine/README.md
- [[Observacoes com valor, cf e origem (resposta, ficha, importacao)]] - concept - engine/README.md
- [[Organizacao dos modulos do motor]] - concept - engine/README.md
- [[Percentual do parecer max(0, CF) x 100 (divergencia)]] - concept - docs/revisoes/2026-10-21-revisao-motor.md
- [[Percentual max(0,CF)100 e cortes de bloco por meta.limiares]] - concept - engine/README.md
- [[Plano de implementacao do motor (secao 1)]] - document - docs/superpowers/plans/2026-10-20-motor-secao-1.md
- [[Potencial conservador com intervalos inferiorsuperior]] - rationale - engine/README.md
- [[Revisao do motor de inferencia (21102026)]] - document - docs/revisoes/2026-10-21-revisao-motor.md
- [[Sessao.restaurar  exportar sem replay]] - concept - engine/README.md
- [[Tabela de conformidade com a especificacao (16 itens)]] - concept - docs/revisoes/2026-10-21-revisao-motor.md
- [[Traco de inferencia e eventos (fato_adicionado, regra_disparada)]] - concept - engine/README.md
- [[Triagem obrigatoria por telas antes das perguntas dinamicas]] - concept - engine/README.md
- [[kb como pacote folha (nao importa engine)]] - rationale - kb/README.md
- [[ordem_respostas no snapshot (reprocessar lotes na correcao)]] - concept - api/README.md
- [[parecer() tres blocos, CF, percentuais, urgencia]] - concept - engine/README.md

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/README_da_API_e_decisões
SORT file.name ASC
```

## Connections to other communities
- 4 edges to [[_COMMUNITY_Versões da base, casos e execução local]]

## Top bridge nodes
- [[Classe Sessao (dialogo, estado, correcao, modo)]] - degree 10, connects to 1 community
- [[Backend FastAPI + SQLite (casca fina sobre motor e kb)]] - degree 5, connects to 1 community
- [[Compatibilidade com o motor via para_motor (exclude_none)]] - degree 4, connects to 1 community
- [[kb como pacote folha (nao importa engine)]] - degree 3, connects to 1 community