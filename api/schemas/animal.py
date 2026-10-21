"""Contrato de animais, ficha e importação de prontuário (4.5.2). Dados fictícios apenas."""
from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field

from api.schemas import CONFIG_REQUISICAO
from api.schemas.sessao import Fase, NivelUrgencia
from kb.modelos import Modo


class AnimalResumo(BaseModel):
    id: str
    brinco: str
    nome: str | None  # a importação aceita linha sem nome
    dias_em_lactacao: int | None  # calculado de data_ultimo_parto; None se ausente ou inválida
    ultima_sessao_id: str | None


class ListaAnimais(BaseModel):
    total: int
    itens: list[AnimalResumo]


class NovoAnimal(BaseModel):
    model_config = CONFIG_REQUISICAO

    brinco: str = Field(min_length=1)
    nome: str
    ficha: dict[str, Any] = {}


class Animal(BaseModel):
    """A ficha completa. ``origens`` marca por campo ``manual`` ou ``importacao``; campo ``null`` = ausente."""

    id: str
    brinco: str
    nome: str | None
    dias_em_lactacao: int | None
    ficha: dict[str, Any]
    origens: dict[str, Literal["manual", "importacao"]]


class SessaoDoAnimal(BaseModel):
    sessao_id: str
    modo: Modo
    versao_base: str
    fase: Fase
    urgencia: NivelUrgencia
    top1: str | None
    criada_em: str  # ISO-8601


class ListaSessoesAnimal(BaseModel):
    itens: list[SessaoDoAnimal]


# --- importação de prontuário --------------------------------------------------------------

class LinhaImportada(BaseModel):
    linha: int
    brinco: str


class LinhaAtualizada(BaseModel):
    linha: int
    brinco: str
    campos: list[str]  # campos cujo valor mudou


class ErroCampo(BaseModel):
    campo: str
    mensagem: str


class LinhaRejeitada(BaseModel):
    linha: int
    erros: list[ErroCampo]


class ResultadoImportacao(BaseModel):
    """``gravado: false`` quando só simulou (``?gravar=false``)."""

    formato: Literal["csv", "json"]
    gravado: bool
    criados: list[LinhaImportada]
    atualizados: list[LinhaAtualizada]
    rejeitados: list[LinhaRejeitada]
