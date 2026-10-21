"""Repositórios SQLite: o único lugar da API com SQL. Nenhuma lógica de domínio.

Funções de módulo que recebem ``conn`` (de ``api.db.conexao.abrir``). Nenhuma faz ``commit``: quem chama
agrupa as escritas de uma ação em ``with conn:`` (uma transação só). Linhas voltam como ``dict``; as colunas
``*_json`` são decodificadas e perdem o sufixo (``snapshot_json`` -> ``snapshot``). Datas e horas são ISO-8601.
"""
from __future__ import annotations

import json
import sqlite3
from datetime import datetime
from fractions import Fraction

_TABELAS_COM_ID = frozenset({"animais", "sessoes", "execucoes_casos"})


# --- utilidades -----------------------------------------------------------------------------


def _json(valor: object) -> str:
    return json.dumps(valor, ensure_ascii=False)


def _instante(agora: datetime) -> str:
    return agora.isoformat(timespec="seconds")


def _dict(linha: sqlite3.Row | None) -> dict | None:
    """Linha como ``dict``, com as colunas ``*_json`` decodificadas para o nome sem sufixo."""
    if linha is None:
        return None
    saida: dict = {}
    for coluna in linha.keys():
        valor = linha[coluna]
        if coluna.endswith("_json"):
            coluna, valor = coluna.removesuffix("_json"), json.loads(valor)
        saida[coluna] = valor
    return saida


def proximo_id(conn: sqlite3.Connection, tabela: str, prefixo: str, largura: int) -> str:
    """Próximo id sequencial da tabela, como ``an_001`` (``prefixo`` sem o sublinhado; ``largura`` dígitos)."""
    if tabela not in _TABELAS_COM_ID:  # nome de tabela não é parâmetro SQL: só aceita as conhecidas
        raise ValueError(f"Tabela sem id sequencial: {tabela}")
    prefixo = prefixo.rstrip("_") + "_"
    maior = conn.execute(
        f"SELECT MAX(CAST(SUBSTR(id, ?) AS INTEGER)) FROM {tabela}", (len(prefixo) + 1,)
    ).fetchone()[0]
    return f"{prefixo}{(maior or 0) + 1:0{largura}d}"


# --- animais --------------------------------------------------------------------------------


def inserir_animal(
    conn: sqlite3.Connection, *, brinco: str, nome: str | None, ficha: dict, origens: dict, agora: datetime
) -> str:
    """Insere o animal e devolve o id. Brinco repetido levanta ``sqlite3.IntegrityError``."""
    animal_id = proximo_id(conn, "animais", "an", 3)
    instante = _instante(agora)
    conn.execute(
        "INSERT INTO animais (id, brinco, nome, ficha_json, origens_json, criado_em, atualizado_em)"
        " VALUES (?, ?, ?, ?, ?, ?, ?)",
        (animal_id, brinco, nome, _json(ficha), _json(origens), instante, instante),
    )
    return animal_id


def obter_animal(conn: sqlite3.Connection, animal_id: str) -> dict | None:
    return _dict(conn.execute("SELECT * FROM animais WHERE id = ?", (animal_id,)).fetchone())


def obter_animal_por_brinco(conn: sqlite3.Connection, brinco: str) -> dict | None:
    return _dict(conn.execute("SELECT * FROM animais WHERE brinco = ?", (brinco,)).fetchone())


def listar_animais(conn: sqlite3.Connection, busca: str | None) -> list[dict]:
    """Animais por brinco, cada um com ``ultima_sessao_id`` (ou ``None``).

    ``busca`` procura em ``brinco`` e ``nome`` sem diferenciar maiúsculas; o filtro é feito aqui,
    com ``casefold``, porque o ``lower()`` do SQLite só trata ASCII (acentos ficariam de fora).
    """
    linhas = conn.execute(
        "SELECT a.*, (SELECT s.id FROM sessoes s WHERE s.animal_id = a.id ORDER BY s.rowid DESC LIMIT 1)"
        " AS ultima_sessao_id FROM animais a ORDER BY a.brinco"
    ).fetchall()
    animais = [_dict(linha) for linha in linhas]
    termo = (busca or "").strip().casefold()
    if not termo:
        return animais
    return [a for a in animais if termo in a["brinco"].casefold() or termo in (a["nome"] or "").casefold()]


def atualizar_animal(conn: sqlite3.Connection, animal_id: str, *, ficha: dict, origens: dict, agora: datetime) -> None:
    conn.execute(
        "UPDATE animais SET ficha_json = ?, origens_json = ?, atualizado_em = ? WHERE id = ?",
        (_json(ficha), _json(origens), _instante(agora), animal_id),
    )


# --- sessões --------------------------------------------------------------------------------


