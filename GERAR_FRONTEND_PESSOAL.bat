@echo off
title Padronizador - Gerar Frontend
color 0B

echo ============================================================
echo  GERAR FRONTEND PRONTO PARA AMBIENTE CORPORATIVO
echo ============================================================
echo.
echo Execute este arquivo na maquina pessoal, onde npm funciona.
echo Ele cria a pasta frontend\dist.
echo.

where node >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERRO] Node.js nao encontrado.
    echo Instale Node.js LTS na maquina pessoal.
    pause
    exit /b 1
)

cd frontend

echo [1/2] Instalando dependencias do frontend...
call npm install

echo [2/2] Gerando build de producao...
call npm run build

cd ..

echo.
echo ============================================================
echo  Build concluido.
echo  Agora suba a pasta frontend\dist para o GitHub.
echo  No corporativo, rode INICIAR_PADRONIZADOR.bat
echo ============================================================
pause
