from pydantic_settings import BaseSettings 

#settings app 
class Settings(BaseSettings):
    app_name: str = "#"
    debug: bool = True #vision error
    database_url: str = "#" 
    cors_origins: list =[
        "http://localhost:8000",
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ]
    static_dir: str = "static"
    images_dir: str = "static/images"

    class Config:
        env_file = ".env"

settings = Settings()