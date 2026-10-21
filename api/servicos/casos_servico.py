"""Execução dos casos de teste de uma versão da base (4.5.3): roda, compara com a versão pai e grava.

Os casos vêm de ``casos/casos.json`` (iguais para todas as versões); cada execução fica em ``execucoes_casos``
e ``resultados_casos``. A decisão de cada caso é do motor (``engine.casos.executar_caso``), sem LLM.

**Para a ativação (Task 11, ruling 7):** o cabeçalho conta em ``falhou`` só o status ``falhou``; um caso ``erro``
(mal formado ou recusado pelo motor) entra em ``total`` e em nenhum dos dois. Quem decide se uma versão pode ser
ativada deve contar como falhando os resultados ``falhou`` **e** ``erro``, olhando ``resultados``, não ``falhou``.
"""
from __future__ import annotations

import json
import logging
from dataclasses import dataclass

from pydantic import ValidationError

from api.contexto import Contexto
from api.db import repositorios as repo
from api.erros import nao_encontrado
from api.schemas.base import Execucao, ExecucaoCabecalho, FalhaCaso, ListaExecucoes, Mudanca, ResultadoCaso
from api.servicos import base_servico
from api.servicos.ficha import mostrar_valor
from engine.casos import executar_caso
from kb import para_motor
from kb.modelos import Caso

_log = logging.getLogger("api")

_LIMITE_ERRO = 300  # a mensagem de um caso com erro é curta: a lista de resultados continua legível
_ERRO_GENERICO = "Erro ao executar o caso."
_TEXTO_DO_ERRO_DE_VALIDACAO = {"extra_forbidden": "campo não reconhecido", "missing": "campo obrigatório"}


@dataclass
class _CasoLido:
    id: str
    descricao: str
    caso: dict | None  # o dict do motor; None se o caso não passou na validação
    erro: str | None  # por que não passou na validação


# --- leitura dos casos -----------------------------------------------------------------------


def _curta(texto: object) -> str:
    """A mensagem numa linha só, limitada, e nunca vazia."""
    limpa = " ".join(str(texto or "").split())
    return (limpa if len(limpa) <= _LIMITE_ERRO else limpa[: _LIMITE_ERRO - 3] + "...") or _ERRO_GENERICO


def _mensagem_de_validacao(erro: ValidationError) -> str:
    """Até três campos com problema, em português; nunca o valor enviado nem o texto em inglês do Pydantic."""
    partes = []
    for item in erro.errors(include_url=False, include_input=False, include_context=False)[:3]:
        onde = ".".join(str(p) for p in item["loc"]) or "caso"
        partes.append(f"{onde}: {_TEXTO_DO_ERRO_DE_VALIDACAO.get(item['type'], 'valor inválido')}")
    return _curta("Caso mal formado. " + "; ".join(partes))


def _ler_casos(ctx: Contexto) -> list[_CasoLido]:
    """Os casos de ``casos/casos.json``, na ordem do arquivo; sem o arquivo, nenhum.

    Valida **um a um** com ``kb.modelos.Caso`` (o mesmo modelo de ``Repositorio.carregar_casos``, que é tudo ou
    nada: um caso mal formado derrubaria a execução inteira). O caso que não passa, que não é um objeto ou que
    repete um id já visto vira um ``_CasoLido`` com ``erro``, e a execução segue. Um arquivo que não é JSON, ou
    que não é uma lista, continua sendo falha do servidor (como um arquivo de versão corrompido).
    """
    # Espelha ``kb.carregador.Repositorio.carregar_casos``: o mesmo caminho (``<raiz>/casos/casos.json``), a mesma
    # codificação (``utf-8-sig``, aceita o BOM) e arquivo ausente = lista vazia. O único desvio é validar caso a
    # caso em vez de tudo ou nada (ver acima). Se aquele método mudar, mude aqui; o teste do BOM compara os dois.
    arquivo = ctx.repo.raiz / "casos" / "casos.json"
    if not arquivo.is_file():
        return []
    brutos = json.loads(arquivo.read_text(encoding="utf-8-sig"))
    if not isinstance(brutos, list):
        raise ValueError("casos.json deve conter uma lista de casos.")
    lidos: list[_CasoLido] = []
    vistos: set[str] = set()
    for posicao, bruto in enumerate(brutos, start=1):
        campos = bruto if isinstance(bruto, dict) else {}
        id_bruto, descricao_bruta = campos.get("id"), campos.get("descricao")
        caso_id = id_bruto if isinstance(id_bruto, str) and id_bruto else f"#{posicao}"  # sem id: a posição
        descricao = descricao_bruta if isinstance(descricao_bruta, str) else ""
        caso: dict | None = None
        erro: str | None = None
        try:
            caso = Caso.model_validate(bruto).model_dump(mode="json", exclude_none=True)
        except ValidationError as exc:
            erro = _mensagem_de_validacao(exc)
        if caso_id in vistos:  # o banco guarda um resultado por (execução, caso): o id tem de ser único
            caso, erro, caso_id = None, "Id de caso repetido.", f"{caso_id}#{posicao}"
        vistos.add(caso_id)
        lidos.append(_CasoLido(id=caso_id, descricao=descricao, caso=caso, erro=erro))
    return lidos


