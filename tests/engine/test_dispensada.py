"""Pergunta dispensada: um sinal mais preciso já respondido torna outra pergunta desnecessária."""
import unittest

from engine.sessao import Sessao
from tests.engine.apoio import base, condicao, doenca, regra, simbolo


def _base():
    """Febre vem da temperatura (mais precisa) ou, na falta dela, das extremidades."""
    temperatura = simbolo('temperatura', dominio='numerico')
    extremidades = simbolo('extremidades', dominio='categorico', dispensada_se=['temperatura'])
    extremidades['dominio']['valores'] = ['normal', 'quente', 'fria']
    return base([temperatura, extremidades, simbolo('febre', 'derivado'), doenca('d')],
                [regra('r-temp', 'febre', 0.95, condicao('temperatura', 39.5, op='≥')),
                 regra('r-ext', 'febre', 0.45, condicao('extremidades', 'quente')),
                 regra('r-d', 'd', 0.7, condicao('febre'))])


def _perguntas(sessao):
    feitas = []
    while (proxima := sessao.estado()['proxima']) is not None:
        feitas.append(proxima['id'])
        sessao.responder(proxima['id'], None)
    return feitas


class TestPerguntaDispensada(unittest.TestCase):
    def test_temperatura_respondida_dispensa_as_extremidades(self):
        s = Sessao(_base(), 'veterinario', ficha={'temperatura': 40})
        self.assertNotIn('extremidades', _perguntas(s))

    def test_temperatura_desconhecida_mantem_as_extremidades(self):
        s = Sessao(_base(), 'veterinario', ficha={'temperatura': 'nao_sei'})
        self.assertIn('extremidades', _perguntas(s))

    def test_sem_temperatura_pergunta_as_extremidades(self):
        self.assertIn('extremidades', _perguntas(Sessao(_base(), 'veterinario')))


if __name__ == '__main__':
    unittest.main()
