graph TD
    %% Define os Nós (Componentes) dentro de Subgrafos
    subgraph Cam [📷 Fonte de Vídeo (Câmera IP)]
        Video[Stream de Vídeo HTTP]
    end

    subgraph IA [🧠 Servidor IA (services/ai-python)]
        direction TB
        PyService(1. Consome Stream de Vídeo)
        PyModel(2. Classifica Resíduo)
        PyMQTT(3a. Publica Comando MQTT)
        PyKafka(3b. Publica Evento Kafka)
        
        PyService --> PyModel
        PyModel --> PyMQTT
        PyModel --> PyKafka
    end

    subgraph Hardware [⚙️ Módulo IoT (Arduino/ESP32)]
        direction TB
        MQTTSub(1. Ouve Tópico MQTT)
        Servos(2. Aciona Servos Inferior/Superior)
        MQTTSub --> Servos
    end

    subgraph Java [☕ Serviço de Persistência (services/persistence-java)]
        direction TB
        KafkaSub(1. Ouve Tópico Kafka)
        JavaDB(2. Salva no Banco de Dados)
        JavaWS(3. Transmite via WebSocket)
        JavaAPI(4. Expõe API REST de Histórico)
        
        KafkaSub --> JavaDB
        JavaDB --> JavaWS
    end

    subgraph Frontend [🖥️ Frontend Web (services/frontend-web)]
        direction TB
        WSSub(Ouve WebSocket - Tempo Real)
        APICall(Busca API REST - Histórico)
        Dashboard(Exibe Dashboard/Gráficos)
        
        WSSub --> Dashboard
        APICall --> Dashboard
    end

    subgraph Infra [🐳 Infraestrutura (docker-compose)]
        MQTT[Broker MQTT (Mosquitto)]
        Kafka[Broker Kafka (c/ ZK)]
        DB[Banco de Dados (PostgreSQL)]
    end

    %% == Conexões de Fluxo de Dados ==
    
    %% Fluxo de Vídeo
    Video -- "Consumido por" --> PyService
    
    %% Fluxo de Comando (Baixa Latência)
    PyMQTT -- "Comando (String 'plastic')" ---|BAIXA LATÊNCIA|---> MQTT
    MQTT -- "Comando lido por" --> MQTTSub
    
    %% Fluxo de Dados (Resiliência)
    PyKafka -- "Evento (JSON {...})" ---|RESILIÊNCIA|---> Kafka
    Kafka -- "Evento consumido por" --> KafkaSub
    
    %% Fluxo do Frontend
    JavaWS -- "Push em /topic/detections" --> WSSub
    JavaAPI -- "GET /api/v1/history" --- APICall
    
    %% Fluxo do Banco de Dados
    JavaDB -- "Salva em" --> DB