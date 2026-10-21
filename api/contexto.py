"""Contexto de uma requisição: configuração, conexão SQLite e repositório de versões da base."""
from __future__ import annotations

import sqlite3
from collections.abc import Iterator
from dataclasses import dataclass

from fastapi import Request

from api.config import Configuracao
from api.db.conexao import abrir
from kb.carregador import Repositorio


@dataclass
class Contexto:
    config: Configuracao
    conn: sqlite3.Connection
    repo: Repositorio


def obter_contexto(request: Request) -> Iterator[Contexto]:
    """Dependência do FastAPI: um contexto por requisição, com a conexão fechada ao final."""
    config: Configuracao = request.app.state.config
    conn = abrir(config.db_path)
    try:
        yield Contexto(config=config, conn=conn, repo=Repositorio(config.base_dir, hoje=config.hoje))
    finally:
        conn.close()
