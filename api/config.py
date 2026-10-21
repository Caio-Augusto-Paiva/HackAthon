"""Configuração da API: caminhos por variável de ambiente e relógio injetável (para os testes)."""
from __future__ import annotations

import os
from collections.abc import Callable
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path

VERSAO_API = "0.1.0"


@dataclass(frozen=True)
class Configuracao:
    base_dir: Path
    db_path: Path
    web_dist: Path
    hoje: Callable[[], date]
    agora: Callable[[], datetime]


def carregar_configuracao() -> Configuracao:
    """Lê ``ANAMNESE_BASE_DIR`` (padrão ``base``) e ``ANAMNESE_DB`` (padrão ``dados/anamnese.db``)."""
    return Configuracao(
        base_dir=Path(os.environ.get("ANAMNESE_BASE_DIR", "base")),
        db_path=Path(os.environ.get("ANAMNESE_DB", "dados/anamnese.db")),
        web_dist=Path("web/dist"),
        hoje=date.today,
        agora=datetime.now,
    )
