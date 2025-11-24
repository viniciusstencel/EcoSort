FROM python:3.11-slim
WORKDIR /app

COPY requirements.txt .

# --- CORREÇÃO ---
# Substituímos 'libgl1-mesa-glx' (antigo) por 'libgl1' (novo)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

COPY src/ /app/src/
COPY models/ /app/models/

CMD ["python3", "-u" , "src/main_service.py"]