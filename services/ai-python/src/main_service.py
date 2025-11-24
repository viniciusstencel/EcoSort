import cv2
import time
import requests
import json
import sys
import random
from datetime import datetime


# --- IMPORT DA SUA CLASSE DE STREAM ---
from stream_handler import StreamHandler
from comms_handler import KerasObjectDetector

# --- IMPORT DO MODELO (Descomente quando tiver o arquivo .h5) ---
# from classification_model import KerasObjectDetector

# ==============================================================================
# CONFIGURAÇÕES GLOBAIS
# ==============================================================================

# 1. Endpoints
JAVA_API_ENDPOINT = "http://host.docker.internal:8080/api/residues/classify" # 'host.docker.internal' acessa o localhost da máquina fora do docker
IOT_API_BASE_URL = "http://ecosort.local/classify"  # <-- Troque pelo IP do ESP32

# 2. Configurações da Câmera
SNAPSHOT_URL = "http://ecosort.local/capture" # <-- ATUALIZE COM O IP DA CAMERA

# 3. Configurações de Comportamento
CONFIDENCE_THRESHOLD = 0.70
DETECTION_COOLDOWN = 10  # Tempo entre um envio e outro

# 4. Flags de Debug e Ambiente
SHOW_VIDEO_DEBUG = False  # <--- MANTENHA FALSE SE RODAR NO DOCKER
SIMULATE_DETECTION = False # <--- TRUE = Gera detecção falsa para teste de rede. FALSE = Usa a I.A.

# ==============================================================================
# FUNÇÕES DE API
# ==============================================================================

def send_to_java_api(classification, confidence):
    try:
        payload = {
            "classification": classification,
            "confidence": float(confidence),
            "timestamp": datetime.now().isoformat()
        }
        print(f" [JAVA] Enviando JSON...")
        response = requests.post(JAVA_API_ENDPOINT, json=payload, timeout=3)
        if response.status_code in [200, 201]:
             print(f" [JAVA] Sucesso: {response.status_code}")
        else:
             print(f" [JAVA] Erro: {response.status_code} - {response.text}")
    except Exception as e:
        print(f" [JAVA] Falha de conexão: {e}")

def send_to_iot_device(classification):
    try:
        params = {'cmd': classification} 
        print(f" [IOT] Enviando comando '{classification}'...")
        response = requests.post(IOT_API_BASE_URL, params=params, timeout=2)
        if response.status_code == 200:
            print(f" [IOT] Sucesso: Comando recebido.")
        else:
            print(f" [IOT] Erro: {response.status_code}")
    except Exception as e:
        print(f" [IOT] Falha de conexão: {e}")

# ==============================================================================
# MAIN LOOP
# ==============================================================================

def main():
    print(f"--- INICIANDO SERVIÇO ---")
    print(f"--- Modo Simulação: {SIMULATE_DETECTION} ---")
    print(f"--- Modo Vídeo: {SHOW_VIDEO_DEBUG} ---")

    # 1. Inicializa Handler
    stream_handler = StreamHandler(SNAPSHOT_URL)

    # 2. Inicializa Modelo (Se não for simulação)
    detector = None
    if not SIMULATE_DETECTION:
        print("Carregando modelo de IA...")
        try:
            # CORREÇÃO APLICADA AQUI:
            # Passamos model_path, labels_path, width, height, threshold
            detector = KerasObjectDetector("model.h5", "labels.txt", 224, 224, CONFIDENCE_THRESHOLD)
            print("Modelo carregado com sucesso!")
        except TypeError as e:
            print(f"Erro de argumentos na classe do Modelo: {e}")
            return # Para o código se não conseguir carregar
        except Exception as e:
            print(f"Erro genérico ao carregar modelo: {e}")
            return

    last_detection_time = 0
    
    try:
        while True:
            # ---------------------------------------------------------
            # 1. CAPTURA (3 FOTOS)
            # ---------------------------------------------------------
            # O stream_handler já imprime os logs de nitidez
            success, frame = stream_handler.get_best_frame_of_three()
            
            if not success or frame is None:
                print("Erro na captura. Tentando novamente em 2s...")
                time.sleep(2)
                continue

            # ---------------------------------------------------------
            # 2. DETECÇÃO (REAL OU SIMULADA)
            # ---------------------------------------------------------
            detected_label = None
            confidence = 0.0

            if SIMULATE_DETECTION:
                # MODO TESTE DE CONEXÃO: Força uma detecção a cada ciclo se passou o tempo
                # Simula uma alternância entre plastico e metal
                mock_labels = ["plastico", "metal", "vidro"]
                detected_label = random.choice(mock_labels)
                confidence = 0.95
                print(f" [SIMULACAO] Gerado rótulo falso: {detected_label}")
            
            else:
                # MODO REAL (I.A.)
                if detector:
                    try:
                        # prediction = detector.predict(frame)
                        # if prediction['confidence'] > CONFIDENCE_THRESHOLD:
                        #     detected_label = prediction['label']
                        #     confidence = prediction['confidence']
                        pass # Remova esse pass quando descomentar acima
                    except Exception as e:
                        print(f"Erro na IA: {e}")
                else:
                    print(" [AVISO] IA desativada e Simulação desativada. Nada será detectado.")

            # ---------------------------------------------------------
            # 3. LÓGICA DE ENVIO (COOLDOWN)
            # ---------------------------------------------------------
            current_time = time.time()
            time_since_last = current_time - last_detection_time

            if detected_label:
                if time_since_last > DETECTION_COOLDOWN:
                    print(f"\n>>> PROCESSANDO DETECÇÃO: {detected_label.upper()} <<<")
                    
                    # 1. Enviar para Java
                    send_to_java_api(detected_label, confidence)
                    
                    # 2. Enviar para ESP32
                    send_to_iot_device(detected_label)
                    
                    last_detection_time = current_time
                    print(">>> Fim do ciclo de envio. Entrando em Cooldown.\n")
                else:
                    # Log opcional para saber que ignorou por causa do tempo
                    print(f" [INFO] Detecção ignorada (Cooldown: {int(DETECTION_COOLDOWN - time_since_last)}s restante)")

            # ---------------------------------------------------------
            # 4. DEBUG VISUAL (Só funciona se não for Docker/Headless)
            # ---------------------------------------------------------
            if SHOW_VIDEO_DEBUG:
                cv2.imshow('EcoSort Vision', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            
            # Pequena pausa para não fritar a CPU se o ciclo for muito rápido
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\nParando serviço...")
    except Exception as e:
        print(f"Erro fatal na Main: {e}")
    finally:
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()