def inserir_sessao(
    conn: sqlite3.Connection,
    *,
    animal_id: str,
    modo: str,
    versao_base: str,
    snapshot: dict,
    fase: str,
    agora: datetime,
) -> str:
    """Insere a sessão com ``revisao`` 1 e devolve o id."""
    sessao_id = proximo_id(conn, "sessoes", "ses", 4)
    instante = _instante(agora)
    conn.execute(
        "INSERT INTO sessoes (id, animal_id, modo, versao_base, revisao, fase, motivo_parada,"
        " bandeiras_reconhecidas_json, snapshot_json, criada_em, atualizada_em)"
        " VALUES (?, ?, ?, ?, 1, ?, NULL, '[]', ?, ?, ?)",
        (sessao_id, animal_id, modo, versao_base, fase, _json(snapshot), instante, instante),
    )
    return sessao_id


def obter_sessao(conn: sqlite3.Connection, sessao_id: str) -> dict | None:
    return _dict(conn.execute("SELECT * FROM sessoes WHERE id = ?", (sessao_id,)).fetchone())


def salvar_sessao(
    conn: sqlite3.Connection,
    sessao_id: str,
    *,
    snapshot: dict,
    fase: str,
    motivo_parada: str | None,
    modo: str,
    reconhecidas: list[str],
    agora: datetime,
    subir_revisao: bool,
) -> int:
    """Regrava o estado da sessão e devolve a ``revisao`` (sobe 1 só se ``subir_revisao``)."""
    cursor = conn.execute(
        "UPDATE sessoes SET snapshot_json = ?, fase = ?, motivo_parada = ?, modo = ?,"
        " bandeiras_reconhecidas_json = ?, atualizada_em = ?, revisao = revisao + ? WHERE id = ?",
        (_json(snapshot), fase, motivo_parada, modo, _json(reconhecidas), _instante(agora), int(subir_revisao), sessao_id),
    )
    if cursor.rowcount == 0:
        raise LookupError(f"Sessão inexistente: {sessao_id}")
    return conn.execute("SELECT revisao FROM sessoes WHERE id = ?", (sessao_id,)).fetchone()[0]


def listar_sessoes_do_animal(conn: sqlite3.Connection, animal_id: str) -> list[dict]:
    """Sessões do animal, a mais nova primeiro (os ids são sequenciais, então ``rowid`` acompanha a criação)."""
    linhas = conn.execute("SELECT * FROM sessoes WHERE animal_id = ? ORDER BY rowid DESC", (animal_id,)).fetchall()
    return [_dict(linha) for linha in linhas]


# --- projeção das respostas e das perguntas (consulta e auditoria) --------------------------


def projetar_respostas(
    conn: sqlite3.Connection,
    sessao_id: str,
    fatos: dict[str, dict],
    ordem: list[list[str]],
    modo: str,
    agora: datetime,
) -> None:
    """Grava os fatos da sessão (``{valor, cf, origem, tela_id}`` por símbolo), só os novos ou alterados.

    ``ordem`` é a ``ordem_respostas`` do motor (lotes na ordem de entrada); a coluna ``ordem`` guarda a posição
    do lote, de 1 em diante (símbolo fora de qualquer lote conta como no primeiro, igual ao motor).
    ``nao_sei`` é verdadeiro para CF 0. ``modo_na_resposta`` e ``respondida_em`` só mudam quando o valor muda.
    """
    posicao = {simbolo: n for n, lote in enumerate(ordem, start=1) for simbolo in lote}
    gravadas = {
        linha["simbolo"]: linha
        for linha in conn.execute(
            "SELECT simbolo, valor_json, nao_sei, origem, tela_id, ordem FROM respostas WHERE sessao_id = ?",
            (sessao_id,),
        )
    }
    instante = _instante(agora)
    for simbolo, fato in fatos.items():
        valor_json = _json(fato.get("valor"))
        nao_sei = int(Fraction(str(fato["cf"])) == 0)
        origem, tela_id, ordem_fato = fato.get("origem"), fato.get("tela_id"), posicao.get(simbolo, 1)
        antes = gravadas.get(simbolo)
        if antes is None:
            conn.execute(
                "INSERT INTO respostas (sessao_id, simbolo, valor_json, nao_sei, origem, tela_id, ordem,"
                " modo_na_resposta, respondida_em) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (sessao_id, simbolo, valor_json, nao_sei, origem, tela_id, ordem_fato, modo, instante),
            )
        elif (antes["valor_json"], antes["nao_sei"]) != (valor_json, nao_sei):
            conn.execute(
                "UPDATE respostas SET valor_json = ?, nao_sei = ?, origem = ?, tela_id = ?, ordem = ?,"
                " modo_na_resposta = ?, respondida_em = ? WHERE sessao_id = ? AND simbolo = ?",
                (valor_json, nao_sei, origem, tela_id, ordem_fato, modo, instante, sessao_id, simbolo),
            )
        elif (antes["origem"], antes["tela_id"], antes["ordem"]) != (origem, tela_id, ordem_fato):
            conn.execute(
                "UPDATE respostas SET origem = ?, tela_id = ?, ordem = ? WHERE sessao_id = ? AND simbolo = ?",
                (origem, tela_id, ordem_fato, sessao_id, simbolo),
            )


