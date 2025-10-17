# ⚙️ Arquitetura de Microsserviços EcoSort: Classificação de Resíduos em Tempo Real

O projeto EcoSort é uma solução de *streaming* robusta, projetada para automação de classificação de resíduos, combinando um sistema embarcado de baixa latência (IoT) com uma infraestrutura de microsserviços altamente escalável (Kubernetes e Kafka).

## Visão Geral da Arquitetura (Orientada a Eventos - EDA)

A arquitetura é dividida em quatro camadas principais, conectadas por eventos duráveis e assíncronos (Kafka):

1.  **Camada de Borda (Edge/IoT):** Captura de dados e atuação física.
2.  **Camada de Processamento (IA):** Consumo do *stream* e geração de eventos de classificação.
3.  **Camada de Persistência (Backend Java):** Armazenamento de dados e interface com o frontend.
4.  **Camada de Orquestração (Kubernetes/Kafka):** Resiliência, escalabilidade e comunicação.

---

## Detalhamento dos Componentes

### 1. 🤖 Módulo IoT/Hardware (ESP32-CAM)

O ponto de contato físico, responsável pela aquisição de imagens e pela atuação do mecanismo de separação.

| Aspecto | Implementação | Função e Protocolo |
| :--- | :--- | :--- |
| **Aquisição da Imagem** | **Servidor HTTP Embarcado** no ESP32-CAM. | Expõe o *stream* de vídeo (M-JPEG) em uma URL de rede local (ex: `http://192.168.1.100/stream`). O IoT atua passivamente, *servindo* a imagem. |
| **Comando de Atuação** | **MQTT Subscriber** no ESP32. | Recebe comandos instantaneamente (payload de classificação) para acionar servo motores ou atuadores do mecanismo de separação de resíduos. |
| **Lógica de Borda** | Lógica de *fail-safe* (C/C++). | Garante que, em caso de falha de comunicação, o resíduo seja direcionado a um compartimento seguro ("Outros"). |

### 2. 🧠 Servidor IA (Classificador Python - Microsserviço)

O coração do sistema de classificação, focado em consumir o *stream* e produzir o evento de resultado.

| Aspecto | Implementação | Justificativa |
| :--- | :--- | :--- |
| **Consumo do Stream** | Biblioteca **OpenCV (`cv2.VideoCapture`)** no Python. | Consome ativamente o *stream* M-JPEG do ESP32-CAM frame a frame para baixa latência de detecção. |
| **Modelo de Inferência** | **TensorFlow/Keras** (usando Transfer Learning - MobileNetV2/EfficientNet). | Garante alta acurácia (meta de 90%) e desempenho rápido na classificação do resíduo. |
| **Produção de Eventos** | **Produtor Kafka** (`kafka-python`). | Envia o resultado da classificação (tipo, confiança, timestamp) para o **Tópico Kafka: `classification-result`**. |
| **Atuação** | **MQTT Publisher**. | Publica a classificação final (e o comando) de volta ao ESP32 via MQTT, ativando a separação física. |

### 3. 🏦 Serviço de Persistência e Backend (Java - Microsserviço)

O serviço Java atua como o **consumidor principal** do fluxo de eventos e a interface com o Frontend.

| Aspecto | Implementação | Função Arquitetural |
| :--- | :--- | :--- |
| **Consumo de Eventos** | **Consumidor Kafka** (ex: Spring Kafka) assinando o Tópico: **`classification-result`**. | Garante que *todos* os eventos de classificação (produzidos pelo Python) sejam recebidos e processados de forma confiável. |
| **Persistência de Dados** | **PostgreSQL** com Mapeamento Objeto-Relacional (JPA). | Centraliza a lógica de persistência e garante a integridade dos dados históricos (essenciais para relatórios de sustentabilidade). |
| **Feedback em Tempo Real** | Gerenciamento de sessões **WebSockets**. | Envia o resultado da classificação diretamente para o Frontend (React.js) para feedback imediato e gamificação. |

### 4. 🐳 Orquestração e Base Operacional (Kubernetes & Kafka)

A infraestrutura que garante que o sistema seja tolerante a falhas, escalável e de alto desempenho.

| Componente | Função Detalhada | Benefício |
| :--- | :--- | :--- |
| **Orquestrador** | **Kubernetes (K8s)** | Gerencia o ciclo de vida dos contêineres, realiza **autocorreção** (reiniciando serviços que falham) e abstrai a infraestrutura de nuvem. |
| **Broker de Mensagens** | **Apache Kafka Cluster** | Atua como o **canal durável e de alta vazão** para o *streaming* de eventos. Garante que nenhum dado seja perdido, mesmo se o Backend Java (consumidor) estiver temporariamente offline. |
| **Escalabilidade Automática**| **Horizontal Pod Autoscaler (HPA)** no Kubernetes. | Monitora a carga do Serviço IA (Python) e do Backend Java, e automaticamente cria mais *pods* (instâncias) para lidar com picos de volume de resíduos. |
| **Comunicação de Rede** | **Service Objects (K8s) e Rede MQTT** | O K8s garante que o Python e o Java se comuniquem com o Kafka e o PostgreSQL através de nomes de serviço estáveis, garantindo a alta disponibilidade. |

