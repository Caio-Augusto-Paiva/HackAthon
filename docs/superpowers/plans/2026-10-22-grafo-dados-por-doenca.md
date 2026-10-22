# Grafo 2 — base por doença Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Separar a base em arquivos por doença com junção exata, gerar o grafo 2 do Obsidian sem IA e provar que o motor lê do grafo exato.

**Architecture:** `kb/fonte.py` separa/junta (`base/fonte/`); `kb/exportar_grafo.py` gera o grafo exato (`kb.grafo`) e a extração no esquema do graphify, sem importar graphify; `scripts/grafo_dados.py`, rodado com o Python do graphify, monta comunidades, HTML, relatório e o cofre em `obsidian/02-Dados de Treino/`.

**Tech Stack:** Python 3.12, Pydantic (`kb.modelos`), pytest; graphify (Python separado, só no script).

**Spec:** `docs/superpowers/specs/2026-10-22-grafo-dados-por-doenca-design.md`

## Global Constraints

- Motor, API, validador e casos não mudam; v0002 continua ativa; nada em `base/versoes/` é alterado.
- `kb/` não importa `graphify`.
- Serialização JSON: `json.dumps(..., ensure_ascii=False, indent=2) + "\n"`, `model_dump(mode="json", exclude_none=True)` (igual a `kb.carregador._json`).
- Pasta do cofre: `obsidian/02-Dados de Treino/` (com espaço). Saída do graphify: `graphify-out-dados/`.
- Todas as arestas da extração com `confidence: "EXTRACTED"`; custo de tokens zero.
- Textos em português.

## Review Focus

- Arquivo de doença editado com regra cujo id já existe em outro arquivo → erro claro que cita o id e os dois arquivos (Task 1, `test_id_duplicado_entre_arquivos`).
- Pasta `base/fonte/` sem `indice.json` (ou com ids a mais/a menos) → junta mesmo assim, ordem do índice para os conhecidos e novos ao final (Task 1, `test_regra_nova_entra_e_valida`).
- Caminho com espaço (`02-Dados de Treino`) quebrando o script/CLI → o script recebe o caminho como argumento único (Task 3, execução real).
- Regra de urgência que cita duas doenças → vai para `comum.json`, não duplicada (Task 1, coberto pela checagem “nenhum id repetido”).
- `carregar_do_grafo` sobre um grafo editado com aresta para nó inexistente → `grafo_para_base` já levanta erro; não silenciar (Task 2, `test_carregar_do_grafo_igual_v0002`).

---

### Task 1: separar e juntar (`kb/fonte.py`)

**Files:** Create `kb/fonte.py`; Test `tests/kb/test_fonte.py`; gerar `base/fonte/` com o CLI.

**Interfaces — Produces:**
- `separar(base: Base) -> dict[str, dict]` — chaves `"comum.json"`, `"indice.json"`, `"doencas/<id>.json"`.
- `gravar_fonte(base: Base, pasta: Path) -> list[Path]`
- `ler_fonte(pasta: Path) -> Base` — levanta `FonteInvalida(ValueError)` com mensagem em português.
- CLI `python -m kb.fonte separar --versao vNNNN [--destino base/fonte]` e `juntar [--origem base/fonte] [--salvar --autor X --nota Y]`.

- [ ] **Step 1: testes (falham)** em `tests/kb/test_fonte.py`, usando `carregar_base(RAIZ/'base/versoes/v0002.json')` e `tmp_path`:
  - `test_ida_e_volta_identica`: `ler_fonte(p) == v0002` após `gravar_fonte(v0002, p)`, e `_json(ler_fonte(p).model_dump(mode="json", exclude_none=True)) == (RAIZ/'base/versoes/v0002.json').read_text(encoding="utf-8")`.
  - `test_oito_doencas_com_suas_regras`: 8 arquivos em `doencas/`; cada um contém o símbolo `tipo == "doenca"` do nome do arquivo, todas as regras que o concluem e a regra `classe == "urgencia"` que o cita.
  - `test_ids_unicos_entre_arquivos`: nenhum id de símbolo/regra em dois arquivos.
  - `test_id_duplicado_entre_arquivos`: copiar uma regra de `mastite.json` para `cetose.json` → `FonteInvalida` cujo texto contém o id, `mastite.json` e `cetose.json`.
  - `test_doenca_sem_simbolo`: remover o símbolo da doença do seu arquivo → `FonteInvalida`.
  - `test_json_invalido`: arquivo com `{` → `FonteInvalida` citando o arquivo.
  - `test_regra_nova_entra_e_valida`: acrescentar regra de evidência nova em `mastite.json` (ex.: `R-MAS-99`, `se: [{simbolo: "febre", op: "=", valor: true}]`, `entao: {simbolo: "mastite", cf: 0.2}`) e apagar `indice.json` → base juntada contém a regra, ela fica depois das conhecidas e `validar(base).valida` é verdadeiro.
