"""Salvar uma nova versão da base a partir do grafo editado e ativar uma versão (4.5.3).

**Dependências entre serviços:** ``versoes_servico`` -> ``casos_servico`` -> ``base_servico``, sempre nesse sentido.
Este módulo orquestra: valida a edição e lê o repositório com ``base_servico``, roda e consulta os casos com
``casos_servico``. Nenhum dos dois de baixo importa este; por isso não há ciclo de importação.

Os arquivos de ``base/`` são a fonte da verdade: aqui se grava a versão nova (``Repositorio.salvar_nova``) e se move o
ponteiro ``ativa.json`` (``Repositorio.ativar``). O SQLite recebe o índice (``sincronizar_indice``) e as execuções.
"""
from __future__ import annotations

import logging

from api.contexto import Contexto
from api.db import repositorios as repo
from api.erros import base_invalida, conflito, nao_encontrado
from api.schemas.base import AtivarBody, AtivarResposta, EdicaoBase, Execucao, ExecucaoResumo, SalvarResposta
from api.servicos import base_servico, casos_servico
from api.servicos.ficha import mostrar_valor
from kb.carregador import BaseInvalida
from kb.validador import Relatorio

AUTOR_PADRAO = "equipe"  # suposição: a API não tem login; toda versão salva sai em nome da equipe

_log = logging.getLogger("api")


# --- salvar -----------------------------------------------------------------------------------


def _erros_do_relatorio(relatorio: Relatorio) -> list[dict]:
    """Os erros do relatório como ``detalhes`` do 422 (o mesmo formato de ``Detalhe``); os avisos ficam de fora."""
    return [erro.model_dump(mode="json") for erro in relatorio.erros]


def _resumo(execucao: Execucao) -> ExecucaoResumo:
    return ExecucaoResumo(
        execucao_id=execucao.execucao_id, total=execucao.total, passou=execucao.passou, falhou=execucao.falhou
    )


def _execucao_do_pai(ctx: Contexto, pai: str) -> ExecucaoResumo:
    """A execução mais recente do pai; se ele nunca foi executado, roda os casos nele agora (base de comparação).

    Um pai que já tem execução não é reexecutado: a comparação por caso da versão nova usa as execuções que ele tiver.
    """
    cabecalhos = repo.listar_execucoes(ctx.conn, pai)  # a mais nova primeiro
    if cabecalhos:
        c = cabecalhos[0]
        return ExecucaoResumo(execucao_id=c["id"], total=c["total"], passou=c["passou"], falhou=c["falhou"])
    return _resumo(casos_servico.executar(ctx, pai))


