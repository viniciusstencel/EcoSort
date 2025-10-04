server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
servicer_pb2_grpc.add_AnalizeServiceServicer_to_server(
    AnalizeServicer(), server
)
# A porta 50051 deve ser a mesma configurada no Docker Compose!
server.add_insecure_port('[::]:50051')
server.start()