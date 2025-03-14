@echo off
echo =============================================
echo      DEMO DevOps - Aplicação IMC (Docker)
echo =============================================

REM Verifica se o Docker está em execução
echo Verificando status do Docker...
docker info >nul 2>&1
IF ERRORLEVEL 1 (
    echo [ERRO] O Docker nao esta em execucao.
    echo Por favor, inicie o Docker Desktop antes de continuar.
    pause
    exit /b
)

REM Baixa a imagem mais recente do Docker Hub
echo ---------------------------------------------
echo Baixando a imagem mais recente: maxchaves/imc-app:latest
docker pull maxchaves/imc-app:latest

REM Executa o container da aplicação IMC
echo ---------------------------------------------
echo Iniciando a aplicacao IMC em http://localhost:5000
docker run -d -p 5000:5000 --name imc-app-demo maxchaves/imc-app:latest

REM Mostra o status do container
echo ---------------------------------------------
echo Verificando se o container esta rodando...
docker ps

echo ---------------------------------------------
echo Aplicacao em execucao! Acesse via navegador:
echo → http://localhost:5000
echo ---------------------------------------------

pause
