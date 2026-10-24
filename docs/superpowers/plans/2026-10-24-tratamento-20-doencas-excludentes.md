# Links de tratamento, 20 doenças e doenças excludentes: plano de implementação

> **Para agentes:** SUB-SKILL OBRIGATÓRIA: use superpowers:subagent-driven-development (recomendado) ou superpowers:executing-plans para executar tarefa por tarefa. Os passos usam checkbox (`- [ ]`).

**Objetivo:** no parecer final, oferecer um botão "Como tratar" para cada doença com mais de 20%; ampliar a base de 8 para 20 doenças de vacas leiteiras no Brasil; dar ao motor suporte a pares de doenças excludentes.

**Arquitetura:**
- **Links de tratamento:** são dados da base. Cada símbolo `doenca` ganha um campo `tratamento` com título e URL de uma fonte gratuita (Embrapa, gov.br/MAPA, MSD Veterinary Manual em português). O validador da base só aceita domínios de uma lista permitida, e a API repassa o link no item do parecer. Não haverá página própria de tratamento: isso exigiria conteúdo clínico validado, e o projeto não tem um veterinário revisor.
- **Exclusão:** é uma etapa nova do motor, rodada depois de todas as regras. Os pares ficam em `meta.exclusoes`. Para cada par, se a doença mais forte tiver CF ≥ `limiares.exclusao` e for estritamente maior que a outra, a mais fraca recebe evidência negativa igual ao CF da vencedora. A etapa gera um evento no traço, e isso aparece em "Como cheguei aqui?".
- **Conteúdo novo:** entra pelos arquivos por doença em `base/fonte/doencas/`. Depois vem o comando `juntar`, que gera a v0005, e por fim a ativação.

**Stack:** Python 3.12 (motor, kb, FastAPI, pydantic, pytest), React + TypeScript + Vitest (web).

**Spec:** o pedido do usuário de 2026-10-24, resumido em "Requisitos" abaixo. Não há documento de especificação separado.

## Requisitos (do pedido)

1. Ao terminar o questionário, mostrar um botão por doença com **mais de 20%** de confiança. O botão leva a uma página sobre como tratar a doença. A página pode ser externa e gratuita (pesquisa, fórum ou site médico).
2. Ampliar para as **20 doenças mais comuns** em gado leiteiro brasileiro, com perguntas novas. Uma expansão futura para 50 ou mais não deve exigir mudar o motor.
3. Algumas doenças formam **pares excludentes**, e o motor deve tratar essa exclusão.

## Restrições globais

- Todo texto voltado ao usuário fica em português. O projeto continua só para vacas; touros e bois estão fora do escopo.
- Tudo conhecimento clínico novo tem `fonte` preenchida e `status: "suposicao_a_validar"`.
- O botão de tratamento sempre vem acompanhado deste texto: "Informação geral de fonte pública. O tratamento deve ser indicado por um médico-veterinário."
- Links abrem em nova aba com `rel="noopener noreferrer"`.
- Domínios permitidos para `tratamento.url`: `embrapa.br`, `gov.br`, `msdvetmanual.com`. Só `https://`.
- O front é só para desktop.
- Uma versão da base só é ativada com 0 falhas nos casos.
- Os documentos `docs/entrega/03` e `04` são regenerados com `python scripts/gerar_doc_regras.py --casos base/casos/casos.json --saida docs/entrega`.

## As 20 doenças (decisão)

| Situação | Doenças |
|---|---|
| Mantidas (7) | `acidose`, `cetose`, `dermatite_digital`, `hipocalcemia`, `mastite`, `metrite`, `tpb` |
| Substituem `deslocamento_abomaso` (2) | `deslocamento_abomaso_esquerda`, `deslocamento_abomaso_direita` |
| Novas (11) | `timpanismo_espumoso`, `timpanismo_gasoso`, `retencao_placenta`, `pneumonia`, `reticulopericardite_traumatica`, `hipomagnesemia`, `brucelose`, `leptospirose`, `ibr`, `bvd`, `tuberculose` |

