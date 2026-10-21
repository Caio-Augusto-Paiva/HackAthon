# Plano de implementação — motor da seção 1

**Especificação autorizada:** `docs/prompts/secao-1.md`, implementação solicitada explicitamente no chat em 20/10/2026. As seções 2–5 informam os formatos de integração; não ampliam a entrega para API, interface, editor ou conhecimento clínico.

**Objetivo:** motor determinístico de três camadas, com sessão de perguntas, CF, parada, parecer e explicações. Python 3.12+, biblioteca padrão; testes com `python -m unittest discover -v` (também coletáveis pelo pytest). Não há código/testes anteriores. Trabalho no checkout indicado pelo usuário; sem publicar, alterar a documentação aprovada ou criar base clínica não validada.

## Tarefas e verificações

- [x] 1. CF e avaliação: `engine/cf.py`, `modelos.py`, `avaliacao.py`, `validacao.py`; `tests/engine/test_nucleo.py`. Provar combinações com frações, operadores, ausência de valor, limiares e rejeição de camadas inválidas. RED antes da implementação; GREEN com a suíte inteira.
- [x] 2. Propagação: `engine/inferencia.py`, `traco.py`; `tests/engine/test_inferencia.py`. `inferir(base, fatos)` retorna CF, regras disparadas e traço em ordem de camada/prioridade/especificidade/id. Testar recalculação, negativos, max e urgência.
- [x] 3. Busca e parada: `engine/selecao.py`, `parada.py`; `tests/engine/test_selecao_parada.py`. `analisar(base, fatos, modo)` fornece regras viáveis, potenciais e candidatos; `motivo_parada(...)` respeita triagem, comorbidade, bandeiras e limites. Testar limites superiores com enumeração de respostas e ambos os modos.
- [x] 4. Sessão e apresentação: `engine/memoria.py`, `sessao.py`, `parecer.py`, `explicacao.py`, `casos.py`; `tests/engine/test_sessao.py`. Testar telas, contagem, correção, troca de modo, pausa, oito doenças, por quê/como e executor dos casos. Sem estado global, rede ou banco.
- [x] 5. Integração/documentação: exemplo sintético executável, instruções em `engine/README.md`, revisão e suíte completa; `compileall` e `git diff --check`. Relatar os testes efetivamente executados e as limitações.

Cada tarefa segue teste que falha pelo comportamento ausente → implementação mínima → suíte verde. Asserções usam valores derivados à mão; sem mocks de motor. Testes de integração atravessam os módulos reais.

## Interfaces

Entrada pública: base no formato `meta/simbolos/regras` da seção 2, ou objeto com `model_dump()`; fatos observados por símbolo. Modelos internos imutáveis, sem dependência de Pydantic. Futuro `kb/` pode validar/exportar esse formato sem alterar o motor.

CF internos usam `fractions.Fraction`, construídos de representações decimais, para preservar os limites estritos ±1 e a independência da ordem. Saídas de apresentação usam números JSON e percentuais inteiros. Nenhum CF é anunciado como probabilidade.

## Decisões de implementação

1. A autorização explícita para implementar supera a fase antiga de planejamento em `CLAUDE.md`. O desenho é o documento já fornecido, não um redesenho do projeto.
2. Duas doenças confirmadas não bloqueiam uma à outra: a condição (b) de confirmação considera concorrentes **abertas**, caso contrário contradiz o teste explícito de comorbidade.
3. Intervalo neutro inclusivo [-0,2; 0,2] aparece como 0% e `sem_evidencia`, conforme a frase específica do parecer; acima de 0,2 aplica-se `max(0, CF)*100`. Cortes dos blocos usam CF antes do arredondamento; 50% pertence somente a principais. Arredondamento decimal meio para cima.
4. Bandeira disparada permanece na sessão mesmo após correção, como exige a urgência irreversível. O estado atual é recalculado; o histórico identifica o disparo anterior.
5. `nao_sei` é resposta registrada, não candidata a repetição automática. Continua desconhecida clinicamente (CF 0), mas só uma correção explícita pode substituí-la. Campo de ficha ausente, por sua vez, pode ser perguntado.
6. Potencial usa cada regra uma única vez, incluindo evidência atual e contribuição futura máxima. Evidência negativa ainda não observada é ignorada no limite superior. CF negativos de derivados e condições negadas recebem limites inferior/superior próprios. Respostas passadas não são supostas mutáveis no cálculo; uma correção recalcula tudo.
7. Núcleo rejeita entradas estruturalmente inválidas/camadas impróprias; validação editorial completa, cobertura clínica e grafo pertencem ao futuro `kb/`.

## Focos da revisão

- Sem valor e CF 0 não podem criar evidência por negação ou comparações.
- O potencial deve limitar sequências com evidência negativa e derivados negados.
- `nao_sei`, mudança de modo e correção não devem criar loops nem inflar a contagem.
- Evidências conflitantes de mesma variável e conjunções impossíveis não devem gerar perguntas inúteis.
- Histórico de bandeira e explicações devem manter a origem da decisão após correção.

## Evidência final

Suíte completa: 56 testes, zero falhas. Compileall: saída 0. Exemplos CLI de confirmação e bandeira: saída 0, status passou. Revisão independente: duas falhas corrigidas por regressão RED→GREEN (triagem parcial e contradição através de derivado). Sem alterações nos documentos aprovados. Arquivos de implementação e testes entregues no checkout solicitado, sem publicação.