def _mensagem_ids(faltam: list[str]) -> str:
    if len(faltam) == 1:
        return f"Caso {mostrar_valor(faltam[0])} não encontrado."
    mostrados = ", ".join(mostrar_valor(i) for i in faltam[:5]) + (", ..." if len(faltam) > 5 else "")
    return f"Casos não encontrados: {mostrados}."


# --- execução --------------------------------------------------------------------------------


def _resultado(
    lido: _CasoLido, status: str, *, obtido: dict | None = None, falhas: list | None = None, erro: str | None = None
) -> dict:
    """O dict que ``repo.inserir_execucao`` espera; ``descricao``, ``mudou_vs_pai`` e ``erro`` vão em ``extra``."""
    return {
        "caso_id": lido.id,
        "status": status,
        "obtido": obtido,
        "falhas": falhas or [],
        "extra": {"descricao": lido.descricao, "mudou_vs_pai": None, "erro": erro},
    }


def _rodar(motor: dict, lido: _CasoLido) -> dict:
    """Roda um caso; qualquer problema vira um resultado ``erro`` e não derruba os outros casos."""
    if lido.caso is None:
        return _resultado(lido, "erro", erro=lido.erro)
    try:
        saida = executar_caso(motor, lido.caso)
    except Exception:  # o motor trata só KeyError, ValueError e TypeError; o resto também é problema do caso
        _log.exception("falha inesperada ao executar o caso %s", lido.id)
        return _resultado(lido, "erro", erro=_ERRO_GENERICO)
    if saida["status"] == "erro":
        return _resultado(lido, "erro", erro=_curta(saida.get("erro")))
    return _resultado(lido, saida["status"], obtido=saida["obtido"], falhas=saida["falhas"])


def _status_no_pai(ctx: Contexto, pai: str, casos: set[str]) -> dict[str, str] | None:
    """O status de cada caso de ``casos`` no pai, ou ``None`` se o pai nunca foi executado (ruling 14).

    Por caso: vale a execução **mais recente do pai que contém o caso**; percorre da mais nova para a mais antiga
    e guarda o primeiro status de cada um (para quando já achou todos). Um caso que nenhuma execução do pai rodou
    não entra no dicionário.
    """
    cabecalhos = repo.listar_execucoes(ctx.conn, pai)  # a mais nova primeiro
    if not cabecalhos:
        return None
    status: dict[str, str] = {}
    for cabecalho in cabecalhos:
        for resultado in repo.obter_execucao(ctx.conn, cabecalho["id"])["resultados"]:
            status.setdefault(resultado["caso_id"], resultado["status"])
        if casos <= status.keys():
            break
    return status


def _comparar_com_o_pai(resultados: list[dict], antes_por_caso: dict[str, str]) -> None:
    """Preenche ``mudou_vs_pai`` ("antes->depois") onde o status difere do que o caso teve no pai.

    ``ausente``: nenhuma execução do pai rodou o caso (caso novo na versão).
    """
    for resultado in resultados:
        antes = antes_por_caso.get(resultado["caso_id"], "ausente")
        if antes != resultado["status"]:
            resultado["extra"]["mudou_vs_pai"] = f"{antes}->{resultado['status']}"


