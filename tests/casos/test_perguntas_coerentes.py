"""A fase dinâmica não contradiz a triagem: um "não" na triagem fecha as perguntas que dependem dele."""
import json
import unittest
from pathlib import Path

from engine.sessao import Sessao

RAIZ = Path(__file__).resolve().parents[2]


def _base_ativa():
    versao = json.loads((RAIZ / 'base/ativa.json').read_text(encoding='utf-8'))['versao']
    return json.loads((RAIZ / f'base/versoes/{versao}.json').read_text(encoding='utf-8'))


def _perguntas_feitas(triagem, sim=(), modo='produtor'):
    """Responde a triagem dada, "sim" às perguntas em ``sim`` e "não" (ou "não sei") às demais; devolve os ids perguntados."""
    sessao = Sessao(_base_ativa(), modo)
    for tela, valores in triagem:
        if sessao.estado()['pausa']:
            sessao.acao_bandeira('continuar')
        sessao.responder_triagem(tela, valores)
    feitas = []
    while True:
        estado = sessao.estado()
        if estado['pausa']:
            sessao.acao_bandeira('continuar')
            continue
        proxima = estado['proxima']
        if proxima is None:
            return feitas
        feitas.append(proxima['id'])
        sessao.responder(proxima['id'], True if proxima['id'] in sim else False if proxima['entrada']['tipo'] == 'booleano' else None)


# O quadro testado no navegador: 15 dias, vaca apática, sem apetite, queda de produção, sem outras alterações
# na triagem e, depois, barriga estufada à esquerda e pasto de leguminosa.
TRIAGEM = [
    ('dias_em_lactacao', {'dias_em_lactacao': '15'}),
    ('estado_termico', {'extremidades': 'normal'}),
    ('atitude_locomocao', {'apatia': True, 'claudicacao': False, 'decubito': False}),
    ('apetite_ruminacao', {'apetite': 'ausente'}),
    ('producao_leite', {'queda_producao': True, 'leite_alterado': False, 'ubere_inflamado': False}),
    ('excrecoes', {'diarreia': False, 'corrimento_vaginal': False, 'urina_escura': False}),
]

SIM = {'distensao_flanco_esquerdo', 'pasto_leguminosa_recente'}


class TestPerguntasCoerentes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.feitas = _perguntas_feitas(TRIAGEM, SIM)

    def test_sem_corrimento_nao_pergunta_o_cheiro_da_secrecao(self):
        self.assertNotIn('corrimento_fetido', self.feitas)

    def test_sem_claudicacao_nao_pergunta_o_casco(self):
        casco = {'mancar_pata_traseira_sem_inchaco', 'inchaco_entre_unhas_mau_cheiro'}
        self.assertFalse(casco & set(_perguntas_feitas(TRIAGEM)))

    def test_leite_sem_alteracao_nao_pergunta_sangue_no_leite(self):
        self.assertNotIn('leite_com_sangue', self.feitas)

    def test_sem_apetite_nao_pergunta_emagrecimento_mesmo_comendo(self):
        self.assertNotIn('emagrecimento_progressivo', self.feitas)

    def test_especialista_com_temperatura_nao_pergunta_as_extremidades(self):
        triagem = [('estado_termico', {'temperatura_retal': '40'}) if tela == 'estado_termico' else (tela, valores)
                   for tela, valores in TRIAGEM]
        self.assertNotIn('extremidades', _perguntas_feitas(triagem, modo='veterinario'))

    def test_texto_da_triagem_do_produtor_nao_cita_o_modo_veterinario(self):
        for tela in _base_ativa()['meta']['triagem']:
            self.assertNotIn('veterin', tela['texto']['produtor'].lower(), tela['id'])


if __name__ == '__main__':
    unittest.main()
