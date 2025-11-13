#!/bin/bash

VENV_ACTIVATION="venv/bin/activate"

# ---
# 1. VERIFICA E ATIVA O VENV
# ---
echo "Procurando ambiente virtual..."
if [ ! -f "$VENV_ACTIVATION" ]; then
    echo "Erro: Ambiente virtual não encontrado em '$VENV_ACTIVATION'."
    echo "Por favor, crie-o primeiro com: python3 -m venv venv"
    exit 1
fi

echo "Ativando ambiente virtual..."
source $VENV_ACTIVATION
if [ $? -ne 0 ]; then
    echo "Erro fatal ao ativar o ambiente virtual."
    exit 1
fi

# ---
# 2. FUNÇÃO DE LIMPEZA (PARA DESATIVAR O VENV)
# ---
# Isso será chamado quando o script sair (ex: com CTRL+C)
cleanup() {
    echo -e "\nDesativando ambiente virtual..."
    deactivate
    echo "Script encerrado."
    exit 0
}

# 'trap' captura o sinal de interrupção (CTRL+C) e chama a função 'cleanup'
trap cleanup SIGINT

# ---
# 3. INSTALA DEPENDÊNCIAS
# ---
echo "Verificando/Instalando dependências (dentro do venv)..."
pip install -r requirements.txt

# Verifica se a instalação foi bem-sucedida
if [ $? -ne 0 ]; then
    echo "Erro ao instalar dependências. Verifique o venv e o requirements.txt."
    cleanup # Chama a limpeza para desativar o venv antes de sair
    exit 1
fi

# ---
# 4. LOOP PRINCIPAL
# ---
echo "Pressione [CTRL+C] para parar o script de reinício."
while true; do
    echo "Iniciando o serviço principal (main_service.py)..."
    
    # É mais idiomático usar 'python' quando o venv está ativo
    python -m src.main_service
    
    echo "Serviço parado. Reiniciando em 5 segundos..."
    sleep 5
done