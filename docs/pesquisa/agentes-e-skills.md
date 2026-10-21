# Agentes de IA, Agent Skills e limites de uso (pesquisa, outubro/2026)

Data da pesquisa: 20/10/2026 (data do ambiente). Projeto: Anamnese de Bovinos Leiteiros (Hackathon UFJF 2026).

**Legenda:** CONFIRMADO = visto em documentação oficial consultada nesta pesquisa. NÃO CONFIRMADO = não encontrado em fonte oficial, ou só em blog/fonte secundária, ou contraditório.

**Observação sobre URLs:** várias páginas da OpenAI (developers.openai.com/codex/...) redirecionam para learn.chatgpt.com/docs/...; as URLs abaixo são os destinos finais lidos.

---

## 1. Suporte a Agent Skills e arquivo de instruções do projeto

| Agente | Suporta SKILL.md? | Skills: pasta do usuário | Skills: pasta do projeto | Arquivo de instruções do projeto | Status | Fontes |
|---|---|---|---|---|---|---|
| Claude Code | Sim. CONFIRMADO | `~/.claude/skills/<nome>/SKILL.md` | `.claude/skills/<nome>/SKILL.md` (também em subpastas e plugins) | `CLAUDE.md`. CONFIRMADO. Leitura nativa de `AGENTS.md`: NÃO CONFIRMADO na doc consultada | CONFIRMADO | https://code.claude.com/docs/en/skills |
| OpenAI Codex (CLI, IDE, app desktop) | Sim. CONFIRMADO | `~/.agents/skills/` (CONFIRMADO); admin `/etc/codex/skills`; bundled | `$CWD/.agents/skills` e cada pasta-pai até a raiz do repositório. CONFIRMADO | `AGENTS.md`. Global em `~/.codex` (ou `CODEX_HOME`); projeto da raiz do git até o diretório atual; aceita `AGENTS.override.md`; limite 32 KiB (`project_doc_max_bytes`). CONFIRMADO | CONFIRMADO | https://learn.chatgpt.com/docs/build-skills ; https://learn.chatgpt.com/docs/agent-configuration/agents-md |
| Gemini CLI | Sim (skills e `activate_skill`). CONFIRMADO | `~/.gemini/skills/` ou alias `~/.agents/skills/` | `.gemini/skills/` ou alias `.agents/skills/` | `GEMINI.md`: `~/.gemini/GEMINI.md` mais busca em pastas do workspace e pais. `context.fileName` em `settings.json` aceita lista, por exemplo `["AGENTS.md", "GEMINI.md"]`. CONFIRMADO | **Atenção:** o Gemini CLI deixou de atender usuários Google AI Pro/Ultra e Code Assist individual em 18/06/2026; a substituta é o Antigravity CLI. CONFIRMADO | https://geminicli.com/docs/cli/creating-skills/ ; https://geminicli.com/docs/cli/gemini-md/ ; https://developers.googleblog.com/an-important-update-transitioning-gemini-cli-to-antigravity-cli/ |
| Google Antigravity (app, IDE e CLI) | Sim. CONFIRMADO | App/IDE: `~/.gemini/config/skills/`; CLI: `~/.gemini/antigravity-cli/skills/`; legado `~/.gemini/antigravity/skills/` | `<workspace>/.agents/skills/<pasta>/SKILL.md` (legado `.agent/skills`). CONFIRMADO | `AGENTS.md` ou `GEMINI.md` em qualquer pasta do projeto (ambos lidos). Regras em `.agents/rules/*.md`. Globais: `~/.gemini/AGENTS.md`, `~/.gemini/GEMINI.md`, `~/.gemini/config/rules/*.md`. Limite de 24.000 bytes por arquivo. CONFIRMADO | CONFIRMADO | https://antigravity.google/docs/skills ; https://antigravity.google/docs/rules |

