# Arquitetura tecnológica — implementação disponível

O núcleo é um pacote Python independente de interface, banco e base clínica. A entrada é uma base JSON e um conjunto ordenado de observações da sessão; a saída inclui estado, parecer e explicações. O estado integrado em `codex-davi` inclui interface React, API FastAPI, módulo `kb/` e persistência SQLite. O editor gráfico continua fora desta entrega do frontend.

## Fluxo implementado

```mermaid
flowchart LR
    W[Navegador: React e TypeScript] <-->|HTTP JSON local| C
    J[base/ativa.json: v0002 imutável] --> K[kb: validação, versões e adaptação]
    K --> V[Base.de_dict e guardas]
    C[API FastAPI ou CLI/Python] --> S[Sessao e memória]
    V --> S
    S --> I[Inferência em três camadas]
    I --> Q[Seleção e parada]
    Q --> S
    I --> T[Traço de eventos]
    T --> E[Explicação: por quê e como]
    I --> P[Parecer e urgência]
    E --> C
    P --> C
    S <--> R[Snapshot JSON: exportar e restaurar]
    C <--> D[SQLite: animais, sessões e execuções de casos]
```

`scripts/rodar.ps1` inicia a API e serve a SPA em `127.0.0.1:8000`; `rodar.sh` oferece o fluxo equivalente para Linux/macOS. Na ausência de `web/dist/index.html`, os scripts instalam e compilam a interface. O contrato versionado em `contratos/openapi.json` contém **27 operações HTTP**. A documentação de rotas, configuração e execução está em [api/README.md](../../api/README.md); o contrato da base está em [kb/README.md](../../kb/README.md).

## Sete componentes do modelo conceitual dos organizadores

| Componente de [A], slide 14 | Implementação atual | Parte planejada |
|---|---|---|
| Interface com o usuário | React em `web/`, CLI `engine/__main__.py` e interface Python de `Sessao` | Editor gráfico |
| Motor de inferência | `inferencia`, `avaliacao`, `cf`, `selecao` e `parada`, consumidos pela API | Revisão/calibração clínica |
| Base de conhecimento | `kb/`, versões imutáveis, `base/ativa.json` e `base/versoes/v0002.json` | Edição no frontend e novas versões revisadas |
| Memória de trabalho | `memoria.py`, `Fato`, `sessao.py` e snapshot persistido pela API em SQLite | Ensaios em dispositivos físicos |
| Módulo de explicação | `traco.py` e `explicacao.py`, chamados por `porque`/`como` e exibidos em diálogos na web | Revisão de compreensão com usuários |
| Aquisição de conhecimento | Edição e revisão do JSON, com regras documentadas pelo gerador | Editor em grafo e revisão por especialista |
| Fontes externas de fatos | Argumento `ficha` e observações com origem `importacao` | Prontuário, sensores e conectores reais |

## Tecnologias e dependências

| Item | Estado comprovado |
|---|---|
| Linguagem do núcleo | Python 3.12+, verificado nesta máquina com Python 3.12.14 |
| Incerteza | `fractions.Fraction`, biblioteca padrão |
| Intercâmbio de dados | JSON, biblioteca padrão |
| Testes | `pytest`, `hypothesis`, `httpx`/`TestClient` e `unittest`; Camada 3 em `tests/casos/` |
| Documentação | Markdown e gerador Python com modo `--verificar` |
| Navegação do conhecimento | Graphify e exportação Obsidian, ferramentas auxiliares fora da consulta |
| Dependências de runtime externas do núcleo | Nenhuma |
| API e base editorial | FastAPI/Pydantic, `kb/`, JSON Schema e OpenAPI versionados; versões em `pyproject.toml` |
| Banco | SQLite para animais, sessões, versões e resultados dos casos |
| Web | React 19, TypeScript 5 e Vite 8; Vitest, Testing Library, Playwright/Chromium e axe para verificação |
| Editor gráfico | Pendente, fora deste recorte |
| Licença do projeto | Arquivo de licença ausente; decisão da equipe pendente |

O motor e os exemplos CLI continuam usando só a biblioteca padrão. A API e os testes completos exigem as dependências de `pyproject.toml`: criar `.venv` e instalar `.[dev]` uma vez, com internet. O build web requer Node.js 24 e usa o lockfile do npm. A execução da decisão não chama serviços externos.

## Camada web implementada

`web/src/api/tipos.gerado.ts` deriva do OpenAPI por `npm run gerar-tipos`. O cliente HTTP centraliza erros públicos; as páginas Início, Anamnese e Parecer usam rotas React. A API serve o build e resolve URLs da SPA, preservando as rotas `/api/`.

