"""Regressões dos seis ajustes do motor a partir de aaa7841."""
import unittest
from fractions import Fraction

from engine.sessao import Sessao
from engine.casos import executar_caso
from engine.modelos import Base
from engine.inferencia import inferir
from .apoio import base, simbolo, doenca, regra, condicao


def sessao_com_bandeira_travada():
    b=base([simbolo('x'),simbolo('y'),simbolo('w'),simbolo('z','derivado'),doenca(),
            simbolo('chamar_agora','urgencia')],
           [regra('z1','z',0.8,condicao('x')),regra('z2','z',-0.9,condicao('y')),
            regra('dy','d',0.4,condicao('y')),regra('dw','d',0.4,condicao('w')),
            regra('bv','chamar_agora',0.99,condicao('z'),classe='bandeira_vermelha')],
           triagem=[{'id':'tela_x','selecao':'unica','simbolos':['x']}])
    s=Sessao(b,ficha={'x':True})
    s.acao_bandeira('continuar')
    s.responder('w',True)
    s.responder('y',True)
    return s


class DependenciasBandeiraTests(unittest.TestCase):
    def test_correcao_sem_relacao_preserva_bandeira_travada_e_reconhecimento(self):
        s=sessao_com_bandeira_travada()
        self.assertEqual(s.resultado.bandeiras,())
        self.assertEqual(s.estado()['urgencia'],'chamar_agora')
        s.responder('w',False,corrigir=True)
        self.assertEqual(s.estado()['urgencia'],'chamar_agora')
        self.assertEqual(s.estado()['bandeiras'],['bv'])
        self.assertFalse(s.estado()['pausa'])
        self.assertEqual(s.reconhecidas,{'bv'})

    def test_correcao_da_origem_do_derivado_remove_bandeira_travada(self):
        s=sessao_com_bandeira_travada()
        s.responder_triagem('tela_x',False,corrigir=True)
        self.assertEqual(s.estado()['bandeiras'],[])
        self.assertNotEqual(s.estado()['urgencia'],'chamar_agora')
        self.assertEqual(s.reconhecidas,set())


class InconclusivasExecutorTests(unittest.TestCase):
    def executar_com_esperado(self,esperado):
        b=base([simbolo('x'),doenca('d1'),doenca('d2'),doenca('d3')],
               [regra('r1','d1',0.5,condicao('x')),regra('r2','d2',0.5,condicao('x'))])
        return executar_caso(b,{'modo':'produtor','ficha':{'x':True},'limite_dinamico':0,
                                'esperado':{'inconclusivas':esperado}})

    def test_inconclusivas_aceita_doencas_adicionais_ao_esperado(self):
        resultado=self.executar_com_esperado(['d1'])
        self.assertEqual(resultado['obtido']['inconclusivas'],['d1','d2'])
        self.assertEqual(resultado['status'],'passou',resultado)

    def test_inconclusivas_falha_quando_falta_doenca_esperada(self):
        resultado=self.executar_com_esperado(['d1','d3'])
        self.assertEqual(resultado['status'],'falhou',resultado)
        self.assertEqual(resultado['falhas'][0]['campo'],'inconclusivas')


class CfUrgenciaTests(unittest.TestCase):
    def verificar_rejeicao(self,classe):
        for cf in (-0.9,0):
            with self.subTest(cf=cf):
                b=base([simbolo('x'),doenca(),simbolo('chamar_agora','urgencia')],
                       [regra('r','chamar_agora',cf,condicao('x'),classe=classe)])
                with self.assertRaisesRegex(ValueError,'^CF de urgência ou bandeira deve ser positivo$'):
                    Base.de_dict(b)

    def test_urgencia_rejeita_cf_negativo_e_zero(self):
        self.verificar_rejeicao('urgencia')

    def test_bandeira_rejeita_cf_negativo_e_zero(self):
        self.verificar_rejeicao('bandeira_vermelha')

    def test_inferencia_nao_ativa_alerta_quando_cf_final_nao_e_positivo(self):
        for classe in ('urgencia','bandeira_vermelha'):
            for cf in (0.6,0.8):
                with self.subTest(classe=classe,cf=cf):
                    b=Base.de_dict(base([simbolo('x'),doenca(),simbolo('chamar_agora','urgencia')],
                                        [regra('a','chamar_agora',0.6,condicao('x'),classe=classe),
                                         regra('z','chamar_agora',cf,condicao('x'),classe=classe)]))
                    # Exercita a defesa quando uma Base pronta evita nova validação.
                    b.regras[1]['entao']['cf']=-cf
                    resultado=inferir(b,{'x':True})
                    self.assertLessEqual(resultado.cfs['chamar_agora'],0)
                    self.assertEqual(resultado.urgencia,'sem_problema')
                    self.assertEqual(resultado.bandeiras,())


class ModelDumpTests(unittest.TestCase):
    def test_model_dump_descarta_limites_de_cf_nulos(self):
        class ObjetoBase:
            def model_dump(self,mode='python',exclude_none=False):
                dados=base([simbolo('x'),doenca()],[regra('r','d',0.8,condicao('x'))])
                if not exclude_none:
                    dados['regras'][0]['se'][0].update(cf_minimo=None,cf_maximo=None)
                return dados

        try:
            normalizada=Base.de_dict(ObjetoBase())
        except ValueError as erro:
            self.fail(f'Base válida com campos opcionais nulos foi recusada: {erro}')
        self.assertEqual(inferir(normalizada,{'x':True}).cfs['d'],Fraction(4,5))
