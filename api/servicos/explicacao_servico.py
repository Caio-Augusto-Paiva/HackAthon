"""Parecer, "por quê?", "como?" e traço (4.5.1): a leitura que explica o que o motor decidiu.

Só lê. Cada função restaura a sessão do snapshot e chama o motor; nenhuma decide nada e nenhuma chama LLM (a
explicação vem do traço do motor). Todas passam por ``aplicar(..., muda=False)``: o motor registra a pergunta
apresentada ao calcular o estado (decisão D2) e o snapshot só é regravado se mudou; a ``revisao`` nunca sobe.

O que a API acrescenta ao que o motor devolve:

- parecer: o ``texto`` da urgência no modo da sessão, o ``aviso`` e a ``versao_base`` da sessão (``v0001``, não o
  ``meta.versao`` interno); descarta ``bandeiras`` (já em ``urgencia.regras``);
- "por quê?": a ``pergunta`` de uma pergunta da triagem (o evento da triagem não a traz);
- "como?": o ``texto`` de cada regra (o evento ``regra_disparada`` não o traz) e a origem ``importacao`` no lugar
  de ``ficha`` (decisão D5: o motor só conhece ``ficha``; ``origens_ficha`` diz o que veio do prontuário);
- traço: a mesma troca de origem nos ``fato_adicionado`` e nas ``entradas`` das ``regra_disparada``.
"""
from __future__ import annotations

from collections.abc import Mapping

from api.contexto import Contexto
from api.erros import nao_encontrado, simbolo_invalido
from api.schemas.explicacao import Como, PorQue, Traco
from api.schemas.parecer import Parecer, UrgenciaParecer
from api.schemas.sessao import EstadoSessao
from api.servicos.ficha import mostrar_valor
from api.servicos.sessao_motor import SessaoCarregada, aplicar, carregar
from api.servicos.textos import AVISO_PARECER, TEXTO_URGENCIA, texto_da_regra
from kb.modelos import Regra, Simbolo

TIPOS_COM_COMO = ("doenca", "derivado", "urgencia")  # o que uma regra conclui: o resto é entrada, não conclusão


def _ler(ctx: Contexto, sessao_id: str) -> tuple[SessaoCarregada, EstadoSessao]:
    """A sessão carregada e posta em dia (perguntas apresentadas registradas), sem subir a ``revisao``."""
    carregada = carregar(ctx, sessao_id)
    return carregada, aplicar(ctx, carregada, lambda motor: None, muda=False)


def _simbolo(carregada: SessaoCarregada, id: str) -> Simbolo:
    """O símbolo da base da sessão, ou 404."""
    simbolo = next((s for s in carregada.base.simbolos if s.id == id), None)
    if simbolo is None:
        raise nao_encontrado(f"Símbolo {mostrar_valor(id)} não encontrado.")
    return simbolo


# --- parecer ---------------------------------------------------------------------------------


def obter_parecer(ctx: Contexto, sessao_id: str) -> Parecer:
    """O parecer de agora; ``final`` só se a sessão encerrou (antes disso é o quadro parcial)."""
    carregada, estado = _ler(ctx, sessao_id)
    parecer = carregada.motor.parecer()
    urgencia = estado.urgencia
    return Parecer(
        sessao_id=estado.sessao_id,
        versao_base=estado.versao_base,
        modo=estado.modo,
        final=estado.fase == "encerrada",
        motivo_parada=parecer["motivo_parada"],
        urgencia=UrgenciaParecer(
            nivel=urgencia.nivel,
            origem=urgencia.origem,
            regras=urgencia.regras,
            texto=TEXTO_URGENCIA[(urgencia.nivel, estado.modo)],
        ),
        aviso=AVISO_PARECER,
        blocos=parecer["blocos"],
        inconclusivas=parecer["inconclusivas"],
        bandeiras_nao_verificadas=parecer["bandeiras_nao_verificadas"],
    )


# --- por quê? --------------------------------------------------------------------------------


