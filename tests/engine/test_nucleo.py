from fractions import Fraction as F
from itertools import permutations
import unittest
from .apoio import modulo, base, simbolo, doenca, regra, condicao


class CertezaTests(unittest.TestCase):
    def test_combinacao_exata_sinais_e_extremos(self):
        combinar = modulo('cf').combinar
        for a, b, esperado in [('0.7', '0.6', F(22,25)), ('-0.7', '-0.6', -F(22,25)),
                                ('0.8','-0.5', F(3,5)), ('1','-1', F(0)), ('0','0', F(0))]:
            self.assertEqual(combinar(F(a), F(b)), esperado)

    def test_permutacoes_2_a_6_e_acumuladores_independentes(self):
        combinar = modulo('cf').combinar
        entradas = [F(3,5), F(-2,5), F(1,2), F(-1,5), F(7,10), F(-3,10)]
        for n in range(2,7):
            positivos = F(1)
            negativos = F(1)
            for x in entradas[:n]:
                if x > 0: positivos *= 1-x
                else: negativos *= 1+x
            esperado = (negativos-positivos)/max(positivos,negativos)
            for ordem in permutations(entradas[:n]):
                obtido = F(0)
                for x in ordem: obtido = combinar(obtido,x)
                self.assertEqual(obtido, esperado)

    def test_muitas_positivas_nao_arredondam_para_um(self):
        cf = modulo('cf')
        valor = F(0)
        for _ in range(100): valor = cf.combinar(valor, cf.fracao(0.99))
        self.assertLess(valor, 1)
        self.assertGreater(cf.combinar(valor, F(-99,100)), 0)

    def test_rejeita_cf_invalido(self):
        for valor in [1.01, -1.01, float('nan'), float('inf'), True]:
            with self.assertRaises(ValueError): modulo('cf').fracao(valor)


class AvaliacaoTests(unittest.TestCase):
    def avaliar(self, c, fatos, tipo='booleano'):
        return modulo('avaliacao').avaliar_condicao(c, fatos, {'x': simbolo('x', dominio=tipo)})

    def test_booleano_negativo_e_negacao_explicita(self):
        self.assertEqual(self.avaliar(condicao('x',False), {'x': {'valor':False,'cf':-1}}),1)
        self.assertEqual(self.avaliar(condicao('x',True,negado=True), {'x': {'valor':False,'cf':-1}}),1)

    def test_operadores_numericos_e_categoricos(self):
        for op, valor, esperado in [('=',3,1), ('≠',3,-1), ('<',4,1), ('≤',3,1),('>',4,-1),('≥',3,1),('em',[2,3],1)]:
            self.assertEqual(self.avaliar(condicao('x',valor,op), {'x':{'valor':3,'cf':1}},'numerico'),esperado)
        self.assertEqual(self.avaliar(condicao('x','normal'), {'x':{'valor':'grave','cf':0.6}},'categorico'),-F(3,5))

    def test_ausente_nao_sei_e_cf_zero_nao_avaliam_operador(self):
        for fatos in [{}, {'x':{'valor':None,'cf':0}}, {'x':{'valor':'nao_sei','cf':0}}]:
            for negado in [True,False]:
                self.assertEqual(self.avaliar(condicao('x',20,'≥',negado=negado),fatos,'numerico'),0)

    def test_limiares_cf_inclusivos_e_sinal(self):
        c = condicao('x', cf_minimo=0.5)
        self.assertEqual(self.avaliar(c,{'x':{'valor':True,'cf':0.49}}),0)
        self.assertEqual(self.avaliar(c,{'x':{'valor':True,'cf':0.5}}),F(1,2))
        self.assertEqual(self.avaliar(condicao('x',cf_maximo=0.5),{'x':{'valor':True,'cf':-0.6}}),F(3,5))


class ValidacaoTests(unittest.TestCase):
    def validar(self,b): return modulo('modelos').Base.de_dict(b)

    def test_rejeita_leitura_mesma_camada_e_ciclos(self):
        for origem,destino in [('d','e'),('e','e')]:
            with self.assertRaisesRegex(ValueError,'camada'):
                self.validar(base([doenca('d'),doenca('e')],[regra('r',destino,0.5,condicao(origem))]))

    def test_rejeita_regra_extrema_max_negativo_e_ids_duplicados(self):
        for peso in [-1,1]:
            with self.assertRaises(ValueError): self.validar(base([simbolo('x'),doenca()],[regra('r','d',peso,condicao('x'))]))
        with self.assertRaises(ValueError):
            self.validar(base([simbolo('x'),simbolo('z','derivado',combinacao='max')],[regra('r','z',-0.5,condicao('x'))]))
        with self.assertRaises(ValueError): self.validar(base([simbolo('x'),simbolo('x')],[]))

    def test_rejeita_referencia_inexistente_e_condicao_sem_fonte(self):
        with self.assertRaises(ValueError): self.validar(base([doenca()],[regra('r','d',0.5,condicao('ausente'))]))
        b=base([simbolo('x'),doenca()],[regra('r','d',0.5,condicao('x'))]); b['regras'][0]['fonte']=''
        with self.assertRaises(ValueError): self.validar(b)


if __name__ == '__main__': unittest.main()
