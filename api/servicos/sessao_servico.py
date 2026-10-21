"""Sessões de anamnese: criar, consultar, responder, trocar de modo e agir sobre a bandeira vermelha.

Os 404 e 409 são pré-verificados, nunca deduzidos de exceção.
"""
from __future__ import annotations

from api.contexto import Contexto
from api.db import repositorios as repo
from api.erros import conflito, entrada_invalida, nao_encontrado, resposta_invalida
from api.schemas.sessao import (
    CorrecaoPergunta,
    EstadoSessao,
    NovaSessao,
    RespostaPergunta,
    RespostaTriagem,
    Valor,
)
from api.servicos.comum import texto_legivel
from api.servicos.estado import montar_estado
from api.servicos.ficha import CAMPO_DATA_PARTO, CAMPO_DIAS, ficha_para_motor, mostrar_valor
from api.servicos.sessao_motor import SessaoCarregada, aplicar, carregar, persistir, snapshot_do_motor
from engine.sessao import Sessao
from kb.modelos import Base, DominioBooleano, DominioNumerico, Simbolo, Tela, para_motor


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


# --- responder (POST) e corrigir (PUT) -------------------------------------------------------

_TIPO_DO_VALOR = {  # o tipo exato que o JSON do cliente tem de ter para cada domínio (o outro caso é texto)
    DominioBooleano: (bool, "verdadeiro ou falso (true ou false)"),
    DominioNumerico: (float, "um número"),
}


def _simbolos(carregada: SessaoCarregada) -> dict[str, Simbolo]:
    return {s.id: s for s in carregada.base.simbolos}


def _ids_da_tela(tela: Tela, simbolos: dict[str, Simbolo], modo: str) -> list[str]:
    """Os símbolos que a tela pede no modo; a mesma regra de ``engine.sessao.Sessao._ids_tela``.

    A tela está respondida quando todos eles têm fato (``Sessao._telas_pendentes``). Não basta existir um fato
    com o ``tela_id``: ``simbolos_por_modo`` pode pedir um símbolo a mais depois da troca de modo.
    """
    if tela.simbolos_por_modo is not None:
        return list(tela.simbolos_por_modo.get(modo, []))
    return [id for id in tela.simbolos if not simbolos[id].pergunta or simbolos[id].pergunta.get(modo)]


def _valor_do_dominio(simbolo: Simbolo, valor: Valor) -> Valor:
    """O valor, se o tipo é o do domínio do símbolo; senão 422 ``resposta_invalida``.

    O corpo traz ``bool | float | str``. O JSON ``1`` chega como ``1.0``, que o Python compara igual a ``True``, e o
    motor aceita o texto "sim" como booleano: por isso o tipo é conferido aqui, exatamente. Os limites e as opções
    do domínio ficam para o motor.
    """
    tipo, descricao = _TIPO_DO_VALOR.get(type(simbolo.dominio), (str, "um texto"))
    if type(valor) is not tipo:
        raise resposta_invalida(f"A resposta de {simbolo.id} deve ser {descricao}.")
    return valor


def _resposta_da_tela(tela: Tela, ids: list[str], simbolos: dict[str, Simbolo], corpo: RespostaTriagem):
    """O que o motor recebe: ``None`` (não sei), a lista dos marcados (múltipla) ou o dict ``valores`` (única)."""
    if corpo.nao_sei:
        return None
    valores = corpo.valores
    for id in valores:
        if id not in ids:
            raise resposta_invalida(f"A tela {tela.id} não tem o símbolo {mostrar_valor(id)}.")
    if tela.selecao == "multipla":
        if any(type(marcado) is not bool for marcado in valores.values()):
            raise resposta_invalida("Em seleção múltipla, cada opção é marcada com true ou false.")
        return [id for id, marcado in valores.items() if marcado]
    for id, valor in valores.items():
        _valor_do_dominio(simbolos[id], valor)
    return dict(valores)