O navegador não infere doença, CF, urgência nem próxima pergunta. Renderiza os campos e opções de `EstadoSessao.proxima`; múltiplas respostas enviam todos os booleanos e desconhecimento envia `nao_sei`. Números seguem como texto bruto, sem conversão ou normalização de vírgula. Um 422 conserva o valor e mostra a mensagem no campo; um conflito 409 provoca leitura do estado, sem repetição automática da mutação. O botão fica bloqueado durante o envio.

A partir da segunda pergunta, a lateral apresenta os quatro maiores percentuais retornados por `/parecer`. A tabela final conserva os blocos da API e ordena seus itens por percentual. As barras usam `role="meter"`. Os diálogos por quê/como mostram regras e evidências do backend; a pausa de bandeira tem precedência sobre `proxima: null` e mantém o foco até uma ação autorizada.

O histórico desta navegação permite voltar e corrigir por PUT; o estado clínico persistente pertence à API. Recarregar a página retoma a sessão pelo identificador, mas não reconstrói o histórico local de botões Voltar. O contrato atual não expõe `casas_decimais` na próxima pergunta; a precisão é validada pelo backend (R18). Fontes `@fontsource`, SVGs e estilos são empacotados localmente. Os cenários E2E usam API real, SQLite temporário e casos sintéticos da `v0002`.

A troca produtor ↔ especialista usa `PATCH /api/sessoes/{id}`, com `veterinario` como nome técnico do especialista. Mantém os fatos, o histórico desta navegação e um único parecer da API; controla confirmação, concorrência e conflitos sem cálculo clínico no navegador. Também está disponível na pausa e no parecer parcial. Para corrigir uma tela antiga cujos símbolos mudam entre modos, a interface usa o modo original para o PUT e restaura o escolhido sob a mesma trava, reconciliando falhas com GET. O protocolo e seus limites estão no [roteiro](05-apresentacao-e-demo.md).

Após encerrar voluntariamente pelo alerta, Continuar respondendo envia a ação de bandeira `continuar` e navega conforme o estado recebido. Conflito 409 relê a sessão. Uma parada automática do motor não pode ser anulada pela interface; a limitação e o pedido à API estão em R21.

## Motor e modelo de incerteza

Uma observação é representada por símbolo, valor, CF e origem. Intensidade é valor, não certeza. Um booleano falso carrega evidência negativa; `None` ou `nao_sei` carrega CF zero. Campo vazio da ficha é ausente e pode ser perguntado; desconhecimento explícito conta como resposta.

As camadas são estritas: derivados consomem perguntas/ficha; doenças consomem esses fatos e derivados; urgências e bandeiras consomem camadas inferiores. Uma regra não lê uma conclusão de sua própria camada. A agenda resolve por camada, prioridade decrescente, número de condições e ID. As prioridades da base são 100 para bandeiras, 50 para urgências e 10 para evidências.

O CF da premissa é o mínimo das condições. A regra dispara somente se esse mínimo for **maior que 0,20**; sua contribuição é `CF_premissa × CF_regra`. Pesos ficam entre −0,99 e +0,99. Para duas evidências `a` e `b`, a combinação é:

| Sinais | Combinação |
|---|---|
| Ambas não negativas | `a + b × (1 − a)` |
| Ambas não positivas | `a + b × (1 + a)` |
| Sinais opostos | `(a + b) / (1 − min(abs(a), abs(b)))` |

A guarda defensiva de conflito entre extremos retorna zero. A aritmética interna é racional, evitando arredondamento prematuro. O operador `max` é permitido em derivados positivos; na base atual agrupa dois relatos da alteração do leite.

O parecer exibe `max(0, CF) × 100`, com arredondamento meio para cima, e três blocos: principal a partir de 0,50, diferencial acima de 0,20 e abaixo de 0,50, pouco provável até 0,20. Os cortes de exibição vêm da base. Essa porcentagem é confiança do sistema, **não probabilidade**.

## Diálogo, parada e bandeiras

As seis telas de triagem vêm antes das perguntas dinâmicas. Produtor e veterinário compartilham fatos e motor; disponibilidade e texto das perguntas mudam por modo. A base limita a fase dinâmica a 12/25 perguntas. Perguntas capazes de confirmar uma bandeira pendente têm preferência na seleção.

Após a triagem, a parada considera confirmação, hipóteses concorrentes, potencial conservador, bandeiras pendentes, ausência de perguntas e limite. `limite_dinamico=0` nos dois exemplos é uma substituição por sessão usada para demonstrar somente a triagem.

Bandeira ativa leva a `chamar_agora`, independentemente da hipótese de doença. O produtor recebe pausa; o veterinário não. Respostas novas não reduzem a urgência já travada. A implementação atual trata correções reprocessando os valores atuais por prefixos dos lotes na **ordem real de entrada**: ficha, telas e perguntas. Corrigir não muda essa ordem. Uma bandeira só desaparece se nenhum prefixo com os dados corrigidos a disparar. O reconhecimento vale apenas para bandeiras ativas.

