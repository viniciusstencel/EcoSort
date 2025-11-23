import cv2
import time
import requests
import json
import sys
from datetime import datetime

# --- IMPORT DO SEU MODELO REAL (Descomente quando for usar a IA real) ---
# from classification_model import KerasObjectDetector

# --- CONFIGURAÇÕES GLOBAIS ---

# 1. Endpoints
JAVA_API_ENDPOINT = "http://localhost:8080/api/residues/classify"
IOT_API_BASE_URL = "http://192.168.0.YY:8080/classify"  # <-- Troque pelo IP do ESP32
JAVA_IOT_SIMULATOR_ENDPOINT = "http://localhost:8080/api/residues/test-classify"

# 2. Configurações da Câmera e Detecção
CAMERA_INDEX = 0        # 0 geralmente é a webcam padrão
CONFIDENCE_THRESHOLD = 0.70  # Só aceita se a IA tiver 70% de certeza
DETECTION_COOLDOWN = 5  # Segundos para esperar entre uma detecção e outra (evita spam)

# 3. Depuração
SHOW_VIDEO_DEBUG = True


# -------------------------------
# ### FUNÇÕES DE COMUNICAÇÃO (API) ###
# -------------------------------

def send_to_java_api(classification, confidence):
    """
    Envia o JSON (DTO) para o Backend Java (Spring Boot).
    """
    try:
        payload = {
            "classification": classification,
            "confidence": float(confidence),
            "timestamp": datetime.now().isoformat()
        }
        
        print(f" [JAVA] Enviando: {json.dumps(payload)}")
        response = requests.post(JAVA_API_ENDPOINT, json=payload, timeout=3)
        
        if response.status_code == 200 or response.status_code == 201:
             print(f" [JAVA] Sucesso: {response.status_code}")
        else:
             print(f" [JAVA] Erro API: {response.status_code} - {response.text}")
        
    except requests.exceptions.RequestException as e:
        print(f" [JAVA] Falha de conexão: {e}")

def send_to_iot_device(classification):
    """
    Envia comando simples para o ESP32 mover os servos.
    """
    try:
        # O ESP32 espera ?cmd=plastico
        params = {'cmd': classification} 
        print(f" [IOT] Enviando comando '{classification}' para {IOT_API_BASE_URL}...")
        
        response = requests.post(IOT_API_BASE_URL, params=params, timeout=2)
        
        if response.status_code == 200:
            print(f" [IOT] Sucesso: O dispositivo recebeu o comando.")
        else:
            print(f" [IOT] Erro Device: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f" [IOT] Falha de conexão (Verifique se o ESP32 está ligado): {e}")

# -------------------------------
# ### FUNÇÃO DE TESTE (MOCK) ###
# -------------------------------
def test_iot_to_java_flow(classification_mock):
    print(f"\n--- [TESTE] Iniciando fluxo simulado para: '{classification_mock}' ---")
    
    # 1. Simula envio para o Java (Simulador IoT)
    try:
        url = f"{JAVA_IOT_SIMULATOR_ENDPOINT}/{classification_mock}"
        requests.post(url, timeout=2)
        print(" [TESTE] Passo 1 (Simulador) OK")
    except Exception as e:
        print(f" [TESTE] Passo 1 Falhou: {e}")

    time.sleep(1)

    # 2. Simula envio normal (DB)
    send_to_java_api(classification_mock, 0.99)
    print("--- [TESTE] Fim do ciclo ---")


# -------------------------------
# ### FUNÇÃO PRINCIPAL (CAMERA LOOP) ###
# -------------------------------
def main():
    print(f"--- INICIANDO SERVIÇO DE VISÃO (Câmera {CAMERA_INDEX}) ---")
    
    # 1. Inicializa a Câmera
    cap = cv2.VideoCapture(CAMERA_INDEX)
    
    if not cap.isOpened():
        print("ERRO: Não foi possível abrir a câmera.")
        return

    # 2. Inicializa o Modelo (SE TIVER O ARQUIVO REAL)
    # detector = KerasObjectDetector("model.h5", "labels.txt") # <--- DESCOMENTE AQUI
    print("Modelo de IA carregado (Simulação ou Real).")

    last_detection_time = 0
    
    try:
        while True:
            # Leitura do frame
            ret, frame = cap.read()
            if not ret:
                print("Falha ao capturar imagem da câmera.")
                break

            # ---------------------------------------------------------
            # ÁREA DE DETECÇÃO (IA)
            # ---------------------------------------------------------
            
            detected_label = None
            confidence = 0.0

            # --- OPÇÃO A: SEU CÓDIGO REAL (Descomente abaixo) ---
            # prediction = detector.predict(frame)
            # if prediction['confidence'] > CONFIDENCE_THRESHOLD:
            #     detected_label = prediction['label']
            #     confidence = prediction['confidence']

            # --- OPÇÃO B: MODO MANUAL PARA DEBUG (Use tecla 'p' para simular plastico) ---
            # Isso permite testar sem a IA real rodando
            # Pressione 'p' no teclado enquanto a janela do vídeo está aberta
            key = cv2.waitKey(1) & 0xFF
            if key == ord('p'):
                detected_label = "plastico"
                confidence = 0.95
                print(" [DEBUG] Simulação manual acionada: PLASTICO")
            elif key == ord('m'):
                detected_label = "metal"
                confidence = 0.88
                print(" [DEBUG] Simulação manual acionada: METAL")

            # ---------------------------------------------------------
            # LÓGICA DE ENVIO (COM COOLDOWN)
            # ---------------------------------------------------------
            current_time = time.time()
            
            if detected_label and (current_time - last_detection_time > DETECTION_COOLDOWN):
                print(f"\n!!! DETECÇÃO CONFIRMADA: {detected_label.upper()} ({confidence*100:.1f}%) !!!")
                
                # Desenha no vídeo
                cv2.putText(frame, f"DETECTADO: {detected_label}", (10, 50), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                
                # 1. Envia para o Backend Java (Salvar no BD)
                send_to_java_api(detected_label, confidence)
                
                # 2. Envia para o ESP32 (Mover Servo)
                send_to_iot_device(detected_label)
                
                # Atualiza o tempo da última detecção para ativar o cooldown
                last_detection_time = current_time
            
            # Mostra o vídeo se configurado
            if SHOW_VIDEO_DEBUG:
                # Status na tela
                if (current_time - last_detection_time < DETECTION_COOLDOWN):
                    msg_wait = f"Aguardando... ({int(DETECTION_COOLDOWN - (current_time - last_detection_time))}s)"
                    cv2.putText(frame, msg_wait, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                
                cv2.imshow('EcoSort Vision', frame)

            # Sai se pressionar 'q'
            if key == ord('q'):
                break
                
    except KeyboardInterrupt:
        print("\nInterrompido pelo usuário.")
    finally:
        cap.release()
        cv2.destroyAllWindows()
        print("Serviço encerrado.")

# -------------------------------
# ### EXECUÇÃO ###
# -------------------------------
if __name__ == "__main__":
    
    # Mude para True se quiser apenas testar a conexão sem abrir câmera
    MODO_TESTE_SEM_CAMERA = False 
    
    if MODO_TESTE_SEM_CAMERA:
        print("!!! MODO TESTE (SEM CAMERA) !!!")
        print("Enviando dados falsos em loop para testar rede...")
        try:
            while True:
                test_iot_to_java_flow("teste_vidro")
                print("Aguardando 5s...")
                time.sleep(5)
        except KeyboardInterrupt:
            print("Fim do teste.")
    else:
        # MODO REAL
        # Certifique-se de ter instalado: pip install opencv-python requests
        main()