def _montar(linha: dict) -> Execucao:
    """A ``Execucao`` a partir da linha do banco; ``mudancas`` sai do ``mudou_vs_pai`` de cada resultado."""
    resultados, mudancas = [], []
    for r in linha["resultados"]:
        extra = r["extra"]
        mudou = extra.get("mudou_vs_pai")
        resultados.append(
            ResultadoCaso(
                caso_id=r["caso_id"],
                descricao=extra.get("descricao", ""),
                status=r["status"],
                mudou_vs_pai=mudou,
                falhas=[FalhaCaso.model_validate(f) for f in r["falhas"]],
                obtido=r["obtido"],
                erro=extra.get("erro"),
            )
        )
        if mudou:
            antes, depois = mudou.split("->")
            mudancas.append(Mudanca(caso_id=r["caso_id"], antes=antes, depois=depois))
    return Execucao(
        execucao_id=linha["id"],
        versao=linha["versao"],
        executada_em=linha["executada_em"],
        total=linha["total"],
        passou=linha["passou"],
        falhou=linha["falhou"],
        comparada_com=linha["comparada_com"],
        resultados=resultados,
        mudancas=mudancas,
    )


def executar(ctx: Contexto, versao: str, ids: list[str] | None = None) -> Execucao:
    """Roda os casos (todos, ou só os de ``ids``) na versão, grava a execução e a devolve.

    Versão inexistente e id de caso inexistente são 404 (nada é gravado). Os resultados seguem a ordem do arquivo
    de casos. ``comparada_com`` é o ``meta.pai`` da versão, quando o pai já tem alguma execução. A comparação é
    por caso (ruling 14): o "antes" de cada caso é o status na execução mais recente do pai que o contém, e
    ``ausente`` só vale para o caso que nenhuma execução do pai rodou. A gravação do cabeçalho e dos resultados é
    uma transação só; antes dela, o índice ``versoes_base`` é sincronizado (``sincronizar_indice`` abre a própria
    transação, por isso fica fora do ``with``). Quem chamar isto de dentro de um ``with ctx.conn:`` (Task 11) comete
    a transação aberta antes da hora.
    """
    base = base_servico.obter_versao(ctx, versao)  # 404 se a versão não existe
    lidos = _ler_casos(ctx)
    if ids is not None:
        existentes = {c.id for c in lidos}
        faltam = list(dict.fromkeys(i for i in ids if i not in existentes))
        if faltam:
            raise nao_encontrado(_mensagem_ids(faltam))
        pedidos = set(ids)
        lidos = [c for c in lidos if c.id in pedidos]

    motor = para_motor(base)
    resultados = [_rodar(motor, lido) for lido in lidos]

    pai = base.meta.pai
    antes_por_caso = _status_no_pai(ctx, pai, {r["caso_id"] for r in resultados}) if pai else None
    if antes_por_caso is not None:
        _comparar_com_o_pai(resultados, antes_por_caso)

    base_servico.sincronizar_indice(ctx)  # antes do with: a execução tem chave estrangeira para versoes_base
    with ctx.conn:
        execucao_id = repo.inserir_execucao(
            ctx.conn,
            versao=versao,
            comparada_com=pai if antes_por_caso is not None else None,
            resultados=resultados,
            agora=ctx.config.agora(),
        )
    return _montar(repo.obter_execucao(ctx.conn, execucao_id))


# --- consulta --------------------------------------------------------------------------------


def _exigir_versao(ctx: Contexto, versao: str) -> None:
    """404 se a versão não existe no disco (sem carregar a base)."""
    if versao not in ctx.repo.listar_versoes():
        raise nao_encontrado(f"Versão {mostrar_valor(versao)} não encontrada.")


def obter_execucao(ctx: Contexto, versao: str, execucao_id: str) -> Execucao:
    """A execução com todos os resultados; a de outra versão é 404, como se não existisse."""
    _exigir_versao(ctx, versao)
    linha = repo.obter_execucao(ctx.conn, execucao_id)
    if linha is None or linha["versao"] != versao:
        raise nao_encontrado(f"Execução {mostrar_valor(execucao_id)} não encontrada.")
    return _montar(linha)


def listar_execucoes(ctx: Contexto, versao: str) -> ListaExecucoes:
    """Só o cabeçalho de cada execução da versão (sem ``resultados``), a mais nova primeiro."""
    _exigir_versao(ctx, versao)
    return ListaExecucoes(
        itens=[
            ExecucaoCabecalho(
                execucao_id=linha["id"],
                executada_em=linha["executada_em"],
                total=linha["total"],
                passou=linha["passou"],
                falhou=linha["falhou"],
            )
            for linha in repo.listar_execucoes(ctx.conn, versao)
        ]
    )
