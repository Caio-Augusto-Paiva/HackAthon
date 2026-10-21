# Agentes e skills por prompt

Decisão do arquiteto em 20/10/2026, com base em `docs/pesquisa/agentes-e-skills.md` (fontes e status de confirmação).

## Recursos disponíveis

| Recurso | Quantidade | Uso principal | Observação |
|---|---|---|---|
| Claude Code (Claude Pro) | 1 | consolidação da especificação, plano de implementação, motor (pessoa A) | o mais escasso: janela de 5 h + limite semanal, compartilhado com o claude.ai |
| Codex (ChatGPT Plus) | 1 | revisão com execução de código (Seção 1), API (pessoa B) | janela de 5 h por modelo + limite semanal |
| Gemini Pro (Google AI Pro, app web) | 3 | pesquisa de domínio com Google Search e Deep Research, documentação e slides | o Gemini CLI foi substituído pelo Antigravity CLI para usuários AI Pro em 18/06/2026 |
| Antigravity (plano Pro) | 3 | um por pessoa: revisões que precisam ler o repositório, frontend e e2e (pessoa C), reserva quando o agente principal esgotar a janela | cota renovada a cada 5 h até o limite semanal |

## Princípios

1. **Revisor de outra família de modelo.** As seções foram escritas com Claude; quem revisa é Codex (GPT) ou Gemini/Antigravity, para a revisão ser independente.
2. **Claude Code fica com o que é crítico.** Por ser único e escasso, não é usado em revisão: fica com a consolidação, o plano e o motor.
3. **Espalhar as janelas de 5 h.** Cada revisão vai para um assento diferente; quando um esgota, o Antigravity da mesma pessoa assume.
4. **Skills em formato aberto, num lugar só.** As skills do `obra/superpowers` funcionam em Claude Code, Codex e Antigravity. No repositório: `.agents/skills/` (lido por Codex e Antigravity) com cópia em `.claude/skills/` (Claude Code). Instruções do projeto: `AGENTS.md` (Codex e Antigravity), com `CLAUDE.md` e `GEMINI.md` apontando para ele. Limites: 32 KiB (Codex) e 24.000 bytes (Antigravity).
5. **Licença das skills.** As skills `pptx` e `docx` do `anthropics/skills` são *source-available*, não open source. Como são ferramenta de produção de slides e não fazem parte da solução entregue, não conflitam com a exigência de open source ([A] slide 13) **(suposição)**; se a banca entender diferente, os slides saem do Google Slides ou do LibreOffice Impress.

## Alocação por prompt de revisão

| Prompt | Agente principal | Alternativa | Skills | Por quê |
|---|---|---|---|---|
| Seção 1 — Motor | **Codex** | Antigravity (pessoa A) | `verification-before-completion`, `test-driven-development`, `systematic-debugging` (obra/superpowers) | a revisão exige rodar Python em aritmética exata; o Codex executa em sandbox |
| Seção 2 — Base e editor | **Antigravity** (pessoa B) | Codex | `requesting-code-review`, `verification-before-completion` (obra/superpowers) | precisa ler as Seções 1 a 3 do repositório juntas e testar ida e volta grafo ↔ JSON com um script |
| Seção 3 — Domínio | **Gemini Pro (app), com Deep Research** | Antigravity (pessoa A) com `pdf` (anthropics/skills) | Deep Research e busca no Google (recursos do app, não skills); `pdf` para ler material da Embrapa | conferir fontes clínicas em português e inglês; **e, se possível, um técnico da RERUM ([A] slide 13)** |
| Seção 4 — Tecnologias e API | **Antigravity** (pessoa B) | Codex | `requesting-code-review`, `verification-before-completion` | acesso à web para conferir versões e licenças; leitura das Seções 1 a 3 para ver se as rotas cobrem tudo |
| Seção 5 — Testes e cronograma | **Gemini Pro (app)** | Antigravity (pessoa C) | `writing-plans`, `test-driven-development` (obra/superpowers), `webapp-testing` (anthropics/skills) ou `playwright-skill` (lackeyjb, MIT) | o cronograma é revisão de raciocínio, não de código; os cenários e2e pedem conhecimento de Playwright |

## Implementação (para o plano, Seção 6)

| Pessoa | Pastas | Agente principal | Reserva | Skills |
|---|---|---|---|---|
| A | `engine/`, `kb/modelos.py`, `kb/carregador.py`, `kb/analise.py`, `tests/engine` | Claude Code | Antigravity (A) | `test-driven-development`, `systematic-debugging`, `verification-before-completion`, `executing-plans` |
| B | `api/`, `kb/validador.py`, `kb/grafo.py`, `tests/kb`, `tests/api`, `scripts/` | Codex | Antigravity (B) | `test-driven-development`, `requesting-code-review`, `verification-before-completion` |
| C | `web/`, `e2e/` | Antigravity (C), com o agente de navegador | Gemini Pro (C) para dúvidas de UI | `frontend-design` (anthropics/skills), `webapp-testing` ou `playwright-skill`, `test-driven-development` |
| Todos, quinta à tarde | documentação e slides | Gemini Pro (3 assentos) | Claude Code (se sobrar janela) | `pptx` ou Google Slides; `pdf` para conferir o PDF final |

Skills não confirmadas para este projeto: FastAPI, pytest, React Flow e Vite só aparecem em listas comunitárias (VoltAgent/awesome-agent-skills), não verificadas. Nenhuma skill de documentação em português foi encontrada.
