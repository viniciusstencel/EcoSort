FROM python:3.11-slim
WORKDIR /app

COPY requirements.txt .
RUN apt-get update && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ /app/src/
COPY models/ /app/models/
COPY protos/ /app/protos/
COPY scripts/ /app/scripts/

EXPOSE 50051

CMD ["python3", "-u" , "scripts/run_server.py"]