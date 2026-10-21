# Motor de inferência — seção 1

Implementação independente de web, banco, LLM e serviços externos. Requer Python 3.12 ou superior; não requer instalação de dependências. Execute os comandos abaixo na raiz de `HackAtom`.

## Testes

```powershell
python -m unittest discover -v
```

Os testes também são coletáveis pelo pytest, quando disponível. Neste ambiente foi usado `C:\Users\Usuario\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe` (em PowerShell, prefixe o caminho entre aspas com `&`).

## Demonstração executável

```powershell
python -m engine tests/fixtures/motor/base.json tests/fixtures/motor/confirmacao.json
python -m engine tests/fixtures/motor/base.json tests/fixtures/motor/bandeira.json
```

Os dois comandos imprimem JSON com `status: "passou"` e saem com código 0. Caso falhando ou entrada inválida retorna código 1. A base demonstra seis telas e oito hipóteses **artificiais**; não contém conhecimento veterinário nem serve para triagem de animais.

## Interface Python

```python
import json
from engine.sessao import Sessao

with open('tests/fixtures/motor/base.json', encoding='utf-8') as arquivo:
    base = json.load(arquivo)

sessao = Sessao(base, modo='produtor', ficha={'dias': 10})
print(sessao.estado()['proxima'])
sessao.responder_triagem('medida', {'medida': 5})
sessao.responder_triagem('grupo1', ['sinal1'])
sessao.responder_triagem('grupo2', [])
sessao.responder_triagem('grupo3', [])
sessao.responder_triagem('grupo4', [])
sessao.responder('confirmar1', True)
print(sessao.parecer())
print(sessao.porque('confirmar1'))
print(sessao.como('hipotese1'))
```

- `Sessao(base, modo='produtor', ficha=None, limite_dinamico=None)`: recebe o JSON canônico `meta/simbolos/regras`, ou objeto com `model_dump()`. Limite opcional substitui somente o desta sessão.
- `estado()`: fase, próxima tela/pergunta, urgência, pausa, progresso e motivo de parada. Não apresenta pergunta dinâmica antes de concluir a triagem.
- `responder_triagem(id, resposta, corrigir=False)`: seleção múltipla recebe lista dos ids marcados, inclusive `[]`; escolha única recebe valor ou mapa `símbolo → valor`. `None`, `nao_sei` e `não sei` registram desconhecimento. Responda somente aos símbolos mostrados em `proxima.simbolos`; dados da ficha são preservados. `corrigir=True` altera explicitamente os símbolos da tela já respondida no modo atual.
- `responder(simbolo, valor, corrigir=False)`: responde à pergunta dinâmica atual ou corrige uma resposta anterior. Correção não consome outra pergunta. `nao_sei` conta como respondida, evita repetição e mantém CF 0.
- `trocar_modo('veterinario')`: preserva fatos, contagem e motivos originais. Uma tela com alternativa por modo apresenta os símbolos ainda ausentes no novo modo.
- `acao_bandeira('continuar' | 'ver_parecer')`: reconhece a pausa ou encerra pelo alerta. Veterinários não são pausados. Novas respostas mantêm a urgência já ativada; uma correção explícita pode remover somente as bandeiras que dependem dos símbolos corrigidos, direta ou indiretamente. As dependências vêm da estrutura da base, inclusive dos caminhos por derivados/doenças que não disparam no cálculo atual. As demais bandeiras retidas são preservadas e somadas às que disparam agora. Reconhecimento é mantido só para as ativas; uma bandeira removida e depois reativada pausa novamente.
- `parecer()`: todas as doenças da base, três blocos, CF, percentuais, urgência e aviso de que CF não é probabilidade. Numa base com as oito doenças do projeto, lista as oito. Inconclusivas por limite são hipóteses abertas acima de 0,35. Bandeiras não verificadas são listadas somente na parada por limite e precisam ser viáveis e perguntáveis no modo atual.
- `porque(simbolo)`: motivo gravado quando a pergunta foi apresentada. `como(simbolo)`: evidências disparadas, derivados e origem das observações. Não implementa “por que não é a doença X?”.
- `executar_caso(base, caso)`, em `engine.casos`: convenção da seção 2; ignora respostas não pedidas, preenche ausentes com `nao_sei`, reconhece pausas automaticamente. Suporta `continuacao`, faixas, top1/top3, motivo de parada, `inconclusivas` (a saída contém todas as esperadas, podendo incluir outras) e `alerta.pausa` (ou `alerta: {pausa: ...}`). No executor, a pausa indica se ela ocorreu durante o caso, antes do reconhecimento automático.

Uma observação pode ser `{'valor': ..., 'cf': 0.8, 'origem': 'importacao'}`. Origens: `resposta`, `ficha` ou `importacao`. Booleanos também aceitam `sim`, `nao` e `não`. Intensidade categórica é valor; certeza é campo separado. Não se pode injetar doenças/derivados como fatos observados.