def obter_porque(ctx: Contexto, sessao_id: str, simbolo: str) -> PorQue:
    """O motivo gravado quando a pergunta foi apresentada (decisão 2 da 4.9): não muda com as correções.

    404 se o símbolo não está na base ou se a pergunta ainda não foi apresentada nesta sessão (a ficha e os
    símbolos que o usuário nunca viu não têm "por quê?").
    """
    carregada = carregar(ctx, sessao_id)
    definicao = _simbolo(carregada, simbolo)
    aplicar(ctx, carregada, lambda motor: None, muda=False)
    motor = carregada.motor
    if simbolo not in motor.perguntas:
        raise nao_encontrado(f"A pergunta {mostrar_valor(simbolo)} ainda não foi apresentada nesta sessão.")
    evento = motor.porque(simbolo)
    # a dinâmica grava a pergunta no evento; a da triagem sai do símbolo, no modo atual
    pergunta = (
        evento.get("pergunta")
        or definicao.pergunta.get(motor.modo)
        or next(iter(definicao.pergunta.values()), definicao.nome)
    )
    return PorQue(
        simbolo=simbolo,
        origem=evento["origem"],
        pergunta=pergunta,
        motivo=evento["motivo"],
        serve_a=evento["serve_a"],
        evento_traco=evento["id"],
    )


# --- como? -----------------------------------------------------------------------------------


def _origem(origem: str, simbolo: str, origens_ficha: Mapping[str, str]) -> str:
    """``importacao`` no lugar de ``ficha`` para o símbolo que veio do prontuário; o resto fica como está.

    Só reescreve ``origem == "ficha"``: depois de corrigir uma tela só de ficha, o fato é ``resposta`` e fica assim.
    """
    return "importacao" if origem == "ficha" and origens_ficha.get(simbolo) == "importacao" else origem


def _completar(
    evidencias: list[dict],
    regras: Mapping[str, Regra],
    simbolos: Mapping[str, Simbolo],
    origens_ficha: Mapping[str, str],
) -> None:
    """Acrescenta o ``texto`` a cada evidência e troca ``ficha`` por ``importacao`` (``_origem``), descendo pelas aninhadas."""
    for evidencia in evidencias:
        regra = regras.get(evidencia["regra_id"])
        evidencia["texto"] = texto_da_regra(regra, simbolos) if regra is not None else evidencia["regra_id"]
        for entrada in evidencia["entradas"]:
            entrada["origem"] = _origem(entrada["origem"], entrada["simbolo"], origens_ficha)
            if entrada.get("evidencias"):
                _completar(entrada["evidencias"], regras, simbolos, origens_ficha)


def obter_como(ctx: Contexto, sessao_id: str, simbolo: str) -> Como:
    """De onde vem o CF de uma doença, de um derivado ou de uma urgência, das regras até as respostas.

    404 se o símbolo não está na base; 422 ``simbolo_invalido`` se não é doença, derivado nem urgência (pergunta e
    ficha são entradas: se explicam por "por quê?", não por "como?").
    """
    carregada = carregar(ctx, sessao_id)
    definicao = _simbolo(carregada, simbolo)
    if definicao.tipo not in TIPOS_COM_COMO:
        raise simbolo_invalido(
            f"O símbolo {mostrar_valor(simbolo)} é {definicao.tipo}: só doença, derivado ou urgência têm \"como?\"."
        )
    aplicar(ctx, carregada, lambda motor: None, muda=False)
    explicacao = carregada.motor.como(simbolo)
    base = carregada.base
    _completar(
        explicacao["evidencias"],
        {r.id: r for r in base.regras},
        {s.id: s for s in base.simbolos},
        carregada.origens_ficha,
    )
    return Como(
        simbolo=explicacao["simbolo"],
        nome=explicacao["nome"],
        cf=explicacao["cf"],
        percentual=explicacao["percentual"],
        combinacao=explicacao["combinacao"],
        evidencias=explicacao["evidencias"],
    )


# --- traço -----------------------------------------------------------------------------------


def obter_traco(ctx: Contexto, sessao_id: str) -> Traco:
    """Os eventos do motor, com a mesma regra de origem do "como?": ``importacao`` no lugar de ``ficha``.

    Vale para os ``fato_adicionado`` e para as ``entradas`` de cada ``regra_disparada``; o resto vai como o motor o gerou.
    """
    carregada, _ = _ler(ctx, sessao_id)
    origens_ficha = carregada.origens_ficha
    eventos = []
    for evento in carregada.motor.traco:
        if evento["tipo"] == "fato_adicionado":
            evento = {**evento, "origem": _origem(evento["origem"], evento["simbolo"], origens_ficha)}
        elif evento["tipo"] == "regra_disparada":
            entradas = [{**e, "origem": _origem(e["origem"], e["simbolo"], origens_ficha)} for e in evento["entradas"]]
            evento = {**evento, "entradas": entradas}
        eventos.append(evento)
    return Traco(eventos=eventos)
