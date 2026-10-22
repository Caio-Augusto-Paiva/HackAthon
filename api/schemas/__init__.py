"""Contratos Pydantic da API."""
from typing import Any

from pydantic import ConfigDict

# Corpos que o cliente envia: campo desconhecido é erro (o cliente nunca envia CF; um "cf" no corpo dá 422)
# e NaN/Infinity (que o JSON do Python aceita) não entram como valor.
CONFIG_REQUISICAO = ConfigDict(extra="forbid", allow_inf_nan=False)


def _todos_obrigatorios(schema: dict[str, Any]) -> None:
    schema["required"] = list(schema.get("properties", {}))


# Modelos de RESPOSTA em que o servidor sempre envia todos os campos (os opcionais vão como ``null``). Sem isto o
# schema marca como opcional o campo que tem padrão em Python, e o cliente gerado do OpenAPI trataria
# ``campo?: T`` como se pudesse faltar. Só muda o schema: o modelo continua aceitando a ausência ao validar.
CONFIG_RESPOSTA_COMPLETA = ConfigDict(json_schema_extra=_todos_obrigatorios)
