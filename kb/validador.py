"""Validação semântica da base de conhecimento (sem I/O, determinística).

``validar`` recebe uma ``Base`` já carregada e devolve um ``Relatorio`` com erros
(E01-E29) e avisos (W01-W03). ``validar_dados`` aceita JSON cru e ``validar_edicao``,
o payload do editor (grafo); ambas convertem falhas de estrutura em erros ``E00`` e
nunca levantam. Cada código é uma função privada.
"""
from __future__ import annotations

import re
from collections import Counter
from typing import Literal
from urllib.parse import urlsplit

from pydantic import BaseModel, ValidationError

from kb.analise import (
    CAMADA,
    derivados_de_triagem,
    encontrar_ciclo,
    perguntavel,
    regras_que_concluem,
    simbolos_por_id,
    simbolos_triagem,
    simbolos_triagem_produtor,
)
from kb.grafo import Grafo, grafo_para_base
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
    "E21": "tela_simbolo_invalido", "E22": "cf_urgencia_nao_positivo",
    "E23": "dominio_conceito_nao_booleano",
    "E24": "exclusao_doenca_inexistente", "E25": "exclusao_mesma_doenca",
    "E26": "exclusao_duplicada", "E27": "tratamento_url_invalida",
    "E28": "tratamento_fora_de_doenca", "E29": "dispensada_se_invalida",
    "W01": "simbolo_nao_usado", "W02": "regras_contraditorias", "W03": "suposicoes_pendentes",
}

_ID_SIMBOLO = re.compile(r"[a-z0-9_]+")
_ID_REGRA = re.compile(r"[A-Za-z0-9_-]+")
_CONCEITOS = ("derivado", "doenca", "urgencia")  # símbolos concluídos por regras (booleanos)
_ORDEM_LIMIARES = ("descarte", "0", "premissa", "hipotese_relevante", "exaustao", "potencial", "confirmacao")
_MODOS = ("produtor", "veterinario")
_DOMINIOS_TRATAMENTO = ("embrapa.br", "gov.br", "msdvetmanual.com")


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
    saida = [
        _p("E02", Alvo(tipo="simbolo" if i in ids_simbolos else "regra", id=i),
           f"O id '{i}' aparece {n} vezes entre símbolos e regras; os ids devem ser únicos.")
        for i, n in sorted(contagem.items()) if n > 1
    ]
    telas = Counter(t.id for t in base.meta.triagem)  # telas têm espaço de ids próprio
    saida.extend(
        _p("E02", Alvo(tipo="tela", id=i), f"O id de tela '{i}' aparece {n} vezes na triagem; os ids devem ser únicos.")
        for i, n in sorted(telas.items()) if n > 1
    )
    return saida


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


def _motivo_polaridade(c: Condicao, s: Simbolo, positivos: set[str], negativos: set[str]) -> str | None:
    """Motivo pelo qual a condição sobre um conceito nunca fica positiva (ou ``None``).

    Espelha ``engine.avaliacao.avaliar_condicao`` sobre o CF do conceito: sem limites, o
    valor é ``cf`` (``-cf`` se negado); ``cf_minimo`` dá ``cf`` com ``cf >= min >= 0``;
    ``cf_maximo`` dá ``-cf`` com ``cf <= max``; ``negado`` inverte o sinal. A condição só
    passa da premissa quando o valor é positivo.
    """
    if c.cf_minimo is not None:
        if c.negado:
            return f"'{s.id}' é negado com cf_minimo, o que nunca dá valor positivo"
        precisa = "positivo"
    elif c.cf_maximo is not None:
        if c.negado:
            if c.cf_maximo <= 0:
                return f"'{s.id}' é negado com cf_maximo {c.cf_maximo}, o que exige cf positivo e no máximo {c.cf_maximo}"
            precisa = "positivo"
        else:
            precisa = "negativo"
    else:
        precisa = "negativo" if c.negado else "positivo"
    if precisa == "positivo" and s.id not in positivos:
        return f"a condição sobre '{s.id}' exige cf positivo, mas nenhuma regra o conclui com cf positivo"
    if precisa == "negativo" and s.id not in negativos:
        return f"a condição sobre '{s.id}' exige cf negativo, mas nenhuma regra o conclui com cf negativo"
    return None


