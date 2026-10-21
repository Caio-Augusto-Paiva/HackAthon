"""Contratos Pydantic da API."""
from pydantic import ConfigDict

# Corpos que o cliente envia: campo desconhecido é erro (o cliente nunca envia CF; um "cf" no corpo dá 422)
# e NaN/Infinity (que o JSON do Python aceita) não entram como valor.
CONFIG_REQUISICAO = ConfigDict(extra="forbid", allow_inf_nan=False)