def responder_triagem(
    ctx: Contexto, sessao_id: str, tela_id: str, corpo: RespostaTriagem, *, corrigir: bool
) -> EstadoSessao:
    """POST (primeira resposta da tela) ou PUT (correção). 404 tela; 409 ``ja_respondida``/``nao_respondida``.

    Uma tela só com símbolos da ficha já vem respondida: o POST é 409 e o PUT a corrige. Que a tela seja a próxima
    (ou que as chaves de ``valores`` sejam as dela) é com o motor: ``ValueError`` vira 422 ``resposta_invalida``.
    """
    carregada = carregar(ctx, sessao_id)
    tela = next((t for t in carregada.base.meta.triagem if t.id == tela_id), None)
    if tela is None:
        raise nao_encontrado(f"Tela {mostrar_valor(tela_id)} não encontrada.")
    simbolos = _simbolos(carregada)
    ids = _ids_da_tela(tela, simbolos, carregada.motor.modo)
    fatos = carregada.motor.fatos
    respondida = all(id in fatos for id in ids)
    if respondida and not corrigir:
        raise conflito("Esta tela já foi respondida; para mudar a resposta, corrija-a.", "ja_respondida")
    if not respondida and corrigir:
        raise conflito("Esta tela ainda não foi respondida; responda-a antes de corrigir.", "nao_respondida")
    resposta = _resposta_da_tela(tela, ids, simbolos, corpo)
    return aplicar(
        ctx, carregada, lambda motor: motor.responder_triagem(tela_id, resposta, corrigir=corrigir), muda=True
    )


def responder_pergunta(
    ctx: Contexto, sessao_id: str, simbolo: str, corpo: RespostaPergunta | CorrecaoPergunta, *, corrigir: bool
) -> EstadoSessao:
    """POST (a pergunta dinâmica da vez) ou PUT (corrige uma já respondida na fase dinâmica).

    404 se o símbolo não está na base; 409 ``ja_respondida`` (POST com fato) ou ``nao_respondida`` (PUT fora das
    dinâmicas respondidas, o que inclui os símbolos da triagem, que se corrigem pela tela). Que a pergunta seja a
    próxima e valha no modo é com o motor.
    """
    carregada = carregar(ctx, sessao_id)
    simbolos = _simbolos(carregada)
    if simbolo not in simbolos:
        raise nao_encontrado(f"Símbolo {mostrar_valor(simbolo)} não encontrado.")
    motor = carregada.motor
    if corrigir and simbolo not in motor.dinamicas:
        raise conflito(
            "Só uma pergunta da fase dinâmica já respondida se corrige aqui; as da triagem se corrigem pela tela.",
            "nao_respondida",
        )
    if not corrigir and simbolo in motor.fatos:
        raise conflito("Esta pergunta já foi respondida; para mudar a resposta, corrija-a.", "ja_respondida")
    valor = None if corpo.nao_sei else _valor_do_dominio(simbolos[simbolo], corpo.valor)
    return aplicar(ctx, carregada, lambda m: m.responder(simbolo, valor, corrigir=corrigir), muda=True)


# --- modo e bandeira vermelha ----------------------------------------------------------------


def trocar_modo(ctx: Contexto, sessao_id: str, modo: str) -> EstadoSessao:
    """Troca o modo (``produtor``/``veterinario``) sem perder resposta. O modo inválido já caiu no schema (422)."""
    return aplicar(ctx, carregar(ctx, sessao_id), lambda motor: motor.trocar_modo(modo), muda=True)


def acao_bandeira(ctx: Contexto, sessao_id: str, acao: str) -> EstadoSessao:
    """``continuar`` ou ``ver_parecer``. Sem bandeira registrada o motor recusa: 422 ``resposta_invalida``.

    Com a sessão já encerrada, ``continuar`` é aceito (o motor o aceita e ele só tira a pausa): não vira 422.
    """
    return aplicar(ctx, carregar(ctx, sessao_id), lambda motor: motor.acao_bandeira(acao), muda=True)
