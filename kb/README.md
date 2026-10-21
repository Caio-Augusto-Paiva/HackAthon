# Pacote `kb` — base de conhecimento

Modelos, validação, versionamento e conversão para grafo da base de conhecimento do sistema especialista de anamnese (PoC; dados fictícios, regras **suposição a validar**). Determinístico: sem LLM, sem rede e sem banco de dados. Requer Python 3.12 ou superior e `pydantic>=2.7`.

`kb` é um **pacote folha**: não importa `engine` nem qualquer outro pacote do projeto. Quem consome o `kb` (API, editor, scripts) é que o conecta ao motor; a compatibilidade com o motor é verificada em `tests/kb/test_integracao.py`.

## Módulos

| Módulo | Para que serve |
|---|---|
| `kb/modelos.py` | Modelos Pydantic (`Base`, `Simbolo`, `Regra`, `Condicao`, `Meta`, `Caso`...) e `carregar_base` (dict, texto JSON ou caminho). Normaliza na carga: operadores ASCII (`!=`, `<=`, `>=`) viram `≠`, `≤`, `≥`; `prioridade` ausente vira 100 (bandeira vermelha), 50 (urgência) ou 10 (evidência). Rejeita chaves desconhecidas. |
| `kb/analise.py` | Funções puras sobre a base: dependências entre símbolos e regras, ciclo, ordem topológica, símbolos da triagem, derivados de triagem, quem é perguntável a cada modo. Tolera referências pendentes (quem as reporta é o validador). |
| `kb/grafo.py` | Conversão 1:1 entre `Base` e grafo bipartido símbolos <-> regras (`base_para_grafo`, `grafo_para_base`), usado pelo editor visual. Preserva a ordem de condições e regras. |
| `kb/validador.py` | `validar(base)` e `validar_dados(json_cru)` devolvem um `Relatorio` (erros, avisos, resumo). `validar_dados` nunca levanta: falha de estrutura vira erro `E00`. |
| `kb/carregador.py` | `Repositorio`: versões imutáveis em `versoes/vNNNN.json`, ponteiro `ativa.json`, casos em `casos/casos.json`, hash sha256 por versão. Salvar cria sempre a próxima versão (valida antes; nunca sobrescreve); ativar só move o ponteiro. |

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
| E00 | `estrutura` | O JSON não tem a estrutura esperada (campo ausente, tipo errado, chave desconhecida, `se` vazio). |
| E01 | `simbolo_indefinido` | Regra ou tela de triagem cita um símbolo que não existe. |
| E02 | `id_duplicado` | Id repetido entre símbolos e regras (são nós do mesmo grafo). |
| E03 | `valor_invalido` | Valor ou operador da condição incompatível com o domínio do símbolo. |
| E04 | `cf_fora_do_limite` | `cf` de regra fora de [-0,99; +0,99]. |
| E05 | `ciclo` | Um símbolo depende, direta ou indiretamente, de si mesmo. |
| E06 | `regra_inalcancavel` | A regra nunca pode disparar (nada conclui o símbolo lido, negação sem `cf` negativo, ou símbolo não perguntável). |
| E07 | `bandeira_sem_chamar_agora` | Bandeira vermelha que não conclui `chamar_agora`. |
| E08 | `bandeira_sem_triagem` | Bandeira vermelha que não lê nenhum símbolo vindo da triagem. |
| E09 | `doenca_sem_regra` | Doença que nenhuma regra conclui. |
| E10 | `doenca_sem_regra_produtor` | Nenhuma regra da doença usa só informação que o produtor pode fornecer. |
| E11 | `cobertura_triagem` | Nenhuma regra da doença depende só de símbolos da triagem. |
| E12 | `camada` | Regra lê símbolo de camada igual ou superior à do símbolo que conclui. |
| E13 | `doenca_sem_gravidade` | Doença sem `gravidade`. |
| E14 | `derivado_max_negativo` | Derivado com combinação `max` recebe regra com `cf` negativo. |
| E15 | `limite_cf_invalido` | `cf_minimo`/`cf_maximo` mal usados (fora de [0, 1], os dois juntos, ou sobre símbolo que não é doença/derivado). |
| E16 | `tela_sem_texto` | Tela de triagem sem texto para o modo produtor ou veterinário. |
| E17 | `limiares_fora_de_ordem` | Limiares da meta fora da ordem estrita exigida. |
| E18 | `regra_sem_fonte` | Regra sem fonte. |
| E19 | `classe_incompativel` | Classe da regra incompatível com o símbolo concluído (inclui `sem_problema` como conclusão). |
| E20 | `id_invalido` | Id de símbolo fora de `^[a-z0-9_]+$` ou de regra fora de `^[A-Za-z0-9_-]+$`. |
| W01 | `simbolo_nao_usado` | Pergunta, ficha ou derivado que nenhuma regra lê nem aparece na triagem. |
| W02 | `regras_contraditorias` | Regras com as mesmas condições e conclusões de sinais opostos sobre o mesmo símbolo. |
| W03 | `suposicoes_pendentes` | Existem regras ainda com status `suposicao_a_validar`. |

## Compatibilidade com o motor

O motor (`engine/`) lê a base como dict. Para entregar uma `Base` do `kb` a ele, use:

```python
from engine.modelos import Base as BaseMotor
BaseMotor.de_dict(base.model_dump(mode="json", exclude_none=True))
```

Divergências conhecidas entre os dois formatos (reveladas por `tests/kb/test_integracao.py`):

1. **`exclude_none=True` é obrigatório.** O `model_dump` do `kb` escreve `cf_minimo: null`/`cf_maximo: null` em toda condição; a guarda do motor testa só a presença da chave e rejeita a base com "Limite de CF inválido". Sem `exclude_none` o motor recusa até a base de teste.
2. **Prioridade padrão.** O `kb` injeta `prioridade` 100/50/10 por classe; o motor assume 0 quando a chave falta. Isso só muda a ordem de disparo dentro de uma camada (e, portanto, a ordem do traço), não os CF finais: o teste `test_motor_mesmo_cf_sem_prioridade_explicita` confirma CF idênticos.
3. **Chave `layout`.** O dump inclui `layout` (posições do editor) no topo; o motor a ignora.
4. **Operadores ASCII.** O `kb` converte `!=`, `<=`, `>=` na carga; o motor só aceita os canônicos (`≠`, `≤`, `≥`). Passe sempre pelo `kb` antes do motor.
