#!/bin/bash
echo "Pressione [CTRL+C] para parar o script de reinício."
while true; do
    echo "Iniciando o serviço principal (main_service.py)..."
    
    # -m src.main_service: "Execute o módulo 'main_service' que está dentro do pacote 'src'"
    python -m src.main_service
    
    echo "Serviço parado. Reiniciando em 5 segundos..."
    sleep 5
done