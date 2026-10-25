"""Casos fictícios versionados exercitam o motor real e a execução via API."""
import json
from datetime import date, datetime
from pathlib import Path
import shutil

from fastapi.testclient import TestClient
import pytest

from api.config import Configuracao
from api.main import criar_app
from engine.casos import executar_caso
from engine.sessao import Sessao
from kb import Caso, carregar_base, para_motor

RAIZ = Path(__file__).resolve().parents[2]
ARQUIVO = RAIZ / 'base/casos/casos.json'
VERSOES = sorted((RAIZ / 'base/versoes').glob('v*.json'))


def casos():
    return json.loads(ARQUIVO.read_text(encoding='utf-8'))


def test_conjunto_conhecido_existe_e_cobre_todas_as_doencas_da_ativa_nos_dois_modos():
    assert ARQUIVO.is_file(), 'Falta publicar a Camada 3 em base/casos/casos.json'
    conjunto = casos()
    assert len({c['id'] for c in conjunto}) == len(conjunto) >= 31
    ativa = json.loads((RAIZ / 'base/ativa.json').read_text(encoding='utf-8'))['versao']
    base = carregar_base(RAIZ / 'base/versoes' / f'{ativa}.json')
    for doenca in [s.id for s in base.simbolos if s.tipo == 'doenca']:
        for modo in ('produtor', 'veterinario'):
            assert any(c['modo'] == modo and c['esperado'].get('top1') == doenca
                       and c['esperado'].get('faixas', {}).get(doenca, [0])[0] >= 50
                       for c in conjunto), (doenca, modo)
    for caso in conjunto:
        Caso.model_validate(caso)


@pytest.mark.parametrize('versao', VERSOES, ids=lambda p: p.stem)
def test_casos_conhecidos_por_versao(versao, subtests, record_property):
    base = para_motor(carregar_base(versao))
    ativa = json.loads((RAIZ / 'base/ativa.json').read_text(encoding='utf-8'))['versao']
    resultados = [executar_caso(base, caso) for caso in casos()]
    record_property('resultados_casos', json.dumps(resultados, ensure_ascii=False))
    if versao.stem == ativa:
        for resultado in resultados:
            with subtests.test(caso=resultado['caso_id'], versao=versao.stem):
                assert resultado['status'] == 'passou', resultado


def test_api_executa_todos_os_casos_da_ativa_sem_falhas(tmp_path):
    base_dir = tmp_path / 'base'
    shutil.copytree(RAIZ / 'base', base_dir)
    config = Configuracao(base_dir=base_dir, db_path=tmp_path / 'anamnese.db',
                         web_dist=tmp_path / 'web-dist-ausente',
                         hoje=lambda: date(2026, 10, 21),
                         agora=lambda: datetime(2026, 10, 21, 12, 0))
    ativa = json.loads((base_dir / 'ativa.json').read_text(encoding='utf-8'))['versao']
    with TestClient(criar_app(config)) as cliente:
        resposta = cliente.post(f'/api/base/versoes/{ativa}/execucoes', json={'casos': None})
        assert resposta.status_code == 201, resposta.text
        execucao = resposta.json()
        assert execucao['total'] == len(casos())
        assert execucao['falhou'] == 0, execucao['resultados']
        assert execucao['passou'] == execucao['total']
        consulta = cliente.get(f"/api/base/versoes/{ativa}/execucoes/{execucao['execucao_id']}")
        assert consulta.status_code == 200, consulta.text
        assert consulta.json()['resultados'] == execucao['resultados']


def test_correcao_da_triagem_remove_bandeira_e_preserva_as_demais_respostas():
    ativa = json.loads((RAIZ / 'base/ativa.json').read_text(encoding='utf-8'))['versao']
    sessao = Sessao(para_motor(carregar_base(RAIZ / 'base/versoes' / f'{ativa}.json')),
                    modo='produtor', ficha={'dias_em_lactacao': 120})
    sessao.responder_triagem('estado_termico', 'normal')
    sessao.responder_triagem('atitude_locomocao', ['decubito'])
    assert 'R-BV-01' in sessao.estado()['bandeiras']
    sessao.responder_triagem('atitude_locomocao', [], corrigir=True)
    estado = sessao.estado()
    assert not estado['pausa']
    assert 'R-BV-01' not in estado['bandeiras']
    assert sessao.fatos['dias_em_lactacao'].valor == 120
    assert sessao.fatos['extremidades'].valor == 'normal'
