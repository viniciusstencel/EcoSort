
♻️ Projeto EcoSort: Lixeira Inteligente com Visão Computacional e Automação

Resumo executivo

Este projeto descreve uma lixeira inteligente com uma arquitetura de microsserviços orientada a eventos. O serviço ai-python 🤖 consome um stream de vídeo 📷, classifica os resíduos e dispara dois eventos paralelos: um comando de baixa latência via MQTT 📡 para o hardware (Arduino/ESP32) ⚙️ acionar os servos, e um evento de dados completo via Apache Kafka 📨 para o serviço persistence-java ☕.

O serviço Java persiste esses dados e os transmite via WebSocket 🔌 para o frontend-web 🖥️, atualizando um dashboard em tempo real. Esta arquitetura desacoplada garante que a ação mecânica seja instantânea (via MQTT), enquanto o pipeline de dados para análise e UI é resiliente (via Kafka).

🏗️ 3. Arquitetura geral

O sistema é composto por 5 componentes principais que operam de forma assíncrona:

Hardware (IoT): O Arduino/ESP32 com os servos, atuando como um Consumidor MQTT.

Serviço de IA (services/ai-python): O "Cérebro" do sistema. Consome o stream de vídeo e atua como Produtor MQTT (para o hardware) e Produtor Kafka (para o Java).

Serviço de Persistência (services/persistence-java): O "Historiador". Consome do Kafka, salva no BD e atua como Servidor WebSocket.

Serviço de Frontend (services/frontend-web): O "Dashboard", que é um Cliente WebSocket.

Infraestrutura (infrastructure/): Brokers MQTT e Kafka (com Zookeeper) orquestrados via docker-compose.yml.

🔄 4. Fluxo de funcionamento

O fluxo é paralelo e assíncrono:

O ai-python classifica um resíduo (ex: "metal") a partir do stream de vídeo.

AÇÃO (Hardware): O Python publica a string "metal" no tópico MQTT ecosort/commands.

DADO (Persistência): O Python publica o JSON completo (ex: {"class_name": "metal", ...}) no tópico Kafka ecosort-persistence-events.

(Fluxo Hardware): O Arduino recebe a mensagem MQTT "metal" e move os servos inferior e superior para a posição correta.

(Fluxo Dados): O persistence-java recebe o evento do Kafka, salva-o no banco de dados e, imediatamente, transmite o mesmo JSON via WebSocket para o frontend-web.

💻 6. Software — Ecossistema de Microsserviços

services/ai-python (Processador de Stream / Produtor de Eventos)

Stack: Python, OpenCV, TensorFlow/Keras, paho-mqtt, kafka-python.

Função: Gerencia stream_handler (leitura da câmera), classification_model (inferência) e comms_handler (publicação em MQTT e Kafka).

services/persistence-java (Consumidor de Eventos / Servidor WebSocket)

Stack: Java, Spring Boot, spring-kafka, spring-boot-starter-websocket, spring-data-jpa.

Função: Contém o @KafkaListener para consumir dados, o ResidueRepository para salvar no BD, e o SimpMessagingTemplate para transmitir via WebSocket.

services/frontend-web (Cliente de Visualização)

Stack: React (ou Vue/Angular), Stomp.js/SockJS.

Função: Conecta-se ao WebSocket e exibe os dados de classificação ao vivo.

📡 7. Arquitetura de comunicação

Câmera -> IA: HTTP (Video Stream).

IA -> Hardware (Comando): MQTT (Tópico: ecosort/commands, Payload: "paper"). Foco em latência.

IA -> Java (Dados): Apache Kafka (Tópico: ecosort-persistence-events, Payload: {...JSON...}). Foco em resiliência.

Java -> Frontend (UI): WebSocket (Tópico: /topic/detections, Payload: {...JSON...}). Foco em real-time.

🖥️ 8. Firmware do microcontrolador (MQTT)

O firmware do Arduino/ESP32 é um simples cliente MQTT que ouve o tópico de comandos.

// Pseudocódigo do Arduino
# include <PubSubClient.h> // Cliente MQTT
# include <Servo.h>

Servo servoInferior;
Servo servoSuperior;

// Função chamada quando uma mensagem MQTT chega
void mqttCallback(char* topic, byte* payload, unsigned int length) {
  String command = "";
  for (int i = 0; i < length; i++) {
    command += (char)payload[i];
  }

  if (command == "paper") {
     moverServos(SERVO_INFERIOR_PAPER, SERVO_SUPERIOR_PAPER);
  } else if (command == "plastic") {
     moverServos(SERVO_INFERIOR_PLASTIC, SERVO_SUPERIOR_PLASTIC);
  } // ... etc.
}

void setup() {
  mqttClient.setCallback(mqttCallback);
  mqttClient.subscribe("ecosort/commands");
}

void loop() {
  mqttClient.loop(); // Mantém a conexão MQTT ativa
}
