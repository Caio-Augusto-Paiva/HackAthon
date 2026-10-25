# CLAUDE.md — PoC "Anamnese de Bovinos Leiteiros" (Hackathon UFJF 2026)

Projeto: sistema especialista para o Hackathon UFJF 2026 (XXVIII Semana da Computação DCC/UFJF, proposto pela RERUM Engenharia de Sistemas). Escreva tudo em português.

Fontes oficiais: **[A]** = `apresentacaoRerun.pdf` (16 slides); **[D]** = `DocumentárioRerun.pdf` (3 páginas).

## Grafo de conhecimento — só quando precisar procurar

O grafo é uma ferramenta de **busca**, não uma leitura obrigatória. **Não abra o grafo (nem `GRAPH_REPORT.md`) no início do prompt** nem "para se contextualizar".

**Não use o grafo quando:** a tarefa já diz qual arquivo ou trecho mexer; a informação já está nesta conversa ou neste `CLAUDE.md`; ou o assunto é código e testes (fora do grafo, ver `.graphifyignore`) — aí use `Grep`/`Glob` direto.

**Use o grafo quando** precisar **localizar** uma informação ou um arquivo que você não sabe onde está (decisão, regra, fonte, pesquisa, revisão, requisito), ou recapitular um assunto da documentação. Nesse caso, em vez de ler ou varrer os arquivos de `docs/`, pare no primeiro passo que responder:

1. **Pergunta pontual (primeira opção):** `graphify query "<pergunta>"`, que percorre `graphify-out/graph.json` e devolve só os nós relevantes com `source_file` e `location`.
2. **Assunto inteiro:** a nota `obsidian/01-conhecimento/_COMMUNITY_<nome>.md` e, dela, os links `[[...]]` necessários.
3. **Visão geral do projeto (raro, custa ~7 mil tokens):** `graphify-out/GRAPH_REPORT.md`.
4. **Arquivo original, só se:** for editá-lo; a nota não tiver o detalhe (abra só o trecho em `location`); ou o arquivo estiver fora do grafo.

A fonte canônica do desenho é `docs/superpowers/specs/2026-10-20-anamnese-bovinos-design.md`; `docs/prompts/` e `docs/rascunhos/` são histórico e ficam fora do grafo.

## Manter o grafo atualizado — uma vez por bloco de trabalho

Atualizar o grafo reextrai os documentos com subagentes (a primeira extração custou ~520 mil tokens; ver `graphify-out/cost.json`). Por isso **não atualize a cada documento**. Atualize **uma vez, ao fechar um bloco de trabalho** que tenha criado ou alterado documentos de conhecimento (`.md` em `docs/`, este `CLAUDE.md`, `engine/README.md`, JSON em `docs/referencias/`), antes do push:

1. PDF só de imagem: crie antes a transcrição `.md` em `docs/fontes/`.
2. `/graphify . --update` (incremental) e `graphify export obsidian --dir obsidian/01-conhecimento`.
3. Commit separado: `graphify-out/` e `obsidian/01-conhecimento/` (`chore(grafo): atualiza grafo`).

Mudanças só em código, testes, `web/`, `docs/prompts/` ou `docs/rascunhos/` **não** pedem atualização do grafo.

Pastas do Obsidian: `obsidian/01-conhecimento/` (grafo 1: documentação, abrir como cofre no Obsidian) e `obsidian/02-Dados de Treino/` (grafo 2: dados das 20 doenças, gerado sem IA a partir de `base/fonte/`; ver o README da pasta).

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
- Início terça 20/10 às 9:00; envio de documentação, apresentação e código-fonte até **quinta 22/10 às 20:00**; apresentação sexta 23/10 às 9:00.

### Avaliação ([A] slides 3, 5 e 11; [D] p. 2)

- Nota de 1 a 10 pelo potencial de resolver de fato o problema.
- Complexidade e assertividade desempatam e definem a nota de partida.
- Avaliam também a organização do grupo com a IA e o conhecimento adquirido.
- Habilidade com agentes de IA, trabalho em equipe, liderança e controle emocional.

### Passo a passo sugerido ([A] slide 12; [D] p. 3)

1. Escolher o agente de IA. 2. Pedir à IA que explique sistema especialista e motor de inferência. 3. Escolher a tecnologia. 4. Pesquisar o contexto de negócio. 5. Definir escopo e diretrizes da arquitetura. 6. Definir as regras de produção. 7. Implementar e testar. 8. Estudar em detalhes o que foi produzido.

## Estado atual e onde está cada coisa

Fase de **implementação e entrega**. A especificação e os planos já foram aprovados; não refaça brainstorming nem plano sem pedido.

- Desenho canônico: `docs/superpowers/specs/2026-10-20-anamnese-bovinos-design.md`; planos em `docs/superpowers/plans/`.
- Código: `engine/` (motor, Python só com biblioteca padrão), `kb/` (validação e versões da base), `api/` (FastAPI + SQLite), `web/` (React + TypeScript, feito pelo Codex), `base/` (versões imutáveis; ativa em `base/ativa.json`).
- Documentação de entrega: `docs/entrega/`.
- Editor gráfico da base e sensores ficaram **fora do escopo** do PoC.
- **Dados fictícios apenas.** Nenhum dado real de propriedade ou animal.

## Regras de conduta

- Não inventar requisitos dos organizadores. Tudo que não vier de [A] ou [D] deve ser marcado **(suposição)**.
- Conhecimento veterinário (doenças, limiares, sinais clínicos) é sempre **(suposição a validar)**; citar a fonte quando usar uma.
- Respeitar as restrições obrigatórias em toda proposta; se uma escolha conflitar com elas, dizer isso explicitamente.
