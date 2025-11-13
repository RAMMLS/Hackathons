FROM python:3.11-slim

WORKDIR /app

COPY ./common common

COPY output_validator/app.py /app

RUN pip install --no-cache-dir fastapi uvicorn httpx
RUN pip install --no-cache-dir -r common/requirements.txt

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]