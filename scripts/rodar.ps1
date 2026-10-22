<#
.SYNOPSIS
    Sobe a API de anamnese de bovinos em localhost (http://localhost:8000).

.DESCRIPTION
    1. Confere o Python do .venv (aborta em português se faltar).
    2. Cria o banco SQLite e semeia animais fictícios se o arquivo não existir (-Reset apaga e recria).
    3. Instala e compila web/ quando o projeto existe e web\dist está ausente.
    4. Confere que a porta 8000 está livre (aborta em português se não estiver).
    5. Sobe o uvicorn em 127.0.0.1:8000, espera GET /api/saude responder (até 30 s) e abre o navegador padrão
       (-SemNavegador desliga).
    Ctrl+C encerra o servidor.

    Variáveis opcionais: ANAMNESE_BASE_DIR (pasta da base; padrão "base") e ANAMNESE_DB (arquivo do banco;
    padrão "dados\anamnese.db"). A instalação inicial usa internet; a execução é local.

.PARAMETER SoPreparar
    Executa os passos 1 a 3 e termina, sem subir o servidor.

.PARAMETER Reset
    Apaga o banco e o recria (com os animais fictícios) antes de subir. Só apaga arquivo SQLite (ou vazio): um
    ANAMNESE_DB apontado para outro tipo de arquivo ou para uma pasta é recusado.

.PARAMETER SemNavegador
    Não abre o navegador padrão depois de "Pronto" (use em testes e em máquinas sem interface).

.EXAMPLE
    powershell -ExecutionPolicy Bypass -File scripts\rodar.ps1
    powershell -ExecutionPolicy Bypass -File scripts\rodar.ps1 -SoPreparar
    powershell -ExecutionPolicy Bypass -File scripts\rodar.ps1 -Reset
    powershell -ExecutionPolicy Bypass -File scripts\rodar.ps1 -SemNavegador
#>
param(
    [switch]$SoPreparar,
    [switch]$Reset,
    [switch]$SemNavegador
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

function PortaLivre([int]$porta) {
    $ouvinte = [System.Net.Sockets.TcpListener]::new([System.Net.IPAddress]::Parse($Endereco), $porta)
    try { $ouvinte.Start(); return $true }
    catch { return $false }
    finally { $ouvinte.Stop() }
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
if ([System.IO.Path]::GetFullPath($banco) -match 'OneDrive') {
    Write-Host ('Aviso: o banco fica numa pasta do OneDrive; a sincronização pode travar ou corromper o SQLite. ' +
                'Prefira um caminho fora dela em ANAMNESE_DB, por exemplo: ' +
                '$env:ANAMNESE_DB = "$env:LOCALAPPDATA\anamnese\anamnese.db"') -ForegroundColor Yellow
}
if ($Reset -or -not (Test-Path $banco)) {
    if ($Reset) { Write-Host "Recriando o banco $banco e semeando animais fictícios..." }
    else { Write-Host "Criando o banco $banco e semeando animais fictícios..." }
    & $python scripts\resetar_db.py --semear
    if ($LASTEXITCODE -ne 0) { Falhar 'não consegui preparar o banco (veja a mensagem acima).' }
} else {
    Write-Host "Banco existente mantido: $banco (use -Reset para recriar)."
}

# 3. Prepara o frontend apenas quando o build está ausente.
if (-not (Test-Path (Join-Path $raiz 'web\dist\index.html'))) {
    if (Test-Path (Join-Path $raiz 'web\package.json')) {
        if (-not (Get-Command npm.cmd -ErrorAction SilentlyContinue)) { Falhar 'instale Node.js 24 (com npm) para preparar a interface.' }
        Push-Location (Join-Path $raiz 'web')
        try {
            & npm.cmd ci
            if ($LASTEXITCODE -ne 0) { Falhar 'não consegui instalar as dependências da interface.' }
            & npm.cmd run build
            if ($LASTEXITCODE -ne 0) { Falhar 'não consegui compilar a interface.' }
        } finally { Pop-Location }
    } else {
        Write-Host 'Aviso: web\dist não existe; só a API estará no ar (documentação em /api/docs).' -ForegroundColor Yellow
    }
}

if ($SoPreparar) {
    Write-Host 'Preparo concluído. Para subir o servidor, rode o script sem -SoPreparar.' -ForegroundColor Green
    exit 0
}

# 4. Porta livre (senão o /api/saude abaixo responderia por outro processo)
if (-not (PortaLivre $Porta)) {
    Falhar "a porta $Porta já está em uso (talvez outra instância do servidor). Encerre quem a usa e tente de novo."
}

# 5. Servidor
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
    if (-not $SemNavegador) {
        try { Start-Process "http://localhost:${Porta}" }
        catch { Write-Host 'Não consegui abrir o navegador; abra o endereço acima.' -ForegroundColor Yellow }
    }
    $servidor.WaitForExit()
} finally {
    if ($servidor -and -not $servidor.HasExited) {
        Stop-Process -Id $servidor.Id -Force -ErrorAction SilentlyContinue
        Write-Host 'Servidor encerrado.'
    }
}
