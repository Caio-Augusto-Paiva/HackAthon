"""Contrato das rotas de sessão (4.5.1): ``EstadoSessao`` e os corpos que o cliente envia.

Toda rota de sessão que muda algo devolve o mesmo ``EstadoSessao``; o backend dita a próxima tela
e o frontend só renderiza. Respostas ignoram campo extra (aceitam o dict do motor sem ruído); corpos de
requisição são fechados (``CONFIG_REQUISICAO``).
"""
from __future__ import annotations

from typing import Annotated, Literal, Self

from pydantic import BaseModel, Field, StringConstraints, model_validator

from api.schemas import CONFIG_REQUISICAO, CONFIG_RESPOSTA_COMPLETA
from kb.modelos import Modo

TipoEntrada = Literal["booleano", "categorico", "numerico"]
Fase = Literal["triagem", "dinamica", "encerrada"]
NivelUrgencia = Literal["chamar_agora", "observar", "sem_problema"]
OrigemUrgencia = Literal["padrao", "bandeira_vermelha", "regra_urgencia"]
AcaoDaBandeira = Literal["ver_parecer", "continuar"]
# texto digitado: curto (um número ocupa no máximo 11 caracteres); o motor decide se vale
# float estrito: texto nunca vira número aqui (senão "1"*17 passaria por float); JSON 12 continua valendo
Valor = bool | Annotated[float, Field(strict=True)] | Annotated[str, StringConstraints(max_length=16)]
MAX_SIMBOLOS_POR_TELA = 20


# --- resposta: EstadoSessao ------------------------------------------------------------------

class Opcao(BaseModel):
    valor: str
    rotulo: str


class Campo(BaseModel):
    """Um símbolo de uma tela de triagem. Categórico traz ``opcoes``; numérico, ``unidade``, ``min`` e ``max``.

    Todos os campos vêm sempre na resposta; os que não se aplicam ao tipo de entrada vão como ``null``.
    """

    model_config = CONFIG_RESPOSTA_COMPLETA

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
    """Pergunta da fase dinâmica. ``opcoes``, ``unidade``, ``min`` e ``max`` vêm sempre (``null`` se não se aplicam)."""

    model_config = CONFIG_RESPOSTA_COMPLETA

    tipo: Literal["pergunta"]
    simbolo: str
    entrada: TipoEntrada
    permite_nao_sei: bool
    texto: str
    motivo_resumo: str = Field(
        description="Motivo curto da pergunta, congelado na primeira apresentação: não muda com as respostas seguintes "
        "nem com as correções. O motivo completo (e o que a pergunta serve a confirmar) vem de `GET .../porque/{simbolo}`."
    )
    porque_disponivel: bool
    opcoes: list[Opcao] | None = None
    unidade: str | None = None
    min: float | None = None
    max: float | None = None


class Progresso(BaseModel):
    triagem_respondidas: int
    triagem_total: int
    dinamicas_feitas: int
    limite_dinamico: int | None = Field(
        description="Máximo de perguntas dinâmicas; null no modo especialista, que pergunta até esgotar."
    )


class UrgenciaEstado(BaseModel):
    model_config = CONFIG_RESPOSTA_COMPLETA

    nivel: NivelUrgencia
    provisoria: bool
    origem: OrigemUrgencia
    regras: list[str] = []


class Alerta(BaseModel):
    """Bandeira vermelha. ``pausa`` só é verdadeiro no modo produtor, com bandeira ainda não reconhecida."""

    nivel: Literal["chamar_agora"]
    regras: list[str]
    pausa: bool = Field(
        description="Verdadeiro só no modo produtor, com bandeira ainda não reconhecida: a anamnese fica parada "
        "(`proxima` é null) até `continuar` ou `ver_parecer`. Depois de `ver_parecer` (fase encerrada) vale false."
    )
    acoes: list[AcaoDaBandeira] = Field(
        description="Ações aceitas agora em `POST .../acoes/bandeira`. Com a pausa ativa: `continuar` e `ver_parecer`; "
        "com a sessão já encerrada e a pausa ativa, só `ver_parecer`. Sem pausa (por exemplo, depois de "
        "`ver_parecer`, ou no modo veterinário): `[]`."
    )
    texto: str
    sinais: list[str] = Field(
        default_factory=list,
        description="Condições das bandeiras em linguagem simples (sem repetir), na ordem de `regras`.",
    )


Proxima =Annotated[TelaTriagem | PerguntaDinamica, Field(discriminator="tipo")]


class EstadoSessao(BaseModel):
    sessao_id: str
    animal_id: str
    modo: Modo
    versao_base: str
    revisao: int
    fase: Fase = Field(
        description="`triagem`, `dinamica` ou `encerrada`. Depois de `ver_parecer` a fase é `encerrada` (pausa false, "
        "`alerta.acoes` vazio) e `GET .../parecer` traz `final: true`. `continuar`, a troca de modo (PATCH) e a "
        "correção de uma resposta (PUT) reabrem a sessão (a fase volta a `triagem` ou `dinamica`); uma resposta nova "
        "(POST) a uma sessão encerrada é recusada com 422 `resposta_invalida`."
    )
    progresso: Progresso
    proxima: Proxima | None = Field(
        description="Próxima tela da triagem ou pergunta dinâmica a mostrar. null quando a sessão está encerrada OU "
        "pausada por bandeira vermelha (veja `fase` e `alerta.pausa`): nesse caso mostre o alerta ou o parecer, não uma pergunta."
    )
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

    valores: Annotated[dict[str, Valor], Field(max_length=MAX_SIMBOLOS_POR_TELA)] | None = None
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
