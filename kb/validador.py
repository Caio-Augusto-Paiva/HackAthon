"""Validação semântica da base de conhecimento (sem I/O, determinística).

``validar`` recebe uma ``Base`` já carregada e devolve um ``Relatorio`` com erros
(E01-E20) e avisos (W01-W03). ``validar_dados`` aceita JSON cru e converte falhas
de estrutura em erros ``E00``; nunca levanta. Cada código é uma função privada.
"""
from __future__ import annotations

import re
from collections import Counter
from typing import Literal

from pydantic import BaseModel, ValidationError

from kb.analise import (
    CAMADA,
    derivados_com_cf_negativo,
    derivados_de_triagem,
    encontrar_ciclo,
    perguntavel,
    regras_que_concluem,
    simbolos_por_id,
    simbolos_triagem,
)
from kb.modelos import Base, Condicao, DominioCategorico, DominioNumerico, Regra, Simbolo

CODIGOS: dict[str, str] = {
    "E00": "estrutura", "E01": "simbolo_indefinido", "E02": "id_duplicado",
    "E03": "valor_invalido", "E04": "cf_fora_do_limite", "E05": "ciclo",
    "E06": "regra_inalcancavel", "E07": "bandeira_sem_chamar_agora",
    "E08": "bandeira_sem_triagem", "E09": "doenca_sem_regra",
    "E10": "doenca_sem_regra_produtor", "E11": "cobertura_triagem", "E12": "camada",
    "E13": "doenca_sem_gravidade", "E14": "derivado_max_negativo",
    "E15": "limite_cf_invalido", "E16": "tela_sem_texto",
    "E17": "limiares_fora_de_ordem", "E18": "regra_sem_fonte",
    "E19": "classe_incompativel", "E20": "id_invalido",
    "W01": "simbolo_nao_usado", "W02": "regras_contraditorias", "W03": "suposicoes_pendentes",
}

_ID_SIMBOLO = re.compile(r"[a-z0-9_]+")
_ID_REGRA = re.compile(r"[A-Za-z0-9_-]+")
_CONCEITOS = ("derivado", "doenca", "urgencia")  # símbolos concluídos por regras (booleanos)
_ORDEM_LIMIARES = ("descarte", "0", "premissa", "hipotese_relevante", "exaustao", "potencial", "confirmacao")
_MODOS = ("produtor", "veterinario")


class Alvo(BaseModel):
    tipo: Literal["simbolo", "regra", "tela", "meta"]
    id: str


class Problema(BaseModel):
    codigo: str
    numero: str
    severidade: Literal["erro", "aviso"]
    alvo: Alvo | None
    mensagem: str


class Resumo(BaseModel):
    simbolos: int
    regras: int
    suposicao_a_validar: int


class Relatorio(BaseModel):
    valida: bool
    erros: list[Problema]
    avisos: list[Problema]
    resumo: Resumo


# --- ajudantes ------------------------------------------------------------

def _p(numero: str, alvo: Alvo | None, mensagem: str) -> Problema:
    return Problema(
        codigo=CODIGOS[numero], numero=numero, alvo=alvo, mensagem=mensagem,
        severidade="erro" if numero.startswith("E") else "aviso",
    )


def _regra(r: Regra) -> Alvo:
    return Alvo(tipo="regra", id=r.id)


def _simb(s: Simbolo) -> Alvo:
    return Alvo(tipo="simbolo", id=s.id)


def _ids_da_tela(tela) -> list[str]:
    ids = list(tela.simbolos)
    for lista in (tela.simbolos_por_modo or {}).values():
        ids.extend(lista)
    return list(dict.fromkeys(ids))


def _conceito(s: Simbolo) -> bool:
    return s.tipo in _CONCEITOS


# --- erros ----------------------------------------------------------------

def _e01_simbolo_indefinido(base: Base) -> list[Problema]:
    existentes = simbolos_por_id(base)
    saida = []
    for r in base.regras:
        for sid in dict.fromkeys([c.simbolo for c in r.se] + [r.entao.simbolo]):
            if sid not in existentes:
                saida.append(_p("E01", _regra(r), f"A regra '{r.id}' usa o símbolo '{sid}', que não está definido."))
    for tela in base.meta.triagem:
        for sid in _ids_da_tela(tela):
            if sid not in existentes:
                saida.append(_p("E01", Alvo(tipo="tela", id=tela.id), f"A tela '{tela.id}' usa o símbolo '{sid}', que não está definido."))
    return saida


