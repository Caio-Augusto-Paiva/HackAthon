"""Contrato do parecer (4.5.1): urgência, blocos de doenças e aviso de que a porcentagem não é probabilidade."""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

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
    potencial: int = Field(ge=0, le=100, description="Teto de confiança que a doença ainda pode alcançar com mais respostas (>= percentual).")
    situacao: Situacao


class Bloco(BaseModel):
    id: Literal["hipoteses_principais", "diagnostico_diferencial", "pouco_provavel"]
    titulo: str
    itens: list[ItemDoenca]


class Parecer(BaseModel):
    sessao_id: str
    versao_base: str
    modo: Modo
    final: bool = Field(
        description="Verdadeiro se a sessão está encerrada; false é o quadro parcial. Depois de `ver_parecer` `final` "
        "é true com `motivo_parada` null (a anamnese foi encerrada pelo usuário, não por uma regra de parada)."
    )
    motivo_parada: MotivoParada | None = Field(
        description="Por que o motor parou (`confirmacao`, `sem_perguntas`, `limite`, `sem_potencial`). null enquanto a "
        "sessão está aberta e também depois de `ver_parecer`, mesmo com `final: true`."
    )
    urgencia: UrgenciaParecer
    aviso: str
    blocos: list[Bloco]
    inconclusivas: list[str]
    bandeiras_nao_verificadas: list[str]
