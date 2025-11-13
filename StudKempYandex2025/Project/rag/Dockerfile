FROM python:3.11-slim

WORKDIR /app

# Копируем общий код
COPY ./common /app/common
COPY rag/app.py /app
COPY rag/requirements.txt .
# Устанавливаем системные зависимости для FAISS и PyTorch CPU
RUN apt-get update && apt-get install -y \
    build-essential \
    libopenblas-dev \
    libomp-dev \
    && rm -rf /var/lib/apt/lists/*

# Установка питон-зависимостей
RUN pip install --no-cache-dir fastapi uvicorn requests \
    langchain langchain-community langchain-huggingface \
    sentence-transformers faiss-cpu boto3 python-dotenv


RUN pip install --no-cache-dir -r common/requirements.txt || true

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]