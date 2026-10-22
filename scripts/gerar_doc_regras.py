"""Gera a documentação de regras e casos, ou confere sua sincronização."""
import argparse
from collections import Counter
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import re
import sys

PROJETO = Path(__file__).resolve().parents[1]
if __package__ in (None, ''):
    sys.path.insert(0, str(PROJETO))

from engine.casos import executar_caso
from engine.modelos import Base


def _valor(valor):
    if valor is True:
        return 'sim'
    if valor is False:
        return 'não'
    if valor is None:
        return 'desconhecido'
    if isinstance(valor, (int, float, Fraction)):
        return format(float(valor), '.15g').replace('.', ',')
    if isinstance(valor, list):
        return '{' + ', '.join(_valor(item) for item in valor) + '}'
    return str(valor)


def formatar_condicao(condicao):
    """Mantém distintos valor, operador, negação e limites de certeza."""
    texto = f"{condicao['simbolo']} {condicao.get('op', '=')} {_valor(condicao.get('valor', True))}"
    for campo, operador in (('cf_minimo', '≥'), ('cf_maximo', '≤')):
        if campo in condicao:
            texto += f' [CF {operador} {_valor(condicao[campo])}]'
    return f'NÃO ({texto})' if condicao.get('negado') else texto


def _celula(valor):
    return str(valor).replace('|', r'\|').replace('\r\n', '\n').replace('\n', '<br>')


def _tabela(cabecalho, linhas):
    partes = ['| ' + ' | '.join(cabecalho) + ' |', '| ' + ' | '.join('---' for _ in cabecalho) + ' |']
    partes.extend('| ' + ' | '.join(_celula(c) for c in linha) + ' |' for linha in linhas)
    return '\n'.join(partes)


def _fonte(texto):
    return re.sub(r'https?://[^\s;]+', lambda achado: f'[referência]({achado[0]})', texto)


