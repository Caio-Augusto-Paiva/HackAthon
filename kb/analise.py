"""Análise de dependências entre símbolos e regras (funções puras, sem I/O).

Tolerante a referências pendentes: símbolos não definidos são ignorados aqui;
quem as reporta é ``kb.validador``.
"""
from __future__ import annotations

import heapq

from kb.modelos import Base, Modo, Regra, Simbolo, TipoSimbolo

CAMADA: dict[TipoSimbolo, int] = {
    "pergunta": 0,
    "ficha": 0,
    "derivado": 1,
    "doenca": 2,
    "urgencia": 3,
}


def simbolos_por_id(base: Base) -> dict[str, Simbolo]:
    return {s.id: s for s in base.simbolos}


def regras_que_concluem(base: Base, simbolo_id: str) -> list[Regra]:
    """Regras cuja conclusão é ``simbolo_id``, na ordem da base."""
    return [r for r in base.regras if r.entao.simbolo == simbolo_id]


def dependencias(base: Base) -> dict[str, set[str]]:
    """Para cada símbolo concluído por alguma regra, os símbolos que suas regras leem."""
    existentes = simbolos_por_id(base)
    deps: dict[str, set[str]] = {}
    for regra in base.regras:
        if regra.entao.simbolo not in existentes:
            continue
        lidos = deps.setdefault(regra.entao.simbolo, set())
        lidos.update(c.simbolo for c in regra.se if c.simbolo in existentes)
    return deps


def encontrar_ciclo(base: Base) -> list[str] | None:
    """Caminho de um ciclo (primeiro id repetido no fim) ou ``None``. Determinístico."""
    deps = dependencias(base)
    cor: dict[str, int] = {}  # ausente = não visitado; 1 = na pilha; 2 = concluído
    pilha: list[str] = []

    def visitar(no: str) -> list[str] | None:
        cor[no] = 1
        pilha.append(no)
        for vizinho in sorted(deps.get(no, ())):
            if cor.get(vizinho) == 1:
                return pilha[pilha.index(vizinho):] + [vizinho]
            if vizinho not in cor:
                achado = visitar(vizinho)
                if achado:
                    return achado
        pilha.pop()
        cor[no] = 2
        return None

    for inicio in sorted(simbolos_por_id(base)):
        if inicio not in cor:
            achado = visitar(inicio)
            if achado:
                return achado
    return None


def ordem_topologica(base: Base) -> list[str]:
    """Todos os símbolos, entradas antes das conclusões; desempate por id."""
    deps = dependencias(base)
    pendentes = {i: len(deps.get(i, ())) for i in simbolos_por_id(base)}
    leitores: dict[str, list[str]] = {}
    for concluido, lidos in deps.items():
        for lido in lidos:
            leitores.setdefault(lido, []).append(concluido)
    prontos = [i for i, n in pendentes.items() if n == 0]
    heapq.heapify(prontos)
    ordem: list[str] = []
    while prontos:
        atual = heapq.heappop(prontos)
        ordem.append(atual)
        for leitor in leitores.get(atual, ()):
            pendentes[leitor] -= 1
            if pendentes[leitor] == 0:
                heapq.heappush(prontos, leitor)
    if len(ordem) != len(pendentes):
        raise ValueError("a base tem ciclo de dependências: " + " -> ".join(encontrar_ciclo(base) or []))
    return ordem


def perguntavel(simbolo: Simbolo, modo: Modo) -> bool:
    """Pergunta/ficha com texto não vazio para o modo."""
    if simbolo.tipo not in ("pergunta", "ficha"):
        return False
    return bool(simbolo.pergunta.get(modo, "").strip())


def simbolos_triagem(base: Base) -> set[str]:
    """União dos símbolos de todas as telas de triagem (inclusive por modo)."""
    ids: set[str] = set()
    for tela in base.meta.triagem:
        ids.update(tela.simbolos)
        for lista in (tela.simbolos_por_modo or {}).values():
            ids.update(lista)
    return ids


def derivados_de_triagem(base: Base) -> set[str]:
    """Derivados com ao menos uma regra e cujas regras só leem símbolos de triagem."""
    triagem = simbolos_triagem(base)
    resultado: set[str] = set()
    for s in base.simbolos:
        if s.tipo != "derivado":
            continue
        regras = regras_que_concluem(base, s.id)
        if regras and all(c.simbolo in triagem for r in regras for c in r.se):
            resultado.add(s.id)
    return resultado


def derivados_com_cf_negativo(base: Base) -> set[str]:
    """Derivados concluídos por alguma regra com ``cf < 0``."""
    derivados = {s.id for s in base.simbolos if s.tipo == "derivado"}
    return {r.entao.simbolo for r in base.regras if r.entao.cf < 0 and r.entao.simbolo in derivados}
