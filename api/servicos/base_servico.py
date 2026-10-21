"""Base de conhecimento: versões, grafo do editor, validação, salvar uma nova versão e ativar (4.5.3).

Os arquivos de ``base/`` são a fonte da verdade (via ``kb.carregador.Repositorio``); o SQLite guarda só o
índice (``versoes_base``) e as execuções dos casos. Só ``salvar_versao`` e ``ativar_versao`` gravam arquivo (a
versão nova e o ponteiro ``ativa.json``); o banco é gravado por ``sincronizar_indice`` e pela execução dos casos.
"""
from __future__ import annotations

from api.contexto import Contexto
from api.db import repositorios as repo
from api.erros import base_invalida, conflito, entrada_invalida, nao_encontrado
from api.schemas.base import (
    AtivarBody,
    AtivarResposta,
    EdicaoBase,
    Execucao,
    ExecucaoResumo,
    ListaVersoes,
    SalvarResposta,
    UltimaExecucao,
    VersaoItem,
)
from api.servicos import casos_servico  # ciclo com casos_servico: um só usa o outro dentro de funções, nunca ao importar
from api.servicos.comum import texto_legivel
from api.servicos.ficha import mostrar_valor
from kb import validar_edicao
from kb.carregador import BaseInvalida
from kb.grafo import Grafo, base_para_grafo
from kb.modelos import Base
from kb.validador import Relatorio

AUTOR_PADRAO = "equipe"  # suposição: a API não tem login; toda versão salva sai em nome da equipe


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


def _converter_e_validar(corpo: EdicaoBase) -> tuple[Base | None, Relatorio]:
    """Converte a edição em ``Base`` e a valida (``kb.validar_edicao``); compartilhado por validar e salvar.

    ``base`` é ``None`` quando a estrutura está quebrada (o relatório traz erros ``E00``). O único 422 daqui é o de
    texto ilegível (surrogate Unicode solto): as mensagens do relatório citam ids do corpo, o JSON da resposta não o
    codificaria, e a gravação do arquivo da versão também falharia.
    """
    dados = grafo_da_edicao(corpo)
    if not texto_legivel(corpo.pai, corpo.nota, dados):
        raise entrada_invalida("O texto enviado tem caracteres Unicode inválidos.")
    return validar_edicao(dados)


def validar_edicao_base(ctx: Contexto, corpo: EdicaoBase) -> Relatorio:
    """Valida uma edição sem salvar. Devolve sempre um relatório; estrutura quebrada vira erro ``E00``.

    O único 422 é o de texto ilegível (ver ``_converter_e_validar``).
    """
    return _converter_e_validar(corpo)[1]


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

    **Transações:** este serviço não abre transação própria. ``sincronizar_indice`` e cada ``casos_servico.executar``
    abrem e confirmam a sua; por isso nada aqui roda dentro de um ``with ctx.conn:``. Se a execução dos casos falhar
    (arquivo de casos corrompido, por exemplo), a versão já gravada continua no disco e no índice.
    """
    base, relatorio = _converter_e_validar(corpo)
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

    sincronizar_indice(ctx)  # a versão nova entra no índice (com o hash) antes de qualquer execução gravar
    execucao_pai = _execucao_do_pai(ctx, pai) if pai is not None else None
    execucao_nova = casos_servico.executar(ctx, versao)
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

    Versão inexistente é 404. Se a **última execução** da versão tem algum caso que falhou **ou** deu erro e o corpo
    não traz ``confirmar_falhas: true``, 409 ``casos_falhando`` (nada muda). Conta-se pelos ``resultados``: o campo
    ``falhou`` do cabeçalho não inclui o status ``erro`` (ruling 7).

    Uma versão que nunca foi executada ativa sem confirmação: não há falha conhecida a confirmar (decisão desta
    tarefa; o editor sempre executa ao salvar, então isso só vale para uma versão gravada fora da API).
    """
    if corpo.versao not in ctx.repo.listar_versoes():  # só lista ids bem formados: "abc" também cai aqui
        raise nao_encontrado(f"Versão {mostrar_valor(corpo.versao)} não encontrada.")
    ultima = repo.ultima_execucao(ctx.conn, corpo.versao)
    if ultima is not None and not corpo.confirmar_falhas:
        status = [r["status"] for r in ultima["resultados"]]
        falhando, com_erro = status.count("falhou"), status.count("erro")
        if falhando or com_erro:
            raise conflito(
                f"A última execução da versão {mostrar_valor(corpo.versao)} tem {falhando} caso(s) falhando e "
                f"{com_erro} com erro. Envie confirmar_falhas: true para ativar mesmo assim.",
                codigo="casos_falhando",
            )
    anterior = ctx.repo.versao_ativa()
    ctx.repo.ativar(corpo.versao)
    return AtivarResposta(versao=corpo.versao, anterior=anterior)
