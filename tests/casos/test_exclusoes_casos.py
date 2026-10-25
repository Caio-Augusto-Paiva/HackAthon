"""Casos dos pares excludentes: a doença perdedora termina em pouco_provavel e descartada."""
import json
from pathlib import Path

import pytest

from engine.casos import executar_caso
from engine.sessao import Sessao
from kb import carregar_base, para_motor

RAIZ = Path(__file__).resolve().parents[2]
PERDEDORAS = {
    'C-EXC-DAB': 'deslocamento_abomaso_esquerda',
    'C-EXC-TIM': 'timpanismo_gasoso',
}


def _base_ativa():
    versao = json.loads((RAIZ / 'base/ativa.json').read_text(encoding='utf-8'))['versao']
    return para_motor(carregar_base(RAIZ / 'base/versoes' / f'{versao}.json'))


def _parecer(base, caso):
    """Repete o diálogo do executor de casos e devolve a sessão encerrada."""
    sessao = Sessao(base, caso['modo'], caso.get('ficha'), caso.get('limite_dinamico'))
    for _ in range(500):
        estado = sessao.estado()
        if estado['pausa']:
            sessao.acao_bandeira('continuar')
            continue
        if estado['fase'] == 'encerrada':
            return sessao
        proxima = estado['proxima']
        if proxima['tipo'] == 'tela_triagem':
            sessao.responder_triagem(proxima['id'], caso['triagem'].get(proxima['id'], 'nao_sei'))
        else:
            sessao.responder(proxima['id'], caso['respostas'].get(proxima['id'], 'nao_sei'))
    raise AssertionError('o diálogo não terminou')


@pytest.mark.parametrize('caso_id,perdedora', sorted(PERDEDORAS.items()))
def test_perdedora_do_par_fica_descartada(caso_id, perdedora):
    casos = {c['id']: c for c in json.loads((RAIZ / 'base/casos/casos.json').read_text(encoding='utf-8'))}
    caso = casos[caso_id]
    base = _base_ativa()
    assert executar_caso(base, caso)['status'] == 'passou'
    sessao = _parecer(base, caso)
    # a perdedora foi rebaixada pela exclusão, e não só por um diferencial negativo
    assert perdedora in sessao.resultado.excluidas
    eventos = [e for e in sessao.resultado.traco if e['tipo'] == 'exclusao_aplicada' and e['simbolo'] == perdedora]
    assert eventos, sessao.resultado.traco
    assert all(e['antes'] > 0 for e in eventos), eventos  # tinha evidência positiva antes da exclusão
    parecer = sessao.parecer()
    bloco = next(b for b in parecer['blocos'] if b['id'] == 'pouco_provavel')
    item = next((x for x in bloco['itens'] if x['doenca'] == perdedora), None)
    assert item is not None, (perdedora, parecer['blocos'])
    assert item['situacao'] == 'descartada'
