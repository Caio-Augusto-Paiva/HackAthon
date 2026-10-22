"""Validação estrita de respostas numéricas digitadas (domínio numérico)."""
import unittest
from fractions import Fraction
from decimal import Decimal

from tests.engine.apoio import modulo, simbolo

SIMBOLOS = {
    'dias': simbolo('dias', dominio='numerico'),
    'temp': simbolo('temp', dominio='numerico'),
    'livre': simbolo('livre', dominio='numerico'),
}
SIMBOLOS['dias']['dominio'].update(min=0, max=1000, casas_decimais=0)
SIMBOLOS['temp']['dominio'].update(min=30, max=45, casas_decimais=1)

ACEITOS_DIAS = [12, '12', 0, '1000', 12.0, Fraction(12), Decimal('12')]
RECUSADOS_DIAS = [
    '12.5', 12.5, '-3', '+3', ' 12', '12 ', '1e3', '1_000', '3/2', '0x10', '١٢', '12abc',
    '12; DROP TABLE sessoes', "' OR 1=1 --", '<script>', '', '1001', float('inf'), float('nan'),
    True, '12,5', '1.000', '12\n', '1234567', 1001, -1, Decimal('NaN'), Decimal('Infinity'), Fraction(1, 3),
]


class NumericoEstritoTest(unittest.TestCase):
    def observar(self, id, valor):
        return modulo('modelos').observar(id, valor, SIMBOLOS)

    def test_dias_aceitos(self):
        for valor in ACEITOS_DIAS:
            with self.subTest(valor=valor):
                self.assertEqual(self.observar('dias', valor).valor, Fraction(int(valor)))

    def test_dias_recusados(self):
        for valor in RECUSADOS_DIAS:
            with self.subTest(valor=valor):
                with self.assertRaises(ValueError):
                    self.observar('dias', valor)

    def test_uma_casa(self):
        for valor in ('38,5', '38.5', 38.5):
            with self.subTest(valor=valor):
                self.assertEqual(self.observar('temp', valor).valor, Fraction(385, 10))
        self.assertEqual(self.observar('temp', '38').valor, 38)
        for valor in ('38.55', '38,5,1', '38..5', '38.', '.5', '38.50', 38.55, '29,9', '45,1'):
            with self.subTest(valor=valor):
                with self.assertRaises(ValueError):
                    self.observar('temp', valor)

    def test_sem_casas_declaradas_vale_ate_duas(self):
        self.assertEqual(self.observar('livre', '1,25').valor, Fraction(125, 100))
        self.assertEqual(self.observar('livre', 1.25).valor, Fraction(125, 100))
        for valor in ('1,255', 1.255):
            with self.subTest(valor=valor):
                with self.assertRaises(ValueError):
                    self.observar('livre', valor)

    def test_mensagem_nao_ecoa_valor(self):
        for valor in ('12; DROP TABLE sessoes', '<script>', '1001', '12.5', 99999.5):
            with self.subTest(valor=valor):
                with self.assertRaises(ValueError) as ctx:
                    self.observar('dias', valor)
                self.assertNotIn(str(valor), str(ctx.exception))
                self.assertEqual(str(ctx.exception), 'dias: informe apenas números de 0 a 1000')

    def test_mensagem_sem_max(self):
        SIMBOLOS['livre']['dominio']['min'] = 0
        try:
            with self.assertRaises(ValueError) as ctx:
                self.observar('livre', 'abc')
            self.assertEqual(str(ctx.exception), 'livre: informe apenas números a partir de 0')
        finally:
            del SIMBOLOS['livre']['dominio']['min']

    def test_validacao_da_base_checa_casas_decimais(self):
        from tests.engine.apoio import base
        validar = modulo('validacao').validar
        for ruim in (4, -1, 1.5, True, '1'):
            s = simbolo('n', dominio='numerico'); s['dominio']['casas_decimais'] = ruim
            with self.subTest(ruim=ruim), self.assertRaises(ValueError):
                validar(base([s], []))
        for bom in (0, 3):
            s = simbolo('n', dominio='numerico'); s['dominio']['casas_decimais'] = bom
            validar(base([s], []))


if __name__ == '__main__':
    unittest.main()
