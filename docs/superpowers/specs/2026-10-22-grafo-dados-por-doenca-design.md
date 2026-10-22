# Grafo 2 — base separada por doença e grafo exato no Obsidian

Data: 22/10/2026. Aprovado em conversa pela equipe (fonte = arquivos por doença; abordagem A).

## Objetivo

1. Separar a base de conhecimento única (`base/versoes/vNNNN.json`) em um arquivo por doença mais um arquivo comum, e juntar de volta **sem perder nada**: `juntar(separar(v0002)) == v0002`.
2. Os arquivos separados (`base/fonte/`) passam a ser o que a equipe edita. Juntar gera a próxima versão pelo caminho que já existe (`Repositorio.salvar_nova`, que valida antes de gravar).
3. Construir o grafo 2 do Obsidian em `obsidian/02-Dados de Treino/` (pasta renomeada de `obsidian/02-a-definir/`) a partir desses arquivos, **sem IA**: nós e arestas saem do conversor exato `kb/grafo.py`.
4. Mostrar que o motor pode ler direto do grafo: carregar a base a partir do grafo exato e obter os mesmos resultados nos 34 casos clínicos.

## O que não muda

- Motor (`engine/`), API (`api/`), validador e casos. Nenhuma versão nova é ativada: a v0002 continua ativa.
- As versões em `base/versoes/` continuam imutáveis e são o que o motor e a API leem.
- “Dados de Treino” é o nome da pasta; o sistema não usa aprendizado de máquina.

## Por que o motor não lê o grafo do graphify

O `graph.json` de uma execução normal do graphify vem de extração por IA (arestas INFERRED/AMBIGUOUS, deduplicação por rótulo) e pode variar entre execuções. Ler dele quebraria a restrição de decisão determinística e auditável. O grafo que o motor pode ler é o **grafo exato** (`kb.grafo.Grafo`), que converte base ↔ grafo de forma 1:1. O graphify recebe esse mesmo grafo já pronto, todo EXTRACTED, e só cuida de comunidades, relatório, HTML e cofre do Obsidian.

## Componentes

### `kb/fonte.py` — separar e juntar

Formato em disco (`base/fonte/`):

- `comum.json`: `{"meta": …, "simbolos": […], "regras": […], "layout": {…}}`.
- `doencas/<id_da_doenca>.json`: `{"doenca": "<id>", "simbolos": […], "regras": […]}`.
- `indice.json`: `{"ordem_simbolos": [ids], "ordem_regras": [ids]}` — a ordem original, para a junção ser idêntica.

Regras de separação (determinísticas):

- “Uso” de uma doença D = símbolos nas condições das regras que concluem D, seguindo derivados transitivamente.
- Vai para o arquivo de D: o símbolo D; os símbolos usados **só** por D; as regras que concluem D; as regras que concluem um derivado exclusivo de D; as regras de urgência cujas condições citam D.
- Vai para `comum.json`: `meta`, `layout`, os demais símbolos (compartilhados, níveis de urgência, ficha, perguntas não usadas por doença) e as demais regras (bandeiras vermelhas, derivados compartilhados).

Junção:

- Une `comum.json` e todos os `doencas/*.json` (em ordem alfabética de arquivo).
- Erro claro se um id de símbolo ou de regra aparecer em mais de um arquivo, se um arquivo de doença não tiver o símbolo da doença com `tipo: doenca`, ou se o JSON for inválido.
- Ordena pelo `indice.json`; ids novos (não listados) entram depois, na ordem em que aparecem nos arquivos; ids do índice que sumiram são simplesmente removidos (edição legítima).
- Devolve um `kb.modelos.Base`.

API pública: `separar(base: Base) -> dict[str, dict]` (caminho relativo → conteúdo), `gravar_fonte(base, pasta)`, `ler_fonte(pasta) -> Base`.

CLI (`python -m kb.fonte`):

- `separar --versao v0002 [--destino base/fonte]` — escreve os arquivos.
- `juntar [--origem base/fonte]` — valida e compara com a versão ativa; imprime “idêntica à vNNNN” ou o que mudou (símbolos/regras adicionados, removidos, alterados).
- `juntar --salvar --autor X --nota "…"` — grava a próxima versão com `salvar_nova` (sem ativar).

Serialização igual à do repositório (`json` com `ensure_ascii=False`, indentação 2, `exclude_none`).

### `kb/exportar_grafo.py` — grafo exato e entrada do graphify

Sem dependência do graphify (o `kb` continua leve). A partir de `ler_fonte(pasta)`:

- `grafo_exato.json` = `base_para_grafo(base)` serializado (formato `kb.grafo.Grafo`).
- `extracao.json` no esquema do graphify: um nó por símbolo (`sim:<id>`) e por regra (`regra:<id>`), com `label` legível (nome do símbolo; `"<id>: SE … ENTÃO …"` para regra), `file_type: "concept"`, `source_file` = o arquivo de `base/fonte/` de onde veio; arestas `condicao_de` (símbolo → regra) e `conclui` (regra → símbolo, com `cf`), todas `confidence: "EXTRACTED"`.
- `carregar_do_grafo(caminho) -> Base`: lê `grafo_exato.json` e devolve `grafo_para_base(...)`.

CLI: `python -m kb.exportar_grafo [--origem base/fonte] [--saida graphify-out-dados]`.

### `scripts/grafo_dados.py` — cofre e visualização (roda com o Python do graphify)

Lê `graphify-out-dados/extracao.json`, monta o grafo dirigido com `graphify.build.build_from_json(..., dedup=False)`, agrupa comunidades, rotula cada comunidade pela doença predominante (ou “Comum”), grava `graph.json`, `GRAPH_REPORT.md` e `graph.html` em `graphify-out-dados/` e exporta o cofre para `obsidian/02-Dados de Treino/`. Custo de tokens: zero.

### Arrumação

- Renomear `obsidian/02-a-definir/` → `obsidian/02-Dados de Treino/` (o `README.md` atual é reescrito explicando o grafo 2 e como regenerá-lo).
- Atualizar `CLAUDE.md`, `AGENTS.md` e `.graphifyignore` (comentário do grafo 2; `base/fonte/` e `graphify-out-dados/` fora do grafo 1).

## Testes

- `tests/kb/test_fonte.py`:
  - ida e volta: `ler_fonte(gravar_fonte(v0002))` igual à v0002 (objeto e texto serializado);
  - 8 arquivos de doença, cada um com o símbolo da doença e suas regras de evidência e urgência; nenhum id repetido entre arquivos;
  - erros: id duplicado entre arquivos, arquivo de doença sem símbolo de doença, JSON inválido;
  - edição: regra nova num arquivo de doença aparece na base juntada; a base juntada passa no validador.
- `tests/kb/test_exportar_grafo.py`:
  - `carregar_do_grafo` devolve a v0002;
  - os 34 casos clínicos dão o mesmo resultado lendo a v0002 e lendo do grafo exato;
  - `extracao.json` passa no esquema do graphify (campos obrigatórios; toda aresta aponta para nó existente; tudo EXTRACTED).
- Suíte completa (`pytest`) verde.

## Fora de escopo

Mudar o motor para ler `base/fonte/` diretamente; ativar nova versão; editor gráfico; qualquer extração por IA dos dados das doenças.
