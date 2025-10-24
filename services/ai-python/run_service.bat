@echo off
REM ====================================================================
REM  Script para executar e monitorar o servico de IA em Python
REM  Descricao: Este script inicia o 'main_service.py' como um modulo.
REM             Se o servico parar ou falhar, ele sera reiniciado
REM             automaticamente apos 5 segundos.
REM
REM  Para parar: Pressione CTRL+C na janela do console e confirme (S/N).
REM ====================================================================

REM Define o titulo da janela do console para ser facil de achar
title Servico de Deteccao de IA

echo Script de monitoramento iniciado.
echo Pressione [CTRL+C] a qualquer momento para parar o servico.
echo.

REM :loop e uma 'label', um marcador para onde o 'goto' vai pular
:loop
echo [%TIME%] Iniciando o servico de processamento (main_service.py)...
echo.

REM Executa o Python como um modulo a partir da raiz do projeto.
REM Isso e essencial para que os imports (ex: .classification_model)
REM e os caminhos (ex: 'models/keras_model.h5') funcionem.
python -m src.main_service

echo.
echo [%TIME%] ATENCAO: O servico parou (pode ser um erro ou parada manual).
echo Reiniciando em 5 segundos...

REM Espera 5 segundos antes de reiniciar
timeout /t 5

REM Limpa a tela (opcional, mas mantem o log limpo)
cls

REM Volta para o marcador :loop
goto loop