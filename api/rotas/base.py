"""Rotas da base de conhecimento: leitura e validação (4.5.3). Finas: a lógica fica em ``api/servicos``."""
from __future__ import annotations

from fastapi import APIRouter, Depends

from api.contexto import Contexto, obter_contexto
from api.schemas.base import EdicaoBase, ListaVersoes
from api.servicos import base_servico
from kb.grafo import Grafo
from kb.modelos import Base
from kb.validador import Relatorio

router = APIRouter()


@router.get(
    "/base/versoes", operation_id="listar_versoes", response_model=ListaVersoes, summary="Listar versões da base"
)
def listar_versoes(ctx: Contexto = Depends(obter_contexto)) -> ListaVersoes:
    return base_servico.listar_versoes(ctx)


# exclude_none: devolve o arquivo vNNNN.json como foi gravado (o salvar também omite os campos nulos)
@router.get(
    "/base/versoes/{versao}",
    operation_id="obter_versao",
    response_model=Base,
    response_model_exclude_none=True,
    summary="Obter a base de uma versão",
)
def obter_versao(versao: str, ctx: Contexto = Depends(obter_contexto)) -> Base:
    return base_servico.obter_versao(ctx, versao)


@router.get(
    "/base/versoes/{versao}/grafo",
    operation_id="obter_grafo",
    response_model=Grafo,
    summary="Obter a base como grafo para o editor",
)
def obter_grafo(versao: str, ctx: Contexto = Depends(obter_contexto)) -> Grafo:
    return base_servico.obter_grafo(ctx, versao)


@router.post(
    "/base/validar",
    operation_id="validar_base",
    status_code=200,
    response_model=Relatorio,
    summary="Validar uma edição sem salvar",
)
def validar_base(corpo: EdicaoBase, ctx: Contexto = Depends(obter_contexto)) -> Relatorio:
    return base_servico.validar_edicao_base(ctx, corpo)
