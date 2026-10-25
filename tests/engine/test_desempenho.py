"""Desempenho da seleção: a mesma busca de consistência não é recalculada na mesma análise."""
import collections
import json
import unittest
from pathlib import Path
from unittest import mock

import engine.selecao as selecao
from engine.sessao import Sessao

RAIZ = Path(__file__).resolve().parents[2]


def _base_ativa():
    ativa = json.loads((RAIZ / 'base/ativa.json').read_text(encoding='utf-8'))
    versao = ativa.get('versao') or ativa.get('ativa')
    return json.loads((RAIZ / f'base/versoes/{versao}.json').read_text(encoding='utf-8'))


class TestDesempenhoSelecao(unittest.TestCase):
    def setUp(self):
        selecao.limpar_memoria()

    def test_restaurar_a_mesma_sessao_nao_refaz_a_analise(self):
        """A API restaura a sessão a cada requisição: o mesmo estado não é recalculado."""
        base = _base_ativa()
        primeira = Sessao(base, 'produtor')
        primeira.responder_triagem('dias_em_lactacao', {'dias_em_lactacao': '15'})
        with mock.patch.object(selecao, '_calcular_intervalos', wraps=selecao._calcular_intervalos) as contador:
            restaurada = Sessao.restaurar(_base_ativa(), **primeira.exportar())
        self.assertEqual(contador.call_count, 0)
        self.assertEqual(restaurada.estado(), primeira.estado())

    def test_fatos_diferentes_nao_reaproveitam_a_analise(self):
        base = _base_ativa()
        a = Sessao(base, 'produtor')
        a.responder_triagem('dias_em_lactacao', {'dias_em_lactacao': '15'})
        b = Sessao(base, 'produtor')
        b.responder_triagem('dias_em_lactacao', {'dias_em_lactacao': '2'})
        self.assertNotEqual(a.analise.resultado.fatos['dias_em_lactacao'], b.analise.resultado.fatos['dias_em_lactacao'])

    def test_modo_diferente_nao_reaproveita_a_analise(self):
        base = _base_ativa()
        self.assertNotEqual(Sessao(base, 'produtor').analise.modo, Sessao(base, 'veterinario').analise.modo)

    def test_limites_de_pergunta_avaliados_uma_vez_por_analise(self):
        sessao = Sessao(_base_ativa(), 'produtor')
        selecao.limpar_memoria()
        with mock.patch.object(selecao, 'avaliar_condicao', wraps=selecao.avaliar_condicao) as contador:
            sessao.responder_triagem('dias_em_lactacao', {'dias_em_lactacao': '15'})
        # Sem a memória das folhas são ~8,6 mil avaliações nesta resposta; com ela, ~4 mil.
        self.assertLess(contador.call_count, 6000)

    def test_intervalos_sem_verificacao_calculados_uma_vez_por_entrada(self):
        sessao = Sessao(_base_ativa(), 'produtor')
        original = selecao._calcular_intervalos
        chamadas = collections.Counter()

        def espiao(resultado, modo, fixos=None, excluidas=None, verificar=True):
            if not verificar:
                chamadas[(frozenset((fixos or {}).items()), frozenset(excluidas or ()))] += 1
            return original(resultado, modo, fixos, excluidas, verificar)

        with mock.patch.object(selecao, '_calcular_intervalos', espiao):
            sessao.responder_triagem('dias_em_lactacao', {'dias_em_lactacao': '15'})
        self.assertTrue(chamadas)
        self.assertEqual(max(chamadas.values()), 1, 'busca de consistência repetida com as mesmas entradas')


if __name__ == '__main__':
    unittest.main()
