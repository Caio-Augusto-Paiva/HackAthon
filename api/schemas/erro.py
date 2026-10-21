"""Formato único de erro da API (Seção 4.4): ``{"erro": {codigo, mensagem, requisicao_id, detalhes?}}``."""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel

from kb.validador import Alvo


class Detalhe(BaseModel):
    """Um item de ``detalhes``; o mesmo formato serve ao validador da base."""

    codigo: str
    severidade: Literal["erro", "aviso"]
    alvo: Alvo | None = None
    mensagem: str


class CorpoErro(BaseModel):
    codigo: str
    mensagem: str
    requisicao_id: str
    detalhes: list[Detalhe] | None = None


class ErroResposta(BaseModel):
    erro: CorpoErro
