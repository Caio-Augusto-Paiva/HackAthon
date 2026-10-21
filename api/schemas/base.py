"""Contrato da base de conhecimento (4.5.3): versões, edição, execução dos casos e ativação.

``obter_versao``, ``obter_grafo`` e ``validar_base`` respondem com os modelos do ``kb`` (``Base``,
``Grafo`` e ``Relatorio``); ver ``api.schemas.registro``.
"""
from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field

from api.schemas import CONFIG_REQUISICAO
from kb.validador import Relatorio

StatusCaso = Literal["passou", "falhou", "erro"]
StatusNaComparacao = Literal["passou", "falhou", "erro", "ausente"]  # "ausente": o caso não existia na versão pai


class UltimaExecucao(BaseModel):
    execucao_id: str
    passou: int
    falhou: int


class VersaoItem(BaseModel):
    versao: str
    pai: str | None
    autor: str | None
    data: str | None
    nota: str | None
    simbolos: int
    regras: int
    suposicao_a_validar: int
    ultima_execucao: UltimaExecucao | None


class ListaVersoes(BaseModel):
    ativa: str | None
    itens: list[VersaoItem]


# --- edição (corpo de validar e de salvar) -------------------------------------------------

class GrafoEdicao(BaseModel):
    """Nós e arestas como dicts soltos: erro de estrutura chega ao ``kb`` e volta como ``E00`` (decisão D4)."""

    model_config = CONFIG_REQUISICAO

    nos: list[dict[str, Any]]
    arestas: list[dict[str, Any]]


class EdicaoBase(BaseModel):
    model_config = CONFIG_REQUISICAO

    pai: str | None
    nota: str
    meta: dict[str, Any]
    grafo: GrafoEdicao
    layout: dict[str, Any] = Field(default_factory=dict)


# --- execução dos casos de teste -----------------------------------------------------------

class ExecucaoResumo(BaseModel):
    execucao_id: str
    total: int
    passou: int
    falhou: int


class Mudanca(BaseModel):
    caso_id: str
    antes: StatusNaComparacao
    depois: StatusNaComparacao


class SalvarResposta(BaseModel):
    versao: str
    pai: str | None
    hash: str
    validacao: Relatorio
    execucao_nova: ExecucaoResumo
    execucao_pai: ExecucaoResumo | None = None  # None se a versão pai nunca foi executada
    mudancas: list[Mudanca]


class AtivarBody(BaseModel):
    model_config = CONFIG_REQUISICAO

    versao: str
    confirmar_falhas: bool = False


class AtivarResposta(BaseModel):
    versao: str
    anterior: str | None


class ExecutarBody(BaseModel):
    model_config = CONFIG_REQUISICAO

    casos: list[str] | None = None  # None = todos


class FalhaCaso(BaseModel):
    campo: str
    esperado: Any
    obtido: Any


class ResultadoCaso(BaseModel):
    caso_id: str
    descricao: str
    status: StatusCaso
    mudou_vs_pai: str | None = None  # "antes->depois" só quando difere do pai
    falhas: list[FalhaCaso]
    obtido: dict[str, Any] | None = None
    erro: str | None = None  # caso mal formado: status "erro"


class ExecucaoCabecalho(BaseModel):
    execucao_id: str
    executada_em: str  # ISO-8601
    total: int
    passou: int
    falhou: int


class Execucao(BaseModel):
    execucao_id: str
    versao: str
    executada_em: str
    total: int
    passou: int
    falhou: int
    comparada_com: str | None
    resultados: list[ResultadoCaso]
    mudancas: list[Mudanca]


class ListaExecucoes(BaseModel):
    itens: list[ExecucaoCabecalho]
