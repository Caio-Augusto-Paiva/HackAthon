"""Rotas de sessão (4.5.1). Finas: a lógica fica em ``api/servicos``."""
from __future__ import annotations

from fastapi import APIRouter, Depends

from api.contexto import Contexto, obter_contexto
from api.schemas.sessao import (
    AcaoBandeira,
    CorrecaoPergunta,
    EstadoSessao,
    NovaSessao,
    RespostaPergunta,
    RespostaTriagem,
    TrocaModo,
)
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


@router.patch(
    "/sessoes/{sessao_id}", operation_id="trocar_modo", response_model=EstadoSessao, summary="Trocar o modo da anamnese"
)
def trocar_modo(sessao_id: str, corpo: TrocaModo, ctx: Contexto = Depends(obter_contexto)) -> EstadoSessao:
    return sessao_servico.trocar_modo(ctx, sessao_id, corpo.modo)


@router.post(
    "/sessoes/{sessao_id}/triagem/{tela_id}",
    operation_id="responder_triagem",
    response_model=EstadoSessao,
    summary="Responder uma tela da triagem",
)
def responder_triagem(
    sessao_id: str, tela_id: str, corpo: RespostaTriagem, ctx: Contexto = Depends(obter_contexto)
) -> EstadoSessao:
    return sessao_servico.responder_triagem(ctx, sessao_id, tela_id, corpo, corrigir=False)


@router.put(
    "/sessoes/{sessao_id}/triagem/{tela_id}",
    operation_id="corrigir_triagem",
    response_model=EstadoSessao,
    summary="Corrigir uma tela já respondida",
)
def corrigir_triagem(
    sessao_id: str, tela_id: str, corpo: RespostaTriagem, ctx: Contexto = Depends(obter_contexto)
) -> EstadoSessao:
    return sessao_servico.responder_triagem(ctx, sessao_id, tela_id, corpo, corrigir=True)


@router.post(
    "/sessoes/{sessao_id}/respostas",
    operation_id="responder_pergunta",
    response_model=EstadoSessao,
    summary="Responder a pergunta dinâmica da vez",
)
def responder_pergunta(
    sessao_id: str, corpo: RespostaPergunta, ctx: Contexto = Depends(obter_contexto)
) -> EstadoSessao:
    return sessao_servico.responder_pergunta(ctx, sessao_id, corpo.simbolo, corpo, corrigir=False)


@router.put(
    "/sessoes/{sessao_id}/respostas/{simbolo}",
    operation_id="corrigir_resposta",
    response_model=EstadoSessao,
    summary="Corrigir uma pergunta dinâmica já respondida",
)
def corrigir_resposta(
    sessao_id: str, simbolo: str, corpo: CorrecaoPergunta, ctx: Contexto = Depends(obter_contexto)
) -> EstadoSessao:
    return sessao_servico.responder_pergunta(ctx, sessao_id, simbolo, corpo, corrigir=True)


@router.post(
    "/sessoes/{sessao_id}/acoes/bandeira",
    operation_id="acao_bandeira",
    response_model=EstadoSessao,
    summary="Continuar a anamnese ou ver o parecer após a bandeira vermelha",
)
def acao_bandeira(sessao_id: str, corpo: AcaoBandeira, ctx: Contexto = Depends(obter_contexto)) -> EstadoSessao:
    return sessao_servico.acao_bandeira(ctx, sessao_id, corpo.acao)
