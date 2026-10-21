"""Conexão SQLite e inicialização do esquema (``esquema.sql``)."""
from __future__ import annotations

import sqlite3
from contextlib import closing
from pathlib import Path

CAMINHO_ESQUEMA = Path(__file__).with_name("esquema.sql")


def abrir(caminho: Path) -> sqlite3.Connection:
    """Abre uma conexão com linhas ``sqlite3.Row`` e chaves estrangeiras ligadas.

    ``check_same_thread=False``: a dependência síncrona do FastAPI (abrir, usar, fechar) roda em threads
    do pool que podem ser diferentes; cada conexão pertence a uma só requisição, então não há uso concorrente.
    """
    conn = sqlite3.connect(caminho, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def inicializar(caminho: Path) -> None:
    """Cria a pasta do banco e executa o DDL (``CREATE ... IF NOT EXISTS``), sem tocar no que já existe."""
    caminho.parent.mkdir(parents=True, exist_ok=True)
    ddl = CAMINHO_ESQUEMA.read_text(encoding="utf-8")
    with closing(abrir(caminho)) as conn:
        conn.executescript(ddl)