def _e02_id_duplicado(base: Base) -> list[Problema]:
    ids_simbolos = {s.id for s in base.simbolos}
    contagem = Counter([s.id for s in base.simbolos] + [r.id for r in base.regras])
    return [
        _p("E02", Alvo(tipo="simbolo" if i in ids_simbolos else "regra", id=i),
           f"O id '{i}' aparece {n} vezes entre símbolos e regras; os ids devem ser únicos.")
        for i, n in sorted(contagem.items()) if n > 1
    ]


def _motivo_valor(s: Simbolo, c: Condicao) -> str | None:
    """Motivo pelo qual ``c.valor``/``c.op`` não servem ao domínio de ``s`` (ou ``None``)."""
    v = c.valor
    if v is None:
        return "o valor é nulo"
    dominio = s.dominio if not _conceito(s) else None  # derivado/doença/urgência são booleanos
    if isinstance(dominio, DominioCategorico):
        if c.op in ("=", "≠"):
            if not isinstance(v, str):
                return f"o valor {v!r} não é texto"
            candidatos = [v]
        elif c.op == "em":
            if not isinstance(v, list) or not v:
                return "o operador 'em' exige uma lista não vazia de valores"
            candidatos = v
        else:
            return f"o operador '{c.op}' não vale para símbolo categórico"
        fora = [x for x in candidatos if x not in dominio.valores]
        return f"valor(es) {fora} fora dos valores permitidos {dominio.valores}" if fora else None
    if isinstance(dominio, DominioNumerico):
        if c.op == "em":
            return "o operador 'em' não vale para símbolo numérico"
        if isinstance(v, bool) or not isinstance(v, (int, float)):
            return f"o valor {v!r} não é número"
        if (dominio.min is not None and v < dominio.min) or (dominio.max is not None and v > dominio.max):
            return f"o valor {v} está fora do intervalo [{dominio.min}, {dominio.max}]"
        return None
    if c.op != "=" or v is not True:
        return "símbolo booleano só aceita '=' com valor verdadeiro (use 'negado' para expressar 'não')"
    return None


def _e03_valor_invalido(base: Base) -> list[Problema]:
    existentes = simbolos_por_id(base)
    saida = []
    for r in base.regras:
        for c in r.se:
            s = existentes.get(c.simbolo)
            motivo = _motivo_valor(s, c) if s else None
            if motivo:
                saida.append(_p("E03", _regra(r), f"Na regra '{r.id}', condição sobre '{c.simbolo}': {motivo}."))
    return saida


def _e04_cf_fora_do_limite(base: Base) -> list[Problema]:
    return [
        _p("E04", _regra(r), f"A regra '{r.id}' tem cf {r.entao.cf}, fora de [-0,99; +0,99].")
        for r in base.regras if not -0.99 <= r.entao.cf <= 0.99
    ]


def _e05_ciclo(base: Base) -> list[Problema]:
    ciclo = encontrar_ciclo(base)
    if not ciclo:
        return []
    fluxo = ciclo[::-1]  # encontrar_ciclo vai do concluído ao lido; aqui, ordem do fluxo de dados
    return [_p("E05", Alvo(tipo="simbolo", id=fluxo[0]),
               f"Ciclo: {' -> '.join(fluxo)}. Um símbolo não pode depender, direta ou indiretamente, de si mesmo.")]


def _e06_regra_inalcancavel(base: Base) -> list[Problema]:
    existentes = simbolos_por_id(base)
    concluidos = {r.entao.simbolo for r in base.regras}
    negativos = {r.entao.simbolo for r in base.regras if r.entao.cf < 0}
    triagem = simbolos_triagem(base)
    saida = []
    for r in base.regras:
        motivos = []
        for c in r.se:
            s = existentes.get(c.simbolo)
            if s is None:
                continue
            if _conceito(s):
                if s.id not in concluidos:
                    motivos.append(f"nenhuma regra conclui '{s.id}'")
                elif c.negado and s.id not in negativos:
                    motivos.append(f"'{s.id}' é negado, mas nenhuma regra o conclui com cf negativo")
            elif not (perguntavel(s, "produtor") or perguntavel(s, "veterinario") or s.id in triagem or s.campo_ficha):
                motivos.append(f"'{s.id}' não tem texto de pergunta, não está na triagem nem tem campo de ficha")
        for motivo in dict.fromkeys(motivos):
            saida.append(_p("E06", _regra(r), f"A regra '{r.id}' nunca pode disparar: {motivo}."))
    return saida