**Pares excludentes** (`meta.exclusoes`):
- `deslocamento_abomaso_esquerda` × `deslocamento_abomaso_direita`: o abomaso desloca para um lado só.
- `timpanismo_espumoso` × `timpanismo_gasoso`: o gás fica preso em espuma ou livre, não os dois ao mesmo tempo.
- `retencao_placenta` × `metrite`: no mesmo quadro puerperal, a retenção precede a metrite; o par deixa a hipótese mais forte se destacar. Fonte: Embrapa Gado de Leite.

Brucelose e tuberculose são de notificação obrigatória. Por isso, toda regra que as conclua dispara a urgência `chamar_agora`.

## Foco de revisão

1. **Empate de CF num par excludente:** nenhuma das duas pode ser rebaixada. Teste: `test_exclusao_empate_nao_rebaixa`.
2. **Doença excluída continua sendo perguntada.** Depois da exclusão, a seleção de perguntas não deve priorizar a perdedora, e o `potencial` dela é igual ao percentual. Teste: `test_excluida_tem_potencial_igual_percentual`.
3. **URL de tratamento maliciosa ou fora da lista** (`javascript:`, `http://`, `embrapa.br.evil.com`): o validador recusa. Teste: `test_tratamento_url_fora_da_lista_recusada`.
4. **Doença com exatamente 20% não ganha botão;** com 21% ganha. Teste no front: `não oferece tratamento com exatamente 20%`.
5. **Sessão salva com a v0004 e restaurada depois da v0005,** em que `deslocamento_abomaso` não existe mais: a restauração usa a versão gravada na sessão e não quebra. Teste: `test_sessao_v0004_restaura_apos_ativar_v0005`.

---

### Tarefa 1: modelo e validador (`tratamento` e `exclusoes`)

**Arquivos:**
- Modificar: `kb/modelos.py` (`Simbolo`, `Limiares`, `Meta`), `kb/schema/base.schema.json`, `kb/validador.py`
- Testar: `tests/kb/test_exclusoes_tratamento.py` (novo)

**Interfaces:**
- Produz:
  - `Tratamento(_Modelo)`, com `titulo: str` (1 a 120 caracteres) e `url: str`.
  - `Simbolo.tratamento: Tratamento | None = None`. Só é permitido quando `tipo == "doenca"`.
  - `Exclusao(_Modelo)`, com `doencas: tuple[str, str]`, `fonte: str` (não vazia) e `nota: str`.
  - `Meta.exclusoes: list[Exclusao] = []`.
  - `Limiares.exclusao: float = 0.5`.
  - Códigos de erro do validador: `exclusao_doenca_inexistente`, `exclusao_mesma_doenca`, `exclusao_duplicada`, `tratamento_url_invalida` e `tratamento_fora_de_doenca`.

- [ ] **Passo 1: escrever os testes que falham.** Cada caso parte de uma base mínima válida (fixture de `tests/kb/apoio.py`) e confere `validar(base).valida` e o código do erro:
  - `test_exclusao_valida_aceita`: o par `["a","b"]` é aceito quando as duas são doenças.
  - `test_exclusao_doenca_inexistente`.
  - `test_exclusao_mesma_doenca`: `["a","a"]`.
  - `test_exclusao_duplicada`: `["a","b"]` e `["b","a"]` juntas.
  - `test_tratamento_url_fora_da_lista_recusada`: parametrizado com `javascript:alert(1)`, `http://www.embrapa.br/x`, `https://embrapa.br.evil.com/x` e `https://exemplo.com`.
  - `test_tratamento_url_permitida`: parametrizado com `https://www.embrapa.br/x`, `https://www.gov.br/agricultura/x` e `https://www.msdvetmanual.com/pt/x`.
  - `test_tratamento_em_pergunta_recusado`.
