"""Etapa de doenças excludentes: o par rebaixa a hipótese mais fraca."""
import unittest
from fractions import Fraction

from engine.cf import combinar
from engine.inferencia import inferir
from engine.parecer import montar_parecer
from engine.sessao import Sessao
from .apoio import base, simbolo, doenca, regra, condicao


def montar(pares=(('x', 'y'),), doencas=('x', 'y'), exclusao=None):
    """Uma pergunta `s<d>` por doença, com regra direta de CF 0.99 (o máximo permitido)."""
    simbolos = [simbolo('s' + d) for d in doencas] + [doenca(d) for d in doencas]
    regras = [regra('r' + d, d, '0.99', condicao('s' + d)) for d in doencas]
    b = base(simbolos, regras, triagem=[{'id': 'tela', 'selecao': 'unica', 'simbolos': ['s' + d for d in doencas]}])
    b['meta']['exclusoes'] = [{'doencas': list(p), 'fonte': 'Teste sintético', 'nota': 'nota'} for p in pares]
    if exclusao is not None:
        b['meta']['limiares'] = {'exclusao': exclusao}
    return b


def fatos(**cfs):
    # O CF da doença é premissa * 0.99; dividir por 0.99 faz a doença terminar com o valor pedido.
    return {'s' + d: {'valor': True, 'cf': Fraction(v) / Fraction('0.99')} for d, v in cfs.items()}


class Exclusao(unittest.TestCase):
    def test_exclusao_rebaixa_mais_fraca(self):
        r = inferir(montar(), fatos(x='0.8', y='0.4'))
        self.assertEqual(r.cfs['x'], Fraction(4, 5))
        self.assertEqual(r.cfs['y'], combinar('0.4', '-0.8'))
        self.assertEqual(r.cfs['y'], Fraction(-2, 3))
        self.assertEqual(r.excluidas, frozenset({'y'}))
        item = {i['doenca']: i for b in montar_parecer(r)['blocos'] for i in b['itens']}['y']
        self.assertEqual(item['situacao'], 'descartada')

    def test_exclusao_abaixo_do_limiar_nao_age(self):
        r = inferir(montar(), fatos(x='0.45', y='0.3'))
        self.assertEqual((r.cfs['x'], r.cfs['y']), (Fraction(9, 20), Fraction(3, 10)))
        self.assertEqual(r.excluidas, frozenset())

    def test_exclusao_empate_nao_rebaixa(self):
        r = inferir(montar(), fatos(x='0.7', y='0.7'))
        self.assertEqual((r.cfs['x'], r.cfs['y']), (Fraction(7, 10), Fraction(7, 10)))
        self.assertEqual(r.excluidas, frozenset())

    def test_exclusao_ordem_dos_pares_irrelevante(self):
        dados = fatos(x='0.9', y='0.6', z='0.4')
        a = inferir(montar([('x', 'y'), ('y', 'z')], ('x', 'y', 'z')), dados)
        b = inferir(montar([('y', 'z'), ('x', 'y')], ('x', 'y', 'z')), dados)
        self.assertEqual(a.cfs, b.cfs)
        self.assertEqual(a.excluidas, b.excluidas)
        self.assertEqual(a.cfs['y'], combinar('0.6', '-0.9'))
        # z perde para y pelo CF lido antes de qualquer alteração (0.6 >= 0.5)
        self.assertEqual(a.cfs['z'], combinar('0.4', '-0.6'))

    def test_exclusao_gera_evento_no_traco(self):
        r = inferir(montar(), fatos(x='0.8', y='0.4'))
        eventos = [e for e in r.traco if e['tipo'] == 'exclusao_aplicada']
        self.assertEqual(len(eventos), 1)
        e = eventos[0]
        self.assertEqual((e['simbolo'], e['por']), ('y', 'x'))
        self.assertAlmostEqual(e['antes'], 0.4)
        self.assertAlmostEqual(e['depois'], -2 / 3)
        self.assertEqual((e['fonte'], e['nota']), ('Teste sintético', 'nota'))

    def test_limiar_configuravel(self):
        r = inferir(montar(exclusao=0.9), fatos(x='0.8', y='0.4'))
        self.assertEqual(r.excluidas, frozenset())

    def test_sem_exclusoes_na_base(self):
        b = montar(); del b['meta']['exclusoes']
        self.assertEqual(inferir(b, fatos(x='0.8', y='0.4')).excluidas, frozenset())

    def test_excluida_tem_potencial_igual_percentual(self):
        r = inferir(montar(), fatos(x='0.8', y='0.4'))
        potenciais = {'x': Fraction(4, 5), 'y': Fraction(1)}
        itens = {i['doenca']: i for b in montar_parecer(r, potenciais=potenciais)['blocos'] for i in b['itens']}
        self.assertEqual(itens['y']['potencial'], itens['y']['percentual'])

    def test_excluida_nao_fica_aberta_na_selecao(self):
        from engine.selecao import analisar
        a = analisar(montar(), fatos(x='0.8', y='0.4'), 'veterinario')
        self.assertNotIn('y', a.abertas)

    def test_como_mostra_exclusao(self):
        s = Sessao(montar(), ficha=fatos(x='0.8', y='0.4'))
        etapas = [e for e in s.como('y').get('exclusoes', []) if e['tipo'] == 'exclusao']
        self.assertEqual(len(etapas), 1)
        self.assertEqual(etapas[0]['por'], 'x')


if __name__ == '__main__':
    unittest.main()
