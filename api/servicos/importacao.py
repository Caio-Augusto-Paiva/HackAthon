"""Importação de prontuário (CSV ou JSON): a fonte de dados externa que alimenta a ficha dos animais.

O formato vem da extensão. A chave é o ``brinco``: o que já existe é atualizado (só os campos cujo valor mudou,
que passam a ter origem ``importacao``) e o que não existe é criado. Célula vazia ou ``null`` = ausente: não apaga
o valor que já existe. Linha com erro vai para ``rejeitados`` e não grava nada; as outras seguem. ``gravar=False``
só simula. Só dados fictícios, como em todo o projeto.
"""
from __future__ import annotations

import csv
import io
import json
import re
from dataclasses import dataclass, field

from api.contexto import Contexto
from api.db import repositorios as repo
from api.erros import importacao_invalida
from api.schemas.animal import ErroCampo, LinhaAtualizada, LinhaImportada, LinhaRejeitada, ResultadoImportacao
from api.servicos.animal_servico import base_ativa, texto_legivel
from api.servicos.ficha import campos_da_ficha, completar_ficha, mostrar_valor, validar_ficha
from kb.modelos import Dominio

LIMITE_BYTES = 5 * 1024 * 1024

_VERDADEIRO = frozenset({"true", "sim", "1"})
_FALSO = frozenset({"false", "não", "nao", "0"})
_INTEIRO = re.compile(r"[+-]?[0-9]+")
_DECIMAL = re.compile(r"[+-]?[0-9]+[.,][0-9]+")


@dataclass
class _Linha:
    """Uma linha do arquivo já separada em brinco, nome e ficha (ainda não validada)."""

    numero: int  # CSV: a linha do arquivo (cabeçalho = 1); JSON: índice + 1
    brinco: str | None = None
    nome: str | None = None
    ficha: dict = field(default_factory=dict)
    erros: list[ErroCampo] = field(default_factory=list)


# --- arquivo -> linhas -----------------------------------------------------------------------


def _formato(nome_arquivo: str) -> str:
    extensao = nome_arquivo.rpartition(".")[2].lower() if "." in nome_arquivo else ""
    if extensao not in ("csv", "json"):
        raise importacao_invalida("Formato não suportado: envie um arquivo .csv ou .json.")
    return extensao


def _decodificar(conteudo: bytes) -> str:
    if len(conteudo) > LIMITE_BYTES:
        raise importacao_invalida(f"Arquivo grande demais (máximo {LIMITE_BYTES // (1024 * 1024)} MB).")
    try:
        texto = conteudo.decode("utf-8-sig")  # tira o BOM que o Excel grava
    except UnicodeDecodeError:
        raise importacao_invalida("O arquivo não é um texto UTF-8 legível.") from None
    if "\x00" in texto:
        raise importacao_invalida("O arquivo parece binário, não texto.")
    return texto


def _linha_csv(numero: int, cabecalho: list[str], registro: list[str]) -> _Linha:
    linha = _Linha(numero)
    if len(registro) > len(cabecalho) and any(c.strip() for c in registro[len(cabecalho):]):
        linha.erros.append(ErroCampo(campo="linha", mensagem="A linha tem mais colunas do que o cabeçalho."))
    for coluna, celula in zip(cabecalho, registro):
        texto = celula.strip()
        if not coluna or not texto:  # célula vazia = ausente
            continue
        if coluna == "brinco":
            linha.brinco = texto
        elif coluna == "nome":
            linha.nome = texto
        else:
            linha.ficha[coluna] = texto
    return linha


