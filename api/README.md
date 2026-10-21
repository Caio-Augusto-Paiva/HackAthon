# API de anamnese de bovinos leiteiros (`api/`)

Backend FastAPI + SQLite do PoC do Hackathon UFJF 2026 (tema T1 Anamnese). É uma casca fina sobre o motor de inferência
(`engine/`) e a base de conhecimento (`kb/`): a decisão sai sempre da base explícita e do motor, de forma determinística e
auditável. **Nenhuma chamada de rede e nenhuma LLM no caminho da decisão.** Todos os dados são fictícios.

Especificação: Seção 4 de `docs/superpowers/specs/2026-10-20-anamnese-bovinos-design.md` (contratos e convenções) e
Seção 5.2 (execução em localhost). Plano: `docs/superpowers/plans/2026-10-21-api-secao-4.md`.

## Como rodar

Pré-requisito: o ambiente `.venv` na raiz do repositório, criado uma vez, com internet:

```
python -m venv .venv
.venv\Scripts\python -m pip install -e ".[dev]"
```

Subir a API em `http://localhost:8000` (a partir de qualquer pasta; o script entra na raiz sozinho):

```
powershell -ExecutionPolicy Bypass -File scripts\rodar.ps1
```

| Opção | Efeito |
|---|---|
| `-SoPreparar` | confere o ambiente, cria o banco e semeia; não sobe o servidor |
| `-Reset` | apaga o banco e o recria, com os animais fictícios, antes de subir (só apaga arquivo SQLite; veja abaixo) |
| `-SemNavegador` | não abre o navegador depois de "Pronto" |

O roteiro: (1) confere o Python do `.venv` e aborta em português se faltar; (2) cria o banco e semeia os animais
fictícios se o arquivo não existir; (3) avisa, sem abortar, se `web\dist` não existe (só a API fica no ar); (4) aborta se
a porta 8000 já estiver em uso; (5) sobe `uvicorn api.main:app --host 127.0.0.1 --port 8000`, espera `GET /api/saude`
responder (até 30 s), imprime a URL e abre o navegador padrão (`-SemNavegador` desliga).
**Ctrl+C encerra.** Em Linux e macOS: `scripts/rodar.sh` (`--so-preparar`, `--reset`), mesmo roteiro, mas só imprime a URL.

Sem o script: `.venv\Scripts\python -m uvicorn api.main:app --host 127.0.0.1 --port 8000`.

- Verificação: `GET http://localhost:8000/api/saude` devolve `{"status":"ok","versao_api":"0.1.0"}`.
- Documentação interativa (Swagger): `http://localhost:8000/api/docs`; OpenAPI vivo: `/api/openapi.json`.
- Se `web/dist/index.html` existir, a mesma porta serve o frontend: `/assets` e qualquer `GET` fora de `/api` devolve o
  `index.html` (para o React funcionar ao recarregar a página). Sob `/api` uma rota inexistente continua sendo o 404 em
  JSON, nunca o HTML (também com barras a mais, como `//api/x`). Rota coringa própria (`api/frontend.py`), e não
  `FastAPI.frontend()`, porque o fallback do FastAPI só vale para `Accept: text/html`.
- Com o frontend montado: `POST` numa rota desconhecida e `HEAD /` dão 405 (a coringa só casa `GET`), e `/api/x/` com barra
  final dá 404 em JSON (sem o frontend, uma rota real como `/api/animais/` seria redirecionada com 307 para `/api/animais`).

### Variáveis de ambiente

| Variável | Padrão | O que é |
|---|---|---|
| `ANAMNESE_BASE_DIR` | `base` | pasta da base de conhecimento: `ativa.json` (ponteiro), `versoes/vNNNN.json`, `casos/casos.json` |
| `ANAMNESE_DB` | `dados/anamnese.db` | arquivo SQLite (sessões, animais, índice de versões, execuções de casos); a pasta é criada ao subir |

