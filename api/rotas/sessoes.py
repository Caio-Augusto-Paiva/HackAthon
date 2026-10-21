"""Rotas de sessão (4.5.1). Finas: a lógica fica em ``api/servicos``."""
from __future__ import annotations

from fastapi import APIRouter, Depends

from api.contexto import Contexto, obter_contexto
from api.rotas.respostas import ERROS_DE_CONFLITO, ERROS_DE_RECURSO
from api.schemas.explicacao import Como, PorQue, Traco
from api.schemas.parecer import Parecer
from api.schemas.sessao import (
    AcaoBandeira,
    CorrecaoPergunta,
    EstadoSessao,
    NovaSessao,
    RespostaPergunta,
    RespostaTriagem,
    TrocaModo,
)
from api.servicos import explicacao_servico, sessao_servico

router = APIRouter()


@router.post(
    "/sessoes",
    operation_id="criar_sessao",
    status_code=201,
    responses=ERROS_DE_CONFLITO,
    response_model=EstadoSessao,
    summary="Iniciar anamnese",
)
def criar_sessao(corpo: NovaSessao, ctx: Contexto = Depends(obter_contexto)) -> EstadoSessao:
    return sessao_servico.criar_sessao(ctx, corpo)


@router.get(
    "/sessoes/{sessao_id}",
    operation_id="obter_sessao",
    responses=ERROS_DE_RECURSO,
    response_model=EstadoSessao,
    summary="Estado da anamnese",
)
def obter_sessao(sessao_id: str, ctx: Contexto = Depends(obter_contexto)) -> EstadoSessao:
    return sessao_servico.obter_estado(ctx, sessao_id)


@router.patch(
    "/sessoes/{sessao_id}",
    operation_id="trocar_modo",
    responses=ERROS_DE_RECURSO,
    response_model=EstadoSessao,
    summary="Trocar o modo da anamnese",
)
def trocar_modo(sessao_id: str, corpo: TrocaModo, ctx: Contexto = Depends(obter_contexto)) -> EstadoSessao:
    return sessao_servico.trocar_modo(ctx, sessao_id, corpo.modo)


@router.post(
    "/sessoes/{sessao_id}/triagem/{tela_id}",
    operation_id="responder_triagem",
    responses=ERROS_DE_CONFLITO,
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
    responses=ERROS_DE_CONFLITO,
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
    responses=ERROS_DE_CONFLITO,
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
    responses=ERROS_DE_CONFLITO,
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
    responses=ERROS_DE_RECURSO,
    response_model=EstadoSessao,
    summary="Continuar a anamnese ou ver o parecer após a bandeira vermelha",
)
def acao_bandeira(sessao_id: str, corpo: AcaoBandeira, ctx: Contexto = Depends(obter_contexto)) -> EstadoSessao:
    return sessao_servico.acao_bandeira(ctx, sessao_id, corpo.acao)


@router.get(
    "/sessoes/{sessao_id}/parecer",
    operation_id="obter_parecer",
    responses=ERROS_DE_RECURSO,
    response_model=Parecer,
    summary="Parecer (parcial se a anamnese não encerrou)",
)
def obter_parecer(sessao_id: str, ctx: Contexto = Depends(obter_contexto)) -> Parecer:
    return explicacao_servico.obter_parecer(ctx, sessao_id)


@router.get(
    "/sessoes/{sessao_id}/porque/{simbolo}",
    operation_id="obter_porque",
    responses=ERROS_DE_RECURSO,
    response_model=PorQue,
    summary='"Por quê?" de uma pergunta já apresentada',
)
def obter_porque(sessao_id: str, simbolo: str, ctx: Contexto = Depends(obter_contexto)) -> PorQue:
    return explicacao_servico.obter_porque(ctx, sessao_id, simbolo)


@router.get(
    "/sessoes/{sessao_id}/como/{simbolo}",
    operation_id="obter_como",
    responses=ERROS_DE_RECURSO,
    response_model=Como,
    summary='"Como?" de uma doença, derivado ou urgência',
)
def obter_como(sessao_id: str, simbolo: str, ctx: Contexto = Depends(obter_contexto)) -> Como:
    return explicacao_servico.obter_como(ctx, sessao_id, simbolo)


@router.get(
    "/sessoes/{sessao_id}/traco",
    operation_id="obter_traco",
    responses=ERROS_DE_RECURSO,
    response_model=Traco,
    summary="Traço de inferência da sessão",
)
def obter_traco(sessao_id: str, ctx: Contexto = Depends(obter_contexto)) -> Traco:
    return explicacao_servico.obter_traco(ctx, sessao_id)