def _e06_regra_inalcancavel(base: Base) -> list[Problema]:
    existentes = simbolos_por_id(base)
    concluidos = {r.entao.simbolo for r in base.regras}
    positivos = {r.entao.simbolo for r in base.regras if r.entao.cf > 0}
    # derivado 'max' nunca fica negativo: max(0, saída negativa) = 0
    negativos = {r.entao.simbolo for r in base.regras
                 if r.entao.cf < 0 and (s := existentes.get(r.entao.simbolo)) is not None and s.combinacao != "max"}
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
                else:
                    motivo = _motivo_polaridade(c, s, positivos, negativos)
                    if motivo:
                        motivos.append(motivo)
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


def _produtor_ok(base: Base, existentes: dict, triagem: set, sid: str,
                 memo: dict[str, bool] | None = None) -> bool:
    """O símbolo é obtido do produtor: perguntável a ele, na triagem que ele vê, ficha ou derivado disso.

    ``triagem`` é o conjunto de ``simbolos_triagem_produtor`` (o que as telas mostram ao produtor).

    ``memo`` guarda o resultado por símbolo (sem ele, cadeias de derivados lidos por
    várias regras custam tempo exponencial); um símbolo ainda em andamento (ciclo) conta
    como ``False``.
    """
    memo = {} if memo is None else memo
    if sid in memo:
        return memo[sid]
    s = existentes.get(sid)
    if s is None or s.tipo in ("doenca", "urgencia"):
        return True  # indefinido: E01; doença/urgência lida: E12
    if s.tipo != "derivado":
        return sid in triagem or perguntavel(s, "produtor") or bool(s.campo_ficha)
    memo[sid] = False  # em andamento
    regras = regras_que_concluem(base, sid)
    memo[sid] = bool(regras) and all(
        _produtor_ok(base, existentes, triagem, c.simbolo, memo) for r in regras for c in r.se
    )
    return memo[sid]


