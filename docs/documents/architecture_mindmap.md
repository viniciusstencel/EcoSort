```mermaid
mindmap
  root((♻️ Projeto EcoSort: Lixeira Inteligente))

  (🎯 Objetivo Central: Automação da Separação de Resíduos com Arquitetura de Microsserviços Assíncrona)

  subgraph 📷 Fonte de Vídeo (Câmera IP)
    direction LR
    Stream de Vídeo Contínuo (ex: http://191.168.0.1/stream)
    --Consumido 24/7 por--> 🧠 Servidor IA
  end

  subgraph ⚙️ Módulo IoT/Hardware (Arduino/ESP32)
    direction TB
    Atuadores (Servo Inferior & Servo Superior)
    --Aguardando Comandos em--> MQTT (Tópico: 'ecosort/commands')
  end

  subgraph 🧠 Servidor IA (services/ai-python)
    direction TD
    Entrada: Consome o Stream de Vídeo (via OpenCV)
    Processamento: Classifica o resíduo (via TensorFlow/Keras)
    Saída 1 (Ação Imediata - Baixa Latência)
    --Publica Comando (String) ex: "plastic"--> Broker MQTT (Tópico: 'ecosort/commands')
    Saída 2 (Persistência - Resiliência)
    --Publica Evento (JSON) ex: {"class_name": "plastic", ...}--> Broker Kafka (Tópico: 'ecosort-persistence-events')
  end

  subgraph ☕ Serviço de Persistência (services/persistence-java)
    direction TD
    Entrada: Ouve a fila de eventos
    --Consome Eventos (JSON) de--> Broker Kafka (Tópico: 'ecosort-persistence-events')
    Processamento 1: Persistência
    --Salva Evento no--> Banco de Dados (PostgreSQL)
    Processamento 2: Notificação em Tempo Real
    --Envia Evento (JSON) para--> WebSocket (Tópico: '/topic/detections')
    Processamento 3: Consulta de Histórico
    --Expõe API REST para--> 🖥️ Frontend Web (ex: GET /api/v1/history)
  end

  subgraph 🖥️ Frontend Web (services/frontend-web)
    direction TD
    Dashboard (Tempo Real)
    --Ouve Eventos Ao Vivo de--> WebSocket (Tópico: '/topic/detections')
    Dashboard (Histórico)
    --Busca Dados Passados da--> API REST Java (GET /api/v1/history)
    UI/UX
    --> Exibe Gráficos, Estatísticas, Gamificação
  end

  subgraph 🐳 Orquestração & Infra (infrastructure/docker-config)
    direction TB
    docker-compose.yml
    --Orquestra 7 Serviços--> (Java, Python, React, DB, MQTT, Kafka, Zookeeper)
    Canal de Comando (Baixa Latência)
    --> Broker MQTT (Mosquitto)
    Canal de Dados (Resiliente, "Data Bus")
    --> Broker Apache Kafka & Zookeeper
    Armazenamento de Dados
    --> Banco de Dados (PostgreSQL)
  end
