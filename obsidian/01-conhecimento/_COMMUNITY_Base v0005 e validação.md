---
type: community
cohesion: 0.12
members: 23
---

# Base v0005 e validação

**Cohesion:** 0.12 - loosely connected
**Members:** 23 nodes

## Members
- [[103 simbolos, 137 regras (111 evidencia, 20 urgencia, 6 bandeiras), 20 doencas]] - concept - docs/entrega/02-arquitetura.md
- [[2 pares em meta.exclusoes]] - concept - docs/entrega/02-arquitetura.md
- [[Base ativa meta, simbolos, regras, layout]] - concept - docs/entrega/02-arquitetura.md
- [[Base, validacao e rastreabilidade]] - concept - docs/entrega/02-arquitetura.md
- [[Documento 03 gerado do JSON; 04 da execucao dos casos]] - concept - docs/entrega/02-arquitetura.md
- [[Dominios numericos (dias 0-1000, temp 30-45, pH 0-14, BHB e calcio 0-20)]] - concept - docs/entrega/02-arquitetura.md
- [[Eventos documentam observacoes, regras e combinacoes de CF]] - concept - docs/entrega/02-arquitetura.md
- [[Motivo teste manual dava 0% pois toda regra era conjuncao]] - concept - docs/entrega/02-arquitetura.md
- [[Regras de sinal isolado R-HIP-05, R-HIP-06, R-CET-06, R-DAB-04, R-ACI-05]] - concept - docs/entrega/02-arquitetura.md
- [[Repositorio.salvar_nova(..., pai=...)]] - concept - docs/entrega/02-arquitetura.md
- [[Teste de sincronismo doc x regra executavel]] - concept - docs/entrega/02-arquitetura.md
- [[Traco de eventos]] - concept - docs/entrega/02-arquitetura.md
- [[Tratamento por doenca com texto, fonte e URL (embrapa.br, gov.br, msdvetmanual.com)]] - concept - docs/entrega/02-arquitetura.md
- [[Versao v0001 (nao promovida a clinicamente validada)]] - concept - docs/entrega/02-arquitetura.md
- [[Versao v0002 (56 regras, da branch compartilhada)]] - concept - docs/entrega/02-arquitetura.md
- [[Versao v0003 (cinco regras de sinal isolado)]] - concept - docs/entrega/02-arquitetura.md
- [[Versao v0004 (51 simbolos, 61 regras, 8 doencas; renomeia derivados com acento)]] - concept - docs/entrega/02-arquitetura.md
- [[Versao v0005 (ativa, pai v0004)]] - concept - docs/entrega/02-arquitetura.md
- [[baseativa.json (v0005 imutavel)]] - concept - docs/entrega/02-arquitetura.md
- [[basefontecomum.json e doencasdoenca.json (20 arquivos) com indice.json]] - concept - docs/entrega/02-arquitetura.md
- [[casas_decimais nao exposto; precisao validada no backend (R18)]] - concept - docs/entrega/02-arquitetura.md
- [[juntar reproduziu v0002 byte a byte]] - concept - docs/entrega/02-arquitetura.md
- [[python -m kb.fonte juntar --salvar]] - concept - docs/entrega/02-arquitetura.md

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Base_v0005_e_validação
SORT file.name ASC
```

## Connections to other communities
- 7 edges to [[_COMMUNITY_Componentes do modelo conceitual]]
- 2 edges to [[_COMMUNITY_API, explicação e camada web]]
- 2 edges to [[_COMMUNITY_Diálogo, parada e bandeiras]]
- 2 edges to [[_COMMUNITY_Fonte separada por doença]]
- 1 edge to [[_COMMUNITY_Testes e evidências]]
- 1 edge to [[_COMMUNITY_Agenda e propagação MYCIN]]

## Top bridge nodes
- [[Base, validacao e rastreabilidade]] - degree 24, connects to 4 communities
- [[Traco de eventos]] - degree 3, connects to 2 communities
- [[python -m kb.fonte juntar --salvar]] - degree 5, connects to 1 community
- [[baseativa.json (v0005 imutavel)]] - degree 3, connects to 1 community
- [[casas_decimais nao exposto; precisao validada no backend (R18)]] - degree 2, connects to 1 community