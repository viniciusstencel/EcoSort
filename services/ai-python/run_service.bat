@echo off
REM ====================================================================
REM  Script para executar e monitorar o servico de IA em Python (Windows)
REM  Equivalente ao run_service.sh
REM ====================================================================

title Servico de Deteccao de IA

REM Definindo caminho para ativacao no Windows (pasta Scripts, nao bin)
set "VENV_ACTIVATION=venv\Scripts\activate.bat"

REM ---
REM 1. VERIFICA E ATIVA O VENV
REM ---
echo Procurando ambiente virtual...
if not exist "%VENV_ACTIVATION%" (
    echo [ERRO] Ambiente virtual nao encontrado em '%VENV_ACTIVATION%'.
    echo Por favor, crie-o primeiro com: python -m venv venv
    pause
    exit /b 1
)

echo Ativando ambiente virtual...
call "%VENV_ACTIVATION%"
if %errorlevel% neq 0 (
    echo [ERRO FATAL] Nao foi possivel ativar o ambiente virtual.
    pause
    exit /b 1
)

REM ---
REM 2. INSTALA DEPENDENCIAS
REM ---
echo Verificando/Instalando dependencias (dentro do venv)...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo [ERRO] Falha ao instalar dependencias. Verifique o requirements.txt.
    echo Desativando venv e saindo...
    call deactivate
    pause
    exit /b 1
)

REM ---
REM 3. LOOP PRINCIPAL
REM ---
echo.
echo Dependencias ok. Pressione [CTRL+C] para parar o script de reinicio.
echo.

:loop
    echo [%TIME%] Iniciando o servico principal (main_service.py)...
    
    REM Executa o Python como um modulo a partir da raiz
    python -m src.main_service
    
    echo.
    echo [%TIME%] ATENCAO: O servico parou. Reiniciando em 5 segundos...
    
    REM Espera 5 segundos (pode ser cancelado com CTRL+C)
    timeout /t 5
    
    REM Limpa a tela para manter o log organizado (opcional)
    cls
    
goto loop