def _ler_csv(texto: str) -> list[_Linha]:
    primeira = next((p for p in texto.splitlines() if p.strip()), "")
    separador = ";" if primeira.count(";") > primeira.count(",") else ","
    leitor = csv.reader(io.StringIO(texto, newline=""), delimiter=separador)
    cabecalho: list[str] | None = None
    linhas: list[_Linha] = []
    anterior = 0
    try:
        for registro in leitor:
            inicio, anterior = anterior + 1, leitor.line_num  # um registro entre aspas pode ocupar várias linhas
            if not any(c.strip() for c in registro):
                continue
            if cabecalho is None:
                cabecalho = [c.strip().lower() for c in registro]
                nomes = [c for c in cabecalho if c]
                if "brinco" not in nomes:
                    raise importacao_invalida("O cabeçalho precisa ter a coluna 'brinco'.")
                if len(nomes) != len(set(nomes)):
                    raise importacao_invalida("O cabeçalho tem colunas repetidas.")
                continue
            linhas.append(_linha_csv(inicio, cabecalho, registro))
    except csv.Error:
        raise importacao_invalida("O arquivo não é um CSV legível.") from None
    if cabecalho is None:
        raise importacao_invalida("O arquivo está vazio: falta o cabeçalho.")
    return linhas


def _linha_json(numero: int, item: object) -> _Linha:
    linha = _Linha(numero)
    if not isinstance(item, dict):
        linha.erros.append(ErroCampo(campo="animal", mensagem="Cada item deve ser um objeto."))
        return linha
    for chave in item:
        if chave not in ("brinco", "nome", "ficha"):
            linha.erros.append(
                ErroCampo(campo=str(chave), mensagem="Campo desconhecido; os dados da ficha ficam dentro de 'ficha'.")
            )
    brinco, nome, ficha = item.get("brinco"), item.get("nome"), item.get("ficha")
    if isinstance(brinco, str):
        linha.brinco = brinco.strip()
    elif brinco is not None:
        linha.erros.append(ErroCampo(campo="brinco", mensagem="Deve ser um texto."))
    if isinstance(nome, str):
        linha.nome = nome.strip() or None
    elif nome is not None:
        linha.erros.append(ErroCampo(campo="nome", mensagem="Deve ser um texto."))
    if isinstance(ficha, dict):
        linha.ficha = ficha
    elif ficha is not None:
        linha.erros.append(ErroCampo(campo="ficha", mensagem="Deve ser um objeto."))
    return linha


def _ler_json(texto: str) -> list[_Linha]:
    try:
        dados = json.loads(texto)
    except (ValueError, RecursionError):
        raise importacao_invalida("O arquivo não é um JSON válido.") from None
    if not texto_legivel(dados):
        raise importacao_invalida("O JSON tem caracteres Unicode inválidos.")
    animais = dados.get("animais") if isinstance(dados, dict) else None
    if not isinstance(animais, list):
        raise importacao_invalida('O JSON deve ter o formato {"animais": [ ... ]}.')
    return [_linha_json(i, item) for i, item in enumerate(animais, start=1)]


# --- texto do CSV -> valor do domínio --------------------------------------------------------


def _numero(texto: str) -> int | float | None:
    if _INTEIRO.fullmatch(texto):
        return int(texto)
    if _DECIMAL.fullmatch(texto):
        return float(texto.replace(",", "."))
    return None


def _converter(dominio: Dominio | None, texto: str) -> tuple[bool, object]:
    """``(ok, valor)``: o texto da célula no tipo do domínio; ``dominio`` ``None`` é a data, que fica como texto."""
    if dominio is None:
        return True, texto
    if dominio.tipo == "booleano":
        chave = texto.casefold()
        if chave in _VERDADEIRO:
            return True, True
        return (True, False) if chave in _FALSO else (False, None)
    if dominio.tipo == "categorico":  # "Cruzada" da planilha casa com "cruzada" da base; o resto o validador recusa
        return True, {v.casefold(): v for v in dominio.valores}.get(texto.casefold(), texto)
    numero = _numero(texto)
    return numero is not None, numero


_MENSAGEM_CONVERSAO = {
    "booleano": "deve ser verdadeiro ou falso (use true, false, sim, não, 1 ou 0).",
    "numerico": "deve ser um número.",
}