def gerar_regras(dados, *, caminho_base, sha256, ativa=False):
    """Produz Markdown determinístico a partir da base validada pelo motor."""
    base = Base.de_dict(dados)
    meta = dados.get('meta', {})
    contagem = Counter(r.get('status', 'suposicao_a_validar') for r in base.regras)
    doencas = sorted((s for s in base.simbolos.values() if s['tipo'] == 'doenca'), key=lambda s: s['id'])
    partes = [
        '# Regras de produção — documentação gerada',
        '> GERADO por `scripts/gerar_doc_regras.py`. Edite a base e regenere este arquivo.',
        'Base indicada pelo ponteiro ativo; ativação operacional não é validação clínica.' if ativa else 'Base de desenvolvimento; não é uma base ativa aprovada.',
        f"Versão: `{meta.get('versao', 'não informada')}`. Pai declarado: `{meta.get('pai', 'não informado')}`. "
        f"Data declarada na base: `{meta.get('data', 'não informada')}`.",
        f'Arquivo: `{caminho_base}`. SHA-256 do JSON canônico: `{sha256}`. '
        'O hash usa UTF-8, chaves ordenadas e ausência de espaços, independente das quebras de linha do checkout.',
        f'Regras: **{len(base.regras)}**. Símbolos: **{len(base.simbolos)}**. Doenças: **{len(doencas)}**.',
        _tabela(['Estado', 'Quantidade'], sorted(contagem.items())),
        'As fontes descrevem o contexto clínico. Os números de CF são escolhas de modelagem do projeto; '
        'não são probabilidades nem valores publicados nessas referências.',
        '## Limiares e limites',
        _tabela(['Critério', 'Valor'], [(k, _valor(v)) for k, v in base.meta['limiares'].items()]),
        _tabela(['Modo', 'Limite de perguntas dinâmicas'], sorted(base.meta['limite_dinamico'].items())),
        'A triagem não consome o limite dinâmico. Premissa exige CF estritamente maior que 0,20. '
        '`sem_problema` é um resultado calculado pelo motor, sem regra de produção própria.',
    ]

    def grupo(titulo, regras):
        partes.append('## ' + titulo)
        linhas = [[f"`{r['id']}`", ' E '.join(formatar_condicao(c) for c in r['se']),
                   r['entao']['simbolo'], _valor(r['entao']['cf']), r.get('prioridade', ''),
                   _fonte(r['fonte']), r.get('status', 'suposicao_a_validar'), r.get('nota', '')]
                  for r in sorted(regras, key=lambda r: r['id'])]
        partes.append(_tabela(['ID', 'Condições', 'Conclusão', 'CF', 'Prioridade', 'Fonte', 'Estado', 'Nota'], linhas))

    grupo('Derivados — camada 1', [r for r in base.regras if base.simbolos[r['entao']['simbolo']]['tipo'] == 'derivado'])
    for doenca in doencas:
        grupo(f"{doenca['nome']} — {doenca['id']} (gravidade {doenca['gravidade']})",
              base.regras_para(doenca['id']))
    grupo('Bandeiras vermelhas — camada 3', [r for r in base.regras if r.get('classe') == 'bandeira_vermelha'])
    grupo('Urgências — camada 3', [r for r in base.regras if r.get('classe') == 'urgencia'])
    partes.extend([
        '## Símbolos',
        _tabela(['ID', 'Nome', 'Tipo', 'Domínio', 'Pergunta: produtor', 'Pergunta: veterinário', 'Gravidade', 'Combinação'],
                 [[s['id'], s.get('nome', ''), s['tipo'],
                   ', '.join(f'{k}: {_valor(v)}' for k, v in sorted(s['dominio'].items())),
                   s.get('pergunta', {}).get('produtor', '—'), s.get('pergunta', {}).get('veterinario', '—'),
                   s.get('gravidade', '—'), s.get('combinacao', 'mycin')]
                  for s in sorted(base.simbolos.values(), key=lambda s: s['id'])]),
        '## Telas de triagem',
        _tabela(['Ordem', 'ID', 'Seleção', 'Símbolos', 'Texto: produtor', 'Texto: veterinário', 'Alternativas por modo'],
                 [[n, t['id'], t['selecao'], ', '.join(t['simbolos']),
                   t.get('texto', t.get('textos', {})).get('produtor', ''),
                   t.get('texto', t.get('textos', {})).get('veterinario', ''),
                   '; '.join(f'{modo}: {", ".join(ids)}' for modo, ids in sorted(t.get('simbolos_por_modo', {}).items()))]
                  for n, t in enumerate(base.meta['triagem'], 1)]),
        '## Leitura e limites',
        ('O derivado `evidencia_alteracao_leite` usa `max`: inspeção do leite e teste da caneca '
         'não são somados como achados independentes. As regras R-MAS-01 e R-MAS-03 estão na camada 1; '
         'R-MAS-05 propaga o grupo para a doença. ' if 'evidencia_alteracao_leite' in base.simbolos else '')
        + 'A ordem das tabelas é editorial; a agenda é calculada pelo motor.',
        'Este documento descreve a base de desenvolvimento disponibilizada. Não demonstra equivalência integral '
        'com a Seção 3 da especificação nem aprovação para uso clínico.',
        'Todo o conhecimento veterinário é suposição a validar; extraído de fontes públicas por IA, sem especialista.',
    ])
    return '\n\n'.join(partes) + '\n'


def _ler_casos(caminho):
    arquivos = sorted(caminho.glob('*.json')) if caminho.is_dir() else [caminho]
    casos = []
    for arquivo in arquivos:
        dados = json.loads(arquivo.read_text(encoding='utf-8-sig'))
        casos.extend(dados if isinstance(dados, list) else [dados])
    if not casos:
        raise ValueError('Nenhum caso encontrado para documentar')
    return casos


