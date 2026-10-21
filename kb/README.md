# Pacote `kb` — base de conhecimento

Modelos, validação, versionamento e conversão para grafo da base de conhecimento do sistema especialista de anamnese (PoC; dados fictícios, regras **suposição a validar**). Determinístico: sem LLM, sem rede e sem banco de dados. Requer Python 3.12 ou superior e `pydantic>=2.14,<2.15`: os JSON Schemas versionados em `kb/schema/` são gerados com essa versão (outra versão do Pydantic pode gerar um schema diferente e fazer `test_schema_sincronizado` falhar).

`kb` é um **pacote folha**: não importa `engine` nem qualquer outro pacote do projeto. Quem consome o `kb` (API, editor, scripts) é que o conecta ao motor; a compatibilidade com o motor é verificada em `tests/kb/test_integracao.py`.

## Módulos

| Módulo | Para que serve |
|---|---|
| `kb/modelos.py` | Modelos Pydantic (`Base`, `Simbolo`, `Regra`, `Condicao`, `Meta`, `Caso`...) e `carregar_base` (dict, texto JSON ou caminho; arquivos em UTF-8, com ou sem BOM) e `para_motor`. Normaliza na carga: operadores ASCII (`!=`, `<=`, `>=`) viram `≠`, `≤`, `≥`; `prioridade` ausente continua `None` e não é gravada; `Regra.prioridade_efetiva` devolve a explícita ou o padrão da classe (100 bandeira vermelha, 50 urgência, 10 evidência). Rejeita chaves desconhecidas. |
| `kb/analise.py` | Funções puras sobre a base: dependências entre símbolos e regras, ciclo, ordem topológica, símbolos da triagem, derivados de triagem, quem é perguntável a cada modo. Tolera referências pendentes (quem as reporta é o validador). |
| `kb/grafo.py` | Conversão 1:1 entre `Base` e grafo bipartido símbolos <-> regras (`base_para_grafo`, `grafo_para_base`), usado pelo editor visual. Preserva a ordem de condições e regras. `Aresta.ordem` é opcional: sem ela, vale a ordem das arestas em `Grafo.arestas`; com ela, as numeradas vêm antes (repetir uma `ordem` explícita na mesma regra é erro). Rejeita campo de papel errado (`cf` em condição; `op`/`valor`/`negado`/`cf_minimo`/`cf_maximo` em conclusão). |
| `kb/validador.py` | `validar(base)`, `validar_dados(json_cru)` e `validar_edicao(payload_do_editor)` devolvem um `Relatorio` (erros, avisos, resumo); a última devolve `(base | None, relatorio)` e converte o grafo do editor antes de validar. `validar_dados` e `validar_edicao` nunca levantam: falha de estrutura ou de conversão vira erro `E00`. |
| `kb/carregador.py` | `Repositorio`: versões imutáveis em `versoes/vNNNN.json`, ponteiro `ativa.json`, casos em `casos/casos.json`, hash sha256 por versão (leitura em UTF-8, com ou sem BOM). Salvar cria sempre a próxima versão (valida antes; nunca sobrescreve) e grava de forma atômica: escreve num temporário exclusivo (`tempfile.mkstemp`, `.vNNNN.json.tmp-*`, ignorado por `listar_versoes`), faz `flush` + `fsync` e publica com `os.link` (no Windows, sem hard link, com `os.rename`; ambos falham se o destino existe), removendo o temporário no `finally`. Gravações concorrentes nunca alteram uma versão publicada: a perdedora recebe `FileExistsError`. `ativar` também usa temporário único + `os.replace`; ativar só move o ponteiro. |

## Comandos

Na raiz do repositório (Windows; no shell POSIX use `.venv/bin/python`):

```powershell
python -m venv .venv
.venv/Scripts/python -m pip install -e ".[dev]"

# testes do kb e do motor
.venv/Scripts/python -m pytest -q
python -m unittest discover          # suíte do motor

# regenerar os JSON Schemas versionados em kb/schema/
.venv/Scripts/python scripts/exportar_schema.py
```

`tests/kb/test_integracao.py::test_schema_sincronizado` falha se `kb/schema/base.schema.json` ou `kb/schema/caso.schema.json` não corresponderem ao que o script gera hoje: depois de mudar um modelo, rode o script e versione os dois arquivos. O `.gitattributes` fixa fim de linha LF em `base/**` e `kb/schema/*.json`, para que o hash sha256 de uma versão não mude entre máquinas.

## Códigos do validador

Cada problema traz `numero` (E00, E01...), `codigo` (texto estável abaixo), `severidade`, `alvo` e `mensagem`. Erros (`E`) tornam a base inválida e impedem salvar; avisos (`W`) não.

