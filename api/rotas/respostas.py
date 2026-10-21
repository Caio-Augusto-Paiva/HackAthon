"""Respostas de erro documentadas no OpenAPI (Seção 4.4).

Toda resposta de erro da API tem o corpo ``ErroResposta`` (``api/erros.py``); aqui só se declara, por grupo de
rotas, quais status cada uma pode devolver. O 422 documentado é o da 4.4, não o ``HTTPValidationError`` do FastAPI.
"""
from __future__ import annotations

from typing import Any

from api.schemas.erro import ErroResposta

_DESCRICAO = {
    404: "Recurso não encontrado (`nao_encontrado`).",
    409: "Conflito com o estado atual (`conflito`, `ja_respondida`, `nao_respondida` ou `casos_falhando`).",
    422: "Entrada recusada (`entrada_invalida` e os demais códigos 422 da Seção 4.4).",
    500: "Erro interno (`erro_interno`); a mensagem nunca revela detalhe técnico.",
}


def erros(*status: int) -> dict[int | str, dict[str, Any]]:
    """O argumento ``responses=`` de uma rota: cada status em ``status`` com o corpo ``ErroResposta``."""
    return {codigo: {"model": ErroResposta, "description": _DESCRICAO[codigo]} for codigo in status}


ERROS_SO_INTERNO = erros(500)  # rota sem entrada do cliente
ERROS_DE_ENTRADA = erros(422, 500)  # só a consulta ou o corpo podem ser recusados
ERROS_DE_RECURSO = erros(404, 422, 500)  # o recurso do caminho (ou do corpo) pode não existir
ERROS_DE_CONFLITO = erros(404, 409, 422, 500)  # além disso, o estado atual pode impedir a operação
ERROS_DE_CADASTRO = erros(409, 422, 500)  # cria algo que não depende de outro recurso do cliente
