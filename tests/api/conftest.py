"""Fixtures da API: base temporária, configuração, app e cliente (dados fictícios)."""
from __future__ import annotations

import json
from collections.abc import Callable, Iterator
from datetime import date, datetime
from pathlib import Path

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from api.config import Configuracao
from api.main import criar_app
from kb.carregador import Repositorio
from kb.modelos import carregar_base

RAIZ = Path(__file__).resolve().parents[2]
CAMINHO_BASE_MINIMA = RAIZ / "tests" / "fixtures" / "kb" / "base_minima.json"


@pytest.fixture
def hoje() -> date:
    return date(2026, 10, 20)


@pytest.fixture
def agora() -> datetime:
    return datetime(2026, 10, 20, 10, 0)


@pytest.fixture
def fabrica_base_dir(hoje: date) -> Callable[..., Path]:
    """Devolve ``fabricar(destino, ajustar=None) -> Path``.

    Grava a base mínima como ``v0001`` em ``destino`` e a ativa. ``ajustar(dict)`` altera o
    dict da base antes de salvar (no lugar; se devolver um dict, ele é usado no lugar).
    """

    def fabricar(destino: Path, ajustar: Callable[[dict], dict | None] | None = None) -> Path:
        dados = json.loads(CAMINHO_BASE_MINIMA.read_text(encoding="utf-8"))
        if ajustar is not None:
            dados = ajustar(dados) or dados
        repo = Repositorio(destino, hoje=lambda: hoje)
        repo.salvar_nova(carregar_base(dados), autor="teste", nota="fixture")
        repo.ativar("v0001")
        return destino

    return fabricar


@pytest.fixture
def base_dir(tmp_path: Path, fabrica_base_dir: Callable[..., Path]) -> Path:
    return fabrica_base_dir(tmp_path / "base")


@pytest.fixture
def config(tmp_path: Path, base_dir: Path, hoje: date, agora: datetime) -> Configuracao:
    return Configuracao(
        base_dir=base_dir,
        db_path=tmp_path / "dados" / "anamnese.db",
        web_dist=tmp_path / "web" / "dist",
        hoje=lambda: hoje,
        agora=lambda: agora,
    )


@pytest.fixture
def app(config: Configuracao) -> FastAPI:
    return criar_app(config)


@pytest.fixture
def cliente(app: FastAPI) -> Iterator[TestClient]:
    with TestClient(app, raise_server_exceptions=False) as c:
        yield c