- [ ] **Step 2:** `.venv/Scripts/python -m pytest tests/kb/test_fonte.py -q` → falha por import.
- [ ] **Step 3: implementar** conforme as regras de separação da spec (uso transitivo por derivados; exclusivo → doença; urgência que cita exatamente uma doença → essa doença; resto → comum). Junção: arquivos de doença em ordem alfabética; ordena pelo índice; desconhecidos ao final na ordem de leitura.
- [ ] **Step 4:** testes passam; `python -m kb.fonte separar --versao v0002` gera `base/fonte/`; `python -m kb.fonte juntar` imprime “idêntica à v0002”.
- [ ] **Step 5: commit** `feat(kb): base separada por doença com junção exata`.

### Task 2: grafo exato e extração (`kb/exportar_grafo.py`)

**Files:** Create `kb/exportar_grafo.py`; Test `tests/kb/test_exportar_grafo.py`.

**Interfaces — Consumes:** `ler_fonte`. **Produces:**
- `extracao(base: Base, origem_por_id: dict[str, str]) -> dict` (esquema graphify: nós `sim:<id>`/`regra:<id>` com `id,label,file_type="concept",source_file`; arestas `source,target,relation ∈ {"condicao_de","conclui"},confidence="EXTRACTED",source_file`, `cf` em `conclui`).
- `exportar(origem: Path, saida: Path) -> tuple[Path, Path]` — grava `grafo_exato.json` e `extracao.json`.
- `carregar_do_grafo(caminho: Path) -> Base`.
- CLI `python -m kb.exportar_grafo [--origem base/fonte] [--saida graphify-out-dados]`.

- [ ] **Step 1: testes (falham)**:
  - `test_carregar_do_grafo_igual_v0002`: exportar de uma fonte gerada da v0002 → `carregar_do_grafo(...) == v0002`.
  - `test_casos_iguais_lendo_do_grafo`: para cada caso de `base/casos/casos.json`, `executar_caso(para_motor(v0002), c) == executar_caso(para_motor(base_do_grafo), c)`.
  - `test_extracao_no_esquema_do_graphify`: todo nó tem os 4 campos; toda aresta tem os 5 campos, aponta para nós existentes e é EXTRACTED; 51 nós `sim:` e 56 `regra:`.
- [ ] **Step 2:** falham. **Step 3:** implementar. **Step 4:** passam.
- [ ] **Step 5: commit** `feat(kb): grafo exato da base e extração para o graphify`.

### Task 3: cofre e visualização (`scripts/grafo_dados.py`) + arrumação

**Files:** Create `scripts/grafo_dados.py`; rename `obsidian/02-a-definir/` → `obsidian/02-Dados de Treino/`; rewrite its `README.md`; Modify `CLAUDE.md`, `AGENTS.md`, `.graphifyignore`.

- [ ] **Step 1:** script: `python scripts/grafo_dados.py graphify-out-dados "obsidian/02-Dados de Treino"` com o Python do graphify (`graphify-out/.graphify_python`): `build_from_json(directed=True, dedup=False)`, `cluster`, rótulos pela doença predominante dos `source_file` (`doencas/<id>.json` → nome da doença; senão “Comum”), `to_json`, `generate` (relatório), HTML e cofre Obsidian no diretório indicado.
- [ ] **Step 2:** rodar `kb.exportar_grafo` e o script; conferir que o cofre tem notas e o `graph.json` tem 107 nós.
- [ ] **Step 3:** renomear pasta, README do grafo 2 (o que é, como regenerar em 2 comandos, por que o motor lê o grafo exato e não o do graphify), atualizar referências em `CLAUDE.md`/`AGENTS.md`/`.graphifyignore` (`base/fonte/`, `graphify-out-dados/`, `obsidian/02-Dados de Treino/` fora do grafo 1).
- [ ] **Step 4:** `pytest -q` completo verde. **Step 5: commit** `feat(obsidian): grafo 2 com os dados das 8 doenças`.
