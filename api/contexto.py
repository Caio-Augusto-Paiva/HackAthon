"""Contexto de uma requisição: configuração, conexão SQLite e repositório de versões da base."""
from __future__ import annotations

import sqlite3
from collections.abc import Iterator
from dataclasses import dataclass

from fastapi import Request

from api.config import Configuracao
from kb.carregador import Repositorio


@dataclass
class Contexto:
    config: Configuracao
    conn: sqlite3.Connection | None  # provisório: vira sqlite3.Connection na Task 2
    repo: Repositorio


def obter_contexto(request: Request) -> Iterator[Contexto]:
    """Dependência do FastAPI: um contexto por requisição, com a conexão fechada ao final."""
    config: Configuracao = request.app.state.config
    conn = None  # provisório: a conexão (api.db.conexao.abrir) entra na Task 2
    try:
        yield Contexto(config=config, conn=conn, repo=Repositorio(config.base_dir, hoje=config.hoje))
    finally:
        if conn is not None:
            conn.close()