- [ ] **Passo 2:** rodar `python -m pytest tests/kb/test_exclusoes_tratamento.py -q`. O esperado é FALHA.
- [ ] **Passo 3: implementar** os modelos e as checagens. A regra do domínio usa `urllib.parse.urlsplit`: `scheme == "https"` e `hostname` igual a um domínio permitido ou terminado em `"." + domínio`. Atualizar `base.schema.json` com os mesmos campos.
- [ ] **Passo 4:** rodar `python -m pytest tests/kb -q`. O esperado é PASSAR, incluindo os 296 testes anteriores.
- [ ] **Passo 5:** commit `feat(kb): campos tratamento e exclusoes com validação`.

### Tarefa 2: etapa de exclusão no motor

**Arquivos:**
- Modificar: `engine/inferencia.py` (função nova `aplicar_exclusoes`, chamada no fim de `inferir`, antes do cálculo de urgência), `engine/parecer.py` (potencial), `engine/explicacao.py` (evento no "como")
- Testar: `tests/engine/test_exclusao.py` (novo)

**Interfaces:**
- Consome: `base.meta['exclusoes']`, `base.meta['limiares']['exclusao']` e `cf.combinar`.
- Produz:
  - `aplicar_exclusoes(base, cfs: dict, memoria: dict, traco: list) -> frozenset[str]`, que devolve os ids rebaixados.
  - O campo `Resultado.excluidas: frozenset[str]`.
  - O evento de traço `exclusao_aplicada`, com `simbolo`, `por` (a vencedora), `antes`, `depois`, `fonte` e `nota`.

Algoritmo: ler os CFs de todos os pares **antes** de alterar qualquer um, para que a ordem dos pares não mude o resultado. Para cada par (a, b), sendo `v` a doença de maior CF e `p` a outra:
- se `cfs[v] >= exclusao` e `cfs[v] > cfs[p]`, o novo CF de `p` é `combinar(cfs[p], -cfs[v])`;
- quando `p` aparece em mais de um par, vale a menor das saídas;
- depois de calcular tudo, gravar em `cfs` e em `memoria`.

- [ ] **Passo 1: escrever os testes que falham.** Usar uma base de teste com duas doenças, `x` e `y`, e regras diretas `sx → x` e `sy → y`:
  - `test_exclusao_rebaixa_mais_fraca`: com `x=0.8` e `y=0.4`, `y` termina com `combinar(0.4,-0.8)`, que é igual a `Fraction(-2,3)` (conferir em `cf.combinar`), e fica `situacao == "descartada"`.
  - `test_exclusao_abaixo_do_limiar_nao_age`: com `x=0.45` e `y=0.3`, nada muda.
  - `test_exclusao_empate_nao_rebaixa`: com `x=0.7` e `y=0.7`, nada muda.
  - `test_exclusao_ordem_dos_pares_irrelevante`: três doenças com dois pares, em ordem invertida, dão os mesmos CFs.
  - `test_exclusao_gera_evento_no_traco`: o evento `exclusao_aplicada` tem `por == "x"`.
  - `test_excluida_tem_potencial_igual_percentual`: no `montar_parecer`, o item `y` tem `potencial == percentual`.
  - `test_como_mostra_exclusao`: `Sessao.como("y")` inclui uma etapa com `tipo == "exclusao"` e `por == "x"`.
- [ ] **Passo 2:** rodar `python -m pytest tests/engine/test_exclusao.py -q`. O esperado é FALHA.
- [ ] **Passo 3: implementar.** No `parecer`, quando `id in resultado.excluidas`, usar `potencial = percentual`. Em `selecao.py`, as doenças em `excluidas` não contam como hipótese aberta: filtrar onde a seleção monta as doenças candidatas.
- [ ] **Passo 4:** rodar `python -m pytest tests/engine tests/casos -q`. O esperado é PASSAR. A base v0004 não tem `exclusoes`, então os 34 casos continuam iguais.
- [ ] **Passo 5:** commit `feat(motor): pares de doenças excludentes`.

### Tarefa 3: API e contrato (tratamento e exclusão)

