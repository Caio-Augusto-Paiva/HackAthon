"""Sessões de anamnese: criar e consultar o estado. Os 404 e 409 são pré-verificados, nunca deduzidos de exceção."""
from __future__ import annotations

from api.contexto import Contexto
from api.db import repositorios as repo
from api.erros import conflito, entrada_invalida, nao_encontrado
from api.schemas.sessao import EstadoSessao, NovaSessao
from api.servicos.comum import texto_legivel
from api.servicos.estado import montar_estado
from api.servicos.ficha import CAMPO_DATA_PARTO, CAMPO_DIAS, ficha_para_motor, mostrar_valor
from api.servicos.sessao_motor import SessaoCarregada, aplicar, carregar, persistir, snapshot_do_motor
from engine.sessao import Sessao
from kb.modelos import Base, para_motor


def _versao_da_sessao(ctx: Contexto, pedida: str | None) -> str:
    """A versão pedida (404 se não existe) ou, sem pedido, a ativa (409 se não há ativa)."""
    if pedida is not None:
        if pedida not in ctx.repo.listar_versoes():  # só lista ids bem formados: "abc" também cai aqui
            raise nao_encontrado(f"Versão {mostrar_valor(pedida)} não encontrada.")
        return pedida
    ativa = ctx.repo.versao_ativa()
    if ativa is None:
        raise conflito("Nenhuma versão ativa para criar a sessão; informe a versão_base.")
    return ativa


def _origens_ficha(base: Base, origens: dict) -> dict[str, str]:
    """Origem de cada símbolo de ficha: ``animal.origens`` é por campo; aqui vira por id de símbolo.

    O símbolo dos dias em lactação herda a origem do campo ``data_ultimo_parto`` (é calculado dele). O que o
    animal não registra como importado vale ``"manual"``.
    """
    return {
        s.id: origens.get(CAMPO_DATA_PARTO if s.campo_ficha == CAMPO_DIAS else s.campo_ficha, "manual")
        for s in base.simbolos
        if s.tipo == "ficha" and s.campo_ficha
    }


def criar_sessao(ctx: Contexto, corpo: NovaSessao) -> EstadoSessao:
    if not texto_legivel(corpo.animal_id, corpo.versao_base):  # o banco não grava um surrogate solto
        raise entrada_invalida("O texto enviado tem caracteres Unicode inválidos.")
    animal = repo.obter_animal(ctx.conn, corpo.animal_id)
    if animal is None:
        raise nao_encontrado("Animal não encontrado.")
    versao = _versao_da_sessao(ctx, corpo.versao_base)
    base = ctx.repo.carregar(versao)
    origens_ficha = _origens_ficha(base, animal["origens"])
    ficha = ficha_para_motor(base, animal["ficha"], ctx.config.hoje())  # o que a ficha não tem, a triagem pergunta
    motor = Sessao(para_motor(base), corpo.modo, ficha)
    estado = motor.estado()  # registra as perguntas da primeira tela antes de exportar (decisão D2)
    snapshot = snapshot_do_motor(motor, origens_ficha)
    with ctx.conn:
        sessao_id = repo.inserir_sessao(
            ctx.conn,
            animal_id=animal["id"],
            modo=estado["modo"],
            versao_base=versao,
            snapshot=snapshot,
            fase=estado["fase"],
            agora=ctx.config.agora(),
        )
        persistir(ctx, sessao_id, motor, estado, snapshot, subir_revisao=False)  # motivo_parada e projeções
    linha = repo.obter_sessao(ctx.conn, sessao_id)
    return montar_estado(
        SessaoCarregada(linha=linha, base=base, motor=motor, origens_ficha=origens_ficha), linha["revisao"]
    )


def obter_estado(ctx: Contexto, sessao_id: str) -> EstadoSessao:
    """Leitura: não sobe a ``revisao``; só regrava o snapshot se o motor registrou algo novo (decisão D2)."""
    return aplicar(ctx, carregar(ctx, sessao_id), lambda motor: None, muda=False)