O núcleo `inferir(base, fatos)` é sem estado. Cada resposta da sessão recalcula os CF sem reaplicar evidências já somadas. `analisar(base, fatos, modo)` fornece potencial, viabilidade e escolha de perguntas. A sessão guarda os eventos de perguntas e correções, seguidos do traço do cálculo atual; não acumula os cálculos antigos. Correções são eventos `fato_adicionado` com `correcao: true` e o fato `anterior`; conclusões emitem fatos de origem `regra`.

Campos `null` da ficha são ausentes e continuam perguntáveis, inclusive `{'valor': null}`. Isso é diferente de uma resposta explícita `nao_sei` (ou `{'nao_sei': true}`), que conta como respondida. Seleção múltipla também aceita um mapa completo dos símbolos apresentados para booleanos, sem sobrescrever fatos da ficha que a tela não apresentou.

## Restauração pela API, sem replay

`Sessao.restaurar(base, *, modo, fatos, perguntas_dinamicas, perguntas_feitas, bandeiras_reconhecidas=(), finalizada_por_alerta=False, limite_dinamico=None, correcoes=(), bandeiras_ativas=None)` carrega diretamente os dados persistidos. A base deve ser a mesma versão à qual a sessão está vinculada. A API decodifica as colunas JSON e passa:

- `fatos`: mapa por símbolo, com valor, CF, origem e `tela_id`, ou objetos `Fato`. Fato de resposta com valor nulo/CF 0 é conservado, pois representa `nao_sei`; o filtro de nulos vale somente na carga inicial da ficha.
- `perguntas_dinamicas`: ids das perguntas respondidas, em ordem, sem duplicatas. Uma resposta corrigida continua contando uma vez.
- `perguntas_feitas`: mapa por símbolo ou lista dos eventos `pergunta_feita`, com o motivo original. Pode conter pergunta apresentada ainda não respondida.
- `bandeiras_reconhecidas` e `finalizada_por_alerta`: reconhecimento e encerramento, sem recriar a pausa já aceita.
- `correcoes`: eventos de correção, se persistidos. `bandeiras_ativas`: snapshots das bandeiras retidas após novas respostas; necessário para preservar uma bandeira cujo suporte atual mudou por novas evidências. Na ausência desse campo, são usadas as bandeiras que disparam com os fatos atuais.

O método valida as observações, mas não as submete à regra de “é a próxima pergunta”. Repetir `responder()` para reconstruir o banco seria incorreto: uma correção pode ter alterado a seleção desde que as respostas foram registradas.

`exportar()` produz um snapshot JSON aceito diretamente por `restaurar`, preservando valores/CF racionais sem perda:

```python
dados = json.loads(json.dumps(sessao.exportar()))
restaurada = Sessao.restaurar(base, **dados)
assert restaurada.estado() == sessao.estado()
```

## Organização

| Módulos | Responsabilidade |
|---|---|
| `cf`, `avaliacao` | CF MYCIN e condições |
| `modelos`, `validacao` | adaptação de entrada e guardas de execução |
| `inferencia`, `traco` | agenda em camadas, propagação e eventos |
| `selecao`, `parada` | objetivos abertos, viabilidade, potencial e encerramento |
| `memoria`, `sessao` | diálogo, observações, correção e modo |
| `parecer`, `explicacao` | apresentação e rastreabilidade |
| `casos`, `__main__` | execução reproduzível dos casos |

## Decisões e limites

CF internos são `Fraction`, inclusive após centenas de combinações; a apresentação converte para números JSON. Isso evita arredondar uma conclusão quase certa para ±1 e travar combinações futuras. Testes verificam todas as permutações de 2 a 6 evidências e extremos defensivos.

O potencial considera cada regra uma vez e propaga intervalos inferior/superior. É conservador: pode superestimar a confiança alcançável, nunca deve subestimá-la. Condições da mesma variável compartilham um valor possível; folhas compartilhadas entre condições e derivados são particionadas conjuntamente para rejeitar contradições. Essa checagem pode custar mais em bases com muitos caminhos compartilhados; não é um otimizador global de todas as correlações entre certezas contínuas.

A especificação canônica prevalece sobre o plano histórico: percentual é sempre `max(0, CF) × 100`, inclusive em “sem evidência” (CF 0,15 aparece como 15%). Arredondamento meio para cima. Cortes de bloco vêm de `meta.limiares.bloco_principal`/`bloco_diferencial` (padrões 0,50/0,20), usando CF antes do arredondamento; ids iguais aos da API. Prioridades padrão: bandeira 100, urgência 50, evidência 10; valor explícito 0 é preservado. Doenças confirmadas não bloqueiam umas às outras na parada por comorbidade. Perguntas que podem confirmar bandeiras pendentes têm precedência sobre as demais.

As guardas rejeitam camadas inválidas, referências inexistentes, pesos extremos e observações inválidas. Regras de classe `urgencia` ou `bandeira_vermelha` exigem CF estritamente positivo; zero ou negativo produz `ValueError('CF de urgência ou bandeira deve ser positivo')`. Como defesa adicional, a inferência só conta urgências e bandeiras cujo CF final da conclusão seja maior que zero. Não substituem a validação editorial completa de `kb/` (cobertura por doença, fontes clínicas, alcançabilidade, grafo e schema Pydantic). API, persistência, interface e base clínica não fazem parte desta entrega.
