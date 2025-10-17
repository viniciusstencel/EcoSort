# 🧠 Serviço IA (ia-python) - Classificador de Resíduos

Este microsserviço é o coração da inteligência do projeto EcoSort, responsável por consumir o stream de vídeo em tempo real, executar a inferência do Machine Learning e produzir os eventos de classificação.

## ⚙️ Atuação e Fluxo de Dados

O serviço `ia-python` opera ativamente consumindo dados e produzindo eventos:

1.  **Consumo de Stream:** Utiliza a biblioteca **OpenCV (`cv2`)** para se conectar e consumir o *stream* M-JPEG fornecido pelo hardware IoT (ESP32-CAM) no endereço de rede local.
2.  **Processamento:** Processa os *frames* do vídeo, realiza o pré-processamento necessário (redimensionamento, normalização) e executa a inferência utilizando o modelo **TensorFlow/Keras**.
3.  **Produção de Eventos (Kafka):** Após a classificação, publica o resultado (classe do resíduo, nível de confiança, timestamp) no **Tópico Kafka: `classification-result`**.
4.  **Atuação Física (MQTT):** Publica o comando de atuação (a classificação final) no **Broker MQTT**, que é o protocolo de baixa latência usado para acionar os motores e separadores no hardware.

## 🛠️ Tecnologias Principais

| Componente | Ferramenta | Função |
| :--- | :--- | :--- |
| **Linguagem** | Python | Linguagem ideal para Machine Learning e Visão Computacional. |
| **Framework ML** | TensorFlow/Keras | Motor de inferência para a Rede Neural Convolucional (CNN). |
| **Visão Comp.** | OpenCV (`cv2`) | Usado para consumir o *stream* de vídeo e realizar o pré-processamento da imagem. |
| **Mensageria** | `kafka-python` | Cliente produtor que envia os eventos para o cluster Kafka. |

## 📦 Como Executar Localmente

1.  Certifique-se de que o Broker Kafka e o Broker MQTT estejam em execução via `docker-compose up`.
2.  Instale as dependências: `pip install -r requirements.txt`.
3.  Execute o script principal: `python src/consumer_stream.py`.
### 🖼️ Exemplo de Resposta

```json
{
  "class_id": 2,
  "class_name": "metal",
  "confidence": 0.95
}