Caminhos relativos valem a partir da pasta de onde o servidor sobe; os scripts sobem sempre da raiz do repositório. O
`dados/` está no `.gitignore`.

**A API sobe sem a base.** Sem `ativa.json` (ou sem a versão apontada), `GET /api/saude`, `GET /api/animais` e
`GET /api/base/versoes` respondem normalmente; `POST /api/sessoes` e `POST /api/animais` respondem **409 `conflito`**
("Nenhuma versão ativa ...") e nunca 500. A semente também roda sem a base (veja abaixo).

### Sementes e reset do banco

```
.venv\Scripts\python scripts\semear_ficticios.py        # cria os animais que faltam (idempotente por brinco)
.venv\Scripts\python scripts\resetar_db.py [--semear]   # apaga o .db, recria o esquema e, com --semear, semeia
```

Quatro animais fictícios (`BR-0001` Mimosa, com parto há 6 dias; `BR-0002` Estrela, com parto há 1 dia, para o roteiro da
demonstração; `BR-0003` Jurema; `BR-0004` Boneca), cada um com uma ficha diferente. Os ids são sequenciais: `BR-0001` é
`an_001` **no banco recém-criado** (num banco que já tinha animais, ganha o próximo id livre). Com a base ativa à mão, cada
ficha é validada por ela: o campo que a base não tem ou não aceita é pulado, sem quebrar. Sem a base, a ficha é gravada
como está.

O reset só toca no banco, nunca na pasta da base, e confere o alvo antes de apagar: só apaga se `ANAMNESE_DB` não existe, é
um arquivo vazio ou começa com o cabeçalho `SQLite format 3`. Um JSON, outro arquivo ou uma pasta no lugar do banco é
recusado ("... não é um banco SQLite; recuso apagar."), com saída diferente de zero e nada apagado; os auxiliares
`-wal`/`-shm`/`-journal` só caem depois dessa conferência.

## Estrutura e regras de código

```
api/
  main.py          criar_app(config) -> FastAPI; app = criar_app(); lifespan que cria a pasta e o esquema do .db;
                   middleware do X-Requisicao-Id; monta o frontend por último
  config.py        Configuracao (caminhos por variável de ambiente, relógio injetável para os testes)
  contexto.py      Contexto por requisição (config, conexão SQLite, Repositorio da base)
  erros.py         ErroApi, fábricas e handlers do formato único de erro
  frontend.py      serve web/dist e a rota coringa, só se existir
  exportar_openapi.py   grava contratos/openapi.json
  rotas/           rotas finas
  servicos/        lógica (ficha, animais, importação, sessão, estado, explicação, base, casos, versões)
  schemas/         contratos Pydantic e o mapa operationId -> modelos (registro.py)
  db/              esquema.sql, conexao.py e repositorios.py (o único lugar com SQL)
```

**Regra: rotas finas, SQL só em repositórios.** Uma rota só declara caminho, schema e `operation_id` e chama um serviço;
serviços decidem e orquestram (e levantam `ErroApi`); `api/db/repositorios.py` é o único arquivo com SQL e não tem lógica de
domínio. Toda escrita de um serviço acontece dentro de `with ctx.conn:` (os repositórios não fazem `commit`). Dependências:
`api -> engine -> kb`; `engine/` e `kb/` não são alterados pela API.

### Mapa de rotas por arquivo (27, prefixo `/api`)

