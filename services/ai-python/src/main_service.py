import cv2
import time
import requests
import json
from datetime import datetime # <-- NOVO: Adicionado para o DTO

# Importa as classes dos outros arquivos
# (Assumindo que estão na mesma pasta ou no sys.path)
# from .classification_model import KerasObjectDetector
# from .stream_handler import StreamHandler

# --- CONFIGURAÇÕES GLOBAIS ---

# ... (Configurações 1, 2 e 3 permanecem as mesmas) ...

# 4. Servidor Java (Endpoint Principal - JSON)
# !!! Lembre-se de trocar '192.168.0.XX' pelo IP real do seu PC Java
# (Este é o PASSO 2 do nosso teste)
JAVA_API_ENDPOINT = "http://localhost:8080/api/residues/classify"

# 5. Dispositivo IoT (ESP32/Arduíno - Real)
# !!! Lembre-se de trocar '192.168.0.YY' pelo IP real do seu dispositivo IoT
IOT_API_BASE_URL = "http://192.168.0.YY:8080/classify" # <-- IP do IoT real

# 6. ### ATUALIZADO: ENDPOINT DE TESTE (JAVA SIMULANDO IOT) ###
# !!! Lembre-se de trocar '192.168.0.XX' pelo IP real do seu PC Java
# (Este é o PASSO 1 do nosso teste)
JAVA_IOT_SIMULATOR_ENDPOINT = "http://localhost:8080/api/residues/test-classify"

# 7. Depuração
SHOW_VIDEO_DEBUG = True

# -------------------------------
# (Funções send_to_java_api e send_to_iot_device permanecem as mesmas)
# -------------------------------

def send_to_java_api(detections, source_url):
    """
    Função para enviar dados (JSON completo) ao servidor Java. (Sem alterações)
    Usada pelo loop 'main' principal.
    """
    try:
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
    Função para enviar o comando ao dispositivo IoT REAL. (Sem alterações)
    Usada pelo loop 'main' principal.
    """
    try:
        params = {'cmd': classification} 
        response = requests.post(IOT_API_BASE_URL, params=params, timeout=2)
        print(f"IoT Device REAL Status: {response.status_code} (Comando: {classification})")

    except requests.exceptions.RequestException as e:
        print(f"Erro ao enviar para o dispositivo IoT REAL: {e}")

# -------------------------------
# ### FUNÇÃO DE TESTE ATUALIZADA ###
# -------------------------------
def test_iot_to_java_flow(classification_mock):
    """
    Função de teste ATUALIZADA (Fluxo de 2 Passos):
    Passo 1: Envia para o simulador IoT (Java em /test-classify/{...})
    Passo 2: Envia para o fluxo normal (Java em /classify com JSON)
    """
    print(f"\n--- INICIANDO TESTE DE FLUXO (Python -> IoT Sim -> Python -> Java DB) ---")
    print(f"Classificação Mockada: '{classification_mock}'")
    
    # --- PASSO 1: Enviar para o Simulador IoT (Java) ---
    print("\nPASSO 1: Enviando comando para o 'IoT Simulado' (Java)...")
    try:
        url_step_1 = f"{JAVA_IOT_SIMULATOR_ENDPOINT}/{classification_mock}"
        print(f"URL (Passo 1): {url_step_1}")
        
        response_1 = requests.post(url_step_1, timeout=3)
        
        if response_1.status_code == 200:
            print(f"Sucesso (Passo 1): 'IoT Simulado' recebeu o comando.")
            print(f"Resposta (Passo 1): '{response_1.text}'")
        else:
            print(f"--- FALHA (Passo 1) ---")
            print(f"Status: {response_1.status_code}, Resposta: {response_1.text}")
            print("Abortando teste.")
            return # Aborta o teste se o passo 1 falhar

    except requests.exceptions.RequestException as e:
        print(f"--- ERRO DE CONEXÃO (Passo 1) ---")
        print(f"Não foi possível conectar ao simulador IoT em {JAVA_IOT_SIMULATOR_ENDPOINT}")
        print(f"Erro: {e}")
        return # Aborta

    # Pausa rápida para simular o tempo de processamento
    time.sleep(1) 

    # --- PASSO 2: Enviar para o Fluxo Normal (Java) ---
    print("\nPASSO 2: Enviando DTO (JSON) para o 'Fluxo Normal' (Java DB)...")
    try:
        # Monta o payload (JSON) que o /api/residues/classify espera
        # (Exatamente como o ResidueDTO no Java)
        payload_step_2 = {
            "classification": classification_mock,
            "confidence": 0.99, # Valor mockado
            "timestamp": datetime.now().isoformat() # Timestamp atual em formato ISO
        }
        
        print(f"URL (Passo 2): {JAVA_API_ENDPOINT}")
        print(f"Payload (Passo 2): {json.dumps(payload_step_2, indent=2)}")
        
        # Envia a requisição POST com o corpo JSON
        response_2 = requests.post(JAVA_API_ENDPOINT, json=payload_step_2, timeout=3)

        if response_2.status_code == 200:
            print("--- SUCESSO NO TESTE (COMPLETO) ---")
            print(f"Status (Passo 2): {response_2.status_code}")
            print(f"Resposta do Servidor (Passo 2): '{response_2.text}'")
            print("Fluxo completo testado! Verifique o BD e o Frontend.")
        else:
            print("--- FALHA (Passo 2) ---")
            print(f"Status: {response_2.status_code}, Resposta: {response_2.text}")

    except requests.exceptions.RequestException as e:
        print(f"--- ERRO DE CONEXÃO (Passo 2) ---")
        print(f"Não foi possível conectar ao servidor Java em {JAVA_API_ENDPOINT}")
        print(f"Erro: {e}")
# -------------------------------
# ### FIM DA FUNÇÃO DE TESTE ###
# -------------------------------


def main():
    """
    Função principal de processamento da câmera. (Sem alterações)
    """
    print("Iniciando o serviço de processamento...")
    
    # ... (Código da função 'main' original) ...
    pass # Remova o 'pass' e cole seu código 'main' original aqui


# -------------------------------
# ### COMO EXECUTAR O TESTE ###
# -------------------------------
if __name__ == "__main__":
    
    # Para rodar o TESTE MOCKADO, mude a variável abaixo para True
    # Para rodar o programa NORMAL (câmera), mude para False
    
    MODO_TESTE = True 
    
    if MODO_TESTE:
        # --- Configuração do Teste ---
        
        # 1. Defina aqui o valor que você quer simular
        classificacao_para_testar = "papelao_mock_001" 
        
        # 2. Executa a função de teste
        test_iot_to_java_flow(classificacao_para_testar)
        
    else:
        # Roda o programa principal de processamento da câmera
        # (Certifique-se de colar seu código 'main' acima)
        print("MODO_TESTE=False. (Certifique-se de que a função 'main' está definida)")
        # main() # Descomente isso quando colar sua função main