def _converter_ficha(campos: dict[str, Dominio | None], ficha: dict) -> tuple[dict, list[ErroCampo]]:
    convertida: dict = {}
    erros: list[ErroCampo] = []
    for campo, texto in ficha.items():
        ok, valor = _converter(campos.get(campo), texto)  # campo desconhecido segue como texto: o validador o recusa
        if ok:
            convertida[campo] = valor
        else:
            motivo = _MENSAGEM_CONVERSAO[campos[campo].tipo]
            erros.append(ErroCampo(campo=campo, mensagem=f"Valor {mostrar_valor(texto)} {motivo}"))
    return convertida, erros


# --- importar --------------------------------------------------------------------------------


def _igual(a: object, b: object) -> bool:
    return isinstance(a, bool) == isinstance(b, bool) and a == b  # True != 1 aqui; 3 == 3.0


def importar(ctx: Contexto, nome_arquivo: str, conteudo: bytes, gravar: bool) -> ResultadoImportacao:
    formato = _formato(nome_arquivo)
    texto = _decodificar(conteudo)
    linhas = _ler_csv(texto) if formato == "csv" else _ler_json(texto)
    base = base_ativa(ctx)
    campos = campos_da_ficha(base)

    criados: list[LinhaImportada] = []
    atualizados: list[LinhaAtualizada] = []
    rejeitados: list[LinhaRejeitada] = []
    a_criar: list[tuple[str, str | None, dict, dict]] = []  # brinco, nome, ficha, origens
    a_atualizar: list[tuple[dict, list[str], dict]] = []  # animal gravado, campos que mudam, valores informados
    vistos: dict[str, int] = {}

    for linha in linhas:
        erros = list(linha.erros)
        if linha.brinco:
            if linha.brinco in vistos:
                repetido = f"Brinco repetido no arquivo (já aparece na linha {vistos[linha.brinco]})."
                erros.append(ErroCampo(campo="brinco", mensagem=repetido))
            else:
                vistos[linha.brinco] = linha.numero
        elif not any(e.campo == "brinco" for e in erros):
            erros.append(ErroCampo(campo="brinco", mensagem="Brinco obrigatório."))
        ficha = linha.ficha
        if formato == "csv":
            ficha, erros_de_conversao = _converter_ficha(campos, ficha)
            erros += erros_de_conversao
        erros += validar_ficha(base, ficha)
        if erros:
            rejeitados.append(LinhaRejeitada(linha=linha.numero, erros=erros))
            continue

        informados = {campo: valor for campo, valor in ficha.items() if valor is not None}
        atual = repo.obter_animal_por_brinco(ctx.conn, linha.brinco)
        if atual is None:
            criados.append(LinhaImportada(linha=linha.numero, brinco=linha.brinco))
            origens = {campo: "importacao" for campo in campos if campo in informados}
            a_criar.append((linha.brinco, linha.nome, completar_ficha(base, informados), origens))
        else:
            mudaram = [c for c in campos if c in informados and not _igual(atual["ficha"].get(c), informados[c])]
            atualizados.append(LinhaAtualizada(linha=linha.numero, brinco=linha.brinco, campos=mudaram))
            if mudaram:
                a_atualizar.append((atual, mudaram, informados))

    if gravar:
        agora = ctx.config.agora()
        with ctx.conn:  # tudo ou nada
            for brinco, nome, ficha, origens in a_criar:
                repo.inserir_animal(ctx.conn, brinco=brinco, nome=nome, ficha=ficha, origens=origens, agora=agora)
            for atual, mudaram, informados in a_atualizar:
                ficha = {**completar_ficha(base, atual["ficha"]), **{c: informados[c] for c in mudaram}}
                origens = {**atual["origens"], **{c: "importacao" for c in mudaram}}
                repo.atualizar_animal(ctx.conn, atual["id"], ficha=ficha, origens=origens, agora=agora)
    return ResultadoImportacao(
        formato=formato, gravado=gravar, criados=criados, atualizados=atualizados, rejeitados=rejeitados
    )
