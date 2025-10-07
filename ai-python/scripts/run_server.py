import sys
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import grpc
from concurrent import futures
import logging
import src.ecosort_ai.generated.classification_pb2_grpc as classification_pb2_grpc
from src.ecosort_ai.services.classification_service import AiClassificationService


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    classification_pb2_grpc.add_AiClassificationServiceServicer_to_server(
        AiClassificationService(), server
    )

    port = '50051'
    server.add_insecure_port(f'[::]:{port}')

    server.start()
    logging.info(f"✅ Servidor IA iniciado com sucesso. Escutando na porta {port}.")
    
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        logging.info("Servidor sendo desligado.")
        server.stop(0)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    serve()