FROM python:3.11-slim

WORKDIR /app

COPY tg-bot/requirements.txt .

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY tg-bot/ .

CMD ["python", "main.py"]