| Arquivo | Rotas (`operationId`) |
|---|---|
| `rotas/sistema.py` | `GET /saude` (`saude`) |
| `rotas/animais.py` | `GET /animais` (`listar_animais`), `POST /animais` (`criar_animal`), `POST /animais/importacao` (`importar_animais`), `GET /animais/{id}` (`obter_animal`), `GET /animais/{id}/sessoes` (`listar_sessoes_animal`) |
| `rotas/sessoes.py` | `POST /sessoes` (`criar_sessao`), `GET` e `PATCH /sessoes/{id}` (`obter_sessao`, `trocar_modo`), `POST` e `PUT /sessoes/{id}/triagem/{tela_id}` (`responder_triagem`, `corrigir_triagem`), `POST /sessoes/{id}/respostas` (`responder_pergunta`), `PUT /sessoes/{id}/respostas/{simbolo}` (`corrigir_resposta`), `POST /sessoes/{id}/acoes/bandeira` (`acao_bandeira`), `GET /sessoes/{id}/parecer` (`obter_parecer`), `/porque/{simbolo}` (`obter_porque`), `/como/{simbolo}` (`obter_como`), `/traco` (`obter_traco`) |
| `rotas/base.py` | `GET /base/versoes` (`listar_versoes`), `GET /base/versoes/{v}` (`obter_versao`), `GET /base/versoes/{v}/grafo` (`obter_grafo`), `POST /base/validar` (`validar_base`), `POST /base/versoes` (`salvar_versao`), `PUT /base/ativa` (`ativar_versao`), `POST` e `GET /base/versoes/{v}/execucoes` (`executar_casos`, `listar_execucoes`), `GET /base/versoes/{v}/execucoes/{id}` (`obter_execucao`) |

`rotas/respostas.py` não tem rotas: só declara os erros documentados no OpenAPI.

### Formato de erro

Todo erro é `{"erro": {"codigo", "mensagem", "requisicao_id", "detalhes"?}}`, com o cabeçalho `X-Requisicao-Id` igual. Códigos:
404 `nao_encontrado`; 405 `metodo_nao_permitido` (suposição, fora da tabela da 4.4); 409 `conflito`, `ja_respondida`,
`nao_respondida`, `casos_falhando`; 422 `entrada_invalida`, `resposta_invalida`, `base_invalida`, `simbolo_invalido`,
`importacao_invalida`; 500 `erro_interno` (mensagem fixa, sem detalhe técnico; o servidor registra a causa com o mesmo id).

## Contrato (`contratos/`)

`contratos/openapi.json` é gerado pelo código e versionado; `contratos/exemplos/<operationId>.json` traz um exemplo por
rota, validado contra o schema. Para regenerar o OpenAPI depois de mudar uma rota ou um schema:

```
.venv\Scripts\python -m api.exportar_openapi
```

Monta o app sem subir servidor e sem tocar no banco. O primeiro teste de `tests/api/test_contrato_openapi.py` falha se o
arquivo versionado não for idêntico ao gerado. Por isso o `pydantic` está fixado em `pyproject.toml` (`==2.14.1`): um patch
dele pode mudar o texto do JSON Schema e invalidar o arquivo.

## Testes

```
.venv\Scripts\python -m pytest tests/api -q    # só a API
.venv\Scripts\python -m pytest -q              # tudo (kb, engine, api)
.venv\Scripts\python -m unittest discover      # testes do motor
```

Os testes da API usam a base mínima de `tests/fixtures/kb/base_minima.json` (nunca a base real) e um SQLite temporário.

## Decisões do plano (D1 a D7)

- **D1, snapshot (desvio da 4.6):** a coluna extra `sessoes.snapshot_json` guarda `{"motor": Sessao.exportar(), "origens_ficha": ...,
  "resumo": ...}` e é a **fonte da verdade** para reconstruir a sessão. `respostas`, `perguntas_feitas` e
  `sessoes.bandeiras_reconhecidas_json` são **projeção** gravada na mesma transação, para consulta e auditoria. Coluna extra
  `resultados_casos.extra_json` (`descricao`, `mudou_vs_pai`, `erro`).
- **D2, `estado()` registra perguntas:** o motor cria o evento `pergunta_feita` ao montar o estado. Por isso toda requisição, inclusive
  `GET`, chama `estado()` e regrava o snapshot se mudou; o `GET` não sobe `revisao`.
- **D3, código do 409:** o `codigo` é o específico (`ja_respondida`, `nao_respondida`, `casos_falhando`); brinco duplicado e "sem versão
  ativa" usam `conflito`.
