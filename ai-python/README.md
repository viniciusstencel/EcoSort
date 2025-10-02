# 🧠 Servidor de Classificação de Imagens (Python/FastAPI)

Este serviço de microsserviço é dedicado a rodar o modelo de **Visão Computacional**. Ele recebe a imagem bruta do Backend Java via HTTP, realiza a inferência e retorna uma classificação JSON.

### 🚀 Tecnologias

* **Framework:** **FastAPI** (ou Flask) para criar um endpoint HTTP leve e de alta performance.
* **Modelo:** CNN (ex: MobileNetV2, EfficientNet) treinado em um dataset de resíduos.
* **Biblioteca:** TensorFlow/Keras ou PyTorch.

### 📂 Estrutura Interna

| Arquivo/Pasta | Descrição |
| :--- | :--- |
| **`src/classifier.py`** | Contém a API e a lógica de carregamento do modelo, pré-processamento de imagem e a inferência. |
| **`models/`** | Pasta para armazenar o arquivo do modelo treinado (`model.h5` ou similar). |
| **`requirements.txt`** | Lista as dependências Python necessárias (FastAPI, TensorFlow, etc.). |

### 💻 Endpoint Principal

| Método | Endpoint | Função |
| :--- | :--- | :--- |
| `POST` | `/classificar` | Recebe o payload da imagem e retorna um JSON de classificação. |

### 🖼️ Exemplo de Resposta

```json
{
  "class_id": 2,
  "class_name": "metal",
  "confidence": 0.95
}