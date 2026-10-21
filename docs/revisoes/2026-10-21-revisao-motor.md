# Revisão do motor de inferência (commit 7865df8)

Revisão em 21/10/2026 contra a especificação canônica `docs/superpowers/specs/2026-10-20-anamnese-bovinos-design.md`. O motor foi implementado a partir de `docs/prompts/secao-1.md`, anterior às 18 correções de consistência; divergências marcadas **(spec mudou depois)** não são erro do implementador.

**Verificado:** 56 testes passando (`python -m unittest discover`, 0,6 s); exemplos `python -m engine …` saem com código 0; só biblioteca padrão; CF em `Fraction`. Sondas próprias com as regras da Seção 3 rodam os casos C-MAS-01 e de decúbito em menos de 0,1 s.

## Conformidade

| # | Item | Status | Onde |
|---|---|---|---|
| 1 | Combinação MYCIN (ordem, 0/0, ±0,99, Fraction) | conforme | `cf.py`, `validacao.py` |
| 2 | Condição sem valor ou "não sei" = 0, inclusive negada; ficha ±1 | conforme | `avaliacao.py`, `modelos.py` |
| 3 | Três camadas, `cf_minimo`/`cf_maximo`, derivado `max` | conforme | `validacao.py` |
| 4 | Agenda (prioridade, especificidade, id) | conforme; default de prioridade é 0, não 100/50/10 | `inferencia.py:22` |
| 5 | Próxima pergunta (viáveis, modo, peso via derivados, gravidade → id) | conforme; extra: pergunta de bandeira pendente vem primeiro | `selecao.py` |
| 6 | Hipótese aberta (−0,2; 0,8) | conforme | `parada.py`, `inferencia.py` |
| 7 | Parada (triagem, (b) só abertas, (c), comorbidade, limite, exaustão) | conforme; sem tolerância 1e-9 explícita (com `Fraction` a fronteira é exata) | `parada.py` |
| 8 | Triagem (múltipla vira booleanos, "não sei" = 0, nenhuma alteração = −1) | conforme; aceita lista de marcados, não `{simbolo: bool}` | `sessao.py` |
| 9 | Bandeira some após correção | **diverge (spec mudou depois)** | `sessao.py:25,41`, `test_sessao.py:62-70` |
| 10 | Parecer `max(0, CF) × 100` sempre | **diverge (spec mudou depois)**: −0,2 a 0,2 vira 0% | `parecer.py:9-13`, `test_sessao.py:136` |
| 11 | Traço | parcial: o traço da sessão reacumula eventos a cada resposta; sem evento de correção | `sessao.py:39-40` |
| 12 | Correções e troca de modo | conforme | `sessao.py` |
| 13 | Reconstruir a sessão a partir do banco | **ausente** | `sessao.py` |
| 14 | Nomes do formato da base (Seção 2) | conforme, exceto `bloco_principal`/`bloco_diferencial` não lidos | `modelos.py:7`, `parecer.py` |
| 15 | Executor de casos | parcial: `inconclusivas` e `alerta.pausa` no esperado dão "erro" | `casos.py:41` |
| 16 | Cobertura de testes | faltam os testes das divergências acima e o teste de arquitetura | `tests/engine` |

## Correções necessárias (por gravidade)

1. **Bandeira após correção:** derivar as bandeiras do cálculo atual; manter "reconhecida" só para as ativas; registrar a correção no traço. Inverter `test_sessao.py:62-70` e o README.
2. **Percentual:** `max(0, CF) × 100`, arredondado meio para cima, sempre. Corrigir `test_sessao.py:136` e o README.
3. **Ficha com `null`:** hoje vira "não sei" respondido e pula a pergunta; `null` deve ser ausente (Seção 4.5.2).
4. **Restauração da sessão (bloqueia a API):** criar `Sessao.restaurar(...)` a partir de fatos, perguntas dinâmicas em ordem, perguntas feitas com motivo, bandeiras reconhecidas e encerramento por alerta, sem revalidar "é a próxima". Reproduzir pelo upsert da tabela `respostas` falha quando uma correção muda a pergunta seguinte.
5. **Cortes de bloco:** ler `meta.limiares.bloco_principal`/`bloco_diferencial` (padrões 0,50/0,20).
6. **Executor:** incluir `inconclusivas` e `alerta.pausa` no resultado obtido.
7. **Traço da sessão:** guardar na sessão só `pergunta_feita` e correções, e o traço do último cálculo; emitir `fato_adicionado` de origem regra.
8. **`bandeiras_nao_verificadas`:** só regras viáveis e perguntáveis no modo, e só em parada por limite.
9. **Menores:** prioridade padrão por classe (100/50/10); triagem múltipla aceitar `{simbolo: bool}` ou converter na API; sem hipótese aberta → `sem_potencial`; ids de bloco iguais aos da API (`hipoteses_principais`, `diagnostico_diferencial`, `pouco_provavel`).

## Para a especificação

- Documentar o comportamento extra útil: pergunta que pode verificar bandeira pendente vem antes das demais.
- Árvore da Seção 4.3: o motor tem `sessao.py`, `validacao.py` e `modelos.py` próprios (sem Pydantic), e a agenda fica em `inferencia.py` (não existe `agenda.py`). O motor não depende de `kb/`; `kb/` valida e exporta o mesmo formato.

## O que a API precisa adaptar

Filtrar `null` da ficha e calcular `dias_em_lactacao`; converter `{valores}` em lista de marcados; montar `EstadoSessao` (faltam `tela_id`, `campos`, `opcoes`, `permite_nao_sei`, `motivo_resumo`, `limite_dinamico`, urgência como objeto, `revisao`; nomes de progresso diferem); completar o parecer (`final`, `sessao_id`, `modo`, texto da urgência); mapear os `ValueError` do motor para 409 `ja_respondida`/`nao_respondida` e 422; validar o tipo do símbolo em "como?".
