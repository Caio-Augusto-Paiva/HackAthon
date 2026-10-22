# Notas do apresentador — Anamnese Bovina

Roteiro para a apresentação à banca do Hackathon UFJF 2026. Os tempos são **estimativas** (10 min de fala e 4 min de demonstração), a confirmar em ensaio cronometrado. Os números referem-se à base ativa `v0004` e à última execução das suítes de teste.

| # | Slide | Tempo estimado | Notas |
|---|---|---|---|
| 1 | Capa | 0:20 | Apresentar o tema T1 (Anamnese) e os três integrantes. |
| 2 | Sumário | 0:15 | Percorrer os tópicos sem detalhar. |
| 3 | Equipe e organização | 0:35 | Cada integrante teve um agente de IA e uma área: Caio (Claude Code) — arquitetura dos agentes e do sistema, grafos do projeto e dos dados, validação e interface; Davi (Codex) — sistema especialista, motor de inferência, validação, casos de teste e documentação; Luis (Antigravity) — base de conhecimento, dados em JSON e base clínica. Cada pasta teve um responsável. |
| 4 | Problema e escopo | 0:45 | Citar o tema oficial: coleta estruturada de sinais e histórico de bovinos leiteiros em lactação, com triagem explicável (apresentação RERUM, slide 9). As 8 doenças: mastite, hipocalcemia puerperal, cetose, metrite puerperal, acidose ruminal, deslocamento de abomaso, tristeza parasitária bovina e dermatite digital. |
| 5 | Sistema especialista | 0:40 | Restrição do hackathon: a LLM não pode ser o sistema especialista. A IA ajudou a escrever código e a extrair regras de fontes; a decisão vem só da base explícita e do motor, e é reproduzível. |
| 6 | Motor de inferência | 1:00 | Encadeamento progressivo: cada resposta dispara regras; a próxima pergunta é escolhida pelas hipóteses em aberto. Fatores de certeza no modelo MYCIN, com aritmética racional exata (sem erro de ponto flutuante). Resolução de conflitos por prioridade fixa e, em empate, pela regra mais específica. O percentual é `max(0, CF) × 100`: **confiança do sistema, não probabilidade clínica**. |
| 7 | Funcionamento da consulta | 0:40 | Seis telas de triagem obrigatórias; depois, perguntas dinâmicas até 12 (produtor) ou 25 (especialista). Para ao confirmar uma hipótese (CF ≥ 0,80) ou quando nenhuma pode passar de 0,70. Bandeira vermelha leva a "chamar o veterinário" e pausa o modo produtor. Corrigir uma resposta reprocessa a sessão na ordem original. |
| 8 | Base de conhecimento | 0:40 | 8 doenças, 51 símbolos, 61 regras (47 de evidência, 8 de urgência, 6 bandeiras vermelhas), 34 casos de teste. Versões imutáveis: `v0001` a `v0004`; a `v0003` acrescentou regras de sinal isolado com peso baixo e a `v0004` só corrigiu nomes. A base é editada em arquivos por doença (`base/fonte/`) e reunida em uma nova versão validada. |
| 9 | Grafos | 0:35 | Grafo 1: documentação do projeto, consultada pelos agentes para economizar contexto. Grafo 2: dados das 8 doenças, gerado sem IA a partir da base (112 nós, 149 relações). O motor carrega a base a partir do grafo exato com resultado idêntico nos 34 casos. |
| 10 | Arquitetura | 0:45 | Interface React → API FastAPI (27 operações) → motor em Python ← base em JSON versionada. SQLite guarda sessão e respostas. "Por quê?" e "Como cheguei aqui?" vêm do traço de inferência, apresentados em linguagem comum. Tudo em localhost. |
| 11 | Tecnologias | 0:30 | Critério: código aberto, execução local, poucas dependências. O motor usa apenas a biblioteca padrão. |
| 12 | Processo com IA | 0:50 | Hierarquia: a equipe aprova; modelos mais capazes planejam, revisam e testam; intermediários implementam; leves pesquisam e resumem. Especificação e plano antes do código; teste que falha antes da correção; revisão entre agentes. Exemplo: um teste manual expôs pareceres com 0% em todas as doenças; a correção virou a versão `v0003` após 34/34 casos. |
| 13 | Resultados verificados | 0:55 | 1.082 testes automatizados no backend (motor 134, base 296, API 630, casos 10, documentação 12) e 170 subtestes; 72 testes da interface; 34/34 casos na `v0004`. Os 6 fluxos de ponta a ponta existem; **sua execução nesta etapa precisa ser confirmada** antes de ser citada como resultado. |
| 14 | Documentação | 0:30 | Sete documentos em `docs/entrega/`: processo, arquitetura, regras de produção, casos de teste, apresentação e demonstração, riscos e pendências, ensaio e envio. Os documentos 03 e 04 são gerados da base e verificados por teste. |
| 15 | Demonstração | 4:00 (demo) | Roteiro: iniciar no modo produtor; responder a triagem; observar a barra de hipóteses; provocar um alerta de sinal grave; trocar para o modo especialista sem perder respostas; abrir o parecer e "Como cheguei aqui?". Comando: `scripts/rodar.ps1` (abre `http://localhost:8000`). |
| 16 | Limitações | 0:35 | Prazo de dois dias e meio limitou a 8 doenças; nenhum veterinário validou regras e pesos; no modo produtor, deslocamento de abomaso e dermatite não passam de 70%; casos sintéticos e dados fictícios. O sistema apoia a triagem e não substitui o laudo. |
| 17 | Próximos passos | 0:25 | Novas doenças entram por nova versão da base, sem alterar motor, API ou interface. |
| 18 | Perguntas | — | Abrir para perguntas. |

**Total de fala estimado:** 10:00 (sem a demonstração).

## A confirmar antes da apresentação

- Execução dos 6 testes de ponta a ponta (Playwright) na versão final.
- Duração real, em ensaio cronometrado na máquina da apresentação e na reserva.
- Captura da vista de grafo do Obsidian, se a equipe quiser exibi-la no slide 9.
