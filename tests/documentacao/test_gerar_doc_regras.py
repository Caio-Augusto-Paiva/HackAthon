"""A documentação gerada deve representar o contrato e acompanhar a base."""
from contextlib import redirect_stderr, redirect_stdout
from importlib import import_module
from io import StringIO
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from tests.engine.apoio import base, condicao, doenca, regra, simbolo

PROJETO = Path(__file__).resolve().parents[2]
BASE = PROJETO / 'base/desenvolvimento/anamnese-bovinos-v3.1.0-revisao1.json'
CASOS = PROJETO / 'base/desenvolvimento/casos'


class GeracaoDaDocumentacao(unittest.TestCase):
    def setUp(self):
        try:
            self.gerador = import_module('scripts.gerar_doc_regras')
        except ImportError:
            self.fail('O gerador de documentação ainda não foi implementado.')

    def executar(self, argumentos):
        with redirect_stdout(StringIO()), redirect_stderr(StringIO()):
            return self.gerador.main(argumentos)

    def test_condicao_distingue_valor_booleano_e_limiar_de_cf(self):
        self.assertEqual(
            self.gerador.formatar_condicao(condicao('mastite', cf_minimo=0.5)),
            'mastite = sim [CF ≥ 0,5]',
        )

    def test_condicao_preserva_negacao_e_limite_superior(self):
        self.assertEqual(
            self.gerador.formatar_condicao(condicao('febre', negado=True)),
            'NÃO (febre = sim)',
        )
        self.assertEqual(
            self.gerador.formatar_condicao(condicao('mastite', cf_maximo=0.4)),
            'mastite = sim [CF ≤ 0,4]',
        )

    def test_texto_de_tabela_preserva_conteudo_sem_quebrar_colunas(self):
        dados = base([simbolo('x'), doenca()], [regra('r1', 'd', 0.7, condicao('x'))])
        dados['regras'][0]['nota'] = 'Relato | exame\nsegunda linha'
        texto = self.gerador.gerar_regras(dados, caminho_base='exemplo.json', sha256='abc')
        self.assertIn('Relato \\| exame<br>segunda linha', texto)
        self.assertIn('r1', texto)
        self.assertIn('0,7', texto)

    def test_base_de_desenvolvimento_nao_e_descrita_como_ativa(self):
        dados = json.loads(BASE.read_text(encoding='utf-8'))
        texto = self.gerador.gerar_regras(dados, caminho_base=BASE.name, sha256='abc')
        self.assertIn('Base de desenvolvimento; não é uma base ativa aprovada.', texto)
        self.assertIn('CF ≥ 0,5', texto)
        self.assertIn('evidencia_alteracao_leite', texto)

    def test_base_sem_agrupamento_nao_ganha_descricao_que_nao_possui(self):
        dados = base([simbolo('x'), doenca()], [regra('r1', 'd', 0.7, condicao('x'))])
        texto = self.gerador.gerar_regras(dados, caminho_base='exemplo.json', sha256='abc')
        self.assertNotIn('evidencia_alteracao_leite', texto)

    def test_ausencia_de_base_ativa_exige_indicacao_explicita(self):
        with TemporaryDirectory() as temporario:
            saida = StringIO()
            with patch.object(self.gerador, 'PROJETO', Path(temporario)), redirect_stderr(saida):
                self.assertEqual(self.gerador.main([]), 2)
            self.assertIn('Base ativa ausente; use --base', saida.getvalue())

    def test_verificacao_detecta_edicao_manual_sem_sobrescrever(self):
        with TemporaryDirectory() as temporario:
            argumentos = ['--base', str(BASE), '--casos', str(CASOS), '--saida', temporario]
            self.assertEqual(self.executar(argumentos), 0)
            caminho = Path(temporario) / '03-regras-de-producao.md'
            alterado = caminho.read_text(encoding='utf-8') + '\nEdição manual.\n'
            caminho.write_text(alterado, encoding='utf-8')
            self.assertEqual(self.executar(argumentos + ['--verificar']), 1)
            self.assertEqual(caminho.read_text(encoding='utf-8'), alterado)

    def test_caso_que_falha_nao_pode_ser_reportado_como_aprovado(self):
        caso = json.loads((CASOS / 'alerta-decubito.json').read_text(encoding='utf-8'))
        caso['esperado']['urgencia'] = 'sem_problema'
        with TemporaryDirectory() as temporario:
            caminho = Path(temporario) / 'caso.json'
            caminho.write_text(json.dumps(caso), encoding='utf-8')
            self.assertEqual(self.executar(['--base', str(BASE), '--casos', str(caminho),
                                          '--saida', str(Path(temporario) / 'saida')]), 1)

    def test_entrada_invalida_retorna_erro_claro(self):
        with TemporaryDirectory() as temporario:
            caminho = Path(temporario) / 'invalida.json'
            caminho.write_text('{}', encoding='utf-8')
            self.assertEqual(self.executar(['--base', str(caminho), '--saida', temporario]), 2)

    def test_documentos_commitados_estao_sincronizados_com_base_e_casos(self):
        self.assertEqual(self.executar(['--base', str(BASE), '--casos', str(CASOS),
                                       '--saida', str(PROJETO / 'docs/entrega'), '--verificar']), 0)


if __name__ == '__main__':
    unittest.main()
