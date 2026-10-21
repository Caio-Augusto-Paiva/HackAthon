# SDD ledger — plan: docs/superpowers/plans/2026-10-21-kb-secao-2.md

Spec: docs/superpowers/specs/2026-10-20-anamnese-bovinos-design.md (Seção 2, Seção 5.1 camada 2). Branch: sessao-pair-programming (base fd4180d).

## Varredura prévia
| Par / tarefa | Produz → consome | Achado |
|---|---|---|
| T1 → T2, T3, T4, T5, T6 | modelos `Base`, `Simbolo`, `Regra`, `Tela`, `Caso`, `carregar_base` | nomes consistentes em todas as tarefas |
| T2 → T3 | `simbolos_triagem` | T3 depende de T2 (ordem sequencial atende) |
| T2 → T4 | `perguntavel`, `simbolos_triagem`, `derivados_de_triagem`, `derivados_com_cf_negativo`, `encontrar_ciclo`, `CAMADA`, `regras_que_concluem` | consistente |
| T4 → T5 | `validar`, `Relatorio` | consistente |
| T1/T6 ↔ engine | `Base.model_dump(mode="json", exclude_none=True)` → `engine.modelos.Base.de_dict` | risco: chaves extras (`layout`, `bloco_*`) — coberto pelo teste de T6 |
| T1 | fixture mínima "zero erros e zero avisos" vs tabela de T4 | coerente: todos os símbolos perguntáveis são usados; `sem_problema` não é perguntável |
| T3 | ida e volta com defaults preenchidos | coerente (igualdade de modelos após defaults) |
| T4 | tabela E01–W03 vs regras de cálculo | E05/E12 conjuntos; E10 aceita E11; E09 exclusivo — já anotados no plano |
| T5 | `salvar_nova` valida antes de gravar | coerente com Seção 2 ("bloqueia se houver erro") |

## Rulings prévios
- Ruling: tarefas executadas em sequência (1→2→3→4→5→6), não em paralelo como o plano sugere — a skill proíbe implementadores simultâneos no mesmo checkout — custo: mais tempo de relógio.
- Ruling: ambiente `.venv` com Python 3.12 e pip, não 3.14 com uv — é o que existe nesta máquina e o motor já exige 3.12+; `pyproject.toml` segue compatível com `uv sync` — custo se errado: ajustar `requires-python` depois.
- Ruling: sem worktree; trabalho direto no branch `sessao-pair-programming` (o colega mexe só em `engine/`), push só após a revisão final — custo: rebase se o colega publicar antes.
- Ruling: casos inválidos do validador como mutações em código (pytest parametrizado), não como arquivos `kb_invalidas/E##_*.json` da Seção 5.1 — menos arquivos, mesma cobertura — custo: divergência de forma com a 5.1.
- Ruling: `kb/analise.py`, `kb/modelos.py` e `kb/carregador.py` (donos: pessoa A, Seção 4.8) implementados aqui junto com o resto da Seção 2 — entrega coesa — custo: A revisa depois.

