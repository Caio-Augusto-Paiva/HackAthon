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
- `acao_bandeira('continuar' | 'ver_parecer')`: reconhece a pausa ou encerra pelo alerta. Veterinários não são pausados. Bandeira histórica mantém `chamar_agora` após correção; `como('chamar_agora')` distingue evidências históricas e atuais.
- `parecer()`: todas as doenças da base, três blocos, CF, percentuais, urgência e aviso de que CF não é probabilidade. Numa base com as oito doenças do projeto, lista as oito. Inconclusivas por limite são hipóteses abertas acima de 0,35. Bandeiras com condições desconhecidas são sinalizadas mesmo quando respondidas com `nao_sei`.
- `porque(simbolo)`: motivo gravado quando a pergunta foi apresentada. `como(simbolo)`: evidências disparadas, derivados e origem das observações. Não implementa “por que não é a doença X?”.
- `executar_caso(base, caso)`, em `engine.casos`: convenção da seção 2; ignora respostas não pedidas, preenche ausentes com `nao_sei`, reconhece pausas automaticamente. Suporta `continuacao`, faixas, top1/top3 e motivo de parada.

Uma observação pode ser `{'valor': ..., 'cf': 0.8, 'origem': 'importacao'}`. Origens: `resposta`, `ficha` ou `importacao`. Booleanos também aceitam `sim`, `nao` e `não`. Intensidade categórica é valor; certeza é campo separado. Não se pode injetar doenças/derivados como fatos observados.

O núcleo `inferir(base, fatos)` é sem estado. Cada resposta da sessão recalcula os CF sem reaplicar evidências já somadas. `analisar(base, fatos, modo)` fornece potencial, viabilidade e escolha de perguntas. Somente a sessão acumula histórico e urgência irreversível.

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

Ambiguidades resolvidas: o intervalo [-0,2; 0,2] aparece com 0% e “sem evidência”; doenças confirmadas não bloqueiam umas às outras na parada por comorbidade; potencial não reaplica regras já disparadas. Blocos usam CF antes do arredondamento, com 50% no principal. Arredondamento meio para cima. Registro completo: `docs/superpowers/plans/2026-10-20-motor-secao-1.md`.

As guardas rejeitam camadas inválidas, referências inexistentes, pesos extremos e observações inválidas. Não substituem a validação editorial completa de `kb/` (cobertura por doença, fontes clínicas, alcançabilidade, grafo e schema Pydantic). API, persistência, interface e base clínica não fazem parte desta entrega.
