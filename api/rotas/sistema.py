"""Rotas de sistema."""
from __future__ import annotations

from fastapi import APIRouter

from api.config import VERSAO_API
from api.schemas.sistema import Saude

router = APIRouter()


@router.get("/saude", operation_id="saude", summary="Saúde do servidor")
def saude() -> Saude:
    return Saude(status="ok", versao_api=VERSAO_API)