Notas:
- **Formato SKILL.md:** é o formato aberto Agent Skills (`name` e `description` no frontmatter; pastas opcionais `scripts/`, `references/`, `assets/`). CONFIRMADO em https://agentskills.io/home. Em Antigravity, `description` é obrigatória e `name` opcional (CONFIRMADO). Em Claude Code, todos os campos são opcionais, e `description` é recomendada (CONFIRMADO).
- **Gemini CLI x Antigravity CLI:** o blog oficial diz que Agent Skills, subagentes, hooks e extensões (agora "plugins do Antigravity") foram mantidos, mas que não há paridade 1:1 no lançamento. Não encontrei menção explícita a GEMINI.md/AGENTS.md no artigo do blog. NÃO CONFIRMADO para a CLI nova nesse ponto específico (a página de regras do Antigravity cobre AGENTS.md/GEMINI.md).
- **Caminho de projeto no Antigravity:** a documentação diz que o padrão é `.agents/skills` (CONFIRMADO). Fontes secundárias citam `.agent/`, que é legado.

---

## 2. Skills úteis para o projeto (Python/FastAPI, pytest, React/TypeScript, Vite, React Flow, Playwright, documentação e slides em português)

### 2.1 Repositório obra/superpowers (licença MIT; instalação em Claude Code, Codex, Antigravity, Gemini CLI, Cursor e outros; CONFIRMADO em https://github.com/obra/superpowers)

| Skill | Uso neste projeto | Funciona fora do Claude Code? |
|---|---|---|
| brainstorming | Refinar escopo e desenho, uma pergunta por vez (passo 2 do CLAUDE.md) | Sim: formato aberto e instalação listada para outros agentes (CONFIRMADO) |
| writing-plans | Gerar plano em tarefas de 2 a 5 minutos com caminhos de arquivo e verificação (passo 3) | Sim (idem) |
| executing-plans | Executar o plano inline, com revisão final | Sim (idem) |
| subagent-driven-development | Um subagente novo por tarefa, com revisão de spec e de qualidade | Sim (idem), depende de suporte a subagentes no agente |
| test-driven-development | Teste antes do código de cada tarefa (ciclo vermelho-verde-refatorar) | Sim (idem) |
| systematic-debugging | Causa raiz antes de propor correção (bugs de motor e API) | Sim (idem) |
| verification-before-completion | Exigir evidência de execução antes de dizer que algo passou | Sim (idem) |
| requesting-code-review / receiving-code-review | Revisão contra o plano e tratamento de feedback | Sim (idem) |
| using-git-worktrees / finishing-a-development-branch | Isolamento de branch e fechamento de entrega | Sim (idem) |

### 2.2 Repositório anthropics/skills (CONFIRMADO em https://github.com/anthropics/skills e https://github.com/anthropics/skills/tree/main/skills)

Pastas em `skills/` (19 listadas): academy-guide, algorithmic-art, brand-guidelines, canvas-design, claude-api, discernment-nudge, doc-coauthoring, docx, frontend-design, internal-comms, mcp-builder, pdf, pptx, skill-creator, slack-gif-creator, theme-factory, web-artifacts-builder, webapp-testing, xlsx.

| Skill | Uso neste projeto | Licença / observação |
|---|---|---|
| webapp-testing | Testes ponta a ponta com Playwright para a demo em localhost | Licença específica da pasta: NÃO CONFIRMADO. Repo: "many skills are Apache 2.0" |
| frontend-design | Interface React/TypeScript da anamnese e do editor | Idem |
| web-artifacts-builder | Páginas React com Tailwind e shadcn/ui (apoio para telas) | Idem; NÃO CONFIRMADO se o uso em React Flow é adequado |
| skill-creator | Criar skills próprias do projeto (ex.: regras de produção como skill) | Idem |
| mcp-builder | Só se o grupo expuser o motor como servidor MCP | Idem; uso opcional |
| pptx | Montar os slides da apresentação final | **Source-available, não open source** (CONFIRMADO no README) |
| docx | Documentação obrigatória em Word, se pedida | Idem |
| pdf | Exportar ou ler PDFs de referência (ex.: fontes [A] e [D]) | Idem |
| xlsx | Tabelas de casos de teste e de versões da base, se pedidas | Idem |
| internal-comms | Relatórios de status curtos | Idem |

