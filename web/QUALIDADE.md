# Verificação da interface — 22/10/2026

Interface local de Anamnese Bovina na branch `codex-davi`, com API real e base ativa `v0002`. Referência visual: página Protótipo do Figma, sete frames (incluindo erro numérico), componentes e 16 tokens. As perguntas, nomes clínicos, blocos e orientações vêm da API; diferenças de texto em relação ao exemplo estático do Figma são intencionais. As barras são sólidas e acessíveis, conforme solicitado.

## Evidência automatizada

- `npm test`: **39 testes** aprovados, em sete arquivos; cliente, componentes, início, perguntas, correção, conflitos, bandeira, parecer e inicialização.
- `npm run build`: TypeScript estrito e Vite 8 aprovados. JavaScript de produção: aproximadamente 298 kB, 94 kB gzip; CSS aproximadamente 20 kB, 5 kB gzip. Fontes e SVGs locais.
- `npx playwright test`: **8 cenários** aprovados no Chromium, com API própria, SQLite temporário e casos sintéticos versionados. Nenhuma API clínica foi mockada nos E2E.
- Quatro cenários funcionais: produtor completo C-MAS-01; decúbito, parecer urgente e retomada após encerramento voluntário; temperatura retal do especialista C-MAS-02; número `12,5` rejeitado com 422 e avanço após `12`.
- Quatro cenários de qualidade: seis telas em 375, 768, 1024 e 1440 px; axe com regras WCAG 2 A/AA e 2.1 AA, sem violações detectadas; sem overflow horizontal e sem requisições externas.
- `impeccable detect --json web/src`: **nenhum achado**. O resultado é uma verificação mecânica, não prova de qualidade visual.
- `scripts/rodar.ps1 -SemNavegador`: SPA, rota interna da SPA e `/api/docs` responderam 200. O Swagger continua dependendo de CDN (R17).

## Auditoria e refinamento

| Dimensão | Avaliação de 0 a 4 | Evidência e limite |
|---|---:|---|
| Acessibilidade | 3 | Controles nativos, rótulos e erros associados, foco visível, diálogo com foco preso, texto de gravidade e meters; axe sem violações nas telas. Leitor de tela não ensaiado |
| Desempenho | 3 | SVGs originais, fontes locais, build otimizado, sem efeitos de layout em laço; medições de Web Vitals em máquina de campo pendentes |
| Tokens e consistência | 4 | 16 cores do Figma, tipografia e componentes compartilhados, sombras e estados coerentes; tema fixo do protótipo |
| Responsividade | 3 | Quatro larguras emuladas e revisão das capturas; faltam dispositivos físicos e outros motores |
| Integridade | 4 | Dados clínicos vêm do servidor; detector vazio, todos os fluxos pedidos exercitados; editor fora do escopo |

No passe de refinamento, o PUT de correção dinâmica passou a omitir o símbolo do corpo (teste RED → GREEN), a lateral passou a indicar atualização em vez de manter percentuais antigos, e o carregamento ganhou esqueleto de balão/opções. Há uma única transição entre perguntas; `prefers-reduced-motion` a remove e a mudança continua indicada pelo conteúdo/foco. Estados vazios, falhas de rede, repetição de envio e conflitos têm tratamento explícito.

A revisão visual detectou barras com altura zero no parecer de celular, apesar do resultado axe sem violações. A regressão foi reproduzida com medição no navegador (RED: altura 0), corrigida no flex da coluna móvel e passou a exigir pelo menos 10 px de altura em todas as barras. O título desktop e os botões também foram alinhados às medidas do Figma. Esse achado demonstra por que detector e análise automática não substituem a inspeção das capturas.

A revisão independente também confirmou que corrigir uma resposta antiga removia do histórico local as respostas posteriores, embora o backend mantivesse seus fatos. Um teste de regressão reproduziu a perda de acesso (RED); a correção passou a substituir apenas a entrada editada e conservar as posteriores (GREEN).

O segundo achado da revisão foi a ausência de retomada após Ver parecer. O botão agora usa `continuar` quando a API indica encerramento voluntário (`final: true`, `motivo_parada: null`), com trava de envio e recuperação 409 por GET. A presença do botão e a ausência de promessa de retomada após parada automática são testadas. O fluxo real de bandeira volta à pergunta no E2E; a lacuna de API para forçar continuidade após parada automática está em R21.

O alerta usa o texto e as ações do backend. Esc e clique fora não o dispensam. Por quê e Como têm carregamento, falha com nova tentativa e fechamento com devolução de foco. A tabela conserva títulos dos blocos do backend, sem inventar cortes clínicos no navegador.

## Capturas e limites

[Capturas das seis telas e do erro numérico](../docs/entrega/capturas/) foram obtidas da implementação com API real. O conjunto desktop mostra início, pergunta numérica, lateral, múltipla, alerta e parecer. Há uma captura adicional em 375 px. O protótipo foi comparado com os renders em tipografia, cores, ilustrações, proporções, espaçamento e hierarquia; as perguntas reais podem ocupar mais linhas que o texto do Figma.

Os resultados são evidência de software em dados fictícios. Não demonstram acurácia clínica. Riscos de coleta, precisão no contrato, histórico de edição após recarga, editor e ensaios físicos permanecem registrados no [documento de riscos](../docs/entrega/06-riscos-e-pendencias.md).

## Checkpoint posterior — troca de modo durante a anamnese

O merge `7494e3e` trouxe o prompt e os SVGs animados com classes `olho`/`sino`, preservados nesta alteração. A verificação deste checkpoint amplia a cobertura inicial acima para **60 testes unitários em nove arquivos e 11 cenários E2E**. O build continua em TypeScript estrito; a suíte Python permanece com 1066 aprovados, 1 ignorado e 170 subtestes.

A troca usa PATCH na mesma sessão, confirmação ao entrar no especialista, bloqueio compartilhado com respostas, anúncio para leitores de tela e foco na pergunta. Há cobertura de cancelamento, duplo clique, conflitos 409, erros 404/422/500, histórico corrigível, pausa e parecer parcial. A tabela final continua sendo o parecer único da API, com os sinais anteriores à troca.

A revisão encontrou dois cuidados adicionais cobertos por regressões RED → GREEN: descartar apenas o rascunho quando o campo da tela muda entre modos, e corrigir a tela antiga com os símbolos do modo original antes de restaurar o modo escolhido. A operação permanece sob a mesma trava; falhas são reconciliadas por leitura do estado, sem apagar histórico ou repetir o PUT. Os testes da API real corrigem dias e a observação térmica do produtor antes e depois da termometria do especialista. Axe e a revisão das capturas cobrem o novo controle e a confirmação. Esses resultados continuam sendo evidência de software, sem validação clínica.
