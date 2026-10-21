"""Contrato do parecer (4.5.1): urgência, blocos de doenças e aviso de que a porcentagem não é probabilidade."""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel

from api.schemas.sessao import NivelUrgencia, OrigemUrgencia
from kb.modelos import Modo

Gravidade = Literal["alta", "media", "baixa"]
Situacao = Literal["com_evidencia", "sem_evidencia", "descartada"]
MotivoParada = Literal["confirmacao", "sem_perguntas", "limite", "sem_potencial"]


class UrgenciaParecer(BaseModel):
    nivel: NivelUrgencia
    origem: OrigemUrgencia
    regras: list[str]
    texto: str


class ItemDoenca(BaseModel):
    """``situacao``: ``com_evidencia`` (CF > 0,2), ``sem_evidencia`` (-0,2 a 0,2) ou ``descartada`` (CF < -0,2)."""

    doenca: str
    nome: str
    gravidade: Gravidade
    cf: float
    percentual: int  # round(max(0, cf) * 100): grau de confiança do sistema, não probabilidade
    situacao: Situacao


class Bloco(BaseModel):
    id: Literal["hipoteses_principais", "diagnostico_diferencial", "pouco_provavel"]
    titulo: str
    itens: list[ItemDoenca]


class Parecer(BaseModel):
    sessao_id: str
    versao_base: str
    modo: Modo
    final: bool  # False se a sessão ainda não encerrou
    motivo_parada: MotivoParada | None
    urgencia: UrgenciaParecer
    aviso: str
    blocos: list[Bloco]
    inconclusivas: list[str]
    bandeiras_nao_verificadas: list[str]