Atenção de licença: o CLAUDE.md exige **open source**. Usar docx/pptx/pdf/xlsx como ferramenta de produção dos documentos é diferente de incluí-las no código; mesmo assim, o grupo deve confirmar se isso conflita com a regra do hackathon. NÃO CONFIRMADO se há conflito.

### 2.3 Outras skills (Playwright e catálogos)

| Skill | Repositório | Uso | Observação |
|---|---|---|---|
| playwright-skill | https://github.com/lackeyjb/playwright-skill | Automação e testes Playwright gerados pelo agente | MIT, 3,2 mil estrelas; lista Claude Code, Cursor, Copilot, Codex, Gemini CLI e OpenCode (CONFIRMADO na página do repo) |
| awesome-agent-skills | https://github.com/VoltAgent/awesome-agent-skills | Catálogo grande (badge: cerca de 1.497 skills) | Cita, sem verificação individual: microsoft/fastapi-router-py (FastAPI), testmu-ai/pytest-skill (pytest), microsoft/react-flow-node-ts (React Flow), testmu-ai/vitest-skill (Vitest), anthropics/pptx. Vite: nenhuma skill dedicada encontrada. Documentação em português: nenhuma encontrada. NÃO CONFIRMADO para as skills específicas |
| awesome-claude-skills (travisvn) | https://github.com/travisvn/awesome-claude-skills | Lista curada de skills oficiais e comunitárias | Não há skill de FastAPI, pytest ou React Flow listada (CONFIRMADO na página) |
| awesome-claude-skills (karanb192) | https://github.com/karanb192/awesome-claude-skills | Lista com mais de 50 skills verificadas | Encontrado na busca; página não aberta: NÃO CONFIRMADO |
| hpehl/skills | https://github.com/hpehl/skills | Coleção pessoal, Apache-2.0 | Encontrado na busca; conteúdo não verificado: NÃO CONFIRMADO |
| Padrão aberto | https://agentskills.io/home | Especificação das Agent Skills (pasta com SKILL.md) | CONFIRMADO |

Lacunas: nenhuma skill confirmada para Vite, React Flow específico, FastAPI e pytest com fonte oficial. O grupo deve inspecionar os repositórios antes de instalar (skills de terceiros podem executar código).

### 2.4 Top 12 para este projeto (resumo)

1. brainstorming (obra/superpowers): refinar a especificação antes do código.
2. writing-plans (obra/superpowers): plano com tarefas pequenas e verificáveis.
3. test-driven-development (obra/superpowers): testes antes da implementação.
4. systematic-debugging (obra/superpowers): causa raiz de bugs do motor.
5. verification-before-completion (obra/superpowers): evidência antes de afirmar sucesso.
6. requesting-code-review (obra/superpowers): revisão contra o plano.
7. subagent-driven-development (obra/superpowers): uma tarefa por subagente.
8. webapp-testing (anthropics/skills): Playwright para testes ponta a ponta.
9. playwright-skill (lackeyjb/playwright-skill): Playwright em qualquer agente com formato aberto.
10. frontend-design (anthropics/skills): UI React/TypeScript.
11. pptx (anthropics/skills): slides, com cuidado de licença.
12. skill-creator (anthropics/skills): criar skills próprias de regras de produção.

---

## 3. Recursos próprios úteis

