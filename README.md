# ♻️ Projeto EcoSort: Lixeira Inteligente com Visão Computacional

Este projeto implementa uma lixeira inteligente que utiliza **visão computacional (IA)** para classificar automaticamente resíduos e separá-los em compartimentos corretos, promovendo a reciclagem com alta acurácia. A arquitetura é totalmente modularizada em microsserviços e orquestrada via Docker.

### 🏛️ Arquitetura (Microsserviços)

| Serviço | Tecnologia | Função | Pasta | Emoji |
| :--- | :--- | :--- | :--- | :--- |
| **API Central** | Java (Spring/Quarkus) | Lógica de negócios, API, logs e mensageria. | `backend-java/` | ⚙️ |
| **Servidor IA** | Python (FastAPI/TensorFlow) | Classificação de imagens e retorno de código. | `ia-python/` | 🧠 |
| **Frontend Web** | React.js | Experiência de usuário, gamificação e relatórios em tempo real. | `frontend-react/` | 🖥️ |
| **Microcontrolador** | Arduino/ESP32 (C++) | Captura de imagem e atuação dos motores. | `iot-firmware/` | 🤖 |
| **Infraestrutura** | PostgreSQL, MQTT Broker | Banco de dados persistente e comunicação IoT. | `docker-config/` | 🐳 |

---

### 🚀 Como Iniciar o Projeto (Orquestração)

Todos os serviços (Java, Python, React, PostgreSQL e MQTT) são gerenciados pelo Docker Compose.

1.  **Pré-requisitos:** Instale **Docker** e **Docker Compose**.
2.  **Configuração:** Navegue até a pasta `docker-config/` e preencha o arquivo `.env` com as variáveis necessárias (senhas, portas, etc.).
3.  **Execução:** Na pasta `docker-config/`, execute o comando para construir e subir todos os contêineres em background:

    ```bash
    docker compose up --build -d
    ```

4.  **Acesso:**
    * **API Central (Backend):** `http://localhost:8080/` (ou porta configurada)
    * **Frontend Web (App):** `http://localhost:3000/` (ou porta configurada)

---