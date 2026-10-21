"""Ponte entre o banco e o motor: restaurar a sessão do snapshot, aplicar uma ação e gravar de volta.

O motor não guarda estado entre requisições. ``sessoes.snapshot_json`` (decisão D1) é a fonte da verdade:

    {"motor": Sessao.exportar(), "origens_ficha": {id_do_simbolo: "manual" | "importacao"},
     "resumo": {"urgencia": nivel, "top1": doenca | None}}

``resumo`` é o que o histórico do animal mostra, sem rodar o motor. As tabelas ``respostas`` e ``perguntas_feitas``
e as colunas ``fase``, ``motivo_parada``, ``modo`` e ``bandeiras_reconhecidas_json`` são projeção do snapshot,
gravadas na mesma transação, para consulta e auditoria.

Uma requisição que muda a sessão faz: ``carregar`` -> ``aplicar(ctx, carregada, acao, muda=...)``. A ``acao`` é uma
função do motor (``lambda m: m.responder(...)``); se o motor recusa (``ValueError``), vira 422 ``resposta_invalida``
antes de qualquer escrita. Os 404 e 409 são pré-verificados pelo serviço, nunca deduzidos do texto da exceção.

Nota para as respostas (Task 6): o ``valor`` do corpo é ``bool | float | str``. O Pydantic converte o JSON ``1`` em
``1.0``, que em Python é igual a ``True``; para símbolo booleano confira ``type(valor) is bool`` antes de passar ao motor.
"""
from __future__ import annotations

import json
from collections.abc import Callable
from dataclasses import dataclass
from fractions import Fraction

from api.contexto import Contexto
from api.db import repositorios as repo
from api.erros import nao_encontrado, resposta_invalida
from api.schemas.sessao import EstadoSessao
from api.servicos.estado import montar_estado
from engine.sessao import Sessao
from kb.modelos import Base, para_motor


@dataclass
class SessaoCarregada:
    linha: dict  # a linha de ``sessoes`` (``snapshot``, ``bandeiras_reconhecidas``... já decodificados)
    base: Base  # a base (kb) da ``versao_base`` da sessão
    motor: Sessao
    origens_ficha: dict[str, str]  # id do símbolo de ficha -> "manual" | "importacao"


def restaurar_motor(snapshot: dict, base_motor: dict) -> Sessao:
    """O único ponto que reconstrói o motor de um snapshot (``base_motor`` = ``para_motor(base)``)."""
    return Sessao.restaurar(base_motor, **snapshot["motor"])


def resumo_do_motor(motor: Sessao) -> dict:
    """``{"urgencia": nivel, "top1": doenca | None}``; ``top1`` só se a hipótese mais forte tem evidência."""
    parecer = motor.parecer()
    hipoteses = sorted((i for b in parecer["blocos"] for i in b["itens"]), key=lambda i: (-i["cf"], i["doenca"]))
    top1 = hipoteses[0]["doenca"] if hipoteses and hipoteses[0]["situacao"] == "com_evidencia" else None
    return {"urgencia": parecer["urgencia"], "top1": top1}


def snapshot_do_motor(motor: Sessao, origens_ficha: dict[str, str]) -> dict:
    """O snapshot a gravar. Chame depois de ``motor.estado()``: ele registra as perguntas feitas (decisão D2).

    Passa por JSON para ficar igual ao que o banco devolve (comparável com ``linha["snapshot"]``).
    """
    resumo = resumo_do_motor(motor)
    return json.loads(json.dumps({"motor": motor.exportar(), "origens_ficha": origens_ficha, "resumo": resumo}))


def _fatos_para_projecao(motor: Sessao) -> dict[str, dict]:
    """Os fatos como a tabela ``respostas`` os guarda: valor numérico como número JSON (no snapshot é texto exato)."""
    fatos = {}
    for id, fato in motor.fatos.items():
        valor = fato.valor
        if isinstance(valor, Fraction):
            valor = int(valor) if valor.denominator == 1 else float(valor)
        fatos[id] = {"valor": valor, "cf": str(fato.cf), "origem": fato.origem, "tela_id": fato.tela_id}
    return fatos


def persistir(ctx: Contexto, sessao_id: str, motor: Sessao, estado: dict, snapshot: dict, *, subir_revisao: bool) -> int:
    """Regrava a sessão e as projeções e devolve a ``revisao``. O chamador já está num ``with ctx.conn:``."""
    agora = ctx.config.agora()
    revisao = repo.salvar_sessao(
        ctx.conn,
        sessao_id,
        snapshot=snapshot,
        fase=estado["fase"],
        motivo_parada=estado["motivo_parada"],
        modo=estado["modo"],
        reconhecidas=snapshot["motor"]["bandeiras_reconhecidas"],
        agora=agora,
        subir_revisao=subir_revisao,
    )
    repo.projetar_respostas(
        ctx.conn, sessao_id, _fatos_para_projecao(motor), snapshot["motor"]["ordem_respostas"], estado["modo"], agora
    )
    repo.projetar_perguntas(ctx.conn, sessao_id, snapshot["motor"]["perguntas_feitas"], agora)
    return revisao


def carregar(ctx: Contexto, sessao_id: str) -> SessaoCarregada:
    """A sessão restaurada do snapshot, com a base da versão a que ela está presa. 404 se não existe."""
    linha = repo.obter_sessao(ctx.conn, sessao_id)
    if linha is None:
        raise nao_encontrado("Sessão não encontrada.")
    base = ctx.repo.carregar(linha["versao_base"])
    snapshot = linha["snapshot"]
    return SessaoCarregada(
        linha=linha,
        base=base,
        motor=restaurar_motor(snapshot, para_motor(base)),
        origens_ficha=snapshot.get("origens_ficha", {}),
    )


def aplicar(
    ctx: Contexto, carregada: SessaoCarregada, acao: Callable[[Sessao], object], *, muda: bool
) -> EstadoSessao:
    """Executa ``acao`` no motor, grava o resultado e devolve o ``EstadoSessao``.

    ``muda`` é se a ação altera a sessão para o usuário (resposta, correção, troca de modo, ação da bandeira):
    só então a ``revisao`` sobe. Com ``muda=False`` (leitura) o snapshot só é regravado se mudou, porque
    ``Sessao.estado()`` registra as perguntas apresentadas (decisão D2); a ``revisao`` não sobe.
    """
    motor, linha = carregada.motor, carregada.linha
    try:
        acao(motor)
        estado = motor.estado()
    except ValueError as erro:  # o motor recusou (modo, ordem, valor): nada foi escrito
        raise resposta_invalida(str(erro)) from None
    snapshot = snapshot_do_motor(motor, carregada.origens_ficha)
    if not muda and _sem_novidade(linha, estado, snapshot):
        return montar_estado(carregada, linha["revisao"])
    with ctx.conn:
        revisao = persistir(ctx, linha["id"], motor, estado, snapshot, subir_revisao=muda)
    return montar_estado(carregada, revisao)


def _sem_novidade(linha: dict, estado: dict, snapshot: dict) -> bool:
    """Verdadeiro se a linha já guarda exatamente este estado (nada a regravar)."""
    return (
        snapshot == linha["snapshot"]
        and (estado["fase"], estado["motivo_parada"], estado["modo"])
        == (linha["fase"], linha["motivo_parada"], linha["modo"])
        and snapshot["motor"]["bandeiras_reconhecidas"] == linha["bandeiras_reconhecidas"]
    )