def _e07_bandeira_sem_chamar_agora(base: Base) -> list[Problema]:
    return [
        _p("E07", _regra(r), f"A bandeira vermelha '{r.id}' conclui '{r.entao.simbolo}'; deve concluir 'chamar_agora'.")
        for r in base.regras if r.classe == "bandeira_vermelha" and r.entao.simbolo != "chamar_agora"
    ]


def _e08_bandeira_sem_triagem(base: Base) -> list[Problema]:
    existentes = simbolos_por_id(base)
    permitidos = simbolos_triagem(base) | derivados_de_triagem(base)
    saida = []
    for r in base.regras:
        if r.classe != "bandeira_vermelha":
            continue
        lidos = sorted({c.simbolo for c in r.se if c.simbolo in existentes})
        if lidos and not any(i in permitidos for i in lidos):
            saida.append(_p("E08", _regra(r), f"A bandeira vermelha '{r.id}' lê só {lidos}, nenhum vindo da triagem."))
    return saida


def _e09_doenca_sem_regra(base: Base) -> list[Problema]:
    return [
        _p("E09", _simb(s), f"A doença '{s.id}' não é concluída por nenhuma regra.")
        for s in base.simbolos if s.tipo == "doenca" and not regras_que_concluem(base, s.id)
    ]


def _regras_de_doenca(base: Base):
    for s in base.simbolos:
        if s.tipo == "doenca":
            regras = regras_que_concluem(base, s.id)
            if regras:
                yield s, regras


def _produtor_ok(base: Base, existentes: dict, triagem: set, sid: str, visitando: frozenset = frozenset()) -> bool:
    """O símbolo é obtido do produtor: perguntável a ele, de triagem/ficha ou derivado disso."""
    s = existentes.get(sid)
    if s is None or s.tipo in ("doenca", "urgencia"):
        return True  # indefinido: E01; doença/urgência lida: E12
    if s.tipo == "derivado":
        regras = regras_que_concluem(base, sid)
        return sid not in visitando and bool(regras) and all(
            _produtor_ok(base, existentes, triagem, c.simbolo, visitando | {sid}) for r in regras for c in r.se
        )
    return sid in triagem or perguntavel(s, "produtor") or bool(s.campo_ficha)


def _e10_doenca_sem_regra_produtor(base: Base) -> list[Problema]:
    existentes, triagem = simbolos_por_id(base), simbolos_triagem(base)
    return [
        _p("E10", _simb(s), f"Nenhuma regra da doença '{s.id}' usa só informações que o produtor pode fornecer.")
        for s, regras in _regras_de_doenca(base)
        if not any(all(_produtor_ok(base, existentes, triagem, c.simbolo) for c in r.se) for r in regras)
    ]


def _e11_cobertura_triagem(base: Base) -> list[Problema]:
    existentes = simbolos_por_id(base)
    ok = simbolos_triagem(base) | derivados_de_triagem(base)
    return [
        _p("E11", _simb(s), f"Nenhuma regra da doença '{s.id}' depende só de símbolos da triagem.")
        for s, regras in _regras_de_doenca(base)
        if not any(all(c.simbolo in ok or c.simbolo not in existentes for c in r.se) for r in regras)
    ]


def _e12_camada(base: Base) -> list[Problema]:
    existentes = simbolos_por_id(base)
    saida = []
    for r in base.regras:
        conclusao = existentes.get(r.entao.simbolo)
        if conclusao is None:
            continue
        acima = [c.simbolo for c in r.se if c.simbolo in existentes
                 and CAMADA[existentes[c.simbolo].tipo] >= CAMADA[conclusao.tipo]]
        if acima:
            saida.append(_p("E12", _regra(r),
                            f"A regra '{r.id}' conclui '{conclusao.id}' (camada {CAMADA[conclusao.tipo]}) "
                            f"mas lê {sorted(set(acima))}, de camada igual ou superior."))
    return saida


def _e13_doenca_sem_gravidade(base: Base) -> list[Problema]:
    return [_p("E13", _simb(s), f"A doença '{s.id}' não tem gravidade.")
            for s in base.simbolos if s.tipo == "doenca" and s.gravidade is None]