O núcleo `inferir(base, fatos)` é sem estado. O estado de uma sessão também inclui ordem e reconhecimento. Portanto, determinismo da sessão significa mesma base, mesmos valores, mesma ordem e mesmas ações; não significa ignorar a ordem de chegada dos dados.

## Contratos Python disponíveis

| Entrada pública | Responsabilidade |
|---|---|
| `Base.de_dict(dados)` | Validar e adaptar JSON ou objeto com `model_dump` |
| `inferir(base, fatos)` | Calcular CF, regras disparadas, urgência e traço |
| `analisar(base, fatos, modo)` | Calcular hipóteses abertas, potencial e próxima pergunta |
| `Sessao(base, modo, ficha, limite_dinamico)` | Gerenciar triagem e diálogo |
| `estado`, `responder_triagem`, `responder`, `trocar_modo`, `acao_bandeira` | Operar a consulta |
| `parecer`, `porque`, `como` | Consultar saídas e explicações |
| `exportar` / `Sessao.restaurar(base, **snapshot)` | Serializar e restaurar diretamente o estado |
| `executar_caso(base, caso)` | Executar cenário determinístico e conferir critérios |

Assinaturas completas e exemplos estão no [README do motor](../../engine/README.md). A documentação desta entrega não muda o contrato público.

Para restauração exata, persistir o snapshot completo, inclusive `ordem_respostas`, origens, `tela_id`, perguntas feitas e reconhecimento. Sem a ordem explícita, o método pode derivar uma aproximação que diverge em telas reabertas ao trocar de modo. O parâmetro antigo `bandeiras_ativas` é aceito por compatibilidade e ignorado; as bandeiras são reconstruídas pelos lotes. Isso não equivale a repetir o diálogo pela API.

## Base, validação e rastreabilidade

A base ativa tem `meta`, `simbolos`, `regras` e `layout`, com 51 símbolos e 56 regras. `base/ativa.json` aponta para `v0002`; esse arquivo imutável foi recebido da branch compartilhada e preservado. `kb.validar` não registra erros (W03 informa as 56 suposições pendentes). `Base.de_dict(kb.para_motor(base))` carrega no motor. O arquivo de desenvolvimento foi alinhado aos domínios numéricos da `v0002`, sem mudar IDs, regras ou triagem. Dias em lactação aceita 0–1000 inteiros; temperatura retal, 30–45 °C com uma casa; pH ruminal, 0–14 com uma casa; BHB e cálcio sérico, 0–20 com duas casas. As versões imutáveis foram preservadas.

Uma alteração de regra deve ser gravada com `Repositorio.salvar_nova(..., pai="v0002")`, tornando-se uma versão nova; executar os casos antes de ativar. `v0001` não foi regravada nem promovida a base clinicamente validada. Os 34 casos em `base/casos/casos.json` cobrem os dois modos, oito doenças, seis bandeiras, comorbidade, limite, troca de modo e os dois exemplos preservados. A correção é testada diretamente em `Sessao`, pois `kb.Caso` não codifica essa operação. Os desvios e a observação prévia do caso de abomaso estão em R15/R16 do [registro de riscos](06-riscos-e-pendencias.md).

Os eventos documentam observações, regras e combinações de CF. O motivo de uma pergunta é registrado quando ela é apresentada. A sessão conserva perguntas/correções e somente o cálculo de inferência atual, evitando acumulação de traços antigos. O documento 03 é gerado do JSON; o documento 04, da execução dos casos. O teste de sincronismo impede afirmar uma regra diferente da executável.

## Testes, execução e limites

No checkpoint da troca de modo (`09f5754`), a suíte registra **1066 testes Python aprovados, 1 ignorado e 170 subtestes aprovados**; a suíte `unittest` do motor/base registra **132 testes**, já incluídos na execução pytest, e não deve ser somada a ela. Os **34 casos sintéticos** são uma categoria separada. A interface registra **60 testes Vitest** e **11 cenários Playwright**, descritos em [QUALIDADE.md](../../web/QUALIDADE.md); 39/8 são as contagens históricas da integração inicial. As evidências históricas anteriores constam de [evidencias-verificacao.json](evidencias-verificacao.json). Entre as verificações estão permutações MYCIN, desconhecimento, comorbidade, correção, restauração e isolamento do motor em relação à API, ao banco e a `kb`.

O ensaio HTTP histórico da API é registrado separadamente dos testes atuais no navegador. Ensaio físico com Wi-Fi desligado, máquina reserva e apresentação ainda exigem confirmação da equipe. Não há validação clínica nem autenticação implementada neste recorte. A integração acrescentou `web/` e preparo do build nos scripts; API, motor, kb, contratos e versões imutáveis foram preservados.
