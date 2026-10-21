"""Base de conhecimento: leitura das versões, grafo do editor e validação de uma edição (4.5.3).

Os arquivos de ``base/`` são a fonte da verdade (via ``kb.carregador.Repositorio``); o SQLite guarda só o
índice (``versoes_base``) e as execuções dos casos. Nada aqui grava arquivo; só ``sincronizar_indice`` grava
no banco.
"""
from __future__ import annotations

from api.contexto import Contexto
from api.db import repositorios as repo
from api.erros import entrada_invalida, nao_encontrado
from api.schemas.base import EdicaoBase, ListaVersoes, UltimaExecucao, VersaoItem
from api.servicos.comum import texto_legivel
from api.servicos.ficha import mostrar_valor
from kb import validar_edicao
from kb.grafo import Grafo, base_para_grafo
from kb.modelos import Base
from kb.validador import Relatorio


def sincronizar_indice(ctx: Contexto) -> None:
    """Registra em ``versoes_base`` as versões do disco que ainda faltam (com o hash do arquivo).

    Quem grava uma execução de casos chama isto antes: ``execucoes_casos.versao`` tem chave estrangeira para
    ``versoes_base``. Uma versão já registrada não é lida nem alterada; duas requisições simultâneas não
    colidem (``ON CONFLICT DO NOTHING``).

    **Transação:** a função abre e confirma a própria transação (``with ctx.conn:``). Por isso deve ser chamada
    **antes** do ``with ctx.conn:`` de quem grava a execução, nunca dentro dele: o ``with`` interno faria
    ``commit`` de tudo o que o bloco externo já escreveu, antes da hora, e um erro depois disso não desfaria
    mais essas escritas. Sem versão faltando, não escreve nem abre transação.
    """
    registradas = {linha["versao"] for linha in repo.listar_versoes_base(ctx.conn)}
    faltam = [v for v in ctx.repo.listar_versoes() if v not in registradas]
    if not faltam:
        return
    agora = ctx.config.agora()
    with ctx.conn:
        for versao in faltam:
            meta = ctx.repo.carregar(versao).meta
            repo.sincronizar_versao(
                ctx.conn,
                versao=versao,
                pai=meta.pai,
                autor=meta.autor,
                data=meta.data,
                nota=meta.nota,
                hash=ctx.repo.hash(versao),
                agora=agora,
            )


def _ultima_execucao(ctx: Contexto, versao: str) -> UltimaExecucao | None:
    execucoes = repo.listar_execucoes(ctx.conn, versao)  # a mais nova primeiro; só os cabeçalhos
    if not execucoes:
        return None
    return UltimaExecucao(execucao_id=execucoes[0]["id"], passou=execucoes[0]["passou"], falhou=execucoes[0]["falhou"])


def listar_versoes(ctx: Contexto) -> ListaVersoes:
    """As versões do disco, da mais antiga à mais nova, com a ativa marcada e a última execução de cada uma."""
    itens = []
    for versao in ctx.repo.listar_versoes():
        base = ctx.repo.carregar(versao)
        itens.append(
            VersaoItem(
                versao=versao,
                pai=base.meta.pai,
                autor=base.meta.autor,
                data=base.meta.data,
                nota=base.meta.nota,
                simbolos=len(base.simbolos),
                regras=len(base.regras),
                suposicao_a_validar=sum(1 for r in base.regras if r.status == "suposicao_a_validar"),
                ultima_execucao=_ultima_execucao(ctx, versao),
            )
        )
    return ListaVersoes(ativa=ctx.repo.versao_ativa(), itens=itens)


def obter_versao(ctx: Contexto, versao: str) -> Base:
    """A base da versão; versão inexistente ou identificador inválido (``abc``) é 404.

    A checagem é pela lista do disco, não por exceção: um arquivo corrompido continua sendo erro do servidor.
    """
    if versao not in ctx.repo.listar_versoes():
        raise nao_encontrado(f"Versão {mostrar_valor(versao)} não encontrada.")
    return ctx.repo.carregar(versao)


def obter_grafo(ctx: Contexto, versao: str) -> Grafo:
    return base_para_grafo(obter_versao(ctx, versao))


def grafo_da_edicao(corpo: EdicaoBase) -> dict:
    """O dict que ``kb.validar_edicao`` espera (um ``Grafo``), montado a partir do corpo de uma edição.

    ``meta`` e ``layout`` vêm do envelope; ``nos`` e ``arestas``, de ``corpo.grafo``. Compartilhado com salvar.
    """
    return {"meta": corpo.meta, "nos": corpo.grafo.nos, "arestas": corpo.grafo.arestas, "layout": corpo.layout}


def validar_edicao_base(ctx: Contexto, corpo: EdicaoBase) -> Relatorio:
    """Valida uma edição sem salvar. Devolve sempre um relatório; estrutura quebrada vira erro ``E00``.

    O único 422 é o de texto ilegível (surrogate Unicode solto): as mensagens do relatório citam ids do corpo,
    e o JSON da resposta não o codificaria.
    """
    dados = grafo_da_edicao(corpo)
    if not texto_legivel(corpo.pai, corpo.nota, dados):
        raise entrada_invalida("O texto enviado tem caracteres Unicode inválidos.")
    return validar_edicao(dados)[1]
