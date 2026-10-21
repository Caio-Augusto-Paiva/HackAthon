<#
.SYNOPSIS
    Sobe a API de anamnese de bovinos em localhost (http://localhost:8000).

.DESCRIPTION
    1. Confere o Python do .venv (aborta em português se faltar).
    2. Cria o banco SQLite e semeia animais fictícios se o arquivo não existir (-Reset apaga e recria).
    3. Avisa, sem abortar, se web\dist não existe (só a API fica no ar).
    4. Sobe o uvicorn em 127.0.0.1:8000 e espera GET /api/saude responder (até 30 s).
    Ctrl+C encerra o servidor.

    Variáveis opcionais: ANAMNESE_BASE_DIR (pasta da base; padrão "base") e ANAMNESE_DB (arquivo do banco;
    padrão "dados\anamnese.db"). Nenhuma chamada de rede: tudo roda em localhost.

.PARAMETER SoPreparar
    Executa os passos 1 a 3 e termina, sem subir o servidor.

.PARAMETER Reset
    Apaga o banco e o recria (com os animais fictícios) antes de subir.

.EXAMPLE
    powershell -ExecutionPolicy Bypass -File scripts\rodar.ps1
    powershell -ExecutionPolicy Bypass -File scripts\rodar.ps1 -SoPreparar
    powershell -ExecutionPolicy Bypass -File scripts\rodar.ps1 -Reset
#>
param(
    [switch]$SoPreparar,
    [switch]$Reset
)

$ErrorActionPreference = 'Stop'

$Porta = 8000
$Endereco = '127.0.0.1'
$LimiteEsperaSegundos = 30

$raiz = Split-Path -Parent $PSScriptRoot
Set-Location $raiz

function Falhar([string]$mensagem) {
    Write-Host "ERRO: $mensagem" -ForegroundColor Red
    exit 1
}

# 1. Python do .venv
$python = Join-Path $raiz '.venv\Scripts\python.exe'
if (-not (Test-Path $python)) {
    Falhar ("não encontrei $python. Crie o ambiente uma vez, com internet:`n" +
            "  python -m venv .venv`n" +
            "  .venv\Scripts\python -m pip install -e `".[dev]`"")
}

# 2. Banco: cria e semeia se não existir (ou se -Reset)
$banco = if ($env:ANAMNESE_DB) { $env:ANAMNESE_DB } else { 'dados\anamnese.db' }
if ($Reset -or -not (Test-Path $banco)) {
    if ($Reset) { Write-Host "Recriando o banco $banco e semeando animais fictícios..." }
    else { Write-Host "Criando o banco $banco e semeando animais fictícios..." }
    & $python scripts\resetar_db.py --semear
    if ($LASTEXITCODE -ne 0) { Falhar 'não consegui preparar o banco (veja a mensagem acima).' }
} else {
    Write-Host "Banco existente mantido: $banco (use -Reset para recriar)."
}

# 3. Frontend: opcional
if (-not (Test-Path (Join-Path $raiz 'web\dist\index.html'))) {
    Write-Host 'Aviso: web\dist não existe; só a API estará no ar (documentação em /api/docs).' -ForegroundColor Yellow
}

if ($SoPreparar) {
    Write-Host 'Preparo concluído. Para subir o servidor, rode o script sem -SoPreparar.' -ForegroundColor Green
    exit 0
}

# 4. Servidor
Write-Host "Subindo o servidor em http://${Endereco}:${Porta} ..."
$servidor = Start-Process -FilePath $python -NoNewWindow -PassThru -ArgumentList @(
    '-m', 'uvicorn', 'api.main:app', '--host', $Endereco, '--port', "$Porta"
)

try {
    $limite = (Get-Date).AddSeconds($LimiteEsperaSegundos)
    $pronto = $false
    while (-not $pronto -and -not $servidor.HasExited -and (Get-Date) -lt $limite) {
        try {
            $resposta = Invoke-WebRequest -Uri "http://${Endereco}:${Porta}/api/saude" -UseBasicParsing -TimeoutSec 2
            $pronto = ($resposta.StatusCode -eq 200)
        } catch {
            Start-Sleep -Milliseconds 300
        }
    }

    if (-not $pronto) {
        if ($servidor.HasExited) { Falhar "o servidor encerrou antes de ficar pronto (a porta $Porta está ocupada?)." }
        Falhar "o servidor não respondeu em /api/saude em $LimiteEsperaSegundos segundos."
    }

    Write-Host ''
    Write-Host "Pronto: http://localhost:${Porta}" -ForegroundColor Green
    Write-Host "Documentação da API: http://localhost:${Porta}/api/docs"
    Write-Host 'Ctrl+C encerra o servidor.'
    $servidor.WaitForExit()
} finally {
    if ($servidor -and -not $servidor.HasExited) {
        Stop-Process -Id $servidor.Id -Force -ErrorAction SilentlyContinue
        Write-Host 'Servidor encerrado.'
    }
}
