# src/classification_model.py
import tensorflow as tf
import numpy as np
import cv2

class KerasObjectDetector:
    
    def __init__(self, model_path, labels_path, input_width, input_height, conf_threshold): # Adicionado labels_path
        print(f"Carregando modelo de {model_path}...")
        try:
            self.model = tf.keras.models.load_model(model_path, compile=False)
            self.model.summary()
            print("Modelo Keras carregado com sucesso.")
        except Exception as e:
            print(f"Erro ao carregar o modelo Keras: {e}")
            raise 

        # --- NOVO: CARREGA OS LABELS ---
        print(f"Carregando labels de {labels_path}...")
        try:
            with open(labels_path, 'r') as f:
                # Carrega as linhas e remove o \n e números (ex: "0 Gato", "1 Cachorro")
                self.labels = [line.strip().split(' ', 1)[-1] for line in f.readlines()]
            print(f"Labels carregados: {self.labels}")
        except Exception as e:
            print(f"Erro ao carregar {labels_path}: {e}")
            self.labels = [] # Usa uma lista vazia se falhar
        # -----------------------------

        self.input_width = input_width
        self.input_height = input_height
        self.conf_threshold = conf_threshold

    # ... _preprocess_frame(...) fica igual ...
    def _preprocess_frame(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        input_image = cv2.resize(rgb_frame, (self.input_width, self.input_height))
        # !!! IMPORTANTE: Ajuste a normalização (ex: / 255.0 ou [-1, 1]) !!!
        input_image = input_image / 255.0
        input_tensor = np.expand_dims(input_image, axis=0)
        return input_tensor

    def _postprocess_frame(self, frame, predictions, original_height, original_width):
        annotated_frame = frame.copy()
        detections_list = []

        try:
            # !!! IMPORTANTE: Adapte esta seção para a saída do SEU modelo !!!
            for i in range(len(predictions[0])): 
                score = float(predictions[0][i][4]) 
                if score > self.conf_threshold:
                    box_normalized = [float(coord) for coord in predictions[0][i][0:4]]
                    class_id = int(predictions[0][i][5])
                    
                    # --- NOVO: USA A LISTA DE LABELS ---
                    label_name = f"Classe {class_id}" # Fallback
                    if self.labels and 0 <= class_id < len(self.labels):
                        label_name = self.labels[class_id]
                    # ----------------------------------
                    
                    detection_data = {
                        "class_id": class_id,
                        "class_name": label_name,  # <-- Enviando o nome!
                        "score": score,
                        "box_normalized": box_normalized
                    }
                    detections_list.append(detection_data)
                    
                    # Desenha no frame
                    y_min = int(box_normalized[0] * original_height)
                    x_min = int(box_normalized[1] * original_width)
                    y_max = int(box_normalized[2] * original_height)
                    x_max = int(box_normalized[3] * original_width)
                    
                    cv2.rectangle(annotated_frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
                    label_text = f"{label_name}: {score:.2f}" # <-- Usa o nome aqui
                    cv2.putText(annotated_frame, label_text, (x_min, y_min - 10), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        except Exception as e:
            print(f"Erro no pós-processamento: {e}")

        return annotated_frame, detections_list

    # ... process_frame(...) fica igual ...
    def process_frame(self, frame):
        (original_height, original_width) = frame.shape[:2]
        input_tensor = self._preprocess_frame(frame)
        predictions = self.model.predict(input_tensor, verbose=0)
        annotated_frame, detections_list = self._postprocess_frame(frame, predictions, original_height, original_width)
        return annotated_frame, detections_list