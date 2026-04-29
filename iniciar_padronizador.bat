@echo off
cd /d "%~dp0"
chcp 65001 > nul
title Padronizador de Variaveis - Iniciar
color 0A

echo ============================================================
echo  PADRONIZADOR DE VARIAVEIS
echo  Inicializacao local em modo plug-and-play
echo ============================================================
echo.
echo Este modo foi pensado para usuario final.
echo Ele NAO usa Node, npm, Vite ou node_modules.
echo Ele usa apenas Python + frontend ja compilado em frontend\dist.
echo.

if not exist frontend\dist\index.html (
    color 0C
    echo [ERRO] Interface compilada nao encontrada.
    echo.
    echo Este aplicativo precisa da pasta:
    echo frontend\dist\index.html
    echo.
    echo Como resolver:
    echo 1. Fale com responsavel pelo projeto.
    echo 2. Baixe o projeto novamente com essa pasta
    echo.
    pause
    exit /b 1
)

where python >nul 2>nul
if %errorlevel% neq 0 (
    color 0C
    echo [ERRO] Python nao encontrado nesta maquina.
    echo.
    echo Para usar esta versao local, e necessario ter Python instalado.
    echo Recomendado: Python 3.10 ou superior.
    echo.
    pause
    exit /b 1
)

echo [OK] Python encontrado.
python --version
echo.

cd backend

if not exist .venv (
    echo [1/4] Criando ambiente virtual Python local...
    python -m venv .venv

    if %errorlevel% neq 0 (
        color 0C
        echo [ERRO] Nao foi possivel criar o ambiente virtual .venv.
        pause
        exit /b 1
    )
) else (
    echo [1/4] Ambiente virtual .venv ja existe.
)

echo [2/4] Ativando ambiente virtual...
call .venv\Scripts\activate

if %errorlevel% neq 0 (
    color 0C
    echo [ERRO] Nao foi possivel ativar o .venv.
    pause
    exit /b 1
)

echo [3/4] Validando dependencias Python...
python -m pip install --upgrade pip
pip install -r requirements.txt

if %errorlevel% neq 0 (
    color 0C
    echo.
    echo [ERRO] Falha ao instalar dependencias Python.
    echo.
    echo Possiveis causas:
    echo - Sem acesso a internet
    echo - Proxy corporativo bloqueando pip
    echo - Repositorio de pacotes bloqueado
    echo.
    echo Proximo nivel:
    echo - Entregar pacote com .venv ja preparado
    echo - Ou gerar um .exe com PyInstaller em maquina Windows
    echo.
    pause
    exit /b 1
)

echo [4/4] Iniciando aplicacao...

set PORT=8000

:CHECK_PORT
set MAX_PORT=9000
if %PORT% GTR %MAX_PORT% (
    color 0C
    echo [ERRO] Nao foi possivel encontrar uma porta livre entre 8000 e 9000.
    echo Feche as aplicacoes que estao usando essas portas e tente novamente.
    pause
    exit /b 1
)

netstat -ano | findstr ":%PORT% " >nul
if %errorlevel% ==0 (
    echo [AVISO] Porta %PORT% ja esta em uso. Tentando a proxima porta...
    set /a PORT+=1
    goto CHECK_PORT
)

echo.
echo ============================================================
echo Aplicacao iniciando.....
echo Aguarde alguns segundos......
echo ============================================================
echo.
echo Porta Escolhida: %PORT%
echo Abrindo em http://localhost:%PORT%

echo.
echo Para encerrar a aplicacao.
echo - Feche esta janela ou precione CTRL + C.
echo.

start http://localhost:%PORT%

uvicorn app.main:app --host 127.0.0.1 --port %PORT%

color 0C
echo.
echo ============================================================
echo [OK] Aplicacao encerrada com sucesso.
echo Pressione qualquer tecla para sair......
echo ============================================================
pause


