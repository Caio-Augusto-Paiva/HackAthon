"""Contrato das rotas de sistema."""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel


class Saude(BaseModel):
    status: Literal["ok"]
    versao_api: str
