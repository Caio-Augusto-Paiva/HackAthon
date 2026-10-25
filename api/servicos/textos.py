"""Textos que a API escreve para o usuário (urgência, alerta, aviso do parecer, texto das regras).

Todas as frases são **suposição**: precisam ser validadas com a RERUM e com o veterinário. Ficam num só lugar para a
equipe revisar a redação sem mexer na lógica.
"""
from __future__ import annotations

from collections.abc import Collection, Iterable, Mapping
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # só anotação
    from kb.modelos import Base, Condicao, Regra, Simbolo

# (nível de urgência, modo) -> texto da urgência no parecer
TEXTO_URGENCIA: dict[tuple[str, str], str] = {
    ("chamar_agora", "produtor"): "Chame um veterinário o mais rápido possível.",
    ("chamar_agora", "veterinario"): "Urgência máxima: indicação de atendimento veterinário imediato.",
    ("observar", "produtor"): "Observe o animal de perto e chame um veterinário se ele piorar.",
    ("observar", "veterinario"): "Observação: acompanhar a evolução e reavaliar o quadro.",
    ("sem_problema", "produtor"): "Nenhum problema aparente com o que foi informado. Continue acompanhando o animal.",
    ("sem_problema", "veterinario"): "Sem indício de urgência nos dados informados.",
}

# modo -> texto do alerta de bandeira vermelha
TEXTO_ALERTA: dict[str, str] = {
    "produtor": "Sintoma grave: chame um veterinário o mais rápido possível.",
    "veterinario": "Bandeira vermelha: sinal de gravidade presente nos dados informados.",
}

AVISO_PARECER = "A porcentagem é o grau de confiança do sistema, não uma probabilidade."


def frase_exclusao(vencedora: str) -> str:
    """A frase da etapa de exclusão em "Como cheguei aqui?"; ``vencedora`` é o nome da doença que ficou mais forte."""
    return f"Ficou menos provável porque {vencedora} ficou mais forte, e as duas não costumam ocorrer juntas."


# --- texto de uma regra ----------------------------------------------------------------------
#
# O motor não escreve o texto de uma regra (o evento ``regra_disparada`` não tem ``texto``). A API o monta dos dados
# da regra na base, de forma determinística e sem conteúdo clínico: só id, condições e conclusão em português.


def _numero(valor: float) -> str:
    """``0.6`` -> ``"0,6"``; ``21.0`` -> ``"21"`` (vírgula decimal, sem zeros à direita)."""
    return f"{valor:.10g}".replace(".", ",")


def _valor_legivel(valor: object) -> str:
    if isinstance(valor, bool):  # antes de int: bool é int em Python
        return "sim" if valor else "não"
    if isinstance(valor, int | float):
        return _numero(valor)
    if isinstance(valor, list):  # operador "em"
        return "{" + ", ".join(str(v) for v in valor) + "}"
    return "(sem valor)" if valor is None else str(valor)


def _nome(id: str, simbolos: Mapping[str, Simbolo]) -> str:
    simbolo = simbolos.get(id)
    return simbolo.nome if simbolo is not None else id


def texto_da_condicao(condicao: Condicao, simbolos: Mapping[str, Simbolo]) -> str:
    """``Sinal A = sim``, ``Temperatura ≥ 39,5``, ``Doença D1 com CF ≥ 0,5``; ``NÃO (...)`` se a condição é negada.

    ``cf_minimo`` e ``cf_maximo`` substituem a comparação de valor (como na avaliação do motor, que olha o
    ``cf_minimo`` primeiro).
    """
    nome = _nome(condicao.simbolo, simbolos)
    if condicao.cf_minimo is not None:
        texto = f"{nome} com CF ≥ {_numero(condicao.cf_minimo)}"
    elif condicao.cf_maximo is not None:
        texto = f"{nome} com CF ≤ {_numero(condicao.cf_maximo)}"
    else:
        texto = f"{nome} {condicao.op} {_valor_legivel(condicao.valor)}"
    return f"NÃO ({texto})" if condicao.negado else texto


def texto_da_regra(regra: Regra, simbolos: Mapping[str, Simbolo]) -> str:
    """``R-D1-01: SE Sinal A = sim ENTÃO Doença D1 (CF 0,6)``: o texto de ``Evidencia.texto`` no "como?"."""
    condicoes = " E ".join(texto_da_condicao(c, simbolos) for c in regra.se)
    return f"{regra.id}: SE {condicoes} ENTÃO {_nome(regra.entao.simbolo, simbolos)} (CF {_numero(regra.entao.cf)})"


# --- sinal em linguagem comum ("por quê?") ---------------------------------------------------
#
# Para o produtor ler "Em casos de Cetose, o animal pode apresentar apetite reduzido ou ausente." em vez dos ids das
# regras. Também determinístico e sem conteúdo clínico novo: só reescreve a condição da regra.

_COMPARACAO = {"<": "abaixo de", "≤": "até", ">": "acima de", "≥": "a partir de", "=": "igual a", "≠": "diferente de"}


def _minuscula(nome: str) -> str:
    """``Decúbito`` -> ``decúbito``; siglas como ``BHB`` ou ``pH`` ficam como estão."""
    return nome if len(nome) > 1 and (nome[1].isupper() or nome[0].islower()) else nome[:1].lower() + nome[1:]


def sinal_legivel(condicao: Condicao, simbolos: Mapping[str, Simbolo]) -> str:
    """``apetite reduzido ou ausente``, ``decúbito``, ``ausência de febre``, ``temperatura retal a partir de 39,5 °C``."""
    simbolo = simbolos.get(condicao.simbolo)
    nome = _minuscula(_nome(condicao.simbolo, simbolos))
    valor = condicao.valor
    if isinstance(valor, bool):
        presente = valor != condicao.negado
        return nome if presente else f"ausência de {nome}"
    if isinstance(valor, list):
        texto = f"{nome} {' ou '.join(str(v) for v in valor)}"
    elif isinstance(valor, int | float):
        unidade = getattr(simbolo.dominio, "unidade", None) if simbolo is not None else None
        texto = f"{nome} {_COMPARACAO.get(condicao.op, condicao.op)} {_numero(valor)}" + (f" {unidade}" if unidade else "")
    else:
        texto = f"{nome} {_valor_legivel(valor)}"
    return f"sem {texto}" if condicao.negado else texto


def sinais_das_regras(base: Base, regras: Iterable[str], conhecidos: Collection[str] = ()) -> list[str]:
    """As condições das ``regras``, legíveis e sem repetir; ``conhecidos`` (já respondidos) ficam de fora."""
    simbolos = {s.id: s for s in base.simbolos}
    por_id = {r.id: r for r in base.regras}
    sinais: list[str] = []
    for regra_id in regras:
        for condicao in por_id[regra_id].se if regra_id in por_id else ():
            texto = sinal_legivel(condicao, simbolos)
            if condicao.simbolo not in conhecidos and texto not in sinais:
                sinais.append(texto)
    return sinais
