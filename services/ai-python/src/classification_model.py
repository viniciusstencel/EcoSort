import tensorflow as tf
import numpy as np
import cv2
import os

class KerasObjectDetector:
    
    def __init__(self, model_folder_path, labels_path, input_width=224, input_height=224, conf_threshold=0.70):
        self.input_width = int(input_width)
        self.input_height = int(input_height)
        self.conf_threshold = float(conf_threshold)

        print(f" [IA] Inicializando detector (SavedModel)...")
        
        # 1. Carrega Labels
        self.labels = []
        try:
            print(f" [IA] Lendo labels de: {labels_path}")
            with open(labels_path, 'r', encoding='utf-8') as f:
                # Pega o texto após o primeiro espaço
                self.labels = [line.strip().split(' ', 1)[-1] for line in f.readlines() if line.strip()]
            print(f" [IA] Labels carregados: {self.labels}")
        except Exception as e:
            print(f" [IA] Erro ao ler labels: {e}")
            self.labels = [f"Class {i}" for i in range(10)]

        # 2. Carrega Modelo (API Low-Level - SavedModel)
        # O model_folder_path deve ser a PASTA que contém o arquivo 'saved_model.pb'
        print(f" [IA] Carregando SavedModel da pasta: {model_folder_path}")
        
        try:
            if not os.path.exists(model_folder_path):
                raise FileNotFoundError(f"A pasta do modelo não existe: {model_folder_path}")

            # Carrega o grafo bruto (funciona em qualquer versão do TF)
            self.imported_model = tf.saved_model.load(model_folder_path)
            
            # Obtém a função de inferência padrão
            self.serving_fn = self.imported_model.signatures['serving_default']
            
            print(" [IA] Modelo carregado com sucesso (Modo Low-Level).")
        except Exception as e:
            print(f" [IA] ERRO FATAL ao carregar modelo: {e}")
            raise e

    def predict(self, frame):
        try:
            # --- Preprocessamento ---
            # 1. Redimensionar
            img = cv2.resize(frame, (self.input_width, self.input_height))
            
            # 2. Converter para float32 e Normalizar (0 a 1)
            img_array = np.asarray(img, dtype=np.float32) / 255.0
            
            # 3. Converter para Tensor do TensorFlow (Batch size 1)
            input_tensor = tf.convert_to_tensor([img_array], dtype=tf.float32)

            # --- Inferência (Low-Level) ---
            # Chama a função assinada do modelo
            predictions_dict = self.serving_fn(input_tensor)
            
            # O output é um dicionário (ex: {'dense_1': tensor}). 
            # Pegamos o primeiro valor (que são as probabilidades) independente do nome da chave.
            output_tensor = list(predictions_dict.values())[0]
            
            # Converte de Tensor para Array Numpy
            prediction_scores = output_tensor.numpy()[0]
            
            # --- Pós-processamento ---
            idx = np.argmax(prediction_scores)
            confidence = float(prediction_scores[idx])
            
            # Define o nome da classe
            label_name = self.labels[idx] if idx < len(self.labels) else str(idx)

            # Aplica o Threshold
            if confidence < self.conf_threshold:
                return {"label": None, "confidence": confidence}

            return {
                "label": label_name,
                "confidence": confidence
            }
            
        except Exception as e:
            print(f"Erro na predição: {e}")
            return {"label": None, "confidence": 0.0}