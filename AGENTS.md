# AGENTS.md — instruções para o Codex

As instruções do projeto estão em `CLAUDE.md` (mesmas regras para todos os agentes). Escreva tudo em português.

## Grafo de conhecimento — só quando precisar procurar

- **Não** leia o grafo nem `graphify-out/GRAPH_REPORT.md` no início da tarefa.
- Se a tarefa já indica o arquivo, ou o assunto é código e testes, use busca direta (`rg`).
- Para **localizar** uma decisão, regra, fonte ou requisito que você não sabe onde está, rode primeiro `graphify query "<pergunta>"` e abra só o trecho em `source_file`/`location`, em vez de varrer `docs/`.

## Atualizar o grafo — uma vez por bloco de trabalho

Só ao fechar um bloco que alterou documentos de conhecimento (`.md` em `docs/`, `CLAUDE.md`, `engine/README.md`): `/graphify . --update`, `graphify export obsidian --dir obsidian/01-conhecimento` e commit separado. Mudanças só em código, testes, `web/`, `docs/prompts/` ou `docs/rascunhos/` não pedem atualização.

## Grafo 2 — dados das doenças

`obsidian/02-Dados de Treino/` é gerado sem IA a partir de `base/fonte/` (ver o README da pasta). Não rode `/graphify` nele; regenere com `kb.exportar_grafo` + `scripts/grafo_dados.py`.
