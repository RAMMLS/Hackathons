import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JSON_STORAGE_PATH: str = "users.json"
    cors_origins: list = ["http://localhost:3000", "http://localhost:3001", "http://127.0.0.1:3000"]

settings = Settings()