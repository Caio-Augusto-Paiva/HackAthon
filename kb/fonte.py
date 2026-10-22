"""Base de conhecimento separada por doença (``base/fonte/``) e junção exata de volta.

Formato em disco:

- ``comum.json``: ``meta``, ``layout`` e os símbolos/regras que não pertencem a uma só doença;
- ``doencas/<id>.json``: ``doenca``, os símbolos usados só por ela e as regras que a concluem
  (inclusive derivados exclusivos) e a regra de urgência que a cita;
- ``indice.json``: a ordem original de símbolos e regras, para a junção reproduzir a versão.

``ler_fonte(gravar_fonte(base))`` devolve exatamente ``base``. As versões em ``base/versoes/``
continuam sendo o que o motor lê; ``python -m kb.fonte juntar --salvar`` gera a próxima.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

from pydantic import ValidationError

from kb.modelos import Base, Regra, Simbolo

COMUM = "comum.json"
INDICE = "indice.json"
PASTA_DOENCAS = "doencas"


class FonteInvalida(ValueError):
    """A pasta de fonte não forma uma base: JSON inválido, id repetido ou doença sem símbolo."""


def _texto(dados) -> str:
    return json.dumps(dados, ensure_ascii=False, indent=2) + "\n"


def _dump(modelo) -> dict:
    return modelo.model_dump(mode="json", exclude_none=True)


def _uso_por_doenca(base: Base) -> dict[str, set[str]]:
    """Símbolos que cada doença usa, seguindo derivados transitivamente."""
    tipo = {s.id: s.tipo for s in base.simbolos}
    concluem: dict[str, list[Regra]] = defaultdict(list)
    for regra in base.regras:
        concluem[regra.entao.simbolo].append(regra)

    def usa(simbolo: str, vistos: set[str]) -> set[str]:
        achados: set[str] = set()
        for regra in concluem.get(simbolo, []):
            for condicao in regra.se:
                s = condicao.simbolo
                if s in vistos:
                    continue
                vistos.add(s)
                achados.add(s)
                if tipo.get(s) == "derivado":
                    achados |= usa(s, vistos)
        return achados

    return {d: usa(d, set()) for d, t in tipo.items() if t == "doenca"}


def separar(base: Base) -> dict[str, dict]:
    """Conteúdo de cada arquivo da fonte (caminho relativo -> JSON)."""
    tipo = {s.id: s.tipo for s in base.simbolos}
    uso = _uso_por_doenca(base)
    usado_por: dict[str, set[str]] = defaultdict(set)
    for doenca, simbolos in uso.items():
        for s in simbolos:
            usado_por[s].add(doenca)

    dono_simbolo: dict[str, str] = {}
    for doenca in uso:
        dono_simbolo[doenca] = doenca
    for s, doencas in usado_por.items():
        if len(doencas) == 1 and tipo.get(s) != "doenca":
            dono_simbolo[s] = next(iter(doencas))

    dono_regra: dict[str, str] = {}
    for regra in base.regras:
        alvo = regra.entao.simbolo
        citadas = {c.simbolo for c in regra.se if tipo.get(c.simbolo) == "doenca"}
        if tipo.get(alvo) == "doenca":
            dono_regra[regra.id] = alvo
        elif tipo.get(alvo) == "derivado" and alvo in dono_simbolo:
            dono_regra[regra.id] = dono_simbolo[alvo]
        elif regra.classe == "urgencia" and len(citadas) == 1:
            dono_regra[regra.id] = next(iter(citadas))

    arquivos: dict[str, dict] = {
        COMUM: {"meta": _dump(base.meta), "simbolos": [], "regras": [],
                "layout": {k: _dump(v) for k, v in base.layout.items()}},
    }
    for doenca in sorted(uso):
        arquivos[f"{PASTA_DOENCAS}/{doenca}.json"] = {"doenca": doenca, "simbolos": [], "regras": []}

    def destino(dono: str | None) -> dict:
        return arquivos[f"{PASTA_DOENCAS}/{dono}.json"] if dono else arquivos[COMUM]

    for simbolo in base.simbolos:
        destino(dono_simbolo.get(simbolo.id))["simbolos"].append(_dump(simbolo))
    for regra in base.regras:
        destino(dono_regra.get(regra.id))["regras"].append(_dump(regra))
    arquivos[INDICE] = {"ordem_simbolos": [s.id for s in base.simbolos],
                        "ordem_regras": [r.id for r in base.regras]}
    return arquivos


def gravar_fonte(base: Base, pasta: Path) -> list[Path]:
    """Escreve a fonte em ``pasta``; arquivos de doença que não existem mais são removidos."""
    pasta = Path(pasta)
    (pasta / PASTA_DOENCAS).mkdir(parents=True, exist_ok=True)
    conteudo = separar(base)
    for antigo in (pasta / PASTA_DOENCAS).glob("*.json"):
        if f"{PASTA_DOENCAS}/{antigo.name}" not in conteudo:
            antigo.unlink()
    escritos = []
    for relativo, dados in conteudo.items():
        caminho = pasta / relativo
        caminho.write_text(_texto(dados), encoding="utf-8")
        escritos.append(caminho)
    return escritos


def _ler_json(caminho: Path) -> dict:
    try:
        dados = json.loads(caminho.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise FonteInvalida(f"Arquivo da fonte não encontrado: {caminho.name}.") from None
    except json.JSONDecodeError as erro:
        raise FonteInvalida(f"{caminho.name} não é um JSON válido (linha {erro.lineno}).") from None
    if not isinstance(dados, dict):
        raise FonteInvalida(f"{caminho.name} deve conter um objeto JSON.")
    return dados


def _ordenar(itens: list, ordem: list[str]) -> list:
    posicao = {id_: i for i, id_ in enumerate(ordem)}
    conhecidos = sorted((x for x in itens if x.id in posicao), key=lambda x: posicao[x.id])
    return conhecidos + [x for x in itens if x.id not in posicao]


def ler_fonte(pasta: Path) -> Base:
    """Junta ``comum.json`` e ``doencas/*.json`` numa ``Base`` na ordem do ``indice.json``."""
    pasta = Path(pasta)
    comum = _ler_json(pasta / COMUM)
    arquivos = [(COMUM, comum)] + [(c.name, _ler_json(c)) for c in sorted((pasta / PASTA_DOENCAS).glob("*.json"))]
    indice = _ler_json(pasta / INDICE) if (pasta / INDICE).is_file() else {}

    origem: dict[str, str] = {}
    simbolos: list[Simbolo] = []
    regras: list[Regra] = []
    for nome, dados in arquivos:
        try:
            novos_s = [Simbolo.model_validate(s) for s in dados.get("simbolos", [])]
            novos_r = [Regra.model_validate(r) for r in dados.get("regras", [])]
        except ValidationError as erro:
            raise FonteInvalida(f"{nome} tem um símbolo ou regra fora do formato: {erro.errors()[0]['msg']}.") from None
        for item in [*novos_s, *novos_r]:
            if item.id in origem:
                raise FonteInvalida(f"O id {item.id} aparece em {origem[item.id]} e em {nome}; cada id deve estar em um só arquivo.")
            origem[item.id] = nome
        if nome != COMUM:
            doenca = dados.get("doenca")
            if not any(s.id == doenca and s.tipo == "doenca" for s in novos_s):
                raise FonteInvalida(f"{nome} deve conter o símbolo da doença {doenca!r} com tipo \"doenca\".")
        simbolos += novos_s
        regras += novos_r

    try:
        return Base.model_validate({
            "meta": comum.get("meta", {}),
            "simbolos": [_dump(s) for s in _ordenar(simbolos, indice.get("ordem_simbolos", []))],
            "regras": [_dump(r) for r in _ordenar(regras, indice.get("ordem_regras", []))],
            "layout": comum.get("layout", {}),
        })
    except ValidationError as erro:
        raise FonteInvalida(f"comum.json: {erro.errors()[0]['msg']}.") from None


def _diferencas(nova: Base, ativa: Base) -> list[str]:
    linhas = []
    for nome, a, b in (("símbolo", nova.simbolos, ativa.simbolos), ("regra", nova.regras, ativa.regras)):
        ma, mb = {x.id: x for x in a}, {x.id: x for x in b}
        linhas += [f"+ {nome} {i}" for i in ma.keys() - mb.keys()]
        linhas += [f"- {nome} {i}" for i in mb.keys() - ma.keys()]
        linhas += [f"~ {nome} {i}" for i in ma.keys() & mb.keys() if ma[i] != mb[i]]
    if nova.meta.model_dump(exclude={"versao", "pai", "autor", "data", "nota"}) != \
            ativa.meta.model_dump(exclude={"versao", "pai", "autor", "data", "nota"}):
        linhas.append("~ meta (limiares, triagem ou limites)")
    return sorted(linhas)


def main(argv: list[str] | None = None) -> int:
    from kb.carregador import BaseInvalida, Repositorio

    parser = argparse.ArgumentParser(prog="python -m kb.fonte", description="Separa e junta a base por doença.")
    sub = parser.add_subparsers(dest="comando", required=True)
    p_sep = sub.add_parser("separar", help="escreve base/fonte a partir de uma versão")
    p_sep.add_argument("--versao", required=True)
    p_sep.add_argument("--destino", default="base/fonte")
    p_jun = sub.add_parser("juntar", help="junta base/fonte e compara com a versão ativa")
    p_jun.add_argument("--origem", default="base/fonte")
    p_jun.add_argument("--salvar", action="store_true", help="grava a próxima versão (sem ativar)")
    p_jun.add_argument("--autor")
    p_jun.add_argument("--nota")
    p_jun.add_argument("--raiz", default="base", help="pasta do repositório de versões")
    args = parser.parse_args(argv)
    repo = Repositorio(Path(args.raiz if args.comando == "juntar" else "base"))

    if args.comando == "separar":
        escritos = gravar_fonte(repo.carregar(args.versao), Path(args.destino))
        print(f"{len(escritos)} arquivos escritos em {args.destino} a partir da {args.versao}.")
        return 0

    try:
        nova = ler_fonte(Path(args.origem))
    except FonteInvalida as erro:
        print(f"Erro: {erro}", file=sys.stderr)
        return 1
    ativa_id = repo.versao_ativa()
    diferencas = _diferencas(nova, repo.carregar_ativa()) if ativa_id else ["(sem versão ativa)"]
    print(f"Idêntica à {ativa_id}." if not diferencas else "Diferenças para a versão ativa:\n" + "\n".join(diferencas))
    if args.salvar:
        if not (args.autor and args.nota):
            print("Erro: --salvar exige --autor e --nota.", file=sys.stderr)
            return 2
        try:
            versao = repo.salvar_nova(nova, autor=args.autor, nota=args.nota)
        except BaseInvalida as erro:
            print(f"Erro: {erro}", file=sys.stderr)
            return 1
        print(f"Gravada a {versao} (não ativada).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
