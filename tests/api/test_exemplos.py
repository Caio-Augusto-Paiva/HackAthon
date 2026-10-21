"""Schemas Pydantic e exemplos de contrato (Task 3, passo 0 da 4.8).

Cada operação da API tem um exemplo em ``contratos/exemplos/<operation_id>.json`` e um par de modelos em
``api.schemas.registro.CONTRATOS``. Aqui se confere que os dois combinam e que as regras de modelagem
da Seção 4.7 valem (discriminadores, corpos de requisição fechados, valor ou "não sei").
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest
from pydantic import BaseModel, TypeAdapter, ValidationError

from api.schemas.explicacao import Como
from api.schemas.registro import CONTRATOS
from api.schemas.sessao import (
    CorrecaoPergunta,
    EstadoSessao,
    PerguntaDinamica,
    RespostaPergunta,
    RespostaTriagem,
    TelaTriagem,
)
from kb.grafo import Grafo, grafo_para_base
from kb.modelos import Base

PASTA_EXEMPLOS = Path(__file__).resolve().parents[2] / "contratos" / "exemplos"
OPERACOES = sorted(CONTRATOS)
CHAVES_DO_EXEMPLO = {"operacao", "metodo", "rota", "status", "requisicao", "resposta"}


def _exemplo(operation_id: str) -> dict:
    return json.loads((PASTA_EXEMPLOS / f"{operation_id}.json").read_text(encoding="utf-8"))


def _contido(esperado, obtido, caminho: str = "") -> list[str]:
    """Lista o que do exemplo não aparece, igual, no objeto revalidado (campo desconhecido é descartado)."""
    if isinstance(esperado, dict):
        if not isinstance(obtido, dict):
            return [f"{caminho or '<raiz>'}: esperava objeto"]
        faltas: list[str] = []
        for chave, valor in esperado.items():
            if chave not in obtido:
                faltas.append(f"{caminho}.{chave}: campo desconhecido para o schema")
            else:
                faltas += _contido(valor, obtido[chave], f"{caminho}.{chave}")
        return faltas
    if isinstance(esperado, list):
        if not isinstance(obtido, list) or len(obtido) != len(esperado):
            return [f"{caminho}: lista diferente"]
        return [f for i, (e, o) in enumerate(zip(esperado, obtido)) for f in _contido(e, o, f"{caminho}[{i}]")]
    return [] if esperado == obtido else [f"{caminho}: {esperado!r} virou {obtido!r}"]


def test_um_exemplo_por_operacao():
    assert {p.stem for p in PASTA_EXEMPLOS.glob("*.json")} == set(CONTRATOS)
    assert len(CONTRATOS) == 27


@pytest.mark.parametrize("operation_id", OPERACOES)
def test_exemplo_valida_contra_schema(operation_id: str):
    exemplo = _exemplo(operation_id)
    modelo_corpo, modelo_resposta = CONTRATOS[operation_id]

    assert set(exemplo) == CHAVES_DO_EXEMPLO
    assert exemplo["operacao"] == operation_id
    assert exemplo["metodo"] in {"GET", "POST", "PUT", "PATCH"}
    assert exemplo["rota"].startswith("/api/")
    assert exemplo["status"] in {200, 201}
    # corpo JSON e modelo de corpo andam juntos (a importação é multipart: sem corpo JSON)
    assert (exemplo["requisicao"] is None) == (modelo_corpo is None)

    pares = [(modelo_resposta, exemplo["resposta"])]
    if exemplo["requisicao"] is not None:
        pares.append((modelo_corpo, exemplo["requisicao"]))
    for modelo, dado in pares:
        adaptador = TypeAdapter(modelo)
        validado = adaptador.validate_python(dado)
        # os modelos de resposta ignoram campo extra: o exemplo não pode ter nenhum que o schema não conheça
        assert _contido(dado, adaptador.dump_python(validado, mode="json")) == []


def test_estado_sessao_discriminador():
    criada = _exemplo("criar_sessao")["resposta"]
    assert criada["proxima"]["tipo"] == "tela_triagem"
    assert isinstance(EstadoSessao.model_validate(criada).proxima, TelaTriagem)

    dinamica = _exemplo("obter_sessao")["resposta"]
    assert dinamica["fase"] == "dinamica"
    assert dinamica["proxima"]["tipo"] == "pergunta"
    assert isinstance(EstadoSessao.model_validate(dinamica).proxima, PerguntaDinamica)

    # o discriminador escolhe o modelo só pelo `tipo`; tipo desconhecido não cai em outro modelo
    with pytest.raises(ValidationError):
        EstadoSessao.model_validate({**dinamica, "proxima": {**dinamica["proxima"], "tipo": "outra"}})


def test_estado_sessao_encerrada_sem_proxima():
    estado = EstadoSessao.model_validate({**_exemplo("obter_sessao")["resposta"], "fase": "encerrada", "proxima": None})
    assert estado.proxima is None


def test_resposta_triagem_exige_exatamente_um():
    with pytest.raises(ValidationError):
        RespostaTriagem()
    with pytest.raises(ValidationError):
        RespostaTriagem(valores={"a": True}, nao_sei=True)
    assert RespostaTriagem(nao_sei=True).valores is None
    assert RespostaTriagem(valores={"a": True, "b": 39.8, "c": "reduzido"}).nao_sei is False


def test_resposta_triagem_mensagens_em_portugues():
    with pytest.raises(ValidationError, match="não os dois"):
        RespostaTriagem(valores={"a": True}, nao_sei=True)
    with pytest.raises(ValidationError, match="Informe os valores"):
        RespostaTriagem()


def test_resposta_pergunta_valor_ou_nao_sei():
    with pytest.raises(ValidationError):
        RespostaPergunta(simbolo="x")
    with pytest.raises(ValidationError):
        RespostaPergunta(simbolo="x", valor=True, nao_sei=True)
    assert RespostaPergunta(simbolo="x", nao_sei=True).valor is None
    # False e 0 são valores de verdade, não ausência
    assert RespostaPergunta(simbolo="x", valor=False).valor is False
    assert RespostaPergunta(simbolo="x", valor=0).valor == 0


def test_correcao_pergunta_sem_simbolo_mesma_regra():
    assert CorrecaoPergunta(valor=False).valor is False
    assert CorrecaoPergunta(nao_sei=True).nao_sei is True
    with pytest.raises(ValidationError):
        CorrecaoPergunta()
    with pytest.raises(ValidationError):
        CorrecaoPergunta(valor=True, nao_sei=True)
    assert "simbolo" not in CorrecaoPergunta.model_fields
    # irmãs, não herdeiras: `isinstance(corpo, CorrecaoPergunta)` não confunde um POST com um PUT
    assert not issubclass(RespostaPergunta, CorrecaoPergunta)


def test_cliente_nao_envia_cf():
    with pytest.raises(ValidationError, match="extra_forbidden"):
        RespostaPergunta(simbolo="x", valor=True, cf=0.9)
    with pytest.raises(ValidationError, match="extra_forbidden"):
        RespostaTriagem(valores={"a": True}, cf=0.9)


def test_corpos_de_requisicao_sao_fechados():
    corpos = {modelo for modelo, _ in CONTRATOS.values() if modelo is not None}
    assert len(corpos) == 10
    for modelo in corpos:
        assert modelo.model_config.get("extra") == "forbid", modelo.__name__
        assert modelo.model_config.get("allow_inf_nan") is False, modelo.__name__


def test_valor_nao_numerico_rejeitado_no_corpo():
    with pytest.raises(ValidationError):
        RespostaPergunta(simbolo="x", valor=float("nan"))
    with pytest.raises(ValidationError):
        RespostaTriagem(valores={"temperatura_retal": float("inf")})


def test_respostas_reaproveitam_modelos_do_kb():
    from kb.validador import Relatorio

    assert CONTRATOS["obter_versao"][1] is Base
    assert CONTRATOS["obter_grafo"][1] is Grafo
    assert CONTRATOS["validar_base"][1] is Relatorio
    assert all(issubclass(m, BaseModel) for _, m in CONTRATOS.values())


def test_exemplo_do_grafo_e_a_mesma_base_do_exemplo_da_versao():
    """Os dois exemplos da mesma versão contam a mesma história: o grafo convertido de volta é a base."""
    base = Base.model_validate(_exemplo("obter_versao")["resposta"])
    grafo = Grafo.model_validate(_exemplo("obter_grafo")["resposta"])
    assert grafo_para_base(grafo) == base
    assert grafo.versao == base.meta.versao


def test_como_aceita_evidencias_aninhadas_de_derivado():
    """Entrada com origem ``regra`` (um derivado) traz as evidências que o produziram, em qualquer profundidade."""
    folha = _exemplo("obter_como")["resposta"]["evidencias"][0]
    derivado = {
        "regra_id": "R-DER-01", "texto": "SE apatia ENTÃO febre_provavel +0,50", "fonte": None,
        "status": "validada", "premissa": 1.0, "cf_regra": 0.5, "cf_saida": 0.5,
        "entradas": [{"simbolo": "apatia", "valor": None, "cf": 0.0, "origem": "resposta", "tela_id": "atitude_locomocao"}],
    }
    nivel_dois = {**folha, "entradas": [
        {"simbolo": "febre_provavel", "valor": True, "cf": 0.5, "origem": "regra", "tela_id": None,
         "evidencias": [derivado]},
    ]}
    como = Como.model_validate({**_exemplo("obter_como")["resposta"], "evidencias": [nivel_dois]})
    entrada = como.evidencias[0].entradas[0]
    assert entrada.origem == "regra"
    assert entrada.evidencias[0].regra_id == "R-DER-01"
    assert entrada.evidencias[0].entradas[0].valor is None  # "não sei" chega como None
    assert entrada.evidencias[0].entradas[0].evidencias is None
