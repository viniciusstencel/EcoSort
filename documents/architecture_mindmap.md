```mermaid
mindmap
  root((Projeto EcoSort: Lixeira Inteligente))
    
    (🎯 Objetivo Central: Automação da Separação de Resíduos)
    
    subgraph 🤖 Módulo IoT/Hardware (iot-firmware/)
      Câmera (ESP32-CAM)
        --Captura Imagem--> Envio HTTP (para API Java)
      Atuação (Motores/Servos)
        --Recebe Comando Assíncrono--> MQTT Subscribe
    end
    
    subgraph ⚙️ API Central (backend-java/)
      Fluxo de Entrada
        --> Recebe Imagem (POST /depositar)
      Comunicação IA
        --> Proxy para Servidor Python
      Persistência
        --> Armazena Log de Coleta no PostgreSQL
      Mensageria (Saída)
        --Comando Atuação Leve--> MQTT Publish
        --Feedback em Tempo Real--> WebSocket (para React)
    end
    
    subgraph 🧠 Servidor IA (ia-python/)
      Modelo
        --> CNN (MobileNetV2, YOLO)
      Entrada
        --> Imagem Bruta (HTTP POST)
      Processamento
        --> Inferência / Classificação
      Saída
        --> Retorna JSON (class_id, confidence)
    end
    
    subgraph 🖥️ Frontend Web (frontend-react/)
      Experiência do Usuário
        --> Gamificação (Placar, Pontos)
      Feedback Ao Vivo
        --> WebSocket Listener (Efeitos Bacanas 🎉)
      Dashboard
        --> Relatórios Gráficos (Via API Java)
    end
    
    subgraph 🐳 Orquestração & Infra (docker-config/)
      Docker Compose
        --> Orquestra 5 Serviços (Java, Python, React, DB, MQTT)
      Banco de Dados
        --> PostgreSQL (Dados de Coleta)
      Comunicação Assíncrona
        --> MQTT Broker (Mosquitto)
      Rede
        --> Volumes Persistentes / Rede Interna
    end