"""Mapa ``operationId`` -> (modelo do corpo, modelo da resposta de sucesso) das 27 operações da 4.5.

É a fonte do teste de contrato: cada exemplo de ``contratos/exemplos`` e cada resposta real é validado
com o modelo daqui (``tests/api/apoio.py::validar_contrato``). ``None`` no corpo = a rota não recebe
corpo JSON (GET, ou multipart na importação).
"""
from __future__ import annotations

from api.schemas.animal import (
    Animal,
    ListaAnimais,
    ListaSessoesAnimal,
    NovoAnimal,
    ResultadoImportacao,
)
from api.schemas.base import (
    AtivarBody,
    AtivarResposta,
    EdicaoBase,
    Execucao,
    ExecutarBody,
    ListaExecucoes,
    ListaVersoes,
    SalvarResposta,
)
from api.schemas.explicacao import Como, PorQue, Traco
from api.schemas.parecer import Parecer
from api.schemas.sessao import (
    AcaoBandeira,
    CorrecaoPergunta,
    EstadoSessao,
    NovaSessao,
    RespostaPergunta,
    RespostaTriagem,
    TrocaModo,
)
from api.schemas.sistema import Saude
from kb.grafo import Grafo
from kb.modelos import Base
from kb.validador import Relatorio

CONTRATOS: dict[str, tuple[type | None, type]] = {
    # sistema
    "saude": (None, Saude),
    # sessões
    "criar_sessao": (NovaSessao, EstadoSessao),
    "obter_sessao": (None, EstadoSessao),
    "trocar_modo": (TrocaModo, EstadoSessao),
    "responder_triagem": (RespostaTriagem, EstadoSessao),
    "corrigir_triagem": (RespostaTriagem, EstadoSessao),
    "responder_pergunta": (RespostaPergunta, EstadoSessao),
    "corrigir_resposta": (CorrecaoPergunta, EstadoSessao),
    "acao_bandeira": (AcaoBandeira, EstadoSessao),
    "obter_parecer": (None, Parecer),
    "obter_porque": (None, PorQue),
    "obter_como": (None, Como),
    "obter_traco": (None, Traco),
    # animais
    "listar_animais": (None, ListaAnimais),
    "obter_animal": (None, Animal),
    "criar_animal": (NovoAnimal, Animal),
    "listar_sessoes_animal": (None, ListaSessoesAnimal),
    "importar_animais": (None, ResultadoImportacao),
    # base de conhecimento
    "listar_versoes": (None, ListaVersoes),
    "obter_versao": (None, Base),
    "obter_grafo": (None, Grafo),
    "validar_base": (EdicaoBase, Relatorio),
    "salvar_versao": (EdicaoBase, SalvarResposta),
    "ativar_versao": (AtivarBody, AtivarResposta),
    "executar_casos": (ExecutarBody, Execucao),
    "listar_execucoes": (None, ListaExecucoes),
    "obter_execucao": (None, Execucao),
}
