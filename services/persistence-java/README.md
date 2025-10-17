# ⚙️ API Central (Java Backend)

Este é o **coração** do Projeto EcoSort. A API Central, desenvolvida em Java (usando Spring Boot ou Quarkus), gerencia a lógica de negócios, o fluxo de comunicação e a persistência de dados.

### 🛠️ Responsabilidades

1.  **API Gateway:** Recebe as requisições HTTP do microcontrolador (imagem do resíduo).
2.  **Proxy IA:** Envia a imagem para o Servidor IA (Python) e processa o retorno.
3.  **Persistência:** Armazena os logs de classificação e os dados de coleta no **PostgreSQL**.
4.  **Mensageria IoT (MQTT):** Publica comandos de atuação (posição do motor) no Broker MQTT, acionando o hardware.
5.  **Comunicação Web (WebSockets):** Dispara notificações em tempo real para o Frontend React (gamificação).

### 🌐 Endpoints Principais

| Método | Endpoint | Função |
| :--- | :--- | :--- |
| `POST` | `/api/v1/coleta/depositar` | Recebe a imagem do hardware e inicia o fluxo de classificação e atuação. |
| `GET` | `/api/v1/relatorios/diario` | Fornece dados agregados para o dashboard React. |
| `WS` | `/ws/feed` | Canal WebSocket para enviar notificações ao vivo para o frontend. |

### 📦 Como Construir e Rodar (Localmente)

Para rodar este serviço de forma isolada (sem o Docker Compose):

1.  Certifique-se de que o Java SDK (preferencialmente 17+) está instalado.
2.  Instale as dependências (Maven ou Gradle).
3.  Compile o projeto:
    ```bash
    ./mvnw clean package 
    ```
4.  Execute o JAR:
    ```bash
    java -jar target/seu-app.jar
    ```