### 5. 📁 Estrutura de Pastas do Projeto EcoSort (Formato de Lista Aninhada)

Esta estrutura de pastas organiza o projeto em três camadas principais (Infraestrutura, Serviços e Documentação) para clareza e manutenibilidade.

- **EcoSort/**
    - `.gitignore` (Arquivos ignorados pelo Git)
    - `README.md` (Documentação principal e instruções de uso)

### 1. Diretório `infrastructure/` (Configurações de Orquestração)

Este diretório contém todos os arquivos necessários para rodar e gerenciar o ecossistema (Kafka, PostgreSQL, Kubernetes).

- **infrastructure/**
    - `docker-compose.yml` (Configuração para ambiente de desenvolvimento local)
    - `kafka/` (Configurações do Broker Kafka)
    - `mqtt/` (Configurações do Broker MQTT)
    - `postgres/` (Scripts/Dockerfile para inicialização do PostgreSQL)
    - `kubernetes/` (Manifestos de Deploy em Produção)
        - `ia-deployment.yaml`
        - `java-deployment.yaml`
        - `postgres-deployment.yaml`
        - `...` (Outros manifestos de Service, ConfigMaps, etc.)

### 2. Diretório `services/` (Código dos Microsserviços)

Contém o código-fonte de cada aplicação independente.

#### A. `services/ia-python/` 🧠 Servidor IA

- **ia-python/**
    - `Dockerfile`
    - `requirements.txt` (Dependências Python: TensorFlow, OpenCV, Kafka)
    - `src/` (Código-fonte da lógica de consumo do stream, inferência e publicação)
    - `models/` (Arquivos do modelo de Machine Learning)

#### B. `services/persistence-java/` 🏦 Backend Java

- **persistence-java/**
    - `Dockerfile`
    - `pom.xml` / `build.gradle` (Dependências Java: Spring Boot, Kafka Consumer, JPA)
    - `src/` (Código-fonte do Backend: Consumers, Controllers, Models)

#### C. `services/frontend-web/` 🖥️ Frontend Web

- **frontend-web/**
    - `Dockerfile`
    - `package.json`
    - `nginx.conf` (Configuração do servidor para servir o React)
    - `src/` (Código-fonte do aplicativo React e lógica de WebSockets)

### 3. Diretório `docs/` (Documentação)

- **docs/**
    - `architecture/`
        - `overview.md` (Detalhe da arquitetura de microsserviços)
---

# 📁 Estrutura de Pastas do Projeto EcoSort (Formato Tabela)

| Nível 1 | Nível 2 | Nível 3 | Nível 4 | Arquivo/Descrição |
| :--- | :--- | :--- | :--- | :--- |
| **EcoSort/** | | | | |
| | | | | `.gitignore` |
| | | | | `README.md` |
| | **infrastructure/** | | | |
| | | `kafka/` | | Configuração do Kafka |
| | | `mqtt/` | | Configuração do MQTT |
| | | `postgres/` | | Configuração do PostgreSQL |
| | | `docker-compose.yml` | | Ambiente de Desenvolvimento Local |
| | | `kubernetes/` | | Manifestos de Produção (K8s) |
| | | | `ia-deployment.yaml` | Deploy do Serviço IA |
| | | | `java-deployment.yaml` | Deploy do Serviço Java |
| | | | `postgres-deployment.yaml` | Deploy do Banco de Dados |
| | **services/** | | | |
| | | `ia-python/` | 🧠 Servidor IA | |
| | | | | `Dockerfile` |
| | | | | `requirements.txt` |
| | | | `src/` | Código Python |
| | | | `models/` | Modelos de IA |
| | | `persistence-java/` | 🏦 Backend Java | |
| | | | | `Dockerfile` |
| | | | `src/` | Código Java |
| | | | `pom.xml` / `build.gradle` | Dependências |
| | | `frontend-web/` | 🖥️ Frontend Web | |
| | | | | `Dockerfile` |
| | | | `src/` | Código React |
| | | | `package.json` | Dependências NPM |
| | | | `nginx.conf` | Configuração do Servidor Web |
| | **docs/** | | | |
| | | `architecture/` | | |
| | | | | `overview.md` |