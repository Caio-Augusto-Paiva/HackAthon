# CLAUDE.md — PoC "Anamnese de Bovinos Leiteiros" (Hackathon UFJF 2026)

Projeto: sistema especialista para o Hackathon UFJF 2026 (XXVIII Semana da Computação DCC/UFJF, proposto pela RERUM Engenharia de Sistemas). Escreva tudo em português.

Fontes oficiais: **[A]** = `apresentacaoRerun.pdf` (16 slides); **[D]** = `DocumentárioRerun.pdf` (3 páginas).

## Grafo de conhecimento — ler PRIMEIRO, em todo prompt

Para economizar tokens, **não leia o projeto inteiro**. O conhecimento do projeto (instruções, especificação, fontes, transcrições dos PDFs, pesquisas, revisões, plano e README do motor) está num grafo:

1. **Antes de qualquer tarefa**, leia `graphify-out/GRAPH_REPORT.md` (mapa: nós centrais, comunidades, conexões). Para perguntas específicas, use `graphify query "<pergunta>"` (ou `/graphify query`), que percorre `graphify-out/graph.json`.
2. Abra um arquivo do repositório **só** quando o grafo apontar para ele (`source_file`/`source_location`) ou quando for editá-lo.
3. A fonte canônica do desenho é `docs/superpowers/specs/2026-10-20-anamnese-bovinos-design.md`; `docs/prompts/` e `docs/rascunhos/` são histórico e ficam fora do grafo.
4. O escopo do grafo está em `.graphifyignore` (código e testes ficam de fora; serão o grafo 2).

## Manter o grafo atualizado — sempre que houver documento novo ou alterado

Sempre que criar ou alterar um documento de conhecimento (qualquer `.md` em `docs/`, este `CLAUDE.md`, `engine/README.md`, ou um JSON de referência em `docs/referencias/`), **no mesmo trabalho**:

1. Se for PDF só de imagem, crie antes uma transcrição `.md` em `docs/fontes/` (PDFs ficam fora do grafo; a transcrição entra).
2. Atualize o grafo de forma incremental: `/graphify . --update` (reextrai só o que mudou).
3. Regenere o cofre do Obsidian: `graphify export obsidian --dir obsidian/01-conhecimento`.
4. Faça o commit junto: o documento, `graphify-out/` e `obsidian/01-conhecimento/`.

Pastas do Obsidian: `obsidian/01-conhecimento/` (grafo 1, abrir como cofre no Obsidian) e `obsidian/02-a-definir/` (grafo 2, reservado).

## Papel e limite da sessão de planejamento

- Esta fase é só de **planejamento**: arquitetura, motor de inferência, base de conhecimento, linguagens e bibliotecas, estrutura de pastas, contratos de API, estratégia de testes e execução em localhost.
- **NÃO escreva código de implementação.** Arquivos de especificação e de plano em Markdown são permitidos; código-fonte não.
- Pare depois do plano. Não comece a implementar sem ordem explícita.

## Processo obrigatório

1. **Antes de qualquer coisa**, explicar em poucos parágrafos o que é um sistema especialista e como funciona um motor de inferência: encadeamento para frente e para trás, resolução de conflito, fatores de certeza, explicação "por quê?" e "como?" (diretriz do hackathon, [A] slide 12, passo 2).
2. Usar a skill `superpowers:brainstorming` para refinar escopo e desenho. Uma pergunta por vez, alternativas com recomendação. Ao final, gravar a especificação aprovada em `docs/superpowers/specs/`.
3. Após aprovação da especificação, usar `superpowers:writing-plans` para gerar o plano em `docs/superpowers/plans/`: tarefas pequenas e verificáveis, com testes definidos antes do código de cada tarefa.
4. Parar depois do plano.

## O desafio

- **Objetivo:** "construir uma aplicação para usuário final que resolva um problema da pecuária leiteira por meio de uma base explícita de conhecimento e um motor de inferência" ([A] slide 8; [D] p. 3).
- **Tema: T1 Anamnese.** "Coleta estruturada de sinais e histórico de bovinos leiteiros em lactação, com triagem explicável" ([A] slide 9; [D] p. 3).
- Arquitetura comum aos três temas: base de conhecimento + motor de inferência + aplicação; o tema só define o conhecimento a modelar ([A] slide 9).

### Restrições obrigatórias

1. **Não usar a LLM como o sistema especialista.** "A LLM gera, explica e ajuda a extrair regras; a decisão sai de uma base de conhecimento explícita e de um motor de inferência" ([A] slides 8 e 13; [D] p. 3). Nenhuma chamada a LLM no caminho da decisão em tempo de execução.
2. Decisão **determinística e auditável** ([A] slide 8).
3. **Open source**; a linguagem é escolha do grupo ([A] slides 3 e 13; [D] p. 2).
4. **Rodar por completo em LOCALHOST** ([A] slides 10 e 15; [D] p. 3). Nenhum serviço em nuvem obrigatório.
5. Desenvolvimento apoiado por agente de IA ([A] slide 3; [D] p. 2).

### Componentes da arquitetura ([A] slides 8 e 14, Modelo Conceitual)

