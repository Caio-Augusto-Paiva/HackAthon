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


# exclude_unset (não exclude_none): cada aresta traz só os campos do seu papel, como no exemplo, e um
# `"valor": null` que o kb informou de propósito numa condição continua na resposta (nulo ≠ padrão verdadeiro)
@router.get(
    "/base/versoes/{versao}/grafo",
    operation_id="obter_grafo",
    response_model=Grafo,
    response_model_exclude_unset=True,
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
    """Valida uma edição (grafo, meta e layout) sem gravar nada.

    Responde sempre 200 com o relatório, inclusive quando a estrutura está quebrada (erro `E00`, `estrutura`).
    A única exceção é texto com surrogate Unicode solto (como `\\ud800`), que a resposta não conseguiria
    codificar: vira 422 `entrada_invalida`. Corpo que não é um objeto, ou fora do formato de `EdicaoBase`,
    também é 422 `entrada_invalida`.
    """
    return base_servico.validar_edicao_base(ctx, corpo)
