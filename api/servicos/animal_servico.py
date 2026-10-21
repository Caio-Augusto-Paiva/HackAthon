"""Animais: cadastro, consulta e histórico de sessões. A ficha é validada contra a base ativa."""
from __future__ import annotations

import json

from api.contexto import Contexto
from api.db import repositorios as repo
from api.erros import ErroApi, conflito, entrada_invalida, nao_encontrado
from api.schemas.animal import (
    Animal,
    AnimalResumo,
    ErroCampo,
    ListaAnimais,
    ListaSessoesAnimal,
    NovoAnimal,
    SessaoDoAnimal,
)
from api.servicos.ficha import CAMPO_DATA_PARTO, completar_ficha, dias_em_lactacao, validar_ficha
from engine.sessao import Sessao
from kb.modelos import Base, para_motor


def base_ativa(ctx: Contexto) -> Base:
    """A base da versão ativa; sem versão ativa é 409 ``conflito`` (não há o que validar a ficha)."""
    versao = ctx.repo.versao_ativa()
    if versao is None:
        raise conflito("Nenhuma versão ativa para validar a ficha")
    return ctx.repo.carregar(versao)


def texto_legivel(*valores: object) -> bool:
    r"""``False`` se algum texto (também dentro de dict e lista) tem um surrogate Unicode solto.

    O JSON aceita ``\ud800``; o banco e a resposta não o codificam em UTF-8, e sem esta checagem a gravação
    ou a resposta viraria 500.
    """
    try:
        json.dumps(valores, ensure_ascii=False).encode("utf-8")
    except ValueError:  # UnicodeEncodeError é um ValueError
        return False
    return True


def erro_de_ficha(erros: list[ErroCampo]) -> ErroApi:
    """422 ``entrada_invalida`` com um detalhe por campo (``corpo.ficha.<campo>``, como o 422 do FastAPI)."""
    primeiro = f"{erros[0].campo}: {erros[0].mensagem}"
    resto = f" (e mais {len(erros) - 1}; veja os detalhes)" if len(erros) > 1 else ""
    detalhes = [
        {"codigo": "ficha_invalida", "severidade": "erro", "mensagem": f"corpo.ficha.{e.campo}: {e.mensagem}"}
        for e in erros
    ]
    return entrada_invalida(f"Ficha inválida. {primeiro}{resto}", detalhes)


def _animal(ctx: Contexto, linha: dict) -> Animal:
    ficha = linha["ficha"]
    return Animal(
        id=linha["id"],
        brinco=linha["brinco"],
        nome=linha["nome"],
        dias_em_lactacao=dias_em_lactacao(ficha.get(CAMPO_DATA_PARTO), ctx.config.hoje()),
        ficha=ficha,
        origens=linha["origens"],
    )


def criar_animal(ctx: Contexto, corpo: NovoAnimal) -> Animal:
    base = base_ativa(ctx)
    brinco, nome = corpo.brinco.strip(), corpo.nome.strip()
    if not brinco:
        raise entrada_invalida(
            "Brinco obrigatório.",
            [{"codigo": "string_too_short", "severidade": "erro", "mensagem": "corpo.brinco: Texto curto demais."}],
        )
    if not texto_legivel(brinco, nome, corpo.ficha):
        raise entrada_invalida("O texto enviado tem caracteres Unicode inválidos.")
    erros = validar_ficha(base, corpo.ficha)
    if erros:
        raise erro_de_ficha(erros)
    if repo.obter_animal_por_brinco(ctx.conn, brinco) is not None:
        raise conflito(f"Já existe um animal com o brinco '{brinco}'.")
    with ctx.conn:
        animal_id = repo.inserir_animal(
            ctx.conn,
            brinco=brinco,
            nome=nome,
            ficha=completar_ficha(base, corpo.ficha),
            origens={},  # só "importacao" é registrado; o que não está em origens vale "manual"
            agora=ctx.config.agora(),
        )
    return obter_animal(ctx, animal_id)


def obter_animal(ctx: Contexto, animal_id: str) -> Animal:
    linha = repo.obter_animal(ctx.conn, animal_id)
    if linha is None:
        raise nao_encontrado("Animal não encontrado.")
    return _animal(ctx, linha)


def listar_animais(ctx: Contexto, busca: str | None) -> ListaAnimais:
    hoje = ctx.config.hoje()
    itens = [
        AnimalResumo(
            id=linha["id"],
            brinco=linha["brinco"],
            nome=linha["nome"],
            dias_em_lactacao=dias_em_lactacao(linha["ficha"].get(CAMPO_DATA_PARTO), hoje),
            ultima_sessao_id=linha["ultima_sessao_id"],
        )
        for linha in repo.listar_animais(ctx.conn, busca)
    ]
    return ListaAnimais(total=len(itens), itens=itens)


def listar_sessoes_do_animal(ctx: Contexto, animal_id: str) -> ListaSessoesAnimal:
    if repo.obter_animal(ctx.conn, animal_id) is None:
        raise nao_encontrado("Animal não encontrado.")
    bases: dict[str, dict] = {}  # a base de cada versão, carregada uma vez
    itens = []
    for linha in repo.listar_sessoes_do_animal(ctx.conn, animal_id):
        versao = linha["versao_base"]
        if versao not in bases:
            bases[versao] = para_motor(ctx.repo.carregar(versao))
        # só leitura: restaura o motor do snapshot (D1: {"motor": Sessao.exportar(), ...}) e pede o parecer, sem regravar
        parecer = Sessao.restaurar(bases[versao], **linha["snapshot"]["motor"]).parecer()
        hipoteses = sorted((i for b in parecer["blocos"] for i in b["itens"]), key=lambda i: (-i["cf"], i["doenca"]))
        itens.append(
            SessaoDoAnimal(
                sessao_id=linha["id"],
                modo=linha["modo"],
                versao_base=versao,
                fase=linha["fase"],
                urgencia=parecer["urgencia"],
                top1=hipoteses[0]["doenca"] if hipoteses and hipoteses[0]["situacao"] == "com_evidencia" else None,
                criada_em=linha["criada_em"],
            )
        )
    return ListaSessoesAnimal(itens=itens)
