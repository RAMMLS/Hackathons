from typing import Optional
from app.models.user import UserInDB, UserCreate
from app.services.json_storage import storage
from app.auth.auth_handler import get_password_hash, verify_password
import uuid

class UserService:
    @staticmethod
    def get_user(username: str) -> Optional[UserInDB]:
        user_data = storage.get_user(username)
        if user_data:
            return UserInDB(**user_data)
        return None

    @staticmethod
    def is_username_taken(username: str) -> bool:
        """Проверяет, занято ли имя пользователя"""
        return UserService.get_user(username) is not None

    @staticmethod
    def create_user(user_data: UserCreate) -> UserInDB:
        """Create new user with hashed password"""
        # Проверяем, не занято ли имя пользователя
        if UserService.is_username_taken(user_data.username):
            raise ValueError(f"Username '{user_data.username}' is already taken")

        # Хешируем пароль
        hashed_password = get_password_hash(user_data.password)
        user_dict = {
            "id": str(uuid.uuid4()),
            "username": user_data.username,
            "hashed_password": hashed_password,
            "disabled": False
        }

        storage.create_user(user_data.username, user_dict)
        return UserInDB(**user_dict)

    @staticmethod
    def authenticate_user(username: str, password: str) -> Optional[UserInDB]:
        user = UserService.get_user(username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    @staticmethod
    def get_all_users():
        """Get all users (for admin purposes)"""
        users_data = storage.get_all_users()
        return [UserInDB(**user_data) for user_data in users_data.values()]