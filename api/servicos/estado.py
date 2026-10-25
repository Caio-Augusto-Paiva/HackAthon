"""Adaptação de ``Sessao.estado()`` (motor) ao ``EstadoSessao`` do contrato 4.5.1.

Só traduz o que o motor já decidiu: nome de campos, rótulos da tela, tipos de entrada e textos. Não decide nada
(a próxima tela ou pergunta, a urgência e a pausa vêm do motor) e não toca banco.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from api.schemas.sessao import (
    Alerta,
    Campo,
    EstadoSessao,
    Opcao,
    PerguntaDinamica,
    Progresso,
    TelaTriagem,
    UrgenciaEstado,
)
from api.servicos.textos import TEXTO_ALERTA, sinais_das_regras
from kb.modelos import DominioCategorico, DominioNumerico, Simbolo, Tela

if TYPE_CHECKING:  # só anotação (e, para SessaoCarregada, um import real seria circular)
    from api.servicos.sessao_motor import SessaoCarregada
    from engine.sessao import Sessao


def _entrada(simbolo: Simbolo, tela: Tela | None, modo: str) -> dict:
    """O ``entrada`` do símbolo e o que o domínio acrescenta: ``opcoes`` (categórico) ou ``unidade``/``min``/``max``.

    O rótulo de uma opção vem de ``tela.opcoes["<simbolo>.<valor>"][modo]``; sem ele (ou sem tela, na fase
    dinâmica) o rótulo é o próprio valor.
    """
    dominio = simbolo.dominio
    dados: dict = {"entrada": dominio.tipo}
    if isinstance(dominio, DominioCategorico):
        rotulos = tela.opcoes if tela is not None else {}
        dados["opcoes"] = [
            Opcao(valor=valor, rotulo=rotulos.get(f"{simbolo.id}.{valor}", {}).get(modo) or valor)
            for valor in dominio.valores
        ]
    elif isinstance(dominio, DominioNumerico):
        dados.update(unidade=dominio.unidade, min=dominio.min, max=dominio.max)
    return dados


def _tela(carregada: SessaoCarregada, proxima: dict, modo: str) -> TelaTriagem:
    base = carregada.base
    simbolos = {s.id: s for s in base.simbolos}
    tela = next(t for t in base.meta.triagem if t.id == proxima["id"])
    campos = [
        Campo(
            simbolo=id,
            rotulo=tela.opcoes.get(id, {}).get(modo) or simbolos[id].nome,
            **_entrada(simbolos[id], tela, modo),
        )
        for id in proxima["simbolos"]
    ]
    return TelaTriagem(
        tipo="tela_triagem",
        tela_id=tela.id,
        selecao=proxima["selecao"],
        permite_nao_sei=True,  # (suposição) toda tela aceita "não sei"
        titulo=proxima["texto"],
        campos=campos,
    )


def _pergunta(carregada: SessaoCarregada, proxima: dict, modo: str) -> PerguntaDinamica:
    simbolo = next(s for s in carregada.base.simbolos if s.id == proxima["id"])
    return PerguntaDinamica(
        tipo="pergunta",
        simbolo=simbolo.id,
        permite_nao_sei=True,  # (suposição) toda pergunta aceita "não sei"
        texto=proxima["pergunta"],
        motivo_resumo=carregada.motor.perguntas[simbolo.id]["motivo"],
        porque_disponivel=True,
        **_entrada(simbolo, None, modo),
    )


def origem_urgencia(motor: Sessao, estado: dict) -> tuple[str, list[str]]:
    """``(origem, regras)`` da urgência do estado do motor.

    ``bandeira_vermelha``: as bandeiras travadas. ``regra_urgencia``: as regras de urgência que concluíram o nível.
    ``padrao``: nenhuma regra (``sem_problema``, ou ``observar`` só porque há hipótese acima do limiar).
    """
    if estado["bandeiras"]:
        return "bandeira_vermelha", list(estado["bandeiras"])
    nivel = estado["urgencia"]
    regras = [] if nivel == "sem_problema" else [e["regra_id"] for e in motor.como(nivel)["evidencias"]]
    return ("regra_urgencia" if regras else "padrao"), regras


def montar_estado(carregada: SessaoCarregada, revisao: int) -> EstadoSessao:
    """O ``EstadoSessao`` da sessão carregada, com a ``revisao`` que o chamador gravou ou leu."""
    motor, base = carregada.motor, carregada.base
    estado = motor.estado()
    modo = estado["modo"]
    proxima = estado["proxima"]
    if proxima is None:
        tela_ou_pergunta = None
    elif proxima["tipo"] == "tela_triagem":
        tela_ou_pergunta = _tela(carregada, proxima, modo)
    else:
        tela_ou_pergunta = _pergunta(carregada, proxima, modo)

    progresso = estado["progresso"]
    limite = motor.limite_dinamico if motor.limite_dinamico is not None else getattr(base.meta.limite_dinamico, modo)
    origem, regras = origem_urgencia(motor, estado)
    alerta = None
    if estado["bandeiras"]:
        pausa = estado["pausa"]
        # pausada com a sessão já encerrada (o motor não tem mais o que perguntar): só resta ver o parecer
        acoes = (["ver_parecer"] if estado["fase"] == "encerrada" else ["ver_parecer", "continuar"]) if pausa else []
        alerta = Alerta(
            nivel="chamar_agora",
            regras=list(estado["bandeiras"]),
            pausa=pausa,
            acoes=acoes,
            texto=TEXTO_ALERTA[modo],
            sinais=sinais_das_regras(base, estado["bandeiras"]),
        )
    return EstadoSessao(
        sessao_id=carregada.linha["id"],
        animal_id=carregada.linha["animal_id"],
        modo=modo,
        versao_base=carregada.linha["versao_base"],
        revisao=revisao,
        fase=estado["fase"],
        progresso=Progresso(
            triagem_respondidas=progresso["triagem_respondida"],
            triagem_total=progresso["triagem_total"],
            dinamicas_feitas=progresso["dinamicas_respondidas"],
            limite_dinamico=limite,
        ),
        proxima=tela_ou_pergunta,
        urgencia=UrgenciaEstado(
            nivel=estado["urgencia"], provisoria=estado["fase"] != "encerrada", origem=origem, regras=regras
        ),
        alerta=alerta,
    )
