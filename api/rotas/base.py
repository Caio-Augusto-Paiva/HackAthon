"""Rotas da base: leitura, validação, salvar, ativar e execução dos casos (4.5.3). Finas: a lógica fica em ``api/servicos``."""
from __future__ import annotations

from fastapi import APIRouter, Depends

from api.contexto import Contexto, obter_contexto
from api.schemas.base import (
    AtivarBody,
    AtivarResposta,
    EdicaoBase,
    Execucao,
    ExecutarBody,
    ListaExecucoes,
    ListaVersoes,
    SalvarResposta,
)
from api.servicos import base_servico, casos_servico
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


@router.post(
    "/base/versoes",
    operation_id="salvar_versao",
    status_code=201,
    response_model=SalvarResposta,
    summary="Salvar uma nova versão da base",
)
def salvar_versao(corpo: EdicaoBase, ctx: Contexto = Depends(obter_contexto)) -> SalvarResposta:
    """Grava a próxima versão (`vNNNN`) a partir do grafo editado, sem ativá-la, e roda os casos nela e no pai.

    Com erro de validação (inclusive estrutura quebrada): 422 `base_invalida`, com os erros em `detalhes`, e nada
    é gravado. `pai` nulo vale a versão ativa; um `pai` que não existe é 404 `nao_encontrado`. O pai só é executado
    se ainda não tem execução. `mudancas` lista os casos cujo status mudou em relação ao pai. Se outra gravação
    criou a mesma versão ao mesmo tempo: 409 `conflito`, sem sobrescrever nada. O autor da versão é sempre
    `equipe` (suposição: não há login).
    """
    return base_servico.salvar_versao(ctx, corpo)


@router.put(
    "/base/ativa",
    operation_id="ativar_versao",
    status_code=200,
    response_model=AtivarResposta,
    summary="Ativar uma versão da base",
)
def ativar_versao(corpo: AtivarBody, ctx: Contexto = Depends(obter_contexto)) -> AtivarResposta:
    """Aponta a base ativa para a versão e devolve a que estava ativa (`anterior`).

    Sessões em andamento continuam na versão em que nasceram; só as novas usam a ativa. Se a última execução da
    versão tem caso que falhou ou deu erro e `confirmar_falhas` não é `true`: 409 `casos_falhando`. Versão que nunca
    foi executada ativa sem confirmação. Versão inexistente: 404 `nao_encontrado`.
    """
    return base_servico.ativar_versao(ctx, corpo)


@router.post(
    "/base/versoes/{versao}/execucoes",
    operation_id="executar_casos",
    status_code=201,
    response_model=Execucao,
    summary="Executar os casos de teste numa versão",
)
def executar_casos(versao: str, corpo: ExecutarBody, ctx: Contexto = Depends(obter_contexto)) -> Execucao:
    """Roda os casos (`casos: null` = todos) na versão, grava a execução e a compara com a do pai.

    Um caso mal formado ou recusado pelo motor vira resultado `erro`; os outros seguem. Versão ou id de caso
    inexistente é 404 `nao_encontrado` (nada é gravado).
    """
    return casos_servico.executar(ctx, versao, corpo.casos)


@router.get(
    "/base/versoes/{versao}/execucoes",
    operation_id="listar_execucoes",
    response_model=ListaExecucoes,
    summary="Listar as execuções de uma versão",
)
def listar_execucoes(versao: str, ctx: Contexto = Depends(obter_contexto)) -> ListaExecucoes:
    return casos_servico.listar_execucoes(ctx, versao)


@router.get(
    "/base/versoes/{versao}/execucoes/{execucao_id}",
    operation_id="obter_execucao",
    response_model=Execucao,
    summary="Obter uma execução dos casos",
)
def obter_execucao(versao: str, execucao_id: str, ctx: Contexto = Depends(obter_contexto)) -> Execucao:
    return casos_servico.obter_execucao(ctx, versao, execucao_id)
