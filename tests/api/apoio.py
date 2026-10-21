"""Apoio dos testes da API: validação de contrato e criação de animais e sessões fictícios."""
from __future__ import annotations

from fastapi.testclient import TestClient
from pydantic import TypeAdapter


def validar_contrato(operation_id: str, corpo: dict) -> None:
    """Valida a resposta de sucesso ``corpo`` contra o modelo registrado para ``operation_id``."""
    from api.schemas.registro import CONTRATOS  # import tardio: o registro nasce na Task 3

    _, modelo_resposta = CONTRATOS[operation_id]
    TypeAdapter(modelo_resposta).validate_python(corpo)


def criar_animal_teste(cliente: TestClient, brinco: str = "BR-0001", parto: str = "2026-10-14") -> dict:
    resposta = cliente.post(
        "/api/animais",
        json={"brinco": brinco, "nome": "Mimosa", "ficha": {"data_ultimo_parto": parto}},
    )
    assert resposta.status_code == 201, resposta.text
    return resposta.json()


def criar_sessao_teste(cliente: TestClient, animal_id: str, modo: str = "produtor") -> dict:
    resposta = cliente.post("/api/sessoes", json={"animal_id": animal_id, "modo": modo})
    assert resposta.status_code == 201, resposta.text
    return resposta.json()
