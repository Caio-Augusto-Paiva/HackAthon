---
type: community
cohesion: 0.18
members: 14
---

# Motor e API README

**Cohesion:** 0.18 - loosely connected
**Members:** 14 nodes

## Members
- [[dot-md em docs, CLAUDE.md, engineREADME]] - concept - AGENTS.md
- [[Arvore da secao 4.3 da especificacao (sessao, validacao, modelos)]] - concept - docs/revisoes/2026-10-21-revisao-motor.md
- [[Backend FastAPI + SQLite (casca fina sobre motor e kb)]] - concept - api/README.md
- [[CF MYCIN com Fraction (sem arredondar para +-1)]] - rationale - engine/README.md
- [[Compatibilidade com o motor via para_motor (exclude_none)]] - concept - kb/README.md
- [[Decisao deterministica, sem LLM nem rede no caminho]] - rationale - api/README.md
- [[Demonstracao executavel (python -m engine) com base artificial]] - concept - engine/README.md
- [[Divergencias kb x motor (prioridade, layout, operadores ASCII)]] - concept - kb/README.md
- [[Host confiavel (TrustedHostMiddleware contra DNS rebinding)]] - concept - api/README.md
- [[Motor de inferencia README (engine)]] - document - engine/README.md
- [[Motor independente de web, banco, LLM e servicos externos]] - rationale - engine/README.md
- [[Organizacao dos modulos do motor]] - concept - engine/README.md
- [[kb como pacote folha (nao importa engine)]] - rationale - kb/README.md
- [[python -m unittest discover -s testsengine -t .]] - concept - README.md

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Motor_e_API_README
SORT file.name ASC
```

## Connections to other communities
- 3 edges to [[_COMMUNITY_Pacote kb README]]
- 2 edges to [[_COMMUNITY_Executar demonstração local]]
- 2 edges to [[_COMMUNITY_Sessão, parecer e explicação]]
- 1 edge to [[_COMMUNITY_Arquitetura e instruções do projeto]]
- 1 edge to [[_COMMUNITY_Processo de desenvolvimento e IA]]
- 1 edge to [[_COMMUNITY_Manutenção do grafo]]
- 1 edge to [[_COMMUNITY_Revisão do motor]]

## Top bridge nodes
- [[Motor de inferencia README (engine)]] - degree 9, connects to 2 communities
- [[Backend FastAPI + SQLite (casca fina sobre motor e kb)]] - degree 5, connects to 2 communities
- [[CF MYCIN com Fraction (sem arredondar para +-1)]] - degree 3, connects to 2 communities
- [[Compatibilidade com o motor via para_motor (exclude_none)]] - degree 4, connects to 1 community
- [[kb como pacote folha (nao importa engine)]] - degree 3, connects to 1 community