def _e14_derivado_max_negativo(base: Base) -> list[Problema]:
    negativos = derivados_com_cf_negativo(base)
    return [
        _p("E14", _simb(s), f"O derivado '{s.id}' usa combinação 'max', que não admite regras com cf negativo.")
        for s in base.simbolos if s.tipo == "derivado" and s.combinacao == "max" and s.id in negativos
    ]


def _e15_limite_cf_invalido(base: Base) -> list[Problema]:
    existentes = simbolos_por_id(base)
    saida = []
    for r in base.regras:
        for c in r.se:
            if c.cf_minimo is None and c.cf_maximo is None:
                continue
            problemas = []
            s = existentes.get(c.simbolo)
            if s is not None and s.tipo not in ("doenca", "derivado"):
                problemas.append(f"cf_minimo/cf_maximo só valem sobre doença ou derivado, e '{c.simbolo}' é {s.tipo}")
            for nome, v in (("cf_minimo", c.cf_minimo), ("cf_maximo", c.cf_maximo)):
                if v is not None and not 0 <= v <= 1:
                    problemas.append(f"{nome} {v} sobre '{c.simbolo}' está fora de [0, 1]")
            if c.cf_minimo is not None and c.cf_maximo is not None:
                problemas.append(f"a condição sobre '{c.simbolo}' tem cf_minimo e cf_maximo ao mesmo tempo")
            saida.extend(_p("E15", _regra(r), f"Na regra '{r.id}': {m}.") for m in problemas)
    return saida


def _e16_tela_sem_texto(base: Base) -> list[Problema]:
    existentes = simbolos_por_id(base)
    saida = []
    for tela in base.meta.triagem:
        if all(sid in existentes and existentes[sid].tipo == "ficha" for sid in _ids_da_tela(tela)):
            continue
        faltam = [m for m in _MODOS if not tela.texto.get(m, "").strip()]
        if faltam:
            saida.append(_p("E16", Alvo(tipo="tela", id=tela.id), f"A tela '{tela.id}' não tem texto para: {', '.join(faltam)}."))
    return saida


def _e17_limiares_fora_de_ordem(base: Base) -> list[Problema]:
    lim = base.meta.limiares
    alvo = Alvo(tipo="meta", id="limiares")
    cadeia = [(n, 0.0 if n == "0" else getattr(lim, n)) for n in _ORDEM_LIMIARES]
    pares = list(zip(cadeia, cadeia[1:])) + [
        (("bloco_diferencial", lim.bloco_diferencial), ("bloco_principal", lim.bloco_principal))
    ]
    return [
        _p("E17", alvo, f"Limiares fora de ordem: {a} ({va}) deve ser estritamente menor que {b} ({vb}).")
        for (a, va), (b, vb) in pares if va >= vb
    ]


def _e18_regra_sem_fonte(base: Base) -> list[Problema]:
    return [_p("E18", _regra(r), f"A regra '{r.id}' não cita fonte.")
            for r in base.regras if not (r.fonte or "").strip()]


def _e19_classe_incompativel(base: Base) -> list[Problema]:
    existentes = simbolos_por_id(base)
    saida = []
    for r in base.regras:
        s = existentes.get(r.entao.simbolo)
        if s is None or r.classe == "bandeira_vermelha":  # bandeira: ver E07
            continue
        if r.classe == "urgencia" and (s.tipo != "urgencia" or s.id == "sem_problema"):
            motivo = "deve concluir 'chamar_agora' ou 'observar'"
        elif r.classe == "evidencia" and s.tipo not in ("derivado", "doenca"):
            motivo = "deve concluir um derivado ou uma doença"
        elif s.id == "sem_problema":
            motivo = "'sem_problema' nunca é conclusão de regra"
        else:
            continue
        saida.append(_p("E19", _regra(r), f"A regra '{r.id}' (classe {r.classe}) conclui '{s.id}', mas {motivo}."))
    return saida


def _e20_id_invalido(base: Base) -> list[Problema]:
    return [
        _p("E20", _simb(s), f"O id de símbolo '{s.id}' é inválido; use apenas a-z, 0-9 e '_'.")
        for s in base.simbolos if not _ID_SIMBOLO.fullmatch(s.id)
    ] + [
        _p("E20", _regra(r), f"O id de regra '{r.id}' é inválido; use apenas letras, dígitos, '_' e '-'.")
        for r in base.regras if not _ID_REGRA.fullmatch(r.id)
    ]


# --- avisos ---------------------------------------------------------------

