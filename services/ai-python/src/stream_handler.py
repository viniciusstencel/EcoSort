import cv2
import time
import requests
import numpy as np

class StreamHandler:
    """ 
    Gerencia a captura de snapshots de uma URL. 
    Foca em capturar múltiplas imagens e selecionar a melhor (mais nítida).
    """
    
    def __init__(self, snapshot_url):
        self.snapshot_url = snapshot_url
        print(f"Handler de Snapshot inicializado para: {self.snapshot_url}")

    def _fetch_single_frame(self):
        """ 
        Faz uma requisição HTTP para baixar a imagem atual da URL. 
        Retorna o frame no formato OpenCV (BGR) ou None em caso de erro.
        """
        try:
            response = requests.get(self.snapshot_url, timeout=5)
            if response.status_code == 200:
                # Converte os bytes da resposta para um array numpy
                img_array = np.array(bytearray(response.content), dtype=np.uint8)
                # Decodifica o array para uma imagem OpenCV
                frame = cv2.imdecode(img_array, -1)
                return frame
            else:
                print(f"Erro ao obter imagem: Status Code {response.status_code}")
                return None
        except Exception as e:
            print(f"Exceção ao conectar na URL: {e}")
            return None

    def _calculate_sharpness(self, frame):
        """
        Calcula a nitidez da imagem usando a variância do Laplaciano.
        Quanto maior o valor, mais nítida (menos borrada) é a imagem.
        """
        if frame is None:
            return 0
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return cv2.Laplacian(gray, cv2.CV_64F).var()

    def get_best_frame_of_three(self):
        """ 
        Captura 3 imagens com um intervalo, compara a nitidez delas 
        e retorna a melhor imagem (True, best_frame).
        Retorna (False, None) se falhar em todas.
        """
        frames_collected = []
        
        print("Iniciando captura de 3 quadros...")
        
        for i in range(3):
            frame = self._fetch_single_frame()
            
            if frame is not None:
                score = self._calculate_sharpness(frame)
                frames_collected.append((score, frame))
                print(f"Captura {i+1}/3 - Score de nitidez: {score:.2f}")
            else:
                print(f"Captura {i+1}/3 falhou.")
            
            # Pequeno delay para totalizar aprox 1 segundo para as 3 fotos
            # (ajuste conforme a latência da sua rede/câmera)
            if i < 2: 
                time.sleep(0.3) 

        if not frames_collected:
            print("Falha: Nenhuma imagem pôde ser capturada.")
            return (False, None)

        # Ordena pelo score (nitidez) em ordem decrescente e pega o primeiro
        best_score, best_frame = max(frames_collected, key=lambda item: item[0])
        
        print(f"Melhor imagem selecionada com score: {best_score:.2f}")
        return (True, best_frame)

    def release(self):
        """ 
        Para requisições HTTP simples, não há conexão persistente para fechar,
        mas mantemos o método para compatibilidade com a estrutura antiga.
        """
        pass