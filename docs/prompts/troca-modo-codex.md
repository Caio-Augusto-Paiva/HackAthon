# Prompt para o Codex: trocar de modo no meio da anamnese

Use a skill `impeccable` (o mesmo padrão visual do resto do `web/`) e TDD: o teste vem antes do código.

## Contexto

A especificação pede que o usuário troque entre modo produtor e modo especialista **a qualquer momento**, sem perder respostas. O slide 3 da apresentação também promete isso. O backend já faz a troca, mas a interface não oferece o controle. Esta tarefa é só isso; não mexa em `engine/`, `api/`, `kb/` nem `base/`.

## Antes de começar

1. `git checkout codex-davi && git pull && git merge origin/sessao-pair-programming`. A nossa branch traz o boi animado (`web/src/assets/boi-*.svg`). Se houver conflito nesses SVGs, **mantenha a versão com `class="olho"`/`class="sino"`**.
2. Rode `npm test` e `npm run build` em `web/`: tudo verde antes de mexer.

## O que já existe no backend (não alterar)

- `PATCH /api/sessoes/{sessao_id}` com corpo `{"modo": "produtor" | "veterinario"}` (schema `TrocaModo`, `operationId` `trocar_modo`). Devolve `EstadoSessao`.
- **Atenção ao nome:** na API o modo especialista se chama `veterinario`. Na tela continua aparecendo "especialista".
- O motor mantém todas as respostas, recalcula as hipóteses e a próxima pergunta, e reabre uma sessão que tinha sido encerrada pela bandeira vermelha. Os limites de perguntas dinâmicas mudam (12 no produtor, 25 no especialista), então `progresso.limite_dinamico` e o "Pergunta X de até Y" mudam junto.
- Erros: 409 `conflito` (outra aba mexeu na sessão), 404, 422.

## O que fazer

1. **API do front:** em `web/src/api/sessao.ts`, `trocarModo(id: string, modo: Modo): Promise<EstadoSessao>`, chamando `PATCH ${caminhoSessao(id)}` com `{ modo }`.
2. **Controle na tela de anamnese** (`web/src/paginas/Anamnese.tsx`): troque o rótulo estático "Modo produtor/especialista" do cabeçalho por um controle que mostra o modo atual e permite trocar.
   - Use um botão do componente `Botao` (variante secundária) com o texto "Mudar para modo especialista" ou "Mudar para modo produtor". Não use um seletor nativo.
   - Ao ir para o especialista, peça confirmação no `Modal` existente com o mesmo aviso em vermelho da tela de início (as perguntas têm complexidade maior). Ao ir para o produtor, troque direto.
   - Durante a chamada, reuse a trava `trava` e o estado `enviando`: não pode haver troca de modo e envio de resposta ao mesmo tempo, e o duplo clique não pode disparar duas chamadas.
   - No sucesso: `definirEstado(atualizado)`, limpe o modo de correção (`definirCorrecao(undefined)`) e o histórico local (`definirHistorico([])`), porque as telas guardadas foram calculadas no modo antigo. Leve o foco para a pergunta (`[data-pergunta]`).
   - No 409: recarregue com `obterSessao`, como o `enviar` já faz. Nos outros erros: mensagem em `role="alert"`, "Não consegui trocar o modo. Tente novamente.", e mantenha o modo antigo.
   - Se a sessão estiver pausada pela bandeira vermelha (`estado.alerta?.pausa`), o controle continua disponível. O motor reabre a sessão, e o `AlertaBandeira` some se o novo estado não tiver pausa.
3. **Parecer parcial:** em `web/src/paginas/Parecer.tsx`, quando `!dados.final`, ofereça o mesmo controle ao lado de "Continuar respondendo". Depois de trocar, navegue para `/anamnese/{id}`.
4. Anuncie a troca para leitores de tela: um `role="status"` com "Modo especialista ativado." ou "Modo produtor ativado.".

## Testes (escrever antes)

- `web/src/paginas/Anamnese.test.tsx`:
  - (a) Trocar para o especialista abre a confirmação; confirmar faz `PATCH` com `{"modo":"veterinario"}` e o cabeçalho passa a mostrar "Modo especialista" e o novo total de perguntas.
  - (b) Trocar para o produtor não pede confirmação.
  - (c) Duplo clique faz uma chamada só.
  - (d) Um 409 recarrega a sessão.
  - (e) Um 500 mostra o alerta e mantém o modo.
  - (f) As respostas já dadas não são reenviadas.
- `web/src/api/cliente.test.ts` ou um teste novo de `sessao.ts`: `trocarModo` monta o método, a rota e o corpo corretos.
- `web/e2e/troca-modo.spec.ts`: começa no produtor, responde a triagem, troca para o especialista, confirma que a próxima pergunta vem do modo especialista, responde mais uma e chega ao parecer. Inclua a checagem de acessibilidade com axe, como nos outros specs.

## Fechamento

- Rode `npm test`, `npm run build`, `npm run e2e` (com a API em `http://127.0.0.1:8000`), `.venv/Scripts/python -m pytest -q`. Tudo verde.
- Atualize `docs/entrega/05-apresentacao-e-demo.md`: o roteiro da demo mostra a troca de modo.
- Commits pequenos, por exemplo `feat(web): trocar de modo durante a anamnese`. Push em `codex-davi`.
- Pela regra do `AGENTS.md`, rode `/graphify . --update` e `graphify export obsidian --dir obsidian/01-conhecimento` uma vez, no fim, por causa da alteração em `docs/entrega/`, com commit separado.
