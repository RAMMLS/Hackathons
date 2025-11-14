# Troubleshooting Guide

## Error: ERR_EMPTY_RESPONSE

This error means the backend server closed the connection before sending a response. Here's how to fix it:

### Step 1: Check if all containers are running

```bash
docker ps
```

You should see three containers:
- `ollama-mistral`
- `fastapi-backend`
- `react-frontend`

If any are missing, start them:
```bash
docker-compose up -d
```

### Step 2: Check backend logs

```bash
docker-compose logs backend
```

Look for:
- Python errors
- Connection errors to Ollama
- Import errors

### Step 3: Verify Ollama is running and Mistral model is installed

```bash
# Check if Ollama container is running
docker ps | grep ollama

# List available models
docker exec ollama-mistral ollama list
```

If Mistral is not in the list, pull it:
```bash
docker exec ollama-mistral ollama pull mistral
```

This may take several minutes (the model is ~4GB).

### Step 4: Test Ollama connection

Run the diagnostic script:
```bash
docker exec fastapi-backend python check_ollama.py
```

Or manually test:
```bash
# Test if Ollama is accessible
curl http://localhost:11434/api/tags

# Test if Mistral model works
curl http://localhost:11434/api/generate -d '{
  "model": "mistral",
  "prompt": "Hello",
  "stream": false
}'
```

### Step 5: Check backend health endpoint

```bash
curl http://localhost:8000/health
```

This should return JSON with status information.

### Step 6: Restart services

If everything seems fine but still getting errors:

```bash
docker-compose restart
```

Or rebuild everything:
```bash
docker-compose down
docker-compose up -d --build
```

## Common Issues

### Issue: "Cannot connect to Ollama"

**Solution:**
1. Make sure Ollama container is running: `docker ps`
2. Check Ollama logs: `docker-compose logs ollama`
3. Wait 30-60 seconds after starting Ollama for it to fully initialize
4. Verify the model is pulled: `docker exec ollama-mistral ollama list`

### Issue: "Model not found" or "404 model not found"

**Solution:**
```bash
docker exec ollama-mistral ollama pull mistral
```

### Issue: Backend crashes immediately

**Solution:**
1. Check backend logs: `docker-compose logs backend`
2. Look for Python import errors
3. Rebuild backend: `docker-compose up -d --build backend`

### Issue: Frontend can't connect to backend

**Solution:**
1. Verify backend is running on port 8000: `curl http://localhost:8000/`
2. Check CORS settings in `backend/app/config.py`
3. Make sure `REACT_APP_API_URL` is set correctly (should be `http://localhost:8000`)

### Issue: Request timeout

**Solution:**
- The first request to Mistral can take 30-60 seconds as the model loads
- Subsequent requests should be faster
- If it consistently times out, check system resources (RAM, CPU)

## Browser Extension Errors

The errors about "message port closed" are from browser extensions (like ad blockers, password managers, etc.) and can be safely ignored. They don't affect the application.

## Getting Help

If you're still having issues:

1. Collect logs:
   ```bash
   docker-compose logs > logs.txt
   ```

2. Check system resources:
   ```bash
   docker stats
   ```

3. Verify network connectivity:
   ```bash
   docker exec fastapi-backend ping -c 3 ollama
   ```