def salvar_versao(ctx: Contexto, corpo: EdicaoBase) -> SalvarResposta:
    """Grava a próxima versão a partir do grafo editado, roda os casos nela e no pai e devolve o que mudou.

    Ordem: valida (erros -> 422 ``base_invalida`` com os erros em ``detalhes``, nada gravado) -> confere o pai (404)
    -> ``Repositorio.salvar_nova`` (``FileExistsError`` -> 409 ``conflito``, pelo tipo da exceção) -> índice do
    SQLite -> casos do pai (só se ele ainda não tem execução) e da nova. A versão nova **não** é ativada.

    **Pai:** ``pai`` nulo ou vazio (``""``) vale a versão ativa (``corpo.pai or versao_ativa()``); um ``pai`` que
    não existe é 404. Sem ``pai`` e sem versão ativa, a versão nasce sem pai e ``execucao_pai`` é ``None``.

    **Transações:** este serviço não abre transação própria. ``sincronizar_indice`` e cada ``casos_servico.executar``
    abrem e confirmam a sua; por isso nada aqui roda dentro de um ``with ctx.conn:``.

    **Falha depois de gravar:** se a execução dos casos levantar (arquivo de casos corrompido, por exemplo), a
    exceção segue (500 ``erro_interno``) e a versão já gravada continua no disco e no índice. Essa versão fica sem
    execução e, pelo ruling 15, ativa sem confirmação; para ter os resultados, basta executar os casos depois.
    """
    base, relatorio = base_servico.converter_e_validar(corpo)
    if base is None or not relatorio.valida:
        raise base_invalida("A base editada tem erros de validação; nada foi gravado.", _erros_do_relatorio(relatorio))

    if corpo.pai and corpo.pai not in ctx.repo.listar_versoes():  # pré-verificado: não se casa texto de exceção
        raise nao_encontrado(f"Versão {mostrar_valor(corpo.pai)} não encontrada.")
    pai = corpo.pai or ctx.repo.versao_ativa()  # uma ativa que sumiu do disco é falha do servidor (ValueError, 500)

    try:
        versao = ctx.repo.salvar_nova(base, autor=AUTOR_PADRAO, nota=corpo.nota, pai=pai)
    except BaseInvalida as erro:  # a validação já passou acima; só uma mudança no kb entre as duas a faria falhar
        raise base_invalida(
            "A base editada tem erros de validação; nada foi gravado.", _erros_do_relatorio(erro.relatorio)
        ) from None
    except FileExistsError:  # outra gravação criou esta versão no meio; o kb não sobrescreve nada
        raise conflito(
            "Outra gravação criou esta versão ao mesmo tempo; nada foi sobrescrito. Tente salvar de novo."
        ) from None

    # Segunda chamada (``casos_servico.executar`` também sincroniza, mas só depois de ler os casos): garante a versão
    # nova no índice, com o hash, mesmo se a execução dos casos falhar logo abaixo.
    base_servico.sincronizar_indice(ctx)
    try:
        execucao_pai = _execucao_do_pai(ctx, pai) if pai is not None else None
        execucao_nova = casos_servico.executar(ctx, versao)
    except Exception:
        _log.warning("versão %s gravada; a execução dos casos falhou", versao)
        raise
    return SalvarResposta(
        versao=versao,
        pai=pai,
        hash=ctx.repo.hash(versao),
        validacao=relatorio,
        execucao_nova=_resumo(execucao_nova),
        execucao_pai=execucao_pai,
        mudancas=execucao_nova.mudancas,
    )


# --- ativar -----------------------------------------------------------------------------------


def ativar_versao(ctx: Contexto, corpo: AtivarBody) -> AtivarResposta:
    """Move o ponteiro ``ativa.json`` para a versão e devolve a que estava ativa antes.

    Versão inexistente é 404. Sem ``confirmar_falhas: true``, se o **status mais recente de algum caso** da versão é
    ``falhou`` ou ``erro``, 409 ``casos_falhando`` (nada muda). "Mais recente" é o da execução mais nova da versão que
    contém o caso, restrito aos ids do ``casos.json`` atual (``casos_servico.status_dos_casos``, ruling 15): uma
    execução parcial posterior, só de casos verdes, não apaga uma falha que ela não rodou, e um caso removido do
    arquivo não conta. O campo ``falhou`` do cabeçalho de uma execução não serve: não inclui o status ``erro``.

    Uma versão que nunca foi executada ativa sem confirmação: não há falha conhecida a confirmar (por exemplo, uma
    versão gravada cuja execução dos casos falhou, ou gravada fora da API).

    Se o ``ativa.json`` atual estiver ilegível, a ativação segue com ``anterior = None`` (e um aviso no log): é
    ela que conserta o ponteiro.
    """
    if corpo.versao not in ctx.repo.listar_versoes():  # só lista ids bem formados: "abc" também cai aqui
        raise nao_encontrado(f"Versão {mostrar_valor(corpo.versao)} não encontrada.")
    if not corpo.confirmar_falhas:
        status = list(casos_servico.status_dos_casos(ctx, corpo.versao).values())
        falhando, com_erro = status.count("falhou"), status.count("erro")
        if falhando or com_erro:
            raise conflito(
                f"Na versão {mostrar_valor(corpo.versao)}, {falhando} caso(s) falhando e {com_erro} com erro na "
                "execução mais recente de cada um. Envie confirmar_falhas: true para ativar mesmo assim.",
                codigo="casos_falhando",
            )
    try:
        anterior = ctx.repo.versao_ativa()
    except ValueError as erro:  # ponteiro corrompido: a ativação o regrava, então não pode depender dele
        _log.warning(
            "ponteiro da versão ativa ilegível (%s); a ativação de %s segue sem versão anterior", erro, corpo.versao
        )
        anterior = None
    ctx.repo.ativar(corpo.versao)
    return AtivarResposta(versao=corpo.versao, anterior=anterior)
