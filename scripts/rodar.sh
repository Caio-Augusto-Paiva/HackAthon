#!/usr/bin/env bash
# Sobe a API de anamnese de bovinos em localhost (http://localhost:8000). Equivalente POSIX do rodar.ps1.
#
# Uso: scripts/rodar.sh [--so-preparar] [--reset]
#   --so-preparar  confere o ambiente, cria o banco e semeia; não sobe o servidor
#   --reset        apaga o banco e o recria (com os animais fictícios) antes de subir
#
# Variáveis opcionais: ANAMNESE_BASE_DIR (pasta da base; padrão "base") e ANAMNESE_DB (arquivo do banco; padrão
# "dados/anamnese.db"). Nenhuma chamada de rede. Ctrl+C encerra o servidor.
set -eu

PORTA=8000
ENDERECO=127.0.0.1
LIMITE_ESPERA_SEGUNDOS=30

SO_PREPARAR=0
RESET=0
for argumento in "$@"; do
    case "$argumento" in
        --so-preparar) SO_PREPARAR=1 ;;
        --reset) RESET=1 ;;
        -h|--help) sed -n '2,9p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
        *) echo "ERRO: opção desconhecida: $argumento (use --so-preparar, --reset ou --help)." >&2; exit 1 ;;
    esac
done

RAIZ="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$RAIZ"
export PYTHONIOENCODING=utf-8  # os avisos têm acento; o terminal (e o Git Bash do Windows) é UTF-8

# 1. Python do .venv (.venv/bin no Linux e no macOS; .venv/Scripts no Git Bash do Windows)
PYTHON=""
for candidato in "$RAIZ/.venv/bin/python" "$RAIZ/.venv/Scripts/python.exe" "$RAIZ/.venv/Scripts/python"; do
    if [ -x "$candidato" ]; then PYTHON="$candidato"; break; fi
done
if [ -z "$PYTHON" ]; then
    echo "ERRO: não encontrei o Python do .venv. Crie o ambiente uma vez, com internet:" >&2
    echo "  python3 -m venv .venv" >&2
    echo "  .venv/bin/python -m pip install -e \".[dev]\"" >&2
    exit 1
fi

# 2. Banco: cria e semeia se não existir (ou se --reset)
BANCO="${ANAMNESE_DB:-dados/anamnese.db}"
case "$BANCO" in /*|[A-Za-z]:*) CAMINHO_BANCO="$BANCO" ;; *) CAMINHO_BANCO="$RAIZ/$BANCO" ;; esac
case "$CAMINHO_BANCO" in
    *[Oo]ne[Dd]rive*)
        echo "Aviso: o banco fica numa pasta do OneDrive; a sincronização pode travar ou corromper o SQLite." \
             "Prefira um caminho fora dela em ANAMNESE_DB, por exemplo: export ANAMNESE_DB=\"\$HOME/anamnese/anamnese.db\"" ;;
esac
if [ "$RESET" -eq 1 ] || [ ! -e "$BANCO" ]; then
    if [ "$RESET" -eq 1 ]; then
        echo "Recriando o banco $BANCO e semeando animais fictícios..."
    else
        echo "Criando o banco $BANCO e semeando animais fictícios..."
    fi
    "$PYTHON" scripts/resetar_db.py --semear || { echo "ERRO: não consegui preparar o banco (veja a mensagem acima)." >&2; exit 1; }
else
    echo "Banco existente mantido: $BANCO (use --reset para recriar)."
fi

# 3. Frontend: opcional
if [ ! -f "$RAIZ/web/dist/index.html" ]; then
    echo "Aviso: web/dist não existe; só a API estará no ar (documentação em /api/docs)."
fi

if [ "$SO_PREPARAR" -eq 1 ]; then
    echo "Preparo concluído. Para subir o servidor, rode o script sem --so-preparar."
    exit 0
fi

# 4. Porta livre (senão o /api/saude abaixo responderia por outro processo)
if "$PYTHON" -c "import socket, sys; sys.exit(0 if socket.socket().connect_ex(('$ENDERECO', $PORTA)) == 0 else 1)"; then
    echo "ERRO: a porta $PORTA já está em uso (talvez outra instância do servidor). Encerre quem a usa e tente de novo." >&2
    exit 1
fi

# 5. Servidor
echo "Subindo o servidor em http://$ENDERECO:$PORTA ..."
"$PYTHON" -m uvicorn api.main:app --host "$ENDERECO" --port "$PORTA" &
SERVIDOR=$!
trap 'kill "$SERVIDOR" 2>/dev/null || true' EXIT
trap 'exit 130' INT TERM

responde() {
    # sem proxy: http_proxy/HTTP_PROXY do ambiente não valem para o localhost
    "$PYTHON" -c "import sys, urllib.request as u; o = u.build_opener(u.ProxyHandler({})); sys.exit(0 if o.open('http://$ENDERECO:$PORTA/api/saude', timeout=2).status == 200 else 1)" 2>/dev/null
}

PRONTO=0
FIM=$(( $(date +%s) + LIMITE_ESPERA_SEGUNDOS ))
while [ "$(date +%s)" -lt "$FIM" ]; do
    if ! kill -0 "$SERVIDOR" 2>/dev/null; then
        echo "ERRO: o servidor encerrou antes de ficar pronto (a porta $PORTA está ocupada?)." >&2
        exit 1
    fi
    if responde; then PRONTO=1; break; fi
    sleep 0.3
done
if [ "$PRONTO" -ne 1 ]; then
    echo "ERRO: o servidor não respondeu em /api/saude em $LIMITE_ESPERA_SEGUNDOS segundos." >&2
    exit 1
fi

echo
echo "Pronto: http://localhost:$PORTA"
echo "Documentação da API: http://localhost:$PORTA/api/docs"
echo "Ctrl+C encerra o servidor."
wait "$SERVIDOR"
