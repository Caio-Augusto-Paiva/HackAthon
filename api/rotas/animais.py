"""Rotas de animais, ficha e importação de prontuário (4.5.2). Finas: a lógica fica em ``api/servicos``."""
from __future__ import annotations

from fastapi import APIRouter, Depends, UploadFile

from api.contexto import Contexto, obter_contexto
from api.rotas.respostas import ERROS_DE_CADASTRO, ERROS_DE_ENTRADA, ERROS_DE_RECURSO
from api.schemas.animal import Animal, ListaAnimais, ListaSessoesAnimal, NovoAnimal, ResultadoImportacao
from api.servicos import animal_servico, importacao

router = APIRouter()


@router.get(
    "/animais",
    operation_id="listar_animais",
    responses=ERROS_DE_ENTRADA,
    response_model=ListaAnimais,
    summary="Listar animais",
)
def listar_animais(busca: str | None = None, ctx: Contexto = Depends(obter_contexto)) -> ListaAnimais:
    return animal_servico.listar_animais(ctx, busca)


@router.post(
    "/animais",
    operation_id="criar_animal",
    status_code=201,
    responses=ERROS_DE_CADASTRO,
    response_model=Animal,
    summary="Cadastrar animal",
)
def criar_animal(corpo: NovoAnimal, ctx: Contexto = Depends(obter_contexto)) -> Animal:
    return animal_servico.criar_animal(ctx, corpo)


# declarada antes de /animais/{animal_id}, para "importacao" nunca ser lida como id
@router.post(
    "/animais/importacao",
    operation_id="importar_animais",
    responses=ERROS_DE_CADASTRO,
    response_model=ResultadoImportacao,
    summary="Importar prontuário (CSV ou JSON)",
)
def importar_animais(
    arquivo: UploadFile, gravar: bool = True, ctx: Contexto = Depends(obter_contexto)
) -> ResultadoImportacao:
    # rota síncrona: o FastAPI a roda numa thread, e file.read() é a leitura bloqueante certa aqui
    # (um byte a mais que o limite basta para o serviço recusar sem ler o arquivo todo)
    conteudo = arquivo.file.read(importacao.LIMITE_BYTES + 1)
    return importacao.importar(ctx, arquivo.filename or "", conteudo, gravar)


@router.get(
    "/animais/{animal_id}",
    operation_id="obter_animal",
    responses=ERROS_DE_RECURSO,
    response_model=Animal,
    summary="Ficha do animal",
)
def obter_animal(animal_id: str, ctx: Contexto = Depends(obter_contexto)) -> Animal:
    return animal_servico.obter_animal(ctx, animal_id)


@router.get(
    "/animais/{animal_id}/sessoes",
    operation_id="listar_sessoes_animal",
    responses=ERROS_DE_RECURSO,
    response_model=ListaSessoesAnimal,
    summary="Sessões de anamnese do animal",
)
def listar_sessoes_animal(animal_id: str, ctx: Contexto = Depends(obter_contexto)) -> ListaSessoesAnimal:
    return animal_servico.listar_sessoes_do_animal(ctx, animal_id)
