"""Modo especialista pergunta até esgotar; qualquer modo pode encerrar e ver o resultado na hora."""
import unittest

from engine.sessao import Sessao
from tests.engine.apoio import base, condicao, doenca, regra, simbolo


def _base(limite=None):
    """d1 se confirma só com x; d2 depende de y, que ainda não foi perguntado; d3 depende de z."""
    b = base([simbolo('x'), simbolo('y'), simbolo('z'), doenca('d1'), doenca('d2'), doenca('d3')],
             [regra('r1', 'd1', 0.95, condicao('x')), regra('r2', 'd2', 0.95, condicao('y')),
              regra('r3', 'd3', 0.95, condicao('z'))])
    if limite is not None:
        b['meta']['limite_dinamico'] = {'produtor': limite, 'veterinario': limite}
    return b


def _responder_tudo(sessao, valores):
    feitas = []
    while (proxima := sessao.estado()['proxima']) is not None:
        feitas.append(proxima['id'])
        sessao.responder(proxima['id'], valores.get(proxima['id'], False))
    return feitas


class TestEspecialistaExaustivo(unittest.TestCase):
    def test_produtor_para_na_confirmacao(self):
        s = Sessao(_base(), 'produtor', ficha={'x': True})
        self.assertEqual(s.estado()['motivo_parada'], 'confirmacao')

    def test_especialista_nao_para_na_confirmacao_se_outra_doenca_pode_subir(self):
        s = Sessao(_base(), 'veterinario', ficha={'x': True})
        self.assertIsNone(s.estado()['motivo_parada'])
        self.assertEqual(sorted(_responder_tudo(s, {})), ['y', 'z'])
        self.assertEqual(s.estado()['motivo_parada'], 'sem_perguntas')

    def test_especialista_ignora_o_limite_da_base(self):
        s = Sessao(_base(limite=1), 'veterinario')
        self.assertEqual(len(_responder_tudo(s, {})), 3)

    def test_especialista_respeita_limite_explicito_da_sessao(self):
        s = Sessao(_base(), 'veterinario', limite_dinamico=1)
        self.assertEqual(len(_responder_tudo(s, {})), 1)
        self.assertEqual(s.estado()['motivo_parada'], 'limite')

    def test_progresso_do_especialista_nao_tem_limite(self):
        self.assertIsNone(Sessao(_base(), 'veterinario').limite_efetivo())
        self.assertEqual(Sessao(_base(limite=4), 'produtor').limite_efetivo(), 4)
        self.assertEqual(Sessao(_base(), 'veterinario', limite_dinamico=2).limite_efetivo(), 2)


class TestVerResultadoAgora(unittest.TestCase):
    def test_ver_parecer_sem_bandeira_encerra_e_guarda_o_calculo(self):
        s = Sessao(_base(), 'veterinario', ficha={'x': True})
        antes = s.parecer()['blocos']
        estado = s.acao_bandeira('ver_parecer')
        self.assertEqual((estado['fase'], estado['proxima'], estado['motivo_parada']), ('encerrada', None, None))
        self.assertEqual(s.parecer()['blocos'], antes)

    def test_parecer_encerrado_cedo_mostra_quem_ainda_pode_subir(self):
        s = Sessao(_base(), 'veterinario', ficha={'x': True})
        s.acao_bandeira('ver_parecer')
        itens = {i['doenca']: i for b in s.parecer()['blocos'] for i in b['itens']}
        self.assertGreater(itens['d2']['potencial'], itens['d2']['percentual'])

    def test_continuar_retoma_depois_de_ver_o_resultado(self):
        s = Sessao(_base(), 'veterinario', ficha={'x': True})
        s.acao_bandeira('ver_parecer')
        estado = s.acao_bandeira('continuar')
        self.assertNotEqual(estado['fase'], 'encerrada')
        self.assertIsNotNone(estado['proxima'])

    def test_continuar_sem_ter_encerrado_e_sem_bandeira_e_recusado(self):
        with self.assertRaises(ValueError):
            Sessao(_base(), 'veterinario').acao_bandeira('continuar')


if __name__ == '__main__':
    unittest.main()
