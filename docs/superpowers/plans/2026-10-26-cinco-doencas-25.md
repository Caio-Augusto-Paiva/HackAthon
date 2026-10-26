# Cinco doenças a mais (25 no total): plano de implementação

> **Para agentes:** SUB-SKILL OBRIGATÓRIA: use superpowers:subagent-driven-development (recomendado) ou superpowers:executing-plans para executar tarefa por tarefa. Os passos usam checkbox (`- [ ]`).

**Objetivo:** ampliar a base de 20 para 25 doenças, com as 5 mais comuns entre as que hoje ficam sem resposta, gerando a versão v0008.

**Arquitetura:** só conteúdo da base. O motor, a API e o site não mudam, porque já tratam qualquer número de doenças, pares excludentes, `tratamento` e `dispensada_se`. O conteúdo entra pelos arquivos por doença em `base/fonte/doencas/`. Depois vêm o `juntar --salvar`, a v0008 e a ativação.

**Stack:** JSON da base e Python 3.12 (kb, motor, pytest).

**Spec:** o pedido do usuário de 2026-10-26 ("incluir apenas as próximas 5 doenças mais comuns, totalizando 25"), mais o estudo de benefício feito na conversa. Não há documento de especificação separado.

## As 5 doenças (decisão)

| id | Nome | Gravidade | Por que entra |
|---|---|---|---|
| `ulcera_sola` | Úlcera de sola / doença da linha branca | media | É a maior parte da claudicação; hoje vira "dermatite digital" por falta de alternativa. |
| `flegmao_interdigital` | Flegmão interdigital (podridão do casco) | media | Manqueira aguda com inchaço entre as unhas, febre e mau cheiro. |
| `endometrite` | Endometrite clínica | media | Inflamação do útero depois de 21 dias do parto; hoje vira "metrite". |
| `cisto_ovariano` | Cisto ovariano | baixa | Problema reprodutivo comum, percebido como cio irregular, cio constante ou falta de cio. |
| `lipidose_hepatica` | Lipidose hepática (fígado gorduroso) | alta | Anda junto com a cetose no pós-parto, em vaca gorda no parto. |

**Par excludente novo:** `metrite` × `endometrite`. Pela definição clínica, a metrite puerperal ocorre até 21 dias do parto e a endometrite clínica depois disso, então as duas não coexistem no mesmo momento. Nota da exclusão: "Metrite é do puerpério (até 21 dias); endometrite clínica, depois disso."

**Pares descartados:** úlcera de sola × dermatite digital e flegmão × dermatite digital não entram como exclusão, porque a vaca pode ter lesões diferentes em unhas diferentes. Esses pares entram como diferencial, por meio de regras negativas.

## Restrições globais

- Todo texto voltado ao usuário fica em português. O projeto é só para vacas leiteiras em lactação.
- Todo conhecimento clínico novo tem `fonte` e `status: "suposicao_a_validar"`. Os dados são fictícios.
- `tratamento`: a URL é https de `embrapa.br`, `gov.br` ou `msdvetmanual.com`, conferida na web (HTTP 200 e conteúdo da doença). Nenhuma URL pode ser inventada.
- **Coerência com a triagem:** uma regra cuja pergunta pressupõe um sinal da triagem deve exigir esse sinal. Exemplos: o mau cheiro do pé exige `claudicacao`; o pus no corrimento exige `corrimento_vaginal`. Assim o motor não pergunta o que a triagem já negou.
- **Regras para o produtor:** precisam de pelo menos um sinal da triagem, para caber no limite de 15 perguntas, como na v0005.
- Uma versão só é ativada com 0 falhas nos casos. A v0007 continua imutável; o resultado é a v0008.
- Depois de ativar, regenerar:
  - os documentos 03 e 04: `python scripts/gerar_doc_regras.py --casos base/casos/casos.json --saida docs/entrega`;
  - o grafo 2: `kb.exportar_grafo`, depois `scripts/grafo_dados.py` com o Python de `graphify-out/.graphify_python`;
  - a cópia de desenvolvimento em `base/desenvolvimento/`, com símbolos, regras e triagem iguais aos da ativa.

## Foco de revisão