**Arquivos:**
- Modificar: `api/schemas/parecer.py` (`ItemDoenca`), `api/servicos/explicacao_servico.py` e `api/servicos/textos.py` (frase da exclusão), `engine/parecer.py` (incluir `tratamento` no item)
- Regenerar: `contratos/openapi.json`, `contratos/exemplos/*.json`
- Testar: `tests/api/test_tratamento_exclusao.py` (novo)

**Interfaces:**
- Produz:
  - `ItemDoenca.tratamento: Tratamento | None`, com `{titulo: str, url: str}`.
  - Para a etapa de exclusão em "Como cheguei aqui?", o texto exato: `"Ficou menos provável porque {nome da vencedora} ficou mais forte, e as duas não costumam ocorrer juntas."`

- [ ] **Passo 1: escrever os testes que falham:**
  - `test_parecer_traz_tratamento_da_base`: a URL do item é igual à da base ativa.
  - `test_parecer_tratamento_nulo_sem_campo`: base sem o campo devolve `null`.
  - `test_como_frase_exclusao`: a frase exata, usando uma base de teste com par excludente.
  - `test_sessao_v0004_restaura_apos_ativar_v0005`: criar a sessão com a v0004, ativar uma versão nova e consultar `GET /api/sessoes/{id}/parecer`. Deve devolver 200 com as doenças da v0004.
- [ ] **Passo 2:** rodar o pytest do arquivo. O esperado é FALHA.
- [ ] **Passo 3:** implementar e regenerar o contrato com o mesmo script usado na seção 4 (`scripts/`; ver `tests/api/test_contrato_openapi.py`).
- [ ] **Passo 4:** rodar `python -m pytest tests/api -q`. O esperado é PASSAR.
- [ ] **Passo 5:** commit `feat(api): tratamento no parecer e frase de exclusão`.

### Tarefa 4: botões "Como tratar" no parecer (web)

**Arquivos:**
- Modificar: `web/src/api/tipos.ts` (ou onde `ItemDoenca` está tipado), `web/src/paginas/Parecer.tsx` e `.module.css`, `web/src/teste/cenarios.ts` (exemplo com `tratamento`)
- Testar: `web/src/paginas/Parecer.test.tsx`

**Interfaces:**
- Consome: `ItemDoenca.tratamento` da Tarefa 3.
- Produz: a seção `<section aria-labelledby="titulo-tratar">`, com título "Como tratar" e um link por item com `percentual > 20` e `tratamento` presente.
  - Os links seguem a ordem do parecer.
  - O texto acessível do link é `Como tratar {nome}`.
  - O aviso fixo das Restrições globais aparece logo abaixo do título.
  - Botões usam o mesmo brilho diagonal dos botões da tela final (`Parecer.module.css`).

- [ ] **Passo 1: escrever os testes que falham** em `Parecer.test.tsx`:
  - `oferece um link de tratamento por doença acima de 20%`: com o exemplo de percentuais `[87, 32, 15, …]`, há 2 links, cada um com `href` igual à URL do exemplo, `target="_blank"` e `rel="noopener noreferrer"`.
  - `não oferece tratamento com exatamente 20%`: um item com `percentual: 20` não gera link.
  - `esconde a seção quando nenhuma doença passa de 20%`: `queryByRole('heading', {name: 'Como tratar'})` devolve `null`.
  - `mostra o aviso de que o tratamento é indicado pelo veterinário`.
- [ ] **Passo 2:** rodar `cd web && npx vitest run src/paginas/Parecer.test.tsx`. O esperado é FALHA.
- [ ] **Passo 3:** implementar.
- [ ] **Passo 4:** rodar `cd web && npx vitest run && npx tsc --noEmit`. O esperado é PASSAR.
- [ ] **Passo 5:** commit `feat(web): botões Como tratar no parecer`.

### Tarefa 5: conteúdo das 20 doenças, v0005

