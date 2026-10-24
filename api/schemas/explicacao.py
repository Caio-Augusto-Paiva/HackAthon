"""Contrato da explicação (4.5.1): "por quê?", "como?" e o traço bruto de eventos."""
from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field

from api.schemas import CONFIG_RESPOSTA_COMPLETA
from api.schemas.parecer import Gravidade
from api.schemas.sessao import Valor


class ServeA(BaseModel):
    """Uma doença que a pergunta ajuda a confirmar ou afastar."""

    doenca: str
    nome: str
    gravidade: Gravidade
    cf_atual: float = Field(
        description="CF da doença no momento em que a pergunta foi feita (congelado no evento); não acompanha as respostas seguintes."
    )
    regras: list[str]
    sinais: list[str] = Field(default_factory=list, description="Sinais perguntados, em linguagem comum, que aumentam a confiança na doença.")
    sinais_contra: list[str] = Field(default_factory=list, description="Sinais perguntados que diminuem a confiança na doença (regras com CF negativo).")


class PorQue(BaseModel):
    simbolo: str
    origem: Literal["triagem", "fase_dinamica"]
    pergunta: str
    motivo: str
    serve_a: list[ServeA]
    evento_traco: str  # id do evento ``pergunta_feita`` no traço


class Combinacao(BaseModel):
    """O CF do símbolo depois de combinar a saída de uma regra (``antes`` e ``depois``)."""

    apos_regra: str
    antes: float
    depois: float


class Evidencia(BaseModel):
    regra_id: str
    texto: str
    fonte: str | None
    status: Literal["suposicao_a_validar", "validada"]
    premissa: float
    cf_regra: float
    cf_saida: float
    entradas: list[Entrada]
    frase: str = Field(default="", description="As condições da regra em linguagem comum, ligadas por 'e'.")


class Entrada(BaseModel):
    """Um fato que alimentou a regra; com ``origem: "regra"`` traz as ``evidencias`` que o produziram (senão ``null``)."""

    model_config = CONFIG_RESPOSTA_COMPLETA

    simbolo: str
    valor: Valor | None  # None = "não sei"
    cf: float
    origem: Literal["resposta", "ficha", "importacao", "regra"]
    tela_id: str | None
    evidencias: list[Evidencia] | None = None
    nome: str | None = Field(default=None, description="Nome legível do símbolo.")


Evidencia.model_rebuild()


class EtapaExclusao(BaseModel):
    """A doença perdeu força porque outra do mesmo par excludente ficou mais forte (``por``)."""

    tipo: Literal["exclusao"] = "exclusao"
    por: str = Field(description="Id da doença vencedora do par.")
    por_nome: str
    antes: float
    depois: float
    fonte: str | None = None
    nota: str | None = None
    frase: str


class Como(BaseModel):
    simbolo: str
    nome: str
    cf: float
    percentual: int
    combinacao: list[Combinacao]
    exclusoes: list[EtapaExclusao] = Field(default_factory=list)
    evidencias: list[Evidencia]


class Traco(BaseModel):
    """Eventos em ordem: ``fato_adicionado``, ``regra_disparada``, ``cf_combinado`` e ``pergunta_feita``."""

    eventos: list[dict[str, Any]]
