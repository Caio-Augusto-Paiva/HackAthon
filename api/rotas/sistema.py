"""Rotas de sistema."""
from __future__ import annotations

from fastapi import APIRouter

from api.config import VERSAO_API
from api.rotas.respostas import ERROS_SO_INTERNO
from api.schemas.sistema import Saude

router = APIRouter()


@router.get("/saude", operation_id="saude", responses=ERROS_SO_INTERNO, summary="Saúde do servidor")
def saude() -> Saude:
    return Saude(status="ok", versao_api=VERSAO_API)
