import cv2
import time
import requests  # <-- NOVO: Adicionado para requisições HTTP
import json      # <-- NOVO: Adicionado para enviar dados ao Java

# Importa as classes dos outros arquivos
from .classification_model import KerasObjectDetector
from .stream_handler import StreamHandler
# REMOVIDO: from .comms_handler import CommsHandler

# --- CONFIGURAÇÕES GLOBAIS ---

# 1. Modelo Keras
MODEL_PATH = 'models/keras_model.h5'
LABELS_PATH = 'models/labels.txt'
INPUT_WIDTH = 320
INPUT_HEIGHT = 320
CONF_THRESHOLD = 0.4 

# 2. Câmera (Fonte)
VIDEO_SOURCE_URL = "http://192.168.0.8:4747/video"

# 3. Servidor MQTT (Broker) - REMOVIDO
# MQTT_BROKER_HOST = "127.0.0.1" 
# MQTT_PORT = 1883
# MQTT_TOPIC_PUBLISH = "detections/results" 

# 4. Servidor Java (Endpoint)
# !!! Lembre-se de trocar '192.168.0.XX' pelo IP real do seu PC Java
JAVA_API_ENDPOINT = "http://192.168.0.XX:8080/api/residues/classify"

# 5. Dispositivo IoT (ESP32/Arduíno) - NOVO
# !!! Lembre-se de trocar '192.168.0.YY' pelo IP real do seu dispositivo IoT
IOT_API_BASE_URL = "http://192.168.0.YY/classify" 

# 6. Depuração
SHOW_VIDEO_DEBUG = True # True para ver a janela de vídeo, False para rodar "headless"

# -------------------------------

def send_to_java_api(detections, source_url):
    """
    NOVO: Função para enviar dados ao servidor Java.
    """
    try:
        # Recria a lógica que o CommsHandler provavelmente fazia:
        # Envia a lista completa de detecções
        payload = {
            "detections": detections,
            "source": source_url
        }
        response = requests.post(JAVA_API_ENDPOINT, json=payload, timeout=3)
        print(f"Java API Status: {response.status_code}")
        
    except requests.exceptions.RequestException as e:
        print(f"Erro ao enviar para o servidor Java: {e}")

def send_to_iot_device(classification):
    """
    NOVO: Função para enviar o comando de classificação ao dispositivo IoT.
    Usa um POST com parâmetros de query, conforme solicitado.
    """
    try:
        # Parâmetros da URL (ex: ?cmd=plastic)
        params = {'cmd': classification}
        
        # Faz a requisição POST para a URL base com os parâmetros
        response = requests.post(IOT_API_BASE_URL, params=params, timeout=2)
        print(f"IoT Device Status: {response.status_code} (Comando: {classification})")

    except requests.exceptions.RequestException as e:
        print(f"Erro ao enviar para o dispositivo IoT: {e}")

# -------------------------------

def main():
    print("Iniciando o serviço de processamento...")
    
    # 1. Inicializa os módulos
    try:
        detector = KerasObjectDetector(
            MODEL_PATH, 
            LABELS_PATH, 
            INPUT_WIDTH, 
            INPUT_HEIGHT, 
            CONF_THRESHOLD
        )
        
        stream = StreamHandler(VIDEO_SOURCE_URL)
        
        # REMOVIDO: Inicialização do CommsHandler
        # comms = CommsHandler(MQTT_BROKER_HOST, MQTT_PORT, MQTT_TOPIC_PUBLISH, JAVA_API_ENDPOINT)
        
    except Exception as e:
        print(f"Erro fatal na inicialização: {e}")
        return # Não pode continuar

    # 2. Conecta ao stream
    if not stream.connect():
        print("Falha ao conectar ao stream. Encerrando.")
        return

    print("Serviço iniciado. Pressione 'q' na janela de vídeo para sair.")

    # 3. Loop principal
    try:
        while True:
            # Pega o frame
            ret, frame = stream.get_frame()
            if not ret:
                print("Falha ao obter frame. Tentando reconectar no próximo ciclo...")
                time.sleep(2) # Pausa antes de tentar de novo
                continue

            # Processa o frame
            annotated_frame, detections = detector.process_frame(frame)

            # Envia os resultados (se houver)
            if detections:
                print(f"Detectados {len(detections)} objetos.")
                
                # --- LÓGICA DE COMUNICAÇÃO ATUALIZADA ---
                
                # 1. Envia para o servidor Java (com todas as detecções)
                send_to_java_api(detections, VIDEO_SOURCE_URL)
                
                # 2. Envia para o dispositivo IoT (apenas a primeira detecção)
                # Pega a label da primeira detecção (a mais provável)
                first_classification = detections[0]['label']
                send_to_iot_device(first_classification)
                
                # REMOVIDO: comms.publish_results(detections, VIDEO_SOURCE_URL)

            # Mostra o vídeo (se depuração estiver ativa)
            if SHOW_VIDEO_DEBUG:
                cv2.imshow("Serviço de Processamento", annotated_frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    print("Tecla 'q' pressionada. Encerrando...")
                    break
    
    except KeyboardInterrupt:
        print("\nInterrupção do teclado (Ctrl+C). Encerrando...")
    finally:
        # 4. Limpeza
        print("Iniciando limpeza...")
        stream.release()
        # REMOVIDO: comms.close()
        if SHOW_VIDEO_DEBUG:
            cv2.destroyAllWindows()
        print("Serviço encerrado.")

if __name__ == "__main__":
    main()