def projetar_perguntas(conn: sqlite3.Connection, sessao_id: str, perguntas: dict[str, dict], agora: datetime) -> None:
    """Grava as perguntas feitas (eventos ``pergunta_feita`` por símbolo) que ainda faltam.

    O motivo fica como estava quando a pergunta foi escolhida (nunca é regravado); ``ordem`` é a posição de chegada.
    """
    feitas = {linha[0] for linha in conn.execute("SELECT simbolo FROM perguntas_feitas WHERE sessao_id = ?", (sessao_id,))}
    ordem = conn.execute("SELECT COALESCE(MAX(ordem), 0) FROM perguntas_feitas WHERE sessao_id = ?", (sessao_id,)).fetchone()[0]
    instante = _instante(agora)
    for simbolo, pergunta in perguntas.items():
        if simbolo in feitas:
            continue
        ordem += 1
        conn.execute(
            "INSERT INTO perguntas_feitas (sessao_id, simbolo, ordem, motivo_json, feita_em) VALUES (?, ?, ?, ?, ?)",
            (sessao_id, simbolo, ordem, _json(pergunta.get("motivo")), instante),
        )


# --- versões da base ------------------------------------------------------------------------


def sincronizar_versao(
    conn: sqlite3.Connection,
    *,
    versao: str,
    pai: str | None,
    autor: str | None,
    data: str | None,
    nota: str | None,
    hash: str,
    agora: datetime,
) -> None:
    """Registra a versão no índice se ainda não estiver (uma já registrada não é alterada)."""
    conn.execute(
        "INSERT OR IGNORE INTO versoes_base (versao, pai, autor, data, nota, hash, criada_em)"
        " VALUES (?, ?, ?, ?, ?, ?, ?)",
        (versao, pai, autor, data, nota, hash, _instante(agora)),
    )


def listar_versoes_base(conn: sqlite3.Connection) -> list[dict]:
    return [_dict(linha) for linha in conn.execute("SELECT * FROM versoes_base ORDER BY versao")]


# --- execuções dos casos de teste -----------------------------------------------------------


def inserir_execucao(
    conn: sqlite3.Connection, *, versao: str, comparada_com: str | None, resultados: list[dict], agora: datetime
) -> str:
    """Grava o cabeçalho (com ``total``, ``passou`` e ``falhou``) e um resultado por caso; devolve o id.

    Cada resultado é ``{caso_id, status, obtido, falhas, extra}``. ``falhou`` conta só o status ``falhou``
    (um caso ``erro``, mal formado, entra no ``total`` mas em nenhum dos dois). A ``versao`` precisa estar
    em ``versoes_base`` (``sincronizar_versao``), senão levanta ``sqlite3.IntegrityError``.
    """
    execucao_id = proximo_id(conn, "execucoes_casos", "ex", 4)
    passou = sum(1 for r in resultados if r["status"] == "passou")
    falhou = sum(1 for r in resultados if r["status"] == "falhou")
    conn.execute(
        "INSERT INTO execucoes_casos (id, versao, executada_em, total, passou, falhou, comparada_com)"
        " VALUES (?, ?, ?, ?, ?, ?, ?)",
        (execucao_id, versao, _instante(agora), len(resultados), passou, falhou, comparada_com),
    )
    conn.executemany(
        "INSERT INTO resultados_casos (execucao_id, caso_id, status, obtido_json, falhas_json, extra_json)"
        " VALUES (?, ?, ?, ?, ?, ?)",
        [
            (
                execucao_id,
                r["caso_id"],
                r["status"],
                _json(r.get("obtido")),
                _json(r.get("falhas", [])),
                _json(r.get("extra", {})),
            )
            for r in resultados
        ],
    )
    return execucao_id


def obter_execucao(conn: sqlite3.Connection, execucao_id: str) -> dict | None:
    """Cabeçalho da execução mais ``resultados`` (na ordem em que foram gravados), ou ``None``."""
    execucao = _dict(conn.execute("SELECT * FROM execucoes_casos WHERE id = ?", (execucao_id,)).fetchone())
    if execucao is None:
        return None
    linhas = conn.execute("SELECT * FROM resultados_casos WHERE execucao_id = ? ORDER BY rowid", (execucao_id,))
    execucao["resultados"] = [
        {chave: valor for chave, valor in _dict(linha).items() if chave != "execucao_id"} for linha in linhas
    ]
    return execucao


def listar_execucoes(conn: sqlite3.Connection, versao: str) -> list[dict]:
    """Só o cabeçalho de cada execução da versão, a mais nova primeiro."""
    linhas = conn.execute("SELECT * FROM execucoes_casos WHERE versao = ? ORDER BY rowid DESC", (versao,))
    return [_dict(linha) for linha in linhas]


def ultima_execucao(conn: sqlite3.Connection, versao: str) -> dict | None:
    """A execução mais nova da versão, com ``resultados``, ou ``None``."""
    linha = conn.execute("SELECT id FROM execucoes_casos WHERE versao = ? ORDER BY rowid DESC LIMIT 1", (versao,)).fetchone()
    return None if linha is None else obter_execucao(conn, linha["id"])