1. **Vaca mancando com dermatite digital típica (lesão em morango no talão):** a dermatite digital continua em primeiro lugar, sem perder para a úlcera de sola. Caso: `C-DD-PODAL-DIF`.
2. **Corrimento até 21 dias do parto:** a metrite vence e a endometrite é excluída. Depois de 21 dias, vale o contrário. Casos: `C-EXC-MET-END` e o caso positivo de endometrite.
3. **Vaca sem claudicação na triagem:** nenhuma pergunta de casco nova é feita. Teste: `test_sem_claudicacao_nao_pergunta_o_casco`.
4. **Cetose confirmada em vaca gorda no parto:** a lipidose hepática sobe junto, sem ser excluída, porque as duas coexistem. Caso: `C-N-LIP-01`.
5. **Desempenho:** a primeira análise com 25 doenças continua abaixo de 0,5 s. Teste: `test_primeira_analise_rapida_com_25_doencas`.

---

### Tarefa 1: casos de teste das 5 doenças (vermelho)

**Arquivos:**
- Modificar: `base/casos/casos.json`

**Interfaces:**
- Produz: 12 casos novos, que a Tarefa 2 deve fazer passar.
  - **Positivos (10):** `C-ULC-01`/`C-N-ULC-02`, `C-FLE-01`/`C-N-FLE-02`, `C-END-01`/`C-N-END-02`, `C-CIS-01`/`C-N-CIS-02`, `C-LIP-01`/`C-N-LIP-01`, um do produtor e um do veterinário por doença, como o teste de cobertura exige.
  - **De exclusão e diferencial (2):** `C-EXC-MET-END` e `C-DD-PODAL-DIF`.

- [ ] **Passo 1: escrever os 12 casos** no formato dos casos existentes (`kb/schema/caso.schema.json`), com `esperado.top1` e uma faixa para a doença-alvo.
  - Cada caso positivo marca na triagem o sinal que a regra exige (`claudicacao`, `corrimento_vaginal`, `apetite`…) e não contradiz a triagem.
  - `C-EXC-MET-END`: `dias_em_lactacao` 35, corrimento com pus e sem febre. O top1 esperado é `endometrite`; a metrite fica em `pouco_provavel`, com `situacao` igual a `descartada`.
  - `C-DD-PODAL-DIF`: claudicação com `lesao_erosiva_talao_morango` = sim. O top1 esperado é `dermatite_digital`.
- [ ] **Passo 2:** rodar os casos contra a base atual com `executar_caso` (como em `tests/casos/test_base_ativa.py`). O esperado é que os 12 casos novos FALHEM e os 60 antigos passem.
- [ ] **Passo 3:** commit `test(casos): 12 casos das 5 doenças novas (vermelho)`.

### Tarefa 2: conteúdo das 5 doenças e v0008

**Arquivos:**
- Criar: `base/fonte/doencas/{ulcera_sola,flegmao_interdigital,endometrite,cisto_ovariano,lipidose_hepatica}.json`
- Modificar:
  - `base/fonte/comum.json`: o par `metrite` × `endometrite` em `meta.exclusoes`, e os sinais compartilhados novos, se houver;
  - `base/fonte/indice.json`;
  - `base/fonte/doencas/dermatite_digital.json` e `metrite.json`, só para as regras negativas de diferencial, se forem necessárias.
- Gerar: `base/versoes/v0008.json` e `base/ativa.json` apontando para `v0008`. Atualizar `base/desenvolvimento/`.
- Testar: `tests/casos/test_perguntas_coerentes.py` e `tests/engine/test_desempenho.py`

**Interfaces:**
- Consome: os casos da Tarefa 1.
- Produz: a v0008 ativa com 25 doenças, todas com `tratamento`.

Sinais por doença. Use os ids de símbolo abaixo. As perguntas do produtor ficam em linguagem simples, e cada regra para o produtor exige o sinal de triagem indicado:

| Doença | Sinal de triagem exigido | Perguntas novas (produtor / veterinário) |
|---|---|---|
| `ulcera_sola` | `claudicacao` | `mancar_pata_traseira_sem_inchaco` / `lesao_sola_pinca_dor` (dor à pinça na sola ou na linha branca) |
| `flegmao_interdigital` | `claudicacao` | `inchaco_entre_unhas_mau_cheiro` / `fissura_interdigital_necrotica` |
| `endometrite` | `corrimento_vaginal` e `dias_em_lactacao > 21` | `corrimento_com_pus_apos_21_dias` / `metricheck_purulento` |
| `cisto_ovariano` | `dias_em_lactacao > 40` | `cio_irregular_ou_constante` / `estrutura_ovariana_maior_25mm` (palpação ou ultrassom) |
| `lipidose_hepatica` | `apetite` reduzido ou ausente | `vaca_gorda_no_parto` / `enzimas_hepaticas_elevadas` (AST ou GGT) |

- [ ] **Passo 1: escrever os 2 testes que falham:**
  - Em `tests/casos/test_perguntas_coerentes.py`, `test_sem_claudicacao_nao_pergunta_o_casco`. Com o quadro de `TRIAGEM` (claudicação = não), nenhum id de `{'mancar_pata_traseira_sem_inchaco', 'inchaco_entre_unhas_mau_cheiro'}` aparece em `_perguntas_feitas(TRIAGEM)`.
  - Em `tests/engine/test_desempenho.py`, `test_primeira_analise_rapida_com_25_doencas`. Com a base ativa, criar `Sessao(base, 'produtor')` e `limpar_memoria()`. O tempo de `responder_triagem('dias_em_lactacao', {'dias_em_lactacao': '15'})` deve ser menor que 0,5 s, e a base deve ter 25 símbolos `doenca`.
- [ ] **Passo 2:** rodar os dois testes. O esperado é FALHA, porque a base tem 20 doenças.
- [ ] **Passo 3: escrever os 5 arquivos de doença.**
  - Cada um tem no mínimo 2 perguntas para o produtor, 1 para o veterinário e 3 regras de evidência, sendo uma negativa (diferencial).
  - Cada um tem também `fonte`, `tratamento` (URL verificada) e uma regra de sinal isolado de peso baixo (0,05), no padrão da base.
  - Acrescentar o par excludente em `comum.json`.
  - Rodar `python -m kb.fonte juntar --autor equipe --nota "..."` sem `--salvar`. O validador não deve apontar erros.
- [ ] **Passo 4:** ajustar os pesos até os 72 casos passarem (60 antigos e 12 novos). Registrar no relatório cada peso alterado e o motivo.
- [ ] **Passo 5:** gravar e ativar.
  - Rodar `python -m kb.fonte juntar --salvar --autor equipe --nota "25 doenças: casco, reprodução e lipidose"`.
  - Rodar `Repositorio('base').ativar('v0008')`.
  - Atualizar a cópia de desenvolvimento.
  - Rodar a suíte inteira, `.venv/Scripts/python -m pytest -q`. O esperado é 0 falhas.
- [ ] **Passo 6:** commit `feat(base): v0008 com 25 doenças`.

### Tarefa 3: documentação, grafo 2 e conferência no navegador

**Arquivos:**
- Regenerar: `docs/entrega/03` e `04`, `graphify-out-dados/` e `obsidian/02-Dados de Treino/`
- Modificar:
  - `docs/entrega/01-processo.md`: linha 26/10 v0008 na linha do tempo;
  - `docs/entrega/02`, `05`, `06`, `README.md` e o `README.md` da raiz: v0008, 25 doenças, número de regras e de casos tirados da base, e as contagens de testes da suíte;
  - `CLAUDE.md`: "dados das 25 doenças".
- Testar: `tests/documentacao`

- [ ] **Passo 1:** regenerar os documentos e o grafo 2. Atualizar os números (versão, doenças, regras, casos, testes Python e Vitest) com os valores medidos, e nenhum valor estimado.
- [ ] **Passo 2:** rodar `.venv/Scripts/python -m pytest tests/documentacao -q`. O esperado é PASSAR.
- [ ] **Passo 3: conferir no navegador.** Iniciar o servidor (`.claude/launch.json`, porta 8001) e fazer dois fluxos:
  - **Produtor:** triagem com "mancar" e, em seguida, o inchaço com mau cheiro. O flegmão deve aparecer acima de 20%, com o botão "Como tratar".
  - **Especialista:** vaca com 35 dias e corrimento com pus. A endometrite deve vencer, e a metrite deve aparecer descartada.
- [ ] **Passo 4:** commit `docs: v0008 com 25 doenças e grafo 2` e push.
