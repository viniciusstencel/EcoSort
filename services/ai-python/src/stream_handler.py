# stream_handler.py

import cv2
import time

class StreamHandler:
    """ Gerencia a conexão e captura do stream de vídeo. """
    
    def __init__(self, stream_url):
        self.stream_url = stream_url
        self.cap = None
        print(f"Handler de Stream inicializado para: {self.stream_url}")

    def connect(self):
        """ Tenta estabelecer a conexão com o stream. """
        print(f"Tentando conectar ao stream: {self.stream_url}")
        self.cap = cv2.VideoCapture(self.stream_url)
        
        if not self.cap.isOpened():
            print(f"Erro: Não foi possível conectar ao stream em {self.stream_url}")
            return False
        
        print("Conexão com o stream estabelecida.")
        return True

    def get_frame(self):
        """ 
        Captura um frame. Tenta reconectar se a leitura falhar.
        Retorna: (True, frame) em sucesso, (False, None) em falha.
        """
        if self.cap is None or not self.cap.isOpened():
            print("Stream não está conectado. Tentando reconectar...")
            if not self.connect():
                time.sleep(2) # Espera antes de tentar novamente
                return (False, None)
        
        ret, frame = self.cap.read()
        
        if not ret:
            print("Falha ao capturar o quadro. Conexão pode ter caído.")
            self.release() # Fecha a conexão antiga
            return (False, None) # Sinaliza falha para o loop principal
            
        return (True, frame)

    def release(self):
        """ Libera os recursos da câmera. """
        if self.cap is not None:
            self.cap.release()
            print("Stream liberado.")