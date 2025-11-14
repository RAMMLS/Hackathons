#!/bin/bash

echo "=== Pulling models for Ollama ==="

# Ждем пока Ollama запустится
echo "Waiting for Ollama to be ready..."
for i in {1..30}; do
  if curl -s http://localhost:11434/api/tags >/dev/null; then
    echo "✅ Ollama is ready!"
    break
  fi
  echo "Attempt $i/30: Waiting for Ollama..."
  sleep 2
done

# Загружаем модели
echo "⬇️ Downloading Mistral model..."
curl -X POST http://localhost:11434/api/pull -d '{"name": "mistral"}'

echo "✅ Model download initiated"
echo "Note: This may take several minutes. Check progress with: curl http://localhost:11434/api/tags"
