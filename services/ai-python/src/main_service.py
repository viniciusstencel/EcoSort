# main_service.py

import cv2
import time

# Importa as classes dos outros arquivos
from .classification_model import KerasObjectDetector
from .stream_handler import StreamHandler
from .comms_handler import CommsHandler

# --- CONFIGURAÇÕES GLOBAIS ---

# 1. Modelo Keras
MODEL_PATH = 'models/keras_model.h5'
LABELS_PATH = 'models/labels.txt'
INPUT_WIDTH = 320
INPUT_HEIGHT = 320
CONF_THRESHOLD = 0.4 

# 2. Câmera (Fonte)
VIDEO_SOURCE_URL = "http://192.168.0.8:4747/video"

# 3. Servidor MQTT (Broker)
MQTT_BROKER_HOST = "127.0.0.1" # IP do seu Broker
MQTT_PORT = 1883
MQTT_TOPIC_PUBLISH = "detections/results" 

# 4. Servidor Java (Endpoint)
# !!! Lembre-se de trocar '192.168.0.XX' pelo IP real do seu PC Java
JAVA_API_ENDPOINT = "http://192.168.0.XX:8080/api/residues/classify"

# 5. Depuração
SHOW_VIDEO_DEBUG = True # True para ver a janela de vídeo, False para rodar "headless"

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
        comms = CommsHandler(MQTT_BROKER_HOST, MQTT_PORT, MQTT_TOPIC_PUBLISH, JAVA_API_ENDPOINT)
        
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
                # A chamada permanece a mesma
                comms.publish_results(detections, VIDEO_SOURCE_URL)

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
        comms.close()
        if SHOW_VIDEO_DEBUG:
            cv2.destroyAllWindows()
        print("Serviço encerrado.")

if __name__ == "__main__":
    main()