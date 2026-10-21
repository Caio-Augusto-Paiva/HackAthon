"""Conversão 1:1 entre a base de conhecimento e um grafo bipartido (símbolos <-> regras).

O editor visual (React Flow) trabalha com ``Grafo``; o motor e o disco, com ``Base``.
``grafo_para_base`` reconstrói a base só a partir de ``nos`` e ``arestas``.
"""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from kb.analise import simbolos_triagem
from kb.modelos import Base, Meta, Op, Posicao, Regra, Simbolo

_CAMPOS_CONDICAO = ("op", "valor", "negado", "cf_minimo", "cf_maximo")


class No(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    tipo_no: Literal["simbolo", "regra"]
    triagem: bool = False
    dados: dict


class Aresta(BaseModel):
    """``condicao``: símbolo -> regra; ``conclusao``: regra -> símbolo."""

    model_config = ConfigDict(extra="forbid")

    id: str
    papel: Literal["condicao", "conclusao"]
    origem: str
    destino: str
    ordem: int = 0
    op: Op | None = None
    valor: bool | float | str | list[str] | None = None
    negado: bool | None = None
    cf_minimo: float | None = None
    cf_maximo: float | None = None
    cf: float | None = None


class Grafo(BaseModel):
    model_config = ConfigDict(extra="forbid")

    versao: str | None = None
    meta: Meta
    nos: list[No]
    arestas: list[Aresta]
    layout: dict[str, Posicao] = Field(default_factory=dict)


def base_para_grafo(base: Base) -> Grafo:
    triagem = simbolos_triagem(base)
    nos = [
        No(id=s.id, tipo_no="simbolo", triagem=s.id in triagem, dados=s.model_dump(mode="json"))
        for s in base.simbolos
    ]
    arestas: list[Aresta] = []
    for regra in base.regras:
        nos.append(No(id=regra.id, tipo_no="regra",
                      dados=regra.model_dump(mode="json", exclude={"se", "entao"})))
        for i, cond in enumerate(regra.se):
            extras = {c: getattr(cond, c) for c in _CAMPOS_CONDICAO}
            arestas.append(Aresta(id=f"{regra.id}:se:{i}", papel="condicao", origem=cond.simbolo,
                                  destino=regra.id, ordem=i, **extras))
        arestas.append(Aresta(id=f"{regra.id}:entao", papel="conclusao", origem=regra.id,
                              destino=regra.entao.simbolo, cf=regra.entao.cf))
    return Grafo(versao=base.meta.versao, meta=base.meta.model_copy(deep=True), nos=nos,
                 arestas=arestas, layout={k: v.model_copy() for k, v in base.layout.items()})


def grafo_para_base(grafo: Grafo) -> Base:
    tipos: dict[str, str] = {}
    for no in grafo.nos:
        if no.id in tipos:
            raise ValueError(f"nó duplicado no grafo: {no.id!r}")
        tipos[no.id] = no.tipo_no

    condicoes: dict[str, list[Aresta]] = {}
    conclusoes: dict[str, list[Aresta]] = {}
    for aresta in grafo.arestas:
        for ponta in (aresta.origem, aresta.destino):
            if ponta not in tipos:
                raise ValueError(f"aresta {aresta.id!r} aponta para o nó inexistente {ponta!r}")
        if aresta.papel == "condicao":
            if tipos[aresta.origem] != "simbolo" or tipos[aresta.destino] != "regra":
                raise ValueError(
                    f"aresta {aresta.id!r}: condição deve ir de símbolo para regra "
                    f"({aresta.origem!r} -> {aresta.destino!r})")
            condicoes.setdefault(aresta.destino, []).append(aresta)
        else:
            if tipos[aresta.origem] != "regra" or tipos[aresta.destino] != "simbolo":
                raise ValueError(
                    f"aresta {aresta.id!r}: conclusão deve ir de regra para símbolo "
                    f"({aresta.origem!r} -> {aresta.destino!r})")
            conclusoes.setdefault(aresta.origem, []).append(aresta)

    simbolos = [Simbolo.model_validate(n.dados) for n in grafo.nos if n.tipo_no == "simbolo"]
    regras = []
    for no in (n for n in grafo.nos if n.tipo_no == "regra"):
        concl = conclusoes.get(no.id, [])
        if len(concl) != 1:
            raise ValueError(f"a regra {no.id!r} deve ter exatamente uma conclusão, tem {len(concl)}")
        conds = sorted(condicoes.get(no.id, []), key=lambda a: a.ordem)
        for anterior, atual in zip(conds, conds[1:]):
            if anterior.ordem == atual.ordem:
                raise ValueError(
                    f"regra {no.id!r}: condições {anterior.id!r} e {atual.id!r} "
                    f"têm a mesma ordem ({atual.ordem})")
        se = []
        for a in conds:
            cond = {"simbolo": a.origem}
            cond.update({c: getattr(a, c) for c in _CAMPOS_CONDICAO if getattr(a, c) is not None})
            se.append(cond)
        entao = {"simbolo": concl[0].destino, "cf": concl[0].cf}
        regras.append(Regra.model_validate({**no.dados, "se": se, "entao": entao}))

    return Base(meta=grafo.meta.model_copy(deep=True), simbolos=simbolos, regras=regras,
                layout={k: v.model_copy() for k, v in grafo.layout.items()})
