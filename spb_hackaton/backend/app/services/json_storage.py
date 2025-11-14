import json
import os
from typing import Dict, Any, List, Optional
from app.config import settings

class JSONStorage:
    def __init__(self, file_path: str = settings.JSON_STORAGE_PATH):
        # Если путь пустой или только имя файла, создаем полный путь
        if not file_path or os.path.dirname(file_path) == "":
            self.file_path = os.path.join(os.getcwd(), "users.json")
        else:
            self.file_path = file_path
        
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """Create JSON file if it doesn't exist"""
        # Создаем директорию только если она указана в пути
        directory = os.path.dirname(self.file_path)
        if directory:  # Если есть директория в пути
            os.makedirs(directory, exist_ok=True)
        
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump({"users": {}}, f, indent=2)

    def _read_data(self) -> Dict[str, Any]:
        """Read data from JSON file"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {"users": {}}

    def _write_data(self, data: Dict[str, Any]):
        """Write data to JSON file"""
        directory = os.path.dirname(self.file_path)
        if directory:  # Если есть директория в пути
            os.makedirs(directory, exist_ok=True)
            
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def get_all_users(self) -> Dict[str, Any]:
        """Get all users from storage"""
        data = self._read_data()
        return data.get("users", {})

    def get_user(self, username: str) -> Optional[Dict[str, Any]]:
        """Get user by username"""
        users = self.get_all_users()
        return users.get(username)

    def create_user(self, username: str, user_data: Dict[str, Any]):
        """Create new user"""
        data = self._read_data()
        if "users" not in data:
            data["users"] = {}
        data["users"][username] = user_data
        self._write_data(data)

    def update_user(self, username: str, user_data: Dict[str, Any]):
        """Update existing user"""
        data = self._read_data()
        if username in data.get("users", {}):
            data["users"][username].update(user_data)
            self._write_data(data)

    def delete_user(self, username: str):
        """Delete user"""
        data = self._read_data()
        if username in data.get("users", {}):
            del data["users"][username]
            self._write_data(data)

# Global storage instance
storage = JSONStorage()