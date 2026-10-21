"""Contrato das rotas de sessão (4.5.1): ``EstadoSessao`` e os corpos que o cliente envia.

Toda rota de sessão que muda algo devolve o mesmo ``EstadoSessao``; o backend dita a próxima tela
e o frontend só renderiza. Respostas ignoram campo extra (aceitam o dict do motor sem ruído); corpos de
requisição são fechados (``CONFIG_REQUISICAO``).
"""
from __future__ import annotations

from typing import Annotated, Literal, Self

from pydantic import BaseModel, Field, model_validator

from api.schemas import CONFIG_REQUISICAO
from kb.modelos import Modo

TipoEntrada = Literal["booleano", "categorico", "numerico"]
Fase = Literal["triagem", "dinamica", "encerrada"]
NivelUrgencia = Literal["chamar_agora", "observar", "sem_problema"]
OrigemUrgencia = Literal["padrao", "bandeira_vermelha", "regra_urgencia"]
AcaoDaBandeira = Literal["ver_parecer", "continuar"]
Valor = bool | float | str


# --- resposta: EstadoSessao ------------------------------------------------------------------

class Opcao(BaseModel):
    valor: str
    rotulo: str


class Campo(BaseModel):
    """Um símbolo de uma tela de triagem. Categórico traz ``opcoes``; numérico, ``unidade``, ``min`` e ``max``."""

    simbolo: str
    entrada: TipoEntrada
    rotulo: str | None = None
    opcoes: list[Opcao] | None = None
    unidade: str | None = None
    min: float | None = None
    max: float | None = None


class TelaTriagem(BaseModel):
    tipo: Literal["tela_triagem"]
    tela_id: str
    selecao: Literal["unica", "multipla"]
    permite_nao_sei: bool
    titulo: str
    campos: list[Campo]


class PerguntaDinamica(BaseModel):
    tipo: Literal["pergunta"]
    simbolo: str
    entrada: TipoEntrada
    permite_nao_sei: bool
    texto: str
    motivo_resumo: str
    porque_disponivel: bool
    opcoes: list[Opcao] | None = None
    unidade: str | None = None
    min: float | None = None
    max: float | None = None


class Progresso(BaseModel):
    triagem_respondidas: int
    triagem_total: int
    dinamicas_feitas: int
    limite_dinamico: int


class UrgenciaEstado(BaseModel):
    nivel: NivelUrgencia
    provisoria: bool
    origem: OrigemUrgencia
    regras: list[str] = []


class Alerta(BaseModel):
    """Bandeira vermelha. ``pausa`` só é verdadeiro no modo produtor, com bandeira ainda não reconhecida."""

    nivel: Literal["chamar_agora"]
    regras: list[str]
    pausa: bool
    acoes: list[AcaoDaBandeira]
    texto: str


Proxima = Annotated[TelaTriagem | PerguntaDinamica, Field(discriminator="tipo")]


class EstadoSessao(BaseModel):
    sessao_id: str
    animal_id: str
    modo: Modo
    versao_base: str
    revisao: int
    fase: Fase
    progresso: Progresso
    proxima: Proxima | None  # None = sessão encerrada ou pausada pela bandeira
    urgencia: UrgenciaEstado
    alerta: Alerta | None


# --- requisições ---------------------------------------------------------------------------

class NovaSessao(BaseModel):
    model_config = CONFIG_REQUISICAO

    animal_id: str
    modo: Modo
    versao_base: str | None = None  # None = a versão ativa


class TrocaModo(BaseModel):
    model_config = CONFIG_REQUISICAO

    modo: Modo


class RespostaTriagem(BaseModel):
    """Resposta a uma tela da triagem: os ``valores`` por símbolo ou ``nao_sei``, nunca os dois nem nenhum."""

    model_config = CONFIG_REQUISICAO

    valores: dict[str, Valor] | None = None
    nao_sei: bool = False

    @model_validator(mode="after")
    def _valores_ou_nao_sei(self) -> Self:
        if self.valores is None and not self.nao_sei:
            raise ValueError("Informe os valores da tela ou marque não sei.")
        if self.valores is not None and self.nao_sei:
            raise ValueError("Informe os valores ou marque não sei, não os dois.")
        return self


class _ValorOuNaoSei(BaseModel):
    """O valor da resposta ou ``nao_sei``, nunca os dois nem nenhum (``False`` e ``0`` são valores)."""

    model_config = CONFIG_REQUISICAO

    valor: Valor | None = None
    nao_sei: bool = False

    @model_validator(mode="after")
    def _valor_ou_nao_sei(self) -> Self:
        if self.valor is None and not self.nao_sei:
            raise ValueError("Informe o valor ou marque não sei.")
        if self.valor is not None and self.nao_sei:
            raise ValueError("Informe o valor ou marque não sei, não os dois.")
        return self


class RespostaPergunta(_ValorOuNaoSei):
    """Corpo do ``POST /respostas``: o ``simbolo`` respondido e o valor ou ``nao_sei``."""

    simbolo: str


class CorrecaoPergunta(_ValorOuNaoSei):
    """Corpo do ``PUT /respostas/{simbolo}``: o símbolo vai na rota."""


class AcaoBandeira(BaseModel):
    model_config = CONFIG_REQUISICAO

    acao: AcaoDaBandeira
