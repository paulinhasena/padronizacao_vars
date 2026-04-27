@echo off
title Data Naming AI - Setup
color 0B

echo ============================================================
echo  Data Naming AI - Setup local
echo ============================================================
echo.
echo Este script instala as dependencias do backend e frontend.
echo Rode apenas na primeira vez ou quando atualizar o projeto.
echo.

where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERRO] Python nao encontrado.
    echo Instale Python 3.11+ e marque a opcao "Add Python to PATH".
    pause
    exit /b 1
)

where node >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERRO] Node.js nao encontrado.
    echo Instale Node.js LTS.
    pause
    exit /b 1
)

echo [1/4] Criando ambiente virtual Python...
cd backend
if not exist .venv (
    python -m venv .venv
)

echo [2/4] Instalando dependencias Python...
call .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt

echo [3/4] Instalando dependencias do frontend...
cd ..\frontend
call npm install

echo [4/4] Setup concluido.
cd ..

echo.
echo ============================================================
echo  Pronto. Agora execute start.bat
echo ============================================================
pause
