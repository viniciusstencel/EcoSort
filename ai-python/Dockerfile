FROM python:3.11-slim
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ /app/src/
COPY models/ /app/models/
COPY proto/ /app/proto/

EXPOSE 50051

CMD ["python", "src/host_grpc.py"]