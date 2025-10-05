import logging
import grpc
import src.ecosort_ai.generated.classification_pb2 as classification_pb2
import src.ecosort_ai.generated.classification_pb2_grpc as classification_pb2_grpc
from src.ecosort_ai.inference.classifier import Classifier

MODEL_PATH = 'models/ecosort_classifier_v1.keras'
CLASS_NAMES = ['metal', 'organic', 'paper', 'plastic']

class ClassificationService(classification_pb2_grpc.ClassificationServiceServicer):
    def __init__(self):
        self.classifier = Classifier(model_path=MODEL_PATH, class_names=CLASS_NAMES)

    def Classify(self, request, context):
        image_bytes = request.image_data
        
        result = self.classifier.predict(image_bytes)
        
        if result.get("error"):
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(result["error"])
            return classification_pb2.ClassificationResult()

        return classification_pb2.ClassificationResult(
            class_id=result["class_id"],
            class_name=result["class_name"],
            confidence=result["confidence"]
        )