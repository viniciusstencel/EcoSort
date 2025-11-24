import cv2
import time
import requests
import json
import sys
import random
from datetime import datetime

# --- IMPORT DA SUA CLASSE DE STREAM ---
# Certifique-se que stream_handler.py está na mesma pasta (src)
from stream_handler import StreamHandler
# Certifique-se que classification_model.py está atualizado com a versão 'tf.saved_model.load'
from classification_model import KerasObjectDetector

# ==============================================================================
# CONFIGURAÇÕES GLOBAIS
# ==============================================================================

# 1. Endpoints
# 'host.docker.internal' permite que o Docker acesse o backend rodando no Windows
JAVA_API_ENDPOINT = "http://host.docker.internal:8080/api/residues/classify" 
IOT_API_BASE_URL = "http://ecosort.local/classify"  # <-- Se falhar, tente usar o IP numérico (ex: 192.168.0.X)

# 2. Configurações da Câmera
SNAPSHOT_URL = "http://ecosort.local/capture" # <-- ATUALIZE COM O IP DA CAMERA

# 3. Configurações de Comportamento
CONFIDENCE_THRESHOLD = 0.60 # Ajustado para 60% (0.40 é muito baixo, pode dar falso positivo)
DETECTION_COOLDOWN = 10     # Tempo em segundos entre um envio e outro

# 4. Flags de Debug e Ambiente
SHOW_VIDEO_DEBUG = False    # MANTENHA FALSE NO DOCKER
SIMULATE_DETECTION = False  # FALSE = Usa a I.A. Real

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
        print(f" [JAVA] Enviando JSON para API...")
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

    # 1. Inicializa Handler de Imagem
    stream_handler = StreamHandler(SNAPSHOT_URL)

    # 2. Inicializa Modelo (Se não for simulação)
    detector = None
    if not SIMULATE_DETECTION:
        print("Carregando modelo de IA...")
        try:
            # --- ATENÇÃO AO CAMINHO ---
            # Estamos usando SavedModel (Pasta), não arquivo .h5
            # Certifique-se de que a pasta 'meu_modelo_saved' está dentro de 'models/'
            model_folder_path = "models/meu_modelo_saved" 
            labels_path = "models/labels.txt"
            
            # Instancia o detector (largura e altura 224 são padrão do Teachable Machine)
            detector = KerasObjectDetector(model_folder_path, labels_path, 224, 224, CONFIDENCE_THRESHOLD)
            print("Modelo carregado com sucesso!")
            
        except FileNotFoundError as e:
            print(f"ERRO CRÍTICO: Arquivo não encontrado. Verifique a pasta models/. Detalhe: {e}")
            return
        except Exception as e:
            print(f"Erro genérico ao carregar modelo: {e}")
            return

    last_detection_time = 0
    
    try:
        while True:
            # ---------------------------------------------------------
            # 1. CAPTURA (3 FOTOS)
            # ---------------------------------------------------------
            success, frame = stream_handler.get_best_frame_of_three()
            
            if not success or frame is None:
                print("Erro na captura ou Câmera offline. Tentando novamente em 2s...")
                time.sleep(2)
                continue

            # ---------------------------------------------------------
            # 2. DETECÇÃO (REAL OU SIMULADA)
            # ---------------------------------------------------------
            detected_label = None
            confidence = 0.0

            if SIMULATE_DETECTION:
                mock_labels = ["plastico", "metal", "vidro", "papel"]
                detected_label = random.choice(mock_labels)
                confidence = 0.95
                print(f" [SIMULACAO] Gerado rótulo falso: {detected_label}")
            
            else:
                # MODO REAL (I.A.)
                if detector:
                    try:
                        # Faz a predição usando o frame capturado
                        prediction = detector.predict(frame)
                        
                        # O método predict já retorna 'label': None se a confiança for baixa
                        if prediction['label'] is not None:
                            detected_label = prediction['label']
                            confidence = prediction['confidence']
                            print(f" [IA] Identificado: {detected_label} ({confidence:.2f})")
                        else:
                            # Opcional: Mostrar log de baixa confiança
                            if prediction['confidence'] > 0.1: # Só loga se não for zero absoluto
                                print(f" [IA] Ignorado (Confiança baixa: {prediction['confidence']:.2f})")

                    except Exception as e:
                        print(f"Erro durante a inferência da IA: {e}")
                else:
                    print(" [AVISO] Detector não inicializado.")

            # ---------------------------------------------------------
            # 3. LÓGICA DE ENVIO (COOLDOWN)
            # ---------------------------------------------------------
            current_time = time.time()
            time_since_last = current_time - last_detection_time

            if detected_label:
                if time_since_last > DETECTION_COOLDOWN:
                    print(f"\n>>> PROCESSANDO DETECÇÃO VÁLIDA: {detected_label.upper()} <<<")
                    
                    # 1. Enviar para Java (Banco de Dados)
                    send_to_java_api(detected_label, confidence)
                    
                    # 2. Enviar para ESP32 (Motor/Servo)
                    send_to_iot_device(detected_label)
                    
                    last_detection_time = current_time
                    print(">>> Enviado. Entrando em Cooldown.\n")
                else:
                    remaining = int(DETECTION_COOLDOWN - time_since_last)
                    print(f" [INFO] Cooldown ativo. Ignorando {detected_label} por mais {remaining}s.")

            # ---------------------------------------------------------
            # 4. DEBUG VISUAL (Só funciona fora do Docker)
            # ---------------------------------------------------------
            if SHOW_VIDEO_DEBUG:
                cv2.imshow('EcoSort Vision', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            
            # Pequena pausa para aliviar a CPU
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\nParando serviço...")
    except Exception as e:
        print(f"Erro fatal na Main: {e}")
    finally:
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()