- **D4, `EdicaoBase` frouxa:** `meta`, `grafo.nos`, `grafo.arestas` e `layout` são `dict`/lista de `dict`, para erros de estrutura
  chegarem ao validador do `kb` e voltarem como `E00` com 200 em `/base/validar`. A tipagem forte fica no `Grafo` do `kb`.
- **D5, origem `importacao`:** o motor só conhece `ficha`. A API grava `origens_ficha` no snapshot e, ao montar o "como?", reescreve
  `origem: "ficha"` para `"importacao"` nos campos assim marcados.
- **D6, contrato das respostas reais:** sem `jsonschema`. Cada resposta real e cada exemplo é validado com `TypeAdapter` do modelo
  registrado em `api/schemas/registro.py::CONTRATOS` (por `operationId`); o teste do `openapi.json` confere regeneração idêntica e que os
  `operationId` são os de `CONTRATOS`.
- **D7, ordem das tarefas:** salvar e ativar versão dependem da execução de casos; por isso os casos vieram antes.

## Decisões tomadas na execução (afetam quem usa a API)

- **409 específicos.** Além do D3: `POST /sessoes` sem `versao_base` e sem versão ativa é 409 `conflito`; versão pedida que não existe
  é 404.
- **`ordem_respostas`.** O snapshot guarda `ordem_respostas` (lotes na ordem de entrada); corrigir uma resposta reprocessa os lotes
  nessa ordem. A coluna `respostas.ordem` é a posição do lote (símbolo fora de qualquer lote vale 1).
- **Resumo da sessão.** `snapshot["resumo"] = {urgencia, top1}` é gravado a cada salvamento; o histórico do animal lê o resumo, sem
  rodar o motor.
- **Comparação com a versão pai, caso a caso.** Ao salvar ou executar, o "antes" de cada caso é o status na execução mais recente do
  pai que contém o caso; `ausente` só se nenhuma execução do pai o rodou. `mudancas` lista só quem mudou.
- **Portão de ativação.** `PUT /base/ativa` exige `confirmar_falhas: true` se o status **mais recente** de algum caso (execução mais
  nova da versão que o contém, só entre os ids do `casos.json` atual) for `falhou` ou `erro`; senão 409 `casos_falhando`. Uma execução
  parcial só de casos verdes não apaga uma falha que ela não rodou. Versão nunca executada ativa sem confirmação.
- **Alerta encerrado só com `ver_parecer`.** Com a sessão `encerrada` e a pausa de bandeira, `alerta.acoes == ["ver_parecer"]`.
- **Grafo sem nulos supérfluos.** `GET /base/versoes/{v}/grafo` usa `response_model_exclude_unset`: campos ausentes continuam ausentes,
  e `valor: null` explícito é preservado.
- **`/base/validar` responde sempre 200** com o relatório (inclusive `E00` para estrutura quebrada). A única exceção é texto com
  surrogate Unicode solto, que a resposta não conseguiria codificar: 422 `entrada_invalida`.
- **`starlette==1.9.0` fixado** (versão validada; o `fastapi` aceita faixa aberta, e o `TestClient` depende do suporte ao `httpx 0.28.1`).
- **Importação sem 500.** `POST /animais/importacao` aceita `.csv` e `.json` (até 5 MB, UTF-8, com BOM e separador `;`); linha ruim
  vai para `rejeitados` (sem gravar nada dela), e arquivo ilegível, binário ou sem a coluna `brinco` é 422 `importacao_invalida`.
  `?gravar=false` só simula.
- **Sessão presa à versão.** Ativar ou salvar outra versão não muda sessões em andamento: cada uma fica na `versao_base` com que nasceu.
- **Ficha.** A ficha grava `data_ultimo_parto`; `dias_em_lactacao` é calculado dela (data ausente, inválida ou no futuro: a tela é
  perguntada, nunca erro). O cliente nunca envia CF: envia o valor ou `"nao_sei": true`.
- **Autor das versões.** Toda versão salva pela API tem autor `equipe` (suposição: não há login).
