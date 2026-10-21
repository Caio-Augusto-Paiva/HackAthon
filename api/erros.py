"""Erros da API: exceção de domínio, fábricas e handlers do formato único (Seção 4.4).

Toda resposta de erro tem o corpo ``{"erro": {codigo, mensagem, requisicao_id, detalhes?}}`` e o
cabeçalho ``X-Requisicao-Id`` com o mesmo id. O 500 nunca revela detalhe técnico.
"""
from __future__ import annotations

import logging
import secrets

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from api.schemas.erro import CorpoErro, Detalhe, ErroResposta

CABECALHO_REQUISICAO_ID = "X-Requisicao-Id"
MENSAGEM_ERRO_INTERNO = "Erro interno. Tente novamente."
MENSAGEM_VALOR_INVALIDO = "Valor inválido."

_log = logging.getLogger("api")


class ErroApi(Exception):
    """Erro de domínio: vira a resposta HTTP ``status`` com o formato único."""

    def __init__(self, status: int, codigo: str, mensagem: str, detalhes: list[dict] | None = None):
        super().__init__(mensagem)
        self.status = status
        self.codigo = codigo
        self.mensagem = mensagem
        self.detalhes = detalhes


def nao_encontrado(mensagem: str) -> ErroApi:
    return ErroApi(404, "nao_encontrado", mensagem)


def conflito(mensagem: str, codigo: str = "conflito") -> ErroApi:
    return ErroApi(409, codigo, mensagem)


def resposta_invalida(mensagem: str) -> ErroApi:
    return ErroApi(422, "resposta_invalida", mensagem)


def base_invalida(mensagem: str, detalhes: list[dict]) -> ErroApi:
    return ErroApi(422, "base_invalida", mensagem, detalhes)


def simbolo_invalido(mensagem: str) -> ErroApi:
    return ErroApi(422, "simbolo_invalido", mensagem)


def importacao_invalida(mensagem: str) -> ErroApi:
    return ErroApi(422, "importacao_invalida", mensagem)


def novo_requisicao_id() -> str:
    """``rq_`` + 4 dígitos hexadecimais (ex.: ``rq_8f2a``)."""
    return "rq_" + secrets.token_hex(2)


# --- resposta -------------------------------------------------------------------------------

def _requisicao_id(request: Request) -> str:
    """O id do middleware; se faltar, gera um e o guarda, para o log e a resposta usarem o mesmo."""
    requisicao_id = getattr(request.state, "requisicao_id", None)
    if requisicao_id is None:
        requisicao_id = request.state.requisicao_id = novo_requisicao_id()
    return requisicao_id


def _responder(
    request: Request,
    status: int,
    codigo: str,
    mensagem: str,
    detalhes: list[dict] | None = None,
    cabecalhos: dict[str, str] | None = None,
) -> JSONResponse:
    requisicao_id = _requisicao_id(request)
    corpo = ErroResposta(
        erro=CorpoErro(
            codigo=codigo,
            mensagem=mensagem,
            requisicao_id=requisicao_id,
            detalhes=[Detalhe.model_validate(d) for d in detalhes] if detalhes else None,
        )
    )
    return JSONResponse(
        corpo.model_dump(mode="json", exclude_none=True),
        status_code=status,
        # o middleware só alcança respostas normais; o 500 sai por fora dele, então o id vai aqui
        headers={**(cabecalhos or {}), CABECALHO_REQUISICAO_ID: requisicao_id},
    )


# --- validação (substitui o 422 padrão do FastAPI) ------------------------------------------

_ONDE = {"body": "corpo", "query": "consulta", "path": "caminho", "header": "cabecalho", "cookie": "cookie"}

