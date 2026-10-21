"""Contrato kb -> motor por propriedade: base que o validador aceita, o motor carrega e executa.

Gera mutações da base mínima (CF, classe, destino, domínio, limites de CF, limiares,
cortes de bloco, seleção de tela) e, quando ``validar`` não acusa erro, exige que o motor
carregue a base e rode uma sessão de fumaça sem levantar.
"""
import random

from hypothesis import event, given, settings, strategies as st

from engine.modelos import Base as BaseMotor
from engine.sessao import Sessao
from kb.modelos import carregar_base, para_motor
from kb.validador import validar_dados
from tests.kb.apoio import carregar_minima

CLASSES = ("evidencia", "urgencia", "bandeira_vermelha")
CHAVES_LIMIAR = ("descarte", "premissa", "hipotese_relevante", "exaustao", "potencial", "confirmacao",
                 "bloco_principal", "bloco_diferencial")
DOMINIOS = (
    {"tipo": "booleano"},
    {"tipo": "numerico", "min": 0, "max": 400},
    {"tipo": "numerico"},
    {"tipo": "categorico", "valores": ["a", "b"]},
)

_idx = st.integers(min_value=0, max_value=30)
_cf = st.integers(min_value=-99, max_value=99).map(lambda n: n / 100)
_cf_limite = st.one_of(st.none(), st.integers(min_value=-50, max_value=150).map(lambda n: n / 100))
_limiar = st.integers(min_value=-200, max_value=200).map(lambda n: n / 100)

_mutacao = st.one_of(
    st.tuples(st.just("cf"), _idx, _cf),
    st.tuples(st.just("classe"), _idx, st.sampled_from(CLASSES)),
    st.tuples(st.just("destino"), _idx, _idx),
    st.tuples(st.just("dominio"), _idx, st.sampled_from(range(len(DOMINIOS)))),
    st.tuples(st.just("cf_minimo"), _idx, _cf_limite),
    st.tuples(st.just("cf_maximo"), _idx, _cf_limite),
    st.tuples(st.just("limiar"), st.sampled_from(CHAVES_LIMIAR), _limiar),
    st.tuples(st.just("selecao"), _idx, st.sampled_from(("unica", "multipla"))),
    st.tuples(st.just("combinacao"), _idx, st.sampled_from(("mycin", "max"))),
    st.tuples(st.just("negado"), _idx, st.booleans()),
    st.tuples(st.just("origem"), _idx, _idx),
    st.tuples(st.just("na_tela"), _idx, _idx),
)


def _aplicar(dados: dict, mutacoes) -> dict:
    regras, simbolos, telas = dados["regras"], dados["simbolos"], dados["meta"]["triagem"]
    for nome, a, b in mutacoes:
        if nome == "cf":
            regras[a % len(regras)]["entao"]["cf"] = b
        elif nome == "classe":
            regras[a % len(regras)]["classe"] = b
        elif nome == "destino":
            regras[a % len(regras)]["entao"]["simbolo"] = simbolos[b % len(simbolos)]["id"]
        elif nome == "dominio":
            simbolos[a % len(simbolos)]["dominio"] = dict(DOMINIOS[b])
        elif nome in ("cf_minimo", "cf_maximo"):
            condicoes = [c for r in regras for c in r["se"]]
            condicao = condicoes[a % len(condicoes)]
            if b is None:
                condicao.pop(nome, None)
            else:
                condicao[nome] = b
        elif nome == "limiar":
            dados["meta"].setdefault("limiares", {})[a] = b
        elif nome == "selecao":
            telas[a % len(telas)]["selecao"] = b
        elif nome == "negado":
            condicoes = [c for r in regras for c in r["se"]]
            condicoes[a % len(condicoes)]["negado"] = b
        elif nome == "origem":
            condicoes = [c for r in regras for c in r["se"]]
            condicoes[a % len(condicoes)]["simbolo"] = simbolos[b % len(simbolos)]["id"]
        elif nome == "na_tela":
            tela = telas[a % len(telas)]
            tela["simbolos"].append(simbolos[b % len(simbolos)]["id"])
        elif nome == "combinacao":
            simbolos[a % len(simbolos)]["combinacao"] = b
    return dados


def _valor(simbolo: dict, rng: random.Random):
    dominio = simbolo["dominio"]
    if dominio["tipo"] == "booleano":
        return rng.random() < 0.6
    if dominio["tipo"] == "categorico":
        return rng.choice(dominio["valores"])
    minimo, maximo = dominio.get("min", 0), dominio.get("max", 400)
    return rng.randint(int(minimo), int(maximo))


def _sessao_de_fumaca(motor: dict, modo: str, semente: int) -> None:
    rng = random.Random(semente)
    simbolos = {s["id"]: s for s in motor["simbolos"]}
    sessao = Sessao(motor, modo=modo)
    for _ in range(80):
        estado = sessao.estado()
        proxima = estado["proxima"]
        if estado["pausa"]:
            sessao.acao_bandeira("continuar")
            continue
        if proxima is None:
            break
        if proxima["tipo"] == "tela_triagem":
            ids = proxima["simbolos"]
            if proxima["selecao"] == "multipla":
                resposta = {i: bool(_valor(simbolos[i], rng)) for i in ids}
            else:
                resposta = {i: _valor(simbolos[i], rng) for i in ids}
            sessao.responder_triagem(proxima["id"], resposta)
        else:
            sessao.responder(proxima["id"], _valor(simbolos[proxima["id"]], rng))
    sessao.parecer()
    for id_ in list(sessao.perguntas)[:3]:
        sessao.porque(id_)
    sessao.como("chamar_agora")


@settings(derandomize=True, max_examples=400, deadline=None)
@given(
    mutacoes=st.lists(_mutacao, min_size=1, max_size=3),
    modo=st.sampled_from(("produtor", "veterinario")),
    semente=st.integers(min_value=0, max_value=10_000),
)
def test_validador_aceita_implica_motor_executa(mutacoes, modo, semente):
    dados = _aplicar(carregar_minima(), mutacoes)
    relatorio = validar_dados(dados)
    if not relatorio.valida:
        event("invalida")
        return
    event("valida")
    motor = para_motor(carregar_base(dados))
    BaseMotor.de_dict(motor)
    _sessao_de_fumaca(motor, modo, semente)


def test_a_estrategia_gera_bases_validas_e_invalidas():
    """Guarda contra um teste vazio: a estratégia precisa produzir os dois tipos de base."""
    from hypothesis import find

    valida = find(st.lists(_mutacao, min_size=1, max_size=3),
                  lambda m: validar_dados(_aplicar(carregar_minima(), m)).valida,
                  settings=settings(derandomize=True, max_examples=200, deadline=None))
    invalida = find(st.lists(_mutacao, min_size=1, max_size=3),
                    lambda m: not validar_dados(_aplicar(carregar_minima(), m)).valida,
                    settings=settings(derandomize=True, max_examples=200, deadline=None))
    assert valida is not None and invalida is not None
