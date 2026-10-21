"""Rotas de sessão (4.5.1). Finas: a lógica fica em ``api/servicos``."""
from __future__ import annotations

from fastapi import APIRouter, Depends

from api.contexto import Contexto, obter_contexto
from api.schemas.sessao import EstadoSessao, NovaSessao
from api.servicos import sessao_servico

router = APIRouter()


@router.post(
    "/sessoes", operation_id="criar_sessao", status_code=201, response_model=EstadoSessao, summary="Iniciar anamnese"
)
def criar_sessao(corpo: NovaSessao, ctx: Contexto = Depends(obter_contexto)) -> EstadoSessao:
    return sessao_servico.criar_sessao(ctx, corpo)


@router.get(
    "/sessoes/{sessao_id}", operation_id="obter_sessao", response_model=EstadoSessao, summary="Estado da anamnese"
)
def obter_sessao(sessao_id: str, ctx: Contexto = Depends(obter_contexto)) -> EstadoSessao:
    return sessao_servico.obter_estado(ctx, sessao_id)