def gerar_casos(dados, casos):
    """Executa os casos reais e documenta entradas, critérios e resultados."""
    resultados = [(caso, executar_caso(dados, caso)) for caso in casos]
    passou = all(r['status'] == 'passou' for _, r in resultados)
    partes = ['# Casos de teste — documentação gerada',
              '> GERADO por `scripts/gerar_doc_regras.py`; resultados obtidos com `engine.casos.executar_caso`.',
              f"Base `{dados['meta']['versao']}`. Casos sintéticos executados: **{len(resultados)}**. "
              f"Aprovados: **{sum(r['status'] == 'passou' for _, r in resultados)}**.",
              'Os casos demonstram integração e comportamento determinístico. Não medem acurácia, '
              'sensibilidade ou especificidade clínicas. Os testes unitários são contabilizados separadamente.',
              _tabela(['Caso', 'Resultado', 'Urgência', 'Primeira hipótese', 'Pausa ocorreu'],
                       [[c.get('id', 'sem ID'), r['status'], r.get('obtido', {}).get('urgencia', '—'),
                         r.get('obtido', {}).get('top1', '—'),
                         _valor(r.get('obtido', {}).get('alerta', {}).get('pausa'))] for c, r in resultados])]
    for caso, resultado in resultados:
        partes.extend([f"## {caso.get('id', 'Caso sem ID')}", caso.get('descricao', ''),
                       '### Entrada e resultado esperado',
                       '```json\n' + json.dumps(caso, ensure_ascii=False, indent=2) + '\n```',
                       '### Resultado observado',
                       '```json\n' + json.dumps(resultado, ensure_ascii=False, indent=2, allow_nan=False) + '\n```'])
    limites = dados.get('meta', {}).get('limite_dinamico', {})
    partes.append(f'Este documento executa {len(resultados)} cenário(s) sintético(s); não substitui validação especializada. '
                  'Os desvios em relação à especificação e os limites da coleta estão no registro de riscos. '
                  '`limite_dinamico: 0`, quando presente no caso, encerra após a triagem; '
                  f"os limites normais da base são {limites.get('produtor', 12)}/{limites.get('veterinario', 25)}.")
    return '\n\n'.join(partes) + '\n', passou


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base', type=Path, help='JSON explícito; sem ele, lê base/ativa.json')
    parser.add_argument('--casos', type=Path, help='Arquivo de caso, lista de casos ou pasta de JSONs')
    parser.add_argument('--saida', type=Path, default=PROJETO / 'docs/entrega')
    parser.add_argument('--verificar', action='store_true', help='Compara sem sobrescrever')
    args = parser.parse_args(argv)
    try:
        ativa = args.base is None
        if ativa:
            ponteiro = PROJETO / 'base/ativa.json'
            if not ponteiro.is_file():
                raise ValueError('Base ativa ausente; use --base para indicar a base de desenvolvimento')
            versao = json.loads(ponteiro.read_text(encoding='utf-8-sig'))['versao']
            if not isinstance(versao, str) or not re.fullmatch(r'v[0-9]+', versao):
                raise ValueError('Identificador de versão ativa inválido')
            caminho = PROJETO / 'base/versoes' / f'{versao}.json'
        else:
            caminho = args.base.resolve()
        dados = json.loads(caminho.read_text(encoding='utf-8-sig'))
        canonico = json.dumps(dados, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False)
        digest = hashlib.sha256(canonico.encode('utf-8')).hexdigest()
        try:
            nome = caminho.relative_to(PROJETO).as_posix()
        except ValueError:
            nome = caminho.name
        documentos = {'03-regras-de-producao.md': gerar_regras(dados, caminho_base=nome, sha256=digest, ativa=ativa)}
        sucesso = True
        if args.casos:
            documentos['04-casos-de-teste.md'], sucesso = gerar_casos(dados, _ler_casos(args.casos))
        for nome, texto in documentos.items():
            destino = args.saida / nome
            if args.verificar:
                if not destino.is_file() or destino.read_text(encoding='utf-8') != texto:
                    print(f'Documentação desatualizada: {destino}', file=sys.stderr)
                    sucesso = False
            else:
                args.saida.mkdir(parents=True, exist_ok=True)
                destino.write_text(texto, encoding='utf-8')
                print(f'Gerado: {destino}')
        if args.verificar and sucesso:
            print('Documentação sincronizada com a base e os casos.')
        return 0 if sucesso else 1
    except (OSError, KeyError, ValueError, TypeError) as erro:
        print(f'Erro ao gerar documentação: {erro}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