**Arquivos:**
- Criar: `base/fonte/doencas/<id>.json` para as 13 doenças novas da tabela (as 11 novas e as 2 de deslocamento)
- Remover: `base/fonte/doencas/deslocamento_abomaso.json`. As regras dele são redistribuídas entre os dois lados.
- Modificar:
  - `base/fonte/comum.json`: `meta.exclusoes` com os 3 pares, `limiares.exclusao: 0.5`, `limite_dinamico` com `produtor: 15` e `veterinario: 30`, sinais compartilhados novos (por exemplo `tosse`, `secrecao_nasal`, `aborto_recente`, `distensao_flanco_esquerdo`, `ping_flanco_direito`, `tremores`).
  - O campo `tratamento` em todas as 20 doenças.
  - `base/fonte/indice.json` e `base/casos/casos.json`.
- Gerar: `base/versoes/v0005.json` e `base/ativa.json` apontando para `v0005`.
- Testar: `tests/casos/test_base_ativa.py`, que já roda todos os casos.

Regras de conteúdo para cada doença nova:
- Ter pelo menos 2 perguntas para o produtor e 1 para o veterinário.
- Ter pelo menos 3 regras de evidência, uma delas negativa (diferencial), com fonte bibliográfica.
- `gravidade` deve ser `alta` para brucelose, tuberculose, leptospirose, BVD, deslocamento à direita e reticulopericardite.
- Brucelose e tuberculose concluem `chamar_agora`.
- A redação das perguntas segue as existentes, em linguagem simples para o produtor.

Casos novos, pelo menos 16:
- 1 caso positivo por doença nova (13).
- 1 caso por par excludente (3). Nesses casos, a doença perdedora termina em `pouco_provavel` e com `situacao == "descartada"`.

- [ ] **Passo 1:** escrever os 16 casos em `base/casos/casos.json`. Rodar o motor sobre a base ainda sem as doenças novas e conferir que eles FALHAM.
- [ ] **Passo 2:** escrever os arquivos de doença e editar `comum.json`. Rodar `python -m kb.fonte juntar --autor equipe --nota "20 doenças, pares excludentes e links de tratamento"` sem `--salvar`. O validador não deve apontar erros.
- [ ] **Passo 3:** ajustar os pesos até que todos os 50 casos (34 antigos e 16 novos) passem. Rodar `python -m kb.fonte juntar --salvar --autor equipe --nota "..."` e ativar a v0005.
- [ ] **Passo 4:** rodar a suíte inteira com `python -m pytest -q` e `cd web && npx vitest run`. O esperado é 0 falhas.
  - Testes que fixam a contagem de 8 doenças passam a ler a base ativa, do mesmo modo que já faz `test_respostas_numericas.py`.
  - O `Parecer.test.tsx` usa o exemplo próprio e não muda.
- [ ] **Passo 5:** commit `feat(base): v0005 com 20 doenças, exclusões e tratamentos`.

### Tarefa 6: grafo 2, documentação e conferência final

**Arquivos:**
- Modificar: `kb/exportar_grafo.py` (aresta `exclui` entre as doenças de cada par), `docs/entrega/01`, `02`, `05`, `06`, `README.md` (números da v0005)
- Regenerar: `docs/entrega/03` e `04`, `graphify-out-dados/` e `obsidian/02-Dados de Treino` (com `scripts/grafo_dados.py`)
- Testar: `tests/kb/test_exportar_grafo.py` (caso novo `test_exportar_aresta_exclui`) e `tests/documentacao`

- [ ] **Passo 1:** escrever `test_exportar_aresta_exclui`: a extração da v0005 tem 3 arestas com `relation == "exclui"`. Rodar e conferir que FALHA.
- [ ] **Passo 2:** implementar e regenerar o grafo, o cofre e os documentos.
- [ ] **Passo 3:** rodar `python -m pytest -q` e `cd web && npx vitest run`. O esperado é 0 falhas. Depois, abrir o site local e fazer o fluxo produtor até o parecer, conferindo os botões "Como tratar" e que eles abrem em nova aba.
- [ ] **Passo 4:** commit `docs: v0005 nos documentos e grafo 2 com exclusões` e push.