def _w01_simbolo_nao_usado(base: Base) -> list[Problema]:
    usados = {c.simbolo for r in base.regras for c in r.se} | simbolos_triagem(base)
    return [
        _p("W01", _simb(s), f"O símbolo '{s.id}' não é lido por nenhuma regra nem aparece na triagem.")
        for s in base.simbolos if s.tipo in ("pergunta", "ficha", "derivado") and s.id not in usados
    ]


def _chave_condicao(c: Condicao) -> tuple:
    valor = tuple(c.valor) if isinstance(c.valor, list) else c.valor
    return (c.simbolo, c.op, valor, c.negado, c.cf_minimo, c.cf_maximo)


def _w02_regras_contraditorias(base: Base) -> list[Problema]:
    grupos: dict[tuple, list[Regra]] = {}
    for r in base.regras:
        chave = (frozenset(_chave_condicao(c) for c in r.se), r.entao.simbolo)
        grupos.setdefault(chave, []).append(r)
    saida = []
    for (_, conclusao), regras in grupos.items():
        pos = [r.id for r in regras if r.entao.cf > 0]
        neg = [r.id for r in regras if r.entao.cf < 0]
        if pos and neg:
            saida.append(_p("W02", Alvo(tipo="regra", id=min(pos + neg)),
                            f"As regras {pos} e {neg} têm as mesmas condições e conclusões opostas sobre '{conclusao}'."))
    return saida


def _w03_suposicoes_pendentes(base: Base) -> list[Problema]:
    pendentes = [r.id for r in base.regras if r.status == "suposicao_a_validar"]
    if not pendentes:
        return []
    return [_p("W03", None, f"{len(pendentes)} regra(s) ainda são suposição a validar: {', '.join(pendentes)}.")]


_VERIFICACOES = (
    _e01_simbolo_indefinido, _e02_id_duplicado, _e03_valor_invalido, _e04_cf_fora_do_limite,
    _e05_ciclo, _e06_regra_inalcancavel, _e07_bandeira_sem_chamar_agora, _e08_bandeira_sem_triagem,
    _e09_doenca_sem_regra, _e10_doenca_sem_regra_produtor, _e11_cobertura_triagem, _e12_camada,
    _e13_doenca_sem_gravidade, _e14_derivado_max_negativo, _e15_limite_cf_invalido,
    _e16_tela_sem_texto, _e17_limiares_fora_de_ordem, _e18_regra_sem_fonte,
    _e19_classe_incompativel, _e20_id_invalido,
    _w01_simbolo_nao_usado, _w02_regras_contraditorias, _w03_suposicoes_pendentes,
)


# --- entradas públicas ------------------------------------------------------

def _ordenar(problemas: list[Problema]) -> list[Problema]:
    return sorted(problemas, key=lambda p: (p.numero, p.alvo.id if p.alvo else ""))


def validar(base: Base) -> Relatorio:
    problemas = [p for verificar in _VERIFICACOES for p in verificar(base)]
    erros = _ordenar([p for p in problemas if p.severidade == "erro"])
    avisos = _ordenar([p for p in problemas if p.severidade == "aviso"])
    pendentes = sum(1 for r in base.regras if r.status == "suposicao_a_validar")
    return Relatorio(
        valida=not erros, erros=erros, avisos=avisos,
        resumo=Resumo(simbolos=len(base.simbolos), regras=len(base.regras), suposicao_a_validar=pendentes),
    )


def _relatorio_estrutura(mensagens: list[str]) -> Relatorio:
    erros = [Problema(codigo="estrutura", numero="E00", severidade="erro", alvo=None, mensagem=m) for m in mensagens]
    return Relatorio(valida=False, erros=erros, avisos=[], resumo=Resumo(simbolos=0, regras=0, suposicao_a_validar=0))


def validar_dados(dados) -> Relatorio:
    """Valida JSON cru: falhas de estrutura viram erros ``E00``; nunca levanta."""
    if not isinstance(dados, dict):
        return _relatorio_estrutura([f"A base deve ser um objeto JSON, mas veio {type(dados).__name__}."])
    try:
        base = Base.model_validate(dados)
    except ValidationError as exc:
        return _relatorio_estrutura([
            f"Estrutura inválida em '{'.'.join(str(parte) for parte in e['loc']) or '(raiz)'}': {e['msg']}"
            for e in exc.errors()
        ])
    return validar(base)
