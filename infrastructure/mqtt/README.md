## 📄 README.md - Firmware (`iot-firmware/`)

# 🤖 Firmware do Microcontrolador (Arduino/ESP32)

Esta pasta contém o código C++ que é executado no hardware da lixeira. Ele é dividido logicamente para gerenciar as duas principais funções: **Captura e Envio** e **Recepção e Atuação**.

### 🔌 Componentes de Hardware Abordados

* **Captura:** Módulo ESP32-CAM (câmera + Wi-Fi).
* **Atuação:** Servo motor, motor de passo ou motor DC (com driver).

### 📝 Blocos de Código

1.  **`esp32-cam-code/` (Captura e Envio HTTP)**
    * Responsável por inicializar a câmera e os sensores de detecção.
    * Lógica para tirar a foto e enviá-la via **HTTP POST** para a **API Central Java**.

2.  **`arduino-actuator-code/` (Recepção MQTT e Atuação)**
    * Lógica de conexão com o **Broker MQTT** definido no Docker Compose.
    * **Inscrição** (subscribe) no tópico de comando da API Java.
    * Função de *callback* que recebe o `class_id` e aciona o motor para a posição correta de separação.

### ⚠️ Configuração

Antes de fazer o upload (flashing), você deve configurar as credenciais de Wi-Fi, o endereço IP do Broker MQTT e os tópicos de comunicação.