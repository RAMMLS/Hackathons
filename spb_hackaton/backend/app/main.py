from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import os

# Импорты из вашей структуры
from app.config import settings
# Предполагаем, что у вас есть роутеры в app/routes
from app.routes import auth, profile

app = FastAPI(
    title="Moscow Chat API",
    description="API для чат-бота с московской тематикой",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
try:
    app.include_router(auth.router, prefix="/api/v1")
except Exception as e:
    print(f"Note: Auth router not available: {e}")

try:
    app.include_router(profile.router)
except Exception as e:
    print(f"Note: Profile router not available: {e}")

class ChatRequest(BaseModel):
    message: str
    model: str = "mistral"

class ChatResponse(BaseModel):
    response: str
    model: str

class HealthResponse(BaseModel):
    status: str
    ollama: str
    database: str
    error: str = None

# Конфигурация Ollama
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "ollama")
OLLAMA_PORT = os.getenv("OLLAMA_PORT", "11434")
OLLAMA_URL = f"http://{OLLAMA_HOST}:{OLLAMA_PORT}"

@app.on_event("startup")
async def startup_event():
    print("FastAPI application started")

@app.get("/")
async def root():
    return {
        "message": "Moscow Chat API is running!",
        "endpoints": {
            "health": "/health",
            "chat": "/chat",
            "models": "/models"
        }
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    ollama_status = "disconnected"
    db_status = "unknown"
    error_msg = None
    
    # Проверяем Ollama
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{OLLAMA_URL}/api/tags")
            if response.status_code == 200:
                ollama_status = "connected"
    except Exception as e:
        error_msg = f"Ollama: {str(e)}"
    
    # Проверяем базу данных (упрощенно)
    try:
        db_status = "connected"
    except Exception as e:
        db_status = "disconnected"
        error_msg = f"Database: {str(e)}" if not error_msg else f"{error_msg}, Database: {str(e)}"
    
    status = "healthy" if ollama_status == "connected" and db_status == "connected" else "unhealthy"
    
    return HealthResponse(
        status=status,
        ollama=ollama_status,
        database=db_status,
        error=error_msg
    )

@app.post("/chat", response_model=ChatResponse)
async def chat_with_model(request: ChatRequest):
    try:
        # Формируем запрос к Ollama API
        ollama_data = {
            "model": request.model,
            "prompt": request.message,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "top_p": 0.9
            }
        }
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{OLLAMA_URL}/api/generate",
                json=ollama_data
            )
            
            if response.status_code == 200:
                result = response.json()
                return ChatResponse(
                    response=result.get("response", "No response received"),
                    model=request.model
                )
            else:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Ollama API error: {response.text}"
                )
                
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Request timeout - Ollama is not responding")
    except httpx.ConnectError:
        raise HTTPException(status_code=503, detail="Cannot connect to Ollama service")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/models")
async def get_models():
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{OLLAMA_URL}/api/tags")
            if response.status_code == 200:
                models_data = response.json()
                return models_data
            else:
                raise HTTPException(
                    status_code=response.status_code,
                    detail="Failed to fetch models from Ollama"
                )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
