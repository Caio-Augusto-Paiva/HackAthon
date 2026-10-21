"""Bandeiras travadas dependem só das respostas finais e da ordem em que entraram."""
import json
import unittest

from engine.sessao import Sessao
from .apoio import base, simbolo, doenca, regra, condicao


def regras_sonda(**extras):
    return [regra('z1','z',0.8,condicao('x')),regra('z2','z',-0.9,condicao('y')),
            regra('dy','d',0.4,condicao('y')),regra('dw','d',0.4,condicao('w')),
            regra('bv','chamar_agora',0.99,condicao('z'),classe='bandeira_vermelha')]


def base_sonda():
    return base([simbolo('x','ficha'),simbolo('y'),simbolo('w'),simbolo('z','derivado'),doenca(),
                 simbolo('chamar_agora','urgencia')],regras_sonda())


def sessao_sonda(y,corrigir_para=None):
    s=Sessao(base_sonda(),ficha={'x':True})
    s.acao_bandeira('continuar')
    s.responder('w',True)
    s.responder('y',y)
    if corrigir_para is not None: s.responder('y',corrigir_para,corrigir=True)
    return s


class ReprocessamentoTests(unittest.TestCase):
    def test_mesmas_respostas_finais_dao_mesma_bandeira(self):
        for nome,s in (('direto',sessao_sonda(True)),('falso_corrigido',sessao_sonda(False,True)),
                       ('mesmo_valor',sessao_sonda(True,True))):
            with self.subTest(nome):
                self.assertEqual(s.estado()['urgencia'],'chamar_agora')
                self.assertEqual(s.estado()['bandeiras'],['bv'])

    def test_corrigir_gatilho_remove_bandeira(self):
        b=base([simbolo('x'),simbolo('y'),simbolo('w'),simbolo('z','derivado'),doenca(),
                simbolo('chamar_agora','urgencia')],
               regras_sonda()+[regra('dx','d',0.4,condicao('x'))])
        s=Sessao(b)
        s.responder('w',True)
        s.responder('x',True)
        self.assertEqual(s.estado()['bandeiras'],['bv'])
        s.acao_bandeira('continuar')
        s.responder('y',True)
        s.responder('x',False,corrigir=True)
        self.assertNotIn('bv',s.estado()['bandeiras'])
        self.assertNotEqual(s.estado()['urgencia'],'chamar_agora')

    def test_correcao_parcial_de_tela_multipla_mantem_bandeira(self):
        b=base([simbolo('a'),simbolo('b'),simbolo('y'),simbolo('w'),simbolo('z','derivado'),doenca(),
                simbolo('chamar_agora','urgencia')],
               [regra('z1','z',0.8,condicao('a')),regra('z2','z',-0.9,condicao('y')),
                regra('dy','d',0.4,condicao('y')),regra('dw','d',0.4,condicao('w')),
                regra('bv','chamar_agora',0.99,condicao('z'),classe='bandeira_vermelha')],
               triagem=[{'id':'T','selecao':'multipla','simbolos':['a','b']}])
        s=Sessao(b)
        s.responder_triagem('T',['a'])
        self.assertEqual(s.estado()['bandeiras'],['bv'])
        s.acao_bandeira('continuar')
        s.responder('w',True)
        s.responder('y',True)
        self.assertEqual(s.resultado.bandeiras,())
        s.responder_triagem('T',['a','b'],corrigir=True)
        self.assertEqual(s.estado()['bandeiras'],['bv'])
        self.assertEqual(s.estado()['urgencia'],'chamar_agora')

    def test_reprocessamento_independe_do_historico_de_edicao(self):
        direto=Sessao(base_sonda(),ficha={'x':True})
        direto.acao_bandeira('continuar')
        direto.responder('w',True); direto.responder('y',True)
        editada=Sessao(base_sonda(),ficha={'x':True})
        editada.acao_bandeira('continuar')
        editada.responder('w',True); editada.responder('y',False)
        editada.responder('w',False,corrigir=True); editada.responder('y',True,corrigir=True)
        editada.responder('w',True,corrigir=True)
        for campo in ('urgencia','bandeiras','pausa','fase'):
            self.assertEqual(editada.estado()[campo],direto.estado()[campo],campo)

    def test_restaurar_deriva_bandeiras_sem_bandeiras_ativas(self):
        s=sessao_sonda(False,True)
        snap=json.loads(json.dumps(s.exportar()))
        snap.pop('bandeiras_ativas',None)
        r=Sessao.restaurar(s.base,**snap)
        self.assertEqual(r.estado(),s.estado())
        self.assertEqual(list(r.como('chamar_agora')['bandeiras_historicas']),['bv'])

    def test_restaurar_ignora_bandeiras_ativas_recebidas(self):
        s=sessao_sonda(False,True)
        snap=json.loads(json.dumps(s.exportar()))
        r=Sessao.restaurar(s.base,**{**snap,'bandeiras_ativas':{'inexistente':{}}})
        self.assertEqual(r.estado(),s.estado())

    def test_correcao_que_remove_gatilho_e_volta_a_disparar_pausa_de_novo(self):
        b=base([simbolo('x'),simbolo('w'),simbolo('chamar_agora','urgencia'),doenca()],
               [regra('dw','d',0.4,condicao('w')),regra('dx','d',0.4,condicao('x')),
                regra('bv','chamar_agora',0.99,condicao('x'),classe='bandeira_vermelha')])
        s=Sessao(b)
        s.responder('w',True)
        s.responder('x',True); s.acao_bandeira('continuar')
        s.responder('x',False,corrigir=True)
        self.assertEqual(s.estado()['bandeiras'],[])
        s.responder('x',True,corrigir=True)
        self.assertTrue(s.estado()['pausa'])


if __name__=='__main__':
    unittest.main()