| Número | `codigo` | Significado |
|---|---|---|
| E00 | `estrutura` | O JSON não tem a estrutura esperada (campo ausente, tipo errado, chave desconhecida, `se` vazio, NaN/infinito, `limite_dinamico` negativo) ou o grafo do editor não converte em base. |
| E01 | `simbolo_indefinido` | Regra ou tela de triagem cita um símbolo que não existe. |
| E02 | `id_duplicado` | Id repetido entre símbolos e regras (são nós do mesmo grafo), ou id de tela de triagem repetido. |
| E03 | `valor_invalido` | Valor ou operador da condição incompatível com o domínio do símbolo. |
| E04 | `cf_fora_do_limite` | `cf` de regra fora de [-0,99; +0,99]. |
| E05 | `ciclo` | Um símbolo depende, direta ou indiretamente, de si mesmo. |
| E06 | `regra_inalcancavel` | A regra nunca pode disparar (nada conclui o símbolo lido; a polaridade da condição sobre derivado/doença exige um `cf` que nenhuma regra produz, como negação ou `cf_maximo` sem regra de `cf` negativo, `cf_minimo` com `negado` ou condição positiva sobre conceito sem regra de `cf` positivo; ou símbolo não perguntável). |
| E07 | `bandeira_sem_chamar_agora` | Bandeira vermelha que não conclui `chamar_agora`. |
| E08 | `bandeira_sem_triagem` | Bandeira vermelha que não lê nenhum símbolo vindo da triagem. |
| E09 | `doenca_sem_regra` | Doença que nenhuma regra conclui. |
| E10 | `doenca_sem_regra_produtor` | Nenhuma regra da doença usa só informação que o produtor pode fornecer (conta o que as telas mostram ao produtor, como `Sessao._ids_tela`: lista do modo em `simbolos_por_modo` ou símbolos com pergunta para o produtor). |
| E11 | `cobertura_triagem` | Nenhuma regra da doença depende só de símbolos da triagem. |
| E12 | `camada` | Regra lê símbolo de camada igual ou superior à do símbolo que conclui. |
| E13 | `doenca_sem_gravidade` | Doença sem `gravidade`. |
| E14 | `derivado_max_negativo` | Combinação `max` fora de um derivado, ou derivado `max` com regra de `cf` <= 0 (o motor exige `cf` positivo em todas). |
| E15 | `limite_cf_invalido` | `cf_minimo`/`cf_maximo` mal usados (fora de [0, 1], os dois juntos, ou sobre símbolo que não é doença/derivado). |
| E16 | `tela_sem_texto` | Tela de triagem sem texto para o modo produtor ou veterinário. |
| E17 | `limiares_fora_de_ordem` | Limiares da meta fora de [-1, 1] ou da ordem estrita exigida; `0 <= bloco_diferencial < bloco_principal <= 1`. |
| E18 | `regra_sem_fonte` | Regra sem fonte. |
| E19 | `classe_incompativel` | Classe da regra incompatível com o símbolo concluído: evidência conclui derivado ou doença; urgência e bandeira concluem símbolo de tipo `urgencia` (urgência só `observar` ou `chamar_agora`; `sem_problema` nunca). |
| E20 | `id_invalido` | Id de símbolo fora de `^[a-z0-9_]+$` ou de regra fora de `^[A-Za-z0-9_-]+$`. |
| E21 | `tela_simbolo_invalido` | Tela de triagem lista um símbolo que não é `pergunta` nem `ficha`, ou tela `multipla` com símbolo não booleano. |
| E22 | `cf_urgencia_nao_positivo` | Regra de classe `urgencia` ou `bandeira_vermelha` com `entao.cf <= 0`. |
| E23 | `dominio_conceito_nao_booleano` | Derivado, doença ou urgência com domínio diferente de `booleano`. |
| W01 | `simbolo_nao_usado` | Pergunta, ficha ou derivado que nenhuma regra lê nem aparece na triagem. |
| W02 | `regras_contraditorias` | Regras com as mesmas condições e conclusões de sinais opostos sobre o mesmo símbolo. |
| W03 | `suposicoes_pendentes` | Existem regras ainda com status `suposicao_a_validar`. |

## Segurança de entrada

`carregar_base(str)` trata qualquer texto que não comece com `{` como **caminho de arquivo**. Nunca passe a ela texto vindo de requisição não confiável: na API, decodifique o JSON do corpo e use `validar_dados(dict)` ou `validar_edicao(dict)`, que não tocam o disco.

## Compatibilidade com o motor

O motor (`engine/`) lê a base como dict. Para entregar uma `Base` do `kb` a ele, use `para_motor`, que já aplica `exclude_none=True`:

```python
from engine.modelos import Base as BaseMotor
from kb import para_motor
BaseMotor.de_dict(para_motor(base))
```

Contrato: toda base que `validar` declara válida é aceita por `BaseMotor.de_dict(para_motor(base))` e roda numa `Sessao` de fumaça (coberto por `tests/kb/test_contrato_motor.py` e, por propriedade com `hypothesis`, por `tests/kb/test_contrato_propriedade.py`).

Divergências conhecidas entre os dois formatos (reveladas por `tests/kb/test_integracao.py`):

1. **`exclude_none=True` é obrigatório** (já embutido em `para_motor`). O `model_dump` do `kb` escreve `cf_minimo: null`/`cf_maximo: null` em toda condição; a guarda do motor testa só a presença da chave e rejeita a base com "Limite de CF inválido". Sem `exclude_none` o motor recusa até a base de teste.
2. **Prioridade padrão.** O `kb` não grava a prioridade padrão (o campo fica `None`; use `Regra.prioridade_efetiva`); o motor (`Base.de_dict`) preenche 100/50/10 por classe quando a chave falta. O teste `test_motor_mesmo_cf_sem_prioridade_explicita` confirma CF idênticos.
3. **Chave `layout`.** O dump inclui `layout` (posições do editor) no topo; o motor a ignora.
4. **Operadores ASCII.** O `kb` converte `!=`, `<=`, `>=` na carga; o motor só aceita os canônicos (`≠`, `≤`, `≥`). Passe sempre pelo `kb` antes do motor.
