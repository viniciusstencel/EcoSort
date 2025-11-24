import cv2
import time
import requests
import json
import sys
from datetime import datetime

# --- IMPORT DA NOVA CLASSE DE STREAM ---
from stream_handler import StreamHandler

# --- IMPORT DO SEU MODELO REAL (Descomente quando for usar a IA real) ---
# from classification_model import KerasObjectDetector

# --- CONFIGURAÇÕES GLOBAIS ---

# 1. Endpoints
JAVA_API_ENDPOINT = "http://localhost:8080/api/residues/classify"
IOT_API_BASE_URL = "http://192.168.0.YY:8080/classify"  # <-- IP do ESP32 que recebe comandos (Servo)
JAVA_IOT_SIMULATOR_ENDPOINT = "http://localhost:8080/api/residues/test-classify"

# 2. Configurações da Câmera (SNAPSHOT) e Detecção
# URL do ESP32-CAM ou dispositivo que serve a imagem estática (jpg)
SNAPSHOT_URL = "http://192.168.0.XX/capture"  # <-- ATUALIZE AQUI COM O IP DA CÂMERA

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
    print(f"--- INICIANDO SERVIÇO DE VISÃO (Modo Snapshot) ---")
    print(f"--- Alvo: {SNAPSHOT_URL} ---")
    
    # 1. Inicializa o Handler de Stream (Novo Recurso)
    stream_handler = StreamHandler(SNAPSHOT_URL)
    
    # 2. Inicializa o Modelo (SE TIVER O ARQUIVO REAL)
    # detector = KerasObjectDetector("model.h5", "labels.txt") # <--- DESCOMENTE AQUI
    print("Modelo de IA carregado (Simulação ou Real).")

    last_detection_time = 0
    
    try:
        while True:
            # ---------------------------------------------------------
            # 1. CAPTURA (AQUI OCORRE A LÓGICA DAS 3 FOTOS)
            # ---------------------------------------------------------
            # Essa função leva cerca de 1 segundo para executar
            success, frame = stream_handler.get_best_frame_of_three()
            
            if not success or frame is None:
                print("Aguardando restabelecimento da câmera...")
                time.sleep(2)
                continue

            # ---------------------------------------------------------
            # 2. ÁREA DE DETECÇÃO (IA)
            # ---------------------------------------------------------
            
            detected_label = None
            confidence = 0.0

            # --- OPÇÃO A: SEU CÓDIGO REAL (Descomente abaixo) ---
            # prediction = detector.predict(frame)
            # if prediction['confidence'] > CONFIDENCE_THRESHOLD:
            #     detected_label = prediction['label']
            #     confidence = prediction['confidence']

            # --- OPÇÃO B: MODO MANUAL PARA DEBUG (Use tecla 'p' para simular plastico) ---
            # Como o frame não é contínuo (é um slideshow de fotos analisadas), 
            # o waitKey aqui serve para renderizar a janela e capturar tecla.
            key = cv2.waitKey(100) & 0xFF  # Espera 100ms para desenhar a janela
            
            if key == ord('p'):
                detected_label = "plastico"
                confidence = 0.95
                print(" [DEBUG] Simulação manual acionada: PLASTICO")
            elif key == ord('m'):
                detected_label = "metal"
                confidence = 0.88
                print(" [DEBUG] Simulação manual acionada: METAL")

            # ---------------------------------------------------------
            # 3. LÓGICA DE ENVIO (COM COOLDOWN)
            # ---------------------------------------------------------
            current_time = time.time()
            
            if detected_label and (current_time - last_detection_time > DETECTION_COOLDOWN):
                print(f"\n!!! DETECÇÃO CONFIRMADA: {detected_label.upper()} ({confidence*100:.1f}%) !!!")
                
                # Desenha no frame para feedback visual
                cv2.putText(frame, f"DETECTADO: {detected_label}", (10, 50), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                
                # Mostra a imagem que gerou a detecção imediatamente
                if SHOW_VIDEO_DEBUG:
                    cv2.imshow('EcoSort Vision', frame)
                    cv2.waitKey(1) # Força atualização da janela

                # 1. Envia para o Backend Java (Salvar no BD)
                send_to_java_api(detected_label, confidence)
                
                # 2. Envia para o ESP32 (Mover Servo)
                send_to_iot_device(detected_label)
                
                # Atualiza o tempo da última detecção para ativar o cooldown
                last_detection_time = current_time
            
            # ---------------------------------------------------------
            # 4. VISUALIZAÇÃO GERAL
            # ---------------------------------------------------------
            if SHOW_VIDEO_DEBUG:
                # Status na tela (Feedback de Cooldown)
                if (current_time - last_detection_time < DETECTION_COOLDOWN):
                    msg_wait = f"Cooldown... ({int(DETECTION_COOLDOWN - (current_time - last_detection_time))}s)"
                    cv2.putText(frame, msg_wait, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                
                # Mostra "A melhor das 3 imagens" que foi analisada
                cv2.imshow('EcoSort Vision', frame)

            # Sai se pressionar 'q'
            if key == ord('q'):
                break
                
    except KeyboardInterrupt:
        print("\nInterrompido pelo usuário.")
    except Exception as e:
        print(f"Erro não tratado: {e}")
    finally:
        # stream_handler.release() # (Opcional no modo HTTP, mas boa prática chamar)
        cv2.destroyAllWindows()
        print("Serviço encerrado.")

# -------------------------------
# ### EXECUÇÃO ###
# -------------------------------
if __name__ == "__main__":
    
    # Mude para True se quiser apenas testar a conexão sem câmera
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
        main()