## Tarefas
Task 1: dispatched (base fd4180d)
Task 1: minor (deferred): `Condicao.valor` sem `int` na união converte 21 → 21.0 no dump (kb/modelos.py:115)
Task 1: minor (deferred): `carregar_base` levanta JSONDecodeError/FileNotFoundError, não ValidationError (kb/modelos.py:240)
Task 1: minor (deferred): teste da fixture do motor fixa prioridade == 0 (tests/kb/test_modelos.py:580)
Task 1: minor (deferred): só `limiares.confirmacao` testado entre os 8 defaults
Task 1: complete (commits fd4180d..7905495, review clean)
Ruling: formato de id (símbolo `^[a-z0-9_]+$`, regra `^[A-Za-z0-9_-]+$`) vira erro E20 `id_invalido` do validador (Task 4) — a restrição global existe mas a tabela de códigos não a cobria — custo se errado: um código a mais no relatório.
Task 2: dispatched (base 643c3ec)
Task 2: ⚠️ resolvido pelo coordenador: `Simbolo.pergunta` é dict com default {} (kb/modelos.py), nunca None.
Task 2: minor (deferred): ciclos disjuntos, losango, ciclo inalcançável a partir do 1º nó e base vazia sem teste
Task 2: minor (deferred): direção do caminho do ciclo (concluído → lido) não documentada; mensagem " -> " engana — Task 4 deve exibir no sentido do fluxo de dados
Task 2: minor (deferred): testes acoplados a índices da fixture; teste de ValueError não confere a mensagem; recursão em `visitar`
Task 2: complete (commits 643c3ec..2bcf4a1, review clean)
Task 3: dispatched (base 2bcf4a1)
Ruling: `valor: None` explícito em condição é preservado na ida e volta (via `model_fields_set` da `Aresta`), não proibido — a spec exige conversão 1:1 sem perda; quem decide se None é válido é o validador — custo se errado: um campo a mais a tratar no editor.
Task 3: minor (deferred): ids de aresta duplicados/não canônicos aceitos; chaves de layout sem nó; ValidationError do Pydantic em inglês; `Grafo.versao` ignorado; teste de embaralhamento pode passar vazio; supressão de health check desnecessária
Task 3: fix round 1/5 (3 addressed, 0 open — valor None preservado; id do nó vs dados; teste de nó duplicado; commits 973b3f3..c973f2c)
Task 3: minor (deferred): `op=None`/`negado=None` explícitos na aresta viram default sem erro (kb/grafo.py:125); editor que serializa null em campo não definido muda `valor` para None
Task 3: complete (commits 2bcf4a1..c973f2c, review clean)
Ruling: `valor` None em condição é erro E03 `valor_invalido` no validador — a conversão preserva o None, mas ele não tem significado clínico — custo se errado: base com None explícito deixa de salvar.
Ruling: o validador exibe o caminho do ciclo no sentido do fluxo de dados (lido → concluído), invertendo o que `encontrar_ciclo` devolve — achado menor da Task 2 — custo se errado: só a mensagem.
Task 4: dispatched (base c973f2c)
Task 4: implemented (commit e099918, 179 testes ok) — task review dispatched; resultado pendente. Retomar: ler review de c973f2c..e099918 e seguir o loop.
Ruling: E17 estrito com pivô 0 (`descarte < 0 < premissa < … < confirmacao`; `bloco_diferencial < bloco_principal`) — texto literal da spec — custo se errado: nenhum.
Ruling: E08 só quando NENHUMA condição da bandeira é de triagem; derivados de triagem contam como triagem (mesmo critério do E11) — spec diz "sem nenhuma condição sobre símbolo da triagem" — custo se errado: aceitar bandeira cuja única condição é derivado de triagem.
Ruling: E15 mantém o erro para `cf_minimo` e `cf_maximo` na mesma condição — o plano manda "no máximo um dos dois por condição" e o motor (engine/validacao.py) rejeita os dois juntos; o revisor não via isso — custo se errado: perder a faixa "entre" numa condição.
Ruling: E16 exige texto nos dois modos — spec: "tela de triagem sem texto em algum dos dois modos" — achado menor do revisor descartado.
Task 4: minor (deferred): E06 cobre leitura de doença sem regra (documentar); mensagem E00 com texto do Pydantic em inglês; lacunas de teste (id de regra inválido, E02 entre regras, E04 abaixo de −0,99, E14 caso negativo, E19 evidência → sem_problema, conjunto exato de avisos)
Task 4: fix round 1/5 (4 addressed, 0 open — E17 estrito com pivô 0; E08 quantificador; E15 mantido por ruling; teste de ciclo exato; commits e099918..981ffdd)
Task 4: complete (commits c973f2c..981ffdd, review clean)
Task 5: dispatched (base 981ffdd)
Ruling: `.gitattributes` com `base/** text eol=lf` (e kb/schema/*.json) entra na Task 6 — com autocrlf o checkout no Windows grava CRLF e o hash da versão difere entre PCs — custo se errado: nenhum.
Ruling: escrita interrompida de versão tratada com try/except BaseException que apaga o arquivo recém-criado em modo "x" (cobre erro de escrita, não queda de energia); sem os.link — suficiente para o PoC e sem depender do sistema de arquivos (OneDrive) — custo se errado: arquivo truncado após queda de energia.
Task 5: minor (deferred): `pai` explícito não verificado; ida e volta completa salvar→carregar sem teste; overflow após v9999
Task 5: fix round 1/5 (5 addressed, 0 open — guarda de id de versão; limpeza de escrita interrompida; FileExistsError em português; ativa.json atômico; hash real no teste; commits 4d6771d..e229a19)
Task 5: minor (deferred): temporário fixo `ativa.json.tmp` (concorrência); caminho de falha de `ativar` sem teste; sem fsync; `pai` explícito não validado
Task 5: complete (commits 981ffdd..e229a19, review clean)
Task 6: dispatched (base e229a19)
Ruling: testes do kb exigem o .venv (pydantic); o comando do motor com o Python do sistema passa a ser `python -m unittest discover -s tests/engine -t .` — sem mudar o engine — custo se errado: o colega precisa trocar o comando.
Task 6: minor (deferred): fato numérico inerte no teste de equivalência (fixture do motor não tem regra numérica); teste sem prioridade só compara CF; padrão `base/**` sem diretório ainda
Task 6: complete (commits e229a19..59c4077, review clean)
Final review: With fixes — 2 Important (kb aceita bases que o motor recusa; grafo exige `ordem` ausente do contrato 4.5.3), 8 minor.
Ruling: E14 passa a cobrir `combinacao: max` fora de derivado e regra de derivado max com cf ≤ 0 (código `derivado_max_negativo` mantido) — spec: "max só em derivado" e "todas as regras com cf_regra positivo" — custo: nenhum.
Ruling: novo E21 `tela_simbolo_invalido` (tela da triagem com símbolo que não é pergunta/ficha); id de tela duplicado entra no E02 — o motor rejeita os dois — custo: dois códigos a mais no README.
Ruling: `allow_inf_nan=False` em todos os modelos e `LimiteDinamico` com `ge=0` — o motor rejeita NaN e limite negativo — custo: nenhum.
Ruling: `Aresta.ordem` opcional; sem `ordem`, vale a posição na lista; duplicata só entre ordens explícitas — contrato 4.5.3 não tem `ordem` — custo: nenhum.
Ruling: rodada única de correção da revisão final inclui também `validar_edicao`, verificação de `pai`, reexports do `kb/__init__.py`, pydantic `>=2.14,<2.15`, memoização em `_produtor_ok`, `dados.id` ausente preenchido por `no.id`, campos de papel errado na aresta rejeitados, helper `para_motor` — preparam o caminho da API — custo: mais diff numa só rodada.
Final fix wave: 13 addressed, 0 open (commits 59c4077..f4adac5); re-review clean. Verificação: 280 passed, motor 56 OK, compileall ok, engine intacto.