_TEXTOS_VALIDACAO = {
    "missing": "Campo obrigatório.",
    "json_invalid": "O corpo não é um JSON válido.",
    "string_type": "Deve ser um texto.",
    "int_parsing": "Deve ser um número inteiro.",
    "int_type": "Deve ser um número inteiro.",
    "float_parsing": "Deve ser um número.",
    "float_type": "Deve ser um número.",
    "bool_parsing": "Deve ser verdadeiro ou falso.",
    "bool_type": "Deve ser verdadeiro ou falso.",
    "literal_error": "Valor fora das opções permitidas.",
    "extra_forbidden": "Campo não permitido.",
    "dict_type": "Deve ser um objeto.",
    "model_attributes_type": "Deve ser um objeto.",
    "list_type": "Deve ser uma lista.",
    "string_too_short": "Texto curto demais.",
    "string_too_long": "Texto longo demais.",
    "greater_than": "Valor abaixo do mínimo permitido.",
    "greater_than_equal": "Valor abaixo do mínimo permitido.",
    "less_than": "Valor acima do máximo permitido.",
    "less_than_equal": "Valor acima do máximo permitido.",
    "date_parsing": "Deve ser uma data válida (AAAA-MM-DD).",
    "date_from_datetime_parsing": "Deve ser uma data válida (AAAA-MM-DD).",
    "too_short": "Lista com poucos itens.",
    "too_long": "Lista com itens demais.",
}


def _detalhe_de_validacao(erro: dict) -> dict:
    tipo = erro["type"]
    if tipo == "value_error":  # validadores próprios levantam ValueError com texto em português
        texto = str(erro["msg"]).removeprefix("Value error, ")
    else:  # nunca a "msg" do Pydantic: ela está em inglês e pode citar o valor enviado
        texto = _TEXTOS_VALIDACAO.get(tipo, MENSAGEM_VALOR_INVALIDO)
    caminho = [_ONDE.get(str(p), str(p)) if i == 0 else str(p) for i, p in enumerate(erro["loc"])]
    local = "corpo" if tipo == "json_invalid" else ".".join(caminho)
    # só o tipo, o local e o texto: o valor enviado não volta na resposta
    return {"codigo": tipo, "severidade": "erro", "mensagem": f"{local}: {texto}"}


# --- handlers -------------------------------------------------------------------------------

async def _tratar_erro_api(request: Request, exc: ErroApi) -> JSONResponse:
    return _responder(request, exc.status, exc.codigo, exc.mensagem, exc.detalhes)


async def _tratar_validacao(request: Request, exc: RequestValidationError) -> JSONResponse:
    return _responder(
        request,
        422,
        "entrada_invalida",
        "Os dados enviados não seguem o formato esperado.",
        [_detalhe_de_validacao(e) for e in exc.errors()],
    )


async def _tratar_http(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    cabecalhos = dict(exc.headers or {})
    if exc.status_code == 404:
        return _responder(request, 404, "nao_encontrado", "Recurso não encontrado.", None, cabecalhos)
    if exc.status_code == 405:  # suposição: fora da tabela da 4.4
        return _responder(
            request, 405, "metodo_nao_permitido", "Método não permitido para este recurso.", None, cabecalhos
        )
    if exc.status_code < 500:  # a 4.4 reserva entrada_invalida ao 422: todo outro 4xx do Starlette vira 422
        return _responder(request, 422, "entrada_invalida", "Requisição inválida.")
    return _responder(request, exc.status_code, "erro_interno", MENSAGEM_ERRO_INTERNO, None, cabecalhos)


async def _tratar_inesperado(request: Request, exc: Exception) -> JSONResponse:
    # a mensagem é fixa de propósito: nada da exceção vai para o cliente; o servidor a registra com o id
    _log.error("erro interno %s", _requisicao_id(request), exc_info=exc)
    return _responder(request, 500, "erro_interno", MENSAGEM_ERRO_INTERNO)


def registrar_handlers(app: FastAPI) -> None:
    app.add_exception_handler(ErroApi, _tratar_erro_api)
    app.add_exception_handler(RequestValidationError, _tratar_validacao)
    app.add_exception_handler(StarletteHTTPException, _tratar_http)
    app.add_exception_handler(Exception, _tratar_inesperado)