| Componente | O que o documento pede |
|---|---|
| Base de conhecimento | regras de produção explícitas, variáveis, pesos (CF); versionada e revisada |
| Motor de inferência | casa regras com fatos, resolve conflito, dispara; encadeamento, incerteza, explicação |
| Memória de trabalho | fatos da sessão atual: respostas + conclusões |
| Módulo de explicação | responde "por quê?" e "como?" a partir do traço de inferência |
| Interface do usuário | exibe perguntas, coleta respostas e apresenta o parecer final; diálogo, resultado explicável |
| Aquisição de conhecimento | especialista + engenheiro editam a base |
| Fontes de dados externas | prontuário, sensores, APIs alimentam a memória de trabalho |

### Testes ([A] slide 13)

"Defina casos de teste com resultado esperado junto com o conhecimento do domínio e valide cada versão da base." Prever casos conhecidos (entrada → triagem esperada) executados contra cada versão da base.

### Entregáveis e prazos ([A] slides 3, 10 e 15; [D] p. 2)

- **Demonstração** em localhost.
- **Documentação obrigatória:** processo de desenvolvimento, arquitetura tecnológica e regras de produção.
- **Apresentação obrigatória:** todo o processo, do uso da IA ao resultado.
- Início terça 20/10 às 9:00; envio de documentação, apresentação e código-fonte até **quinta 22/10 às 20:00**; apresentação sexta 23/10 às 9:00. O plano tem que caber em cerca de dois dias e meio.

### Avaliação ([A] slides 3, 5 e 11; [D] p. 2)

- Nota de 1 a 10 pelo potencial de resolver de fato o problema.
- Complexidade e assertividade desempatam e definem a nota de partida.
- Avaliam também a organização do grupo com a IA e o conhecimento adquirido.
- Habilidade com agentes de IA, trabalho em equipe, liderança e controle emocional.

### Passo a passo sugerido ([A] slide 12; [D] p. 3)

1. Escolher o agente de IA. 2. Pedir à IA que explique sistema especialista e motor de inferência. 3. Escolher a tecnologia. 4. Pesquisar o contexto de negócio. 5. Definir escopo e diretrizes da arquitetura. 6. Definir as regras de produção. 7. Implementar e testar. 8. Estudar em detalhes o que foi produzido.

A fase de planejamento cobre os passos 2 a 6.

## Decisões já tomadas (não vêm dos documentos)

- **Tema:** T1 Anamnese.
- **Motor gráfico:** editor visual onde se desenha o fluxo da anamnese (perguntas, condições, regras, conclusões) como grafo. Corresponde ao componente "Aquisição de conhecimento".
- **Linguagens:** Python no backend, React no frontend (inicialmente).

## Proposta inicial de arquitetura (hipótese a validar no brainstorming)

- Motor de regras em Python, puro e independente de interface (pacote próprio, testável sem web): encadeamento, resolução de conflito, fatores de certeza, traço de inferência.
- Base de conhecimento/fluxo como dado versionável (JSON ou YAML com schema), lido pelo editor gráfico e pelo motor; cada versão testável.
- API: FastAPI + Pydantic.
- Frontend: React + TypeScript; React Flow no editor gráfico; tela de anamnese em diálogo, com parecer e explicação.
- Persistência: SQLite.
- Testes: pytest (motor e casos conhecidos) e Playwright (ponta a ponta).
- **Dados fictícios apenas.** Nenhum dado real de propriedade ou animal.

## O plano final deve conter

1. Escopo do PoC (o que entra e o que fica de fora, justificado pelo prazo).
2. Diagrama Mermaid mapeando cada componente do modelo conceitual ([A] slide 14) a um módulo do código.
3. Desenho do motor: tipo de encadeamento e por quê, resolução de conflito, modelo de incerteza (representação e combinação dos CF), formato do traço e geração de "por quê?" e "como?".
4. Formato da base: schema, versionamento, conversão grafo ↔ regras, validação (ciclos, variáveis não definidas, regras inalcançáveis).
5. Conhecimento do domínio: sinais, histórico, categorias de triagem e regras em pseudocódigo, **cada uma marcada como suposição a validar** com especialista ou RERUM.
6. Linguagens, bibliotecas e versões (todas open source) com justificativa.
7. Estrutura de pastas do monorepo e contratos da API (endpoints, payloads).
8. Estratégia de testes: casos conhecidos por versão da base, unitários do motor, ponta a ponta.
9. Execução em localhost com o mínimo de comandos (script ou `docker compose`), sem nuvem.
10. Plano por dia até 22/10 às 20:00, com marcos verificáveis e o que cortar se o prazo apertar.
11. O que vai para a documentação e a apresentação (processo, arquitetura, regras de produção, uso da IA).
12. Riscos e pontos em aberto.

## Regras de conduta

- Não inventar requisitos dos organizadores. Tudo que não vier de [A] ou [D] deve ser marcado **(suposição)**.
- Conhecimento veterinário (doenças, limiares, sinais clínicos) é sempre **(suposição a validar)**; citar a fonte quando usar uma.
- Respeitar as restrições obrigatórias em toda proposta; se uma escolha conflitar com elas, dizer isso explicitamente.
