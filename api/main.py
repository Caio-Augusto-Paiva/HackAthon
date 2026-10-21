"""Fábrica do app FastAPI: ``uvicorn api.main:app --host 127.0.0.1 --port 8000``."""
from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI
from starlette.datastructures import MutableHeaders
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from api.config import VERSAO_API, Configuracao, carregar_configuracao
from api.erros import CABECALHO_REQUISICAO_ID, novo_requisicao_id, registrar_handlers
from api.rotas import sistema


class MiddlewareRequisicaoId:
    """ASGI puro: dá um id a cada requisição (``request.state.requisicao_id``) e o devolve no cabeçalho."""

    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        requisicao_id = novo_requisicao_id()
        scope.setdefault("state", {})["requisicao_id"] = requisicao_id

        async def enviar(mensagem: Message) -> None:
            if mensagem["type"] == "http.response.start":
                MutableHeaders(scope=mensagem)[CABECALHO_REQUISICAO_ID] = requisicao_id
            await send(mensagem)

        await self.app(scope, receive, enviar)


@asynccontextmanager
async def _ciclo_de_vida(app: FastAPI) -> AsyncIterator[None]:
    config: Configuracao = app.state.config
    config.db_path.parent.mkdir(parents=True, exist_ok=True)
    # a Task 2 inicializa aqui o esquema SQLite (api.db.conexao.inicializar)
    yield


def criar_app(config: Configuracao | None = None) -> FastAPI:
    app = FastAPI(
        title="API de anamnese de bovinos leiteiros",
        version=VERSAO_API,
        separate_input_output_schemas=False,
        docs_url="/api/docs",
        redoc_url=None,
        openapi_url="/api/openapi.json",
        lifespan=_ciclo_de_vida,
    )
    app.state.config = config or carregar_configuracao()
    app.add_middleware(MiddlewareRequisicaoId)
    registrar_handlers(app)

    api = APIRouter(prefix="/api")
    api.include_router(sistema.router)
    app.include_router(api)
    return app


app = criar_app()  # sem I/O no import: a pasta do .db só é criada ao subir (lifespan)