| Agente | Recurso | Situação |
|---|---|---|
| Gemini | Deep Research | Existe no app (fontes secundárias). Limite conflitante: uma fonte cita 5 relatórios por mês, outra descreve janelas de 5 horas e semanal. NÃO CONFIRMADO |
| Gemini | Grounding com Google Search | NÃO CONFIRMADO (não encontrei documentação oficial nesta pesquisa) |
| Gemini | Contexto longo | NÃO CONFIRMADO (sem número oficial consultado) |
| Antigravity | Agent Manager (vários agentes) | CONFIRMADO: abre com Ctrl+E no Windows e Linux; `/agents` na CLI alterna subagentes em segundo plano (https://antigravity.google/docs/getting-started) |
| Antigravity | Navegador integrado | CONFIRMADO: há seção de navegador, gravações, allowlist/denylist e perfil Chrome separado (https://antigravity.google/docs/getting-started). Detalhes do agente de navegador: NÃO CONFIRMADO |
| Codex | Execução em sandbox | CONFIRMADO: modos `read-only`, `workspace-write` e `danger-full-access` (https://learn.chatgpt.com/docs/sandboxing). Rede desligada por padrão: NÃO CONFIRMADO |
| Codex | Revisão de código no GitHub (`@codex review`) | NÃO CONFIRMADO: página não encontrada (HTTP 404). A página de segurança cita revisão de PRs no GitHub pelo Codex Security (https://learn.chatgpt.com/docs/security), sem detalhes |

---

## 4. Limites de uso dos planos

| Plano | Janelas e limites | Status | Fonte |
|---|---|---|---|
| Claude Pro (Claude Code) | Janela de sessão de 5 horas (deslizante) e limite semanal, compartilhados entre claude.ai e Claude Code. Não há número oficial de mensagens ou tokens. `/status` mostra o saldo. | CONFIRMADO. Números de terceiros (ex.: 40 a 80 h/semana de Sonnet, 45 a 90 prompts por janela): NÃO CONFIRMADO | https://support.claude.com/en/articles/11145838-using-claude-code-with-your-pro-or-max-plan |
| ChatGPT Plus (Codex) | Estimativa por janela de 5 horas, por modelo (ex.: GPT-6 Luna 350 a 3.000; GPT-6 Sol 15 a 150; GPT-6 Astra 5 a 45 mensagens locais). "Não são limites fixos." Limite semanal: "may also apply", sem número. | CONFIRMADO na página oficial. Histórico (janela removida em julho e restaurada em 25/08/2026): fonte secundária, NÃO CONFIRMADO. Plano Pro: NÃO CONFIRMADO | https://learn.chatgpt.com/docs/pricing |
| Google AI Pro (Gemini CLI) | Página de quotas (data 18/06/2026): 1.500 requisições por usuário por dia; limite por minuto sem número. | Contraditório: a mesma página diz que o Gemini CLI foi substituído pelo Antigravity CLI em 18/06/2026, e o blog oficial diz que usuários AI Pro perderam o Gemini CLI nessa data. Para uso atual, considerar o Antigravity CLI. | https://geminicli.com/docs/resources/quota-and-pricing/ ; https://developers.googleblog.com/an-important-update-transitioning-gemini-cli-to-antigravity-cli/ |
| Google AI Pro (Antigravity) | Cota alta, renovada a cada 5 horas "até o limite semanal ser atingido"; limite semanal maior que nos planos comuns (sem número). Créditos de IA para excedente, com configuração "Never" ou "Always". Documentação: "Usage limits ... subject to modification." | CONFIRMADO no texto oficial, sem data visível e sem números. Relatos de bloqueios de vários dias em março/2026 em fórum: NÃO CONFIRMADO como regra | https://antigravity.google/docs/plans ; https://discuss.ai.google.dev (fóruns, não oficial) |

---

## 5. Pontos em aberto

- Confirmar no app ou no painel de uso do Antigravity os limites reais do plano Google AI Pro.
- Confirmar se a licença de webapp-testing, frontend-design e skill-creator é Apache 2.0 (a pasta não mostrou a licença).
- Confirmar `@codex review` e o comportamento padrão de rede do Codex na documentação atual.
- Decidir se o uso de skills de documento proprietárias (docx, pptx, pdf, xlsx) conflita com a exigência de open source do hackathon.
- Inspecionar as skills de terceiros (FastAPI, pytest, React Flow) antes de instalar, pois podem executar código.