def _e10_doenca_sem_regra_produtor(base: Base) -> list[Problema]:
    existentes, triagem = simbolos_por_id(base), simbolos_triagem_produtor(base)
    memo: dict[str, bool] = {}
    return [
        _p("E10", _simb(s), f"Nenhuma regra da doença '{s.id}' usa só informações que o produtor pode fornecer.")
        for s, regras in _regras_de_doenca(base)
        if not any(all(_produtor_ok(base, existentes, triagem, c.simbolo, memo) for c in r.se) for r in regras)
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
    saida = []
    for s in base.simbolos:
        if s.combinacao != "max":
            continue
        if s.tipo != "derivado":
            saida.append(_p("E14", _simb(s), f"O símbolo '{s.id}' ({s.tipo}) usa combinação 'max', que só vale para derivados."))
        elif any(r.entao.cf <= 0 for r in regras_que_concluem(base, s.id)):
            saida.append(_p("E14", _simb(s),
                            f"O derivado '{s.id}' usa combinação 'max', que exige cf positivo em todas as suas regras."))
    return saida


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
    valores = {n: getattr(lim, n) for n in _ORDEM_LIMIARES if n != "0"}
    valores.update(bloco_principal=lim.bloco_principal, bloco_diferencial=lim.bloco_diferencial)
    saida = [
        _p("E17", alvo, f"O limiar '{n}' ({v}) está fora de [-1, 1].")
        for n, v in valores.items() if not -1 <= v <= 1
    ]
    cadeia = [(n, 0.0 if n == "0" else getattr(lim, n)) for n in _ORDEM_LIMIARES]
    pares = list(zip(cadeia, cadeia[1:])) + [
        (("bloco_diferencial", lim.bloco_diferencial), ("bloco_principal", lim.bloco_principal))
    ]
    saida.extend(
        _p("E17", alvo, f"Limiares fora de ordem: {a} ({va}) deve ser estritamente menor que {b} ({vb}).")
        for (a, va), (b, vb) in pares if va >= vb
    )
    if lim.bloco_diferencial < 0:
        saida.append(_p("E17", alvo, f"O corte 'bloco_diferencial' ({lim.bloco_diferencial}) não pode ser negativo."))
    return saida


def _e18_regra_sem_fonte(base: Base) -> list[Problema]:
    return [_p("E18", _regra(r), f"A regra '{r.id}' não cita fonte.")
            for r in base.regras if not (r.fonte or "").strip()]


def _e19_classe_incompativel(base: Base) -> list[Problema]:
    """Espelha o motor: evidência conclui derivado/doença; urgência e bandeira, símbolo de tipo urgência."""
    existentes = simbolos_por_id(base)
    saida = []
    for r in base.regras:
        s = existentes.get(r.entao.simbolo)
        if s is None:
            continue
        conceito = s.tipo in ("derivado", "doenca")
        if r.classe == "evidencia" and not conceito:
            motivo = "deve concluir um derivado ou uma doença"
        elif r.classe != "evidencia" and conceito:
            motivo = "só pode concluir um símbolo de tipo urgência, e ele é " + s.tipo
        elif r.classe != "evidencia" and s.tipo != "urgencia":
            motivo = "só pode concluir um símbolo de tipo urgência, e ele é " + s.tipo
        elif r.classe == "urgencia" and s.id not in ("observar", "chamar_agora"):
            motivo = "deve concluir 'chamar_agora' ou 'observar' ('sem_problema' é calculado)"
        else:
            continue  # bandeira com destino diferente de 'chamar_agora': ver E07
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


def _e21_tela_simbolo_invalido(base: Base) -> list[Problema]:
    existentes = simbolos_por_id(base)
    saida = []
    for tela in base.meta.triagem:
        for sid in _ids_da_tela(tela):
            s = existentes.get(sid)  # indefinido: E01
            if s is not None and s.tipo not in ("pergunta", "ficha"):
                saida.append(_p("E21", Alvo(tipo="tela", id=tela.id),
                                f"A tela '{tela.id}' lista '{sid}', que é {s.tipo}; só pergunta ou ficha pode estar na triagem."))
            elif s is not None and tela.selecao == "multipla" and s.dominio.tipo != "booleano":
                saida.append(_p("E21", Alvo(tipo="tela", id=tela.id),
                                f"A tela '{tela.id}' é de seleção múltipla, mas '{sid}' tem domínio {s.dominio.tipo}; "
                                "só símbolos booleanos podem estar em tela múltipla."))
    return saida


def _e22_cf_urgencia_nao_positivo(base: Base) -> list[Problema]:
    return [
        _p("E22", _regra(r), f"A regra '{r.id}' (classe {r.classe}) tem cf {r.entao.cf}; urgência e bandeira exigem cf positivo.")
        for r in base.regras if r.classe in ("urgencia", "bandeira_vermelha") and r.entao.cf <= 0
    ]


def _e23_dominio_conceito_nao_booleano(base: Base) -> list[Problema]:
    return [
        _p("E23", _simb(s), f"O símbolo '{s.id}' ({s.tipo}) tem domínio {s.dominio.tipo}; derivado, doença e urgência são booleanos.")
        for s in base.simbolos if _conceito(s) and s.dominio.tipo != "booleano"
    ]


def _url_tratamento_permitida(url: str) -> bool:
    if any(c == "\\" or c.isspace() or ord(c) < 32 or ord(c) == 127 for c in url):
        return False
    try:
        partes = urlsplit(url)
        host, porta = partes.hostname, partes.port
    except ValueError:
        return False
    if partes.scheme != "https" or not host or "@" in partes.netloc or porta not in (None, 443):
        return False
    return any(host == d or host.endswith("." + d) for d in _DOMINIOS_TRATAMENTO)


def _e24_exclusao_doenca_inexistente(base: Base) -> list[Problema]:
    doencas = {s.id for s in base.simbolos if s.tipo == "doenca"}
    return [
        _p("E24", Alvo(tipo="meta", id="exclusoes"), f"A exclusão {list(e.doencas)} cita '{d}', que não é uma doença da base.")
        for e in base.meta.exclusoes for d in dict.fromkeys(e.doencas) if d not in doencas
    ]


def _e25_exclusao_mesma_doenca(base: Base) -> list[Problema]:
    return [
        _p("E25", Alvo(tipo="meta", id="exclusoes"), f"A exclusão {list(e.doencas)} repete a mesma doença; o par precisa de duas doenças diferentes.")
        for e in base.meta.exclusoes if e.doencas[0] == e.doencas[1]
    ]


def _e26_exclusao_duplicada(base: Base) -> list[Problema]:
    contagem = Counter(frozenset(e.doencas) for e in base.meta.exclusoes if e.doencas[0] != e.doencas[1])
    return [
        _p("E26", Alvo(tipo="meta", id="exclusoes"), f"O par excludente {sorted(par)} aparece {n} vezes (a ordem não importa).")
        for par, n in sorted(contagem.items(), key=lambda kv: sorted(kv[0])) if n > 1
    ]


def _e27_tratamento_url_invalida(base: Base) -> list[Problema]:
    return [
        _p("E27", _simb(s), f"A URL de tratamento de '{s.id}' deve ser https e de um destes domínios: {', '.join(_DOMINIOS_TRATAMENTO)}.")
        for s in base.simbolos
        if s.tratamento is not None and not _url_tratamento_permitida(s.tratamento.url)
    ]


def _e28_tratamento_fora_de_doenca(base: Base) -> list[Problema]:
    return [
        _p("E28", _simb(s), f"O símbolo '{s.id}' ({s.tipo}) tem tratamento, que só vale para doença.")
        for s in base.simbolos if s.tratamento is not None and s.tipo != "doenca"
    ]


def _e29_dispensada_se_invalida(base: Base) -> list[Problema]:
    perguntas = {s.id for s in base.simbolos if s.tipo in ("pergunta", "ficha")}
    return [
        _p("E29", _simb(s), f"'{s.id}' só pode ser dispensada por outra pergunta; '{alvo}' não é uma.")
        for s in base.simbolos for alvo in (s.dispensada_se or ())
        if alvo == s.id or alvo not in perguntas
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
    _e19_classe_incompativel, _e20_id_invalido, _e21_tela_simbolo_invalido,
    _e22_cf_urgencia_nao_positivo, _e23_dominio_conceito_nao_booleano,
    _e24_exclusao_doenca_inexistente, _e25_exclusao_mesma_doenca, _e26_exclusao_duplicada,
    _e27_tratamento_url_invalida, _e28_tratamento_fora_de_doenca, _e29_dispensada_se_invalida,
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


def _mensagens_estrutura(exc: ValidationError) -> list[str]:
    return [
        f"Estrutura inválida em '{'.'.join(str(parte) for parte in e['loc']) or '(raiz)'}': {e['msg']}"
        for e in exc.errors()
    ]


def validar_dados(dados) -> Relatorio:
    """Valida JSON cru: falhas de estrutura viram erros ``E00``; nunca levanta."""
    if not isinstance(dados, dict):
        return _relatorio_estrutura([f"A base deve ser um objeto JSON, mas veio {type(dados).__name__}."])
    try:
        base = Base.model_validate(dados)
    except ValidationError as exc:
        return _relatorio_estrutura(_mensagens_estrutura(exc))
    return validar(base)


def validar_edicao(dados) -> tuple[Base | None, Relatorio]:
    """Valida o payload do editor (um ``Grafo`` em dict): converte em ``Base`` e valida.

    Devolve ``(base, relatorio)``; se a conversão falhar, ``base`` é ``None`` e o
    relatório traz erros ``E00``. Nunca levanta.
    """
    if not isinstance(dados, dict):
        return None, _relatorio_estrutura([f"O grafo deve ser um objeto JSON, mas veio {type(dados).__name__}."])
    try:
        base = grafo_para_base(Grafo.model_validate(dados))
    except ValidationError as exc:
        return None, _relatorio_estrutura(_mensagens_estrutura(exc))
    except ValueError as exc:
        return None, _relatorio_estrutura([f"Grafo inválido: {exc}"])
    return base, validar(base)
