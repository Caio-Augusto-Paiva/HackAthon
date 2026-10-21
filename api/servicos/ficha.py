"""Ficha do animal: validação pelo domínio da base, ``dias_em_lactacao`` derivado e conversão para o motor.

A ficha grava ``data_ultimo_parto`` (AAAA-MM-DD). O símbolo de triagem ``dias_em_lactacao`` (o ``campo_ficha``
de mesmo nome) é calculado dela na leitura e na criação da sessão; por isso não é um campo de entrada.
Os demais campos são os ``campo_ficha`` dos símbolos ``tipo == "ficha"`` da base. Valor ``null`` = ausente.
Funções puras: não tocam banco nem relógio (o ``hoje`` vem de quem chama).
"""
from __future__ import annotations

import math
import re
from datetime import date

from api.schemas.animal import ErroCampo
from kb.modelos import Base, Dominio, Simbolo

CAMPO_DATA_PARTO = "data_ultimo_parto"
CAMPO_DIAS = "dias_em_lactacao"

_ISO = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}")  # fromisoformat sozinho também aceita 20261014 e 2026-W42-3
_LIMITE_TEXTO = 40


def _data(texto: object) -> date | None:
    if not isinstance(texto, str) or not _ISO.fullmatch(texto):
        return None
    try:
        return date.fromisoformat(texto)
    except ValueError:  # 2026-02-30
        return None


def dias_em_lactacao(data_ultimo_parto: str | None, hoje: date) -> int | None:
    """Dias desde o parto; ``None`` se a data é ausente, inválida ou está no futuro."""
    parto = _data(data_ultimo_parto)
    if parto is None or parto > hoje:
        return None
    return (hoje - parto).days


# --- campos e domínios -----------------------------------------------------------------------


def _simbolos_de_ficha(base: Base) -> list[Simbolo]:
    return [s for s in base.simbolos if s.tipo == "ficha" and s.campo_ficha and s.campo_ficha != CAMPO_DATA_PARTO]


def campos_da_ficha(base: Base) -> dict[str, Dominio | None]:
    """Campos de entrada da ficha, na ordem da base: ``data_ultimo_parto`` primeiro (domínio ``None`` = data ISO).

    Fica de fora o ``campo_ficha`` ``dias_em_lactacao``: é calculado de ``data_ultimo_parto``.
    """
    campos: dict[str, Dominio | None] = {CAMPO_DATA_PARTO: None}
    for simbolo in _simbolos_de_ficha(base):
        if simbolo.campo_ficha != CAMPO_DIAS:
            campos.setdefault(simbolo.campo_ficha, simbolo.dominio)
    return campos


def completar_ficha(base: Base, ficha: dict) -> dict:
    """Todos os campos da ficha, na ordem da base (``null`` onde falta); campo fora da base é mantido no fim."""
    completa: dict = {campo: None for campo in campos_da_ficha(base)}
    completa.update(ficha)
    return completa


# --- validação -------------------------------------------------------------------------------


def mostrar_valor(valor: object) -> str:
    """O valor como entra numa mensagem: curto, sem despejar texto ou estrutura enviados pelo cliente."""
    if isinstance(valor, str):
        return repr(valor if len(valor) <= _LIMITE_TEXTO else valor[: _LIMITE_TEXTO - 3] + "...")
    if isinstance(valor, bool):
        return "true" if valor else "false"
    if isinstance(valor, float):
        if math.isnan(valor):
            return "NaN"
        if math.isinf(valor):
            return "Infinity" if valor > 0 else "-Infinity"
        return f"{valor:g}"
    if isinstance(valor, int):
        return str(valor) if abs(valor) < 10**15 else "(número enorme)"
    return "(lista)" if isinstance(valor, list) else "(objeto)" if isinstance(valor, dict) else "(outro tipo)"


def _numero(valor: float) -> str:
    return f"{valor:g}"


def _erro_de_valor(dominio: Dominio | None, valor: object) -> str | None:
    """Mensagem de erro se ``valor`` (já não nulo) não cabe no domínio; ``None`` se cabe."""
    if dominio is None:
        if _data(valor) is None:
            return f"Valor {mostrar_valor(valor)} não é uma data AAAA-MM-DD válida."
        return None
    if dominio.tipo == "booleano":
        return None if type(valor) is bool else f"Valor {mostrar_valor(valor)} deve ser verdadeiro ou falso."
    if dominio.tipo == "categorico":
        if isinstance(valor, str) and valor in dominio.valores:
            return None
        return f"Valor {mostrar_valor(valor)} fora de {'/'.join(dominio.valores)}."
    # numérico: bool é int em Python, e NaN/Infinity passam pelo json do Python
    if isinstance(valor, bool) or not isinstance(valor, (int, float)):
        return f"Valor {mostrar_valor(valor)} deve ser um número."
    if isinstance(valor, float) and not math.isfinite(valor):
        return f"Valor {mostrar_valor(valor)} deve ser um número finito."
    abaixo = dominio.min is not None and valor < dominio.min
    acima = dominio.max is not None and valor > dominio.max
    if abaixo or acima:
        if dominio.min is not None and dominio.max is not None:
            faixa = f"{_numero(dominio.min)} a {_numero(dominio.max)}"
        else:
            faixa = f">= {_numero(dominio.min)}" if dominio.min is not None else f"<= {_numero(dominio.max)}"
        return f"Valor {mostrar_valor(valor)} fora do intervalo {faixa}."
    return None


def validar_ficha(base: Base, ficha: dict) -> list[ErroCampo]:
    """Erros por campo (lista vazia = ficha válida). ``null`` é aceito (= ausente); campo desconhecido é erro."""
    campos = campos_da_ficha(base)
    erros: list[ErroCampo] = []
    for campo, valor in ficha.items():
        if campo == CAMPO_DIAS:
            texto = f"Calculado a partir de {CAMPO_DATA_PARTO}; informe a data do último parto."
        elif campo not in campos:
            texto = "Campo desconhecido."
        elif valor is None:
            continue
        else:
            texto = _erro_de_valor(campos[campo], valor)
        if texto:
            erros.append(ErroCampo(campo=str(campo), mensagem=texto))
    return erros


# --- ficha -> motor --------------------------------------------------------------------------


def ficha_para_motor(base: Base, ficha: dict, hoje: date) -> dict[str, object]:
    """Fatos de ficha para ``engine.sessao.Sessao``: chave = **id do símbolo**, só o que tem valor.

    O símbolo cujo ``campo_ficha`` é ``dias_em_lactacao`` vem de ``data_ultimo_parto`` e hoje. Fica de fora (e a
    pergunta é feita na triagem) o que é ``null``, o que a base atual não aceita mais e os dias que não dá para
    calcular (data ausente, inválida, no futuro ou fora do domínio): nunca é erro.
    """
    fatos: dict[str, object] = {}
    for simbolo in _simbolos_de_ficha(base):
        if simbolo.campo_ficha == CAMPO_DIAS:
            valor = dias_em_lactacao(ficha.get(CAMPO_DATA_PARTO), hoje)
        else:
            valor = ficha.get(simbolo.campo_ficha)
        if valor is not None and _erro_de_valor(simbolo.dominio, valor) is None:
            fatos[simbolo.id] = valor
    return fatos
