"""O parecer informa o teto de confiança que cada doença ainda pode alcançar."""
import unittest

from engine.sessao import Sessao
from .test_base_clinica import carregar


class PotencialDoParecer(unittest.TestCase):
    def itens(self, sessao):
        return {i['doenca']: i for b in sessao.parecer()['blocos'] for i in b['itens']}

    def responder_atitude(self, sessao):
        # Telas anteriores sem informação: dias na ficha e "não sei" no estado térmico.
        sessao.responder_triagem('dias_em_lactacao', 10)
        sessao.responder_triagem('estado_termico', 'nao_sei')
        sessao.responder_triagem('atitude_locomocao', {'apatia': False, 'claudicacao': False, 'decubito': True})

    def test_potencial_supera_percentual_quando_faltam_respostas(self):
        sessao = Sessao(carregar(), modo='veterinario')
        self.responder_atitude(sessao)
        itens = self.itens(sessao)
        self.assertGreater(itens['hipocalcemia']['potencial'], itens['hipocalcemia']['percentual'])

    def test_potencial_nunca_fica_abaixo_do_percentual(self):
        sessao = Sessao(carregar(), modo='veterinario')
        for item in self.itens(sessao).values():
            self.assertGreaterEqual(item['potencial'], item['percentual'])
        self.responder_atitude(sessao)
        for item in self.itens(sessao).values():
            self.assertGreaterEqual(item['potencial'], item['percentual'])


if __name__ == '__main__':
    unittest.main()
