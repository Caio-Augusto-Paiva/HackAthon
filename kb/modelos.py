"""Modelos Pydantic da base de conhecimento e dos casos de teste.

Só estrutura e normalização na carga; as verificações entre referências
(ciclos, símbolos inexistentes, camadas) ficam em ``kb.validador``.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

Modo = Literal["produtor", "veterinario"]
TipoSimbolo = Literal["pergunta", "ficha", "derivado", "doenca", "urgencia"]
Op = Literal["=", "≠", "<", "≤", ">", "≥", "em"]
Classe = Literal["evidencia", "bandeira_vermelha", "urgencia"]

PRIORIDADE_POR_CLASSE: dict[str, int] = {"bandeira_vermelha": 100, "urgencia": 50, "evidencia": 10}
OPERADORES_ASCII: dict[str, str] = {"!=": "≠", "<=": "≤", ">=": "≥"}


class _Modelo(BaseModel):
    model_config = ConfigDict(extra="forbid", allow_inf_nan=False)


# --- símbolos -------------------------------------------------------------

class DominioBooleano(_Modelo):
    tipo: Literal["booleano"] = "booleano"


class DominioCategorico(_Modelo):
    tipo: Literal["categorico"] = "categorico"
    valores: list[str] = Field(min_length=1)


class DominioNumerico(_Modelo):
    tipo: Literal["numerico"] = "numerico"
    min: float | None = None
    max: float | None = None
    unidade: str | None = None


Dominio = Annotated[
    DominioBooleano | DominioCategorico | DominioNumerico, Field(discriminator="tipo")
]


class Simbolo(_Modelo):
    id: str
    tipo: TipoSimbolo
    nome: str
    dominio: Dominio
    pergunta: dict[Modo, str] = Field(default_factory=dict)
    por_que: dict[Modo, str] = Field(default_factory=dict)
    campo_ficha: str | None = None
    fonte: str | None = None
    gravidade: Literal["alta", "media", "baixa"] | None = None
    combinacao: Literal["mycin", "max"] = "mycin"
    nota: str | None = None


# --- regras ---------------------------------------------------------------

class Condicao(_Modelo):
    simbolo: str
    op: Op = "="
    valor: bool | float | str | list[str] | None = True
    negado: bool = False
    cf_minimo: float | None = None
    cf_maximo: float | None = None

    @field_validator("op", mode="before")
    @classmethod
    def _normaliza_operador(cls, valor):
        return OPERADORES_ASCII.get(valor, valor) if isinstance(valor, str) else valor


class Conclusao(_Modelo):
    simbolo: str
    cf: float


class Regra(_Modelo):
    id: str
    se: list[Condicao] = Field(min_length=1)
    entao: Conclusao
    classe: Classe = "evidencia"
    prioridade: int | None = None
    fonte: str | None = None
    status: Literal["suposicao_a_validar", "validada"] = "suposicao_a_validar"
    nota: str | None = None

    @model_validator(mode="after")
    def _prioridade_padrao(self):
        if self.prioridade is None:
            self.prioridade = PRIORIDADE_POR_CLASSE[self.classe]
        return self


# --- meta e base ----------------------------------------------------------

class Tela(_Modelo):
    id: str
    selecao: Literal["unica", "multipla"]
    simbolos: list[str] = Field(min_length=1)
    texto: dict[Modo, str] = Field(default_factory=dict)
    opcoes: dict[str, dict[Modo, str]] = Field(default_factory=dict)
    simbolos_por_modo: dict[Modo, list[str]] | None = None


class Limiares(_Modelo):
    descarte: float = -0.2
    premissa: float = 0.2
    hipotese_relevante: float = 0.35
    exaustao: float = 0.60
    potencial: float = 0.70
    confirmacao: float = 0.80
    bloco_principal: float = 0.50
    bloco_diferencial: float = 0.20


class LimiteDinamico(_Modelo):
    produtor: int = Field(default=12, ge=0)
    veterinario: int = Field(default=25, ge=0)


class Meta(_Modelo):
    versao: str | None = None
    pai: str | None = None
    autor: str | None = None
    data: str | None = None
    nota: str | None = None
    limiares: Limiares = Field(default_factory=Limiares)
    limite_dinamico: LimiteDinamico = Field(default_factory=LimiteDinamico)
    triagem: list[Tela] = Field(default_factory=list)


class Posicao(_Modelo):
    x: float
    y: float


class Base(_Modelo):
    meta: Meta
    simbolos: list[Simbolo]
    regras: list[Regra]
    layout: dict[str, Posicao] = Field(default_factory=dict)


# --- casos de teste -------------------------------------------------------

class Continuacao(_Modelo):
    modo: Modo
    triagem: dict = Field(default_factory=dict)
    respostas: dict = Field(default_factory=dict)


class Alerta(_Modelo):
    pausa: bool


class Esperado(_Modelo):
    urgencia: Literal["chamar_agora", "observar", "sem_problema"] | None = None
    bandeira: str | None = None
    top1: str | None = None
    top3_contem: list[str] | None = None
    faixas: dict[str, tuple[float, float]] = Field(default_factory=dict)
    motivo_parada: str | None = None
    inconclusivas: list[str] | None = None
    alerta: Alerta | None = None


class Caso(_Modelo):
    id: str
    descricao: str
    modo: Modo
    ficha: dict = Field(default_factory=dict)
    triagem: dict = Field(default_factory=dict)
    respostas: dict = Field(default_factory=dict)
    continuacao: Continuacao | None = None
    limite_dinamico: int | None = None
    esperado: Esperado


# --- carga ----------------------------------------------------------------

def carregar_base(dados: dict | str | Path) -> Base:
    """Carrega uma base de um dict, de um texto JSON ou de um caminho ``.json`` (UTF-8).

    Atenção: um ``str`` que não começa com ``{`` é tratado como **caminho de arquivo**.
    Nunca passe texto vindo de requisição não confiável; use ``validar_dados`` com o
    JSON já decodificado (dict).
    """
    if isinstance(dados, Path):
        dados = json.loads(dados.read_text(encoding="utf-8"))
    elif isinstance(dados, str):
        if dados.lstrip().startswith("{"):
            dados = json.loads(dados)
        else:
            dados = json.loads(Path(dados).read_text(encoding="utf-8"))
    return Base.model_validate(dados)


def para_motor(base: Base) -> dict:
    """Dict que o motor (``engine.modelos.Base.de_dict``) aceita.

    ``exclude_none=True`` é obrigatório: o motor rejeita ``cf_minimo: null``.
    """
    return base.model_dump(mode="json", exclude_none=True)
