import tensorflow as tf
import numpy as np
from PIL import Image
import io
import logging

class Classifier:
    def __init__(self, model_path: str, class_names: list):
        self.model_path = model_path
        self.class_names = class_names
        self.img_height = 224
        self.img_width = 224
        
        try:
            logging.info(f"Carregando modelo de IA do caminho: {self.model_path}...")
            self.model = tf.keras.models.load_model(self.model_path)
            logging.info("✅ Modelo carregado com sucesso pelo Classifier!")
        except Exception as e:
            logging.error(f"🚨 Falha ao carregar o modelo no Classifier: {e}")
            self.model = None

    def _preprocess_image(self, image_bytes: bytes):
        image = Image.open(io.BytesIO(image_bytes))
        image = image.resize((self.img_width, self.img_height))
        image_array = tf.keras.utils.img_to_array(image)
        image_batch = np.expand_dims(image_array, axis=0)
        return image_batch

    def predict(self, image_bytes: bytes) -> dict:
        if not self.model:
            return {
                "error": "Modelo não está disponível."
            }
            
        processed_image = self._preprocess_image(image_bytes)
        
        prediction = self.model.predict(processed_image)
        
        predicted_index = np.argmax(prediction)
        confidence = np.max(prediction)
        predicted_class_name = self.class_names[predicted_index]

        logging.info(f"Classifier previu: Classe='{predicted_class_name}', Confiança={confidence:.2f}")

        return {
            "class_id": predicted_index,
            "class_name": predicted_class_name,
            "confidence": float(confidence),
            "error": None
        }