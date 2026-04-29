@echo off
title Data Naming AI - Start
color 0A

echo ============================================================
echo  Iniciando Data Naming AI
echo ============================================================
echo.

where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERRO] Python nao encontrado. Rode setup.bat apos instalar Python.
    pause
    exit /b 1
)

where node >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERRO] Node.js nao encontrado. Rode setup.bat apos instalar Node.js.
    pause
    exit /b 1
)

if not exist backend\.venv (
    echo [AVISO] Ambiente Python nao encontrado.
    echo Rode setup.bat antes de iniciar.
    pause
    exit /b 1
)

if not exist frontend\node_modules (
    echo [AVISO] Dependencias do frontend nao encontradas.
    echo Rode setup.bat antes de iniciar.
    pause
    exit /b 1
)

echo [1/3] Subindo backend em http://localhost:8000
start "Data Naming AI - Backend" cmd /k "cd backend && call .venv\Scripts\activate && uvicorn app.main:app --host 127.0.0.1 --port 8000"

echo [2/3] Subindo frontend em http://localhost:5173
start "Data Naming AI - Frontend" cmd /k "cd frontend && npm run dev"

echo [3/3] Abrindo navegador...
timeout /t 6 /nobreak >nul
start http://localhost:5173

echo.
echo ============================================================
echo  Aplicacao iniciada.
echo  Para encerrar, feche as janelas Backend e Frontend.
echo ============================================================
pause
