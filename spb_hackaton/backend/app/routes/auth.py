from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from jose import jwt
from datetime import datetime, timedelta

from database import get_db
from models.users import User, UserRespones # , Token чтобы backend не забывал пользователя, а так же UserRrespones
from service.auth_service import AuthService #Нужно сделать AuthService
from schemas.users import UserBase, User

router = APIRouter()

async def create_access_token(data: dict) -> str:
        to_encode = await data.copy()
        expire = await datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post("registration", status_code=status.HTTP_201_CREATED, response_model=UserRespones, tags=["Регистрация"])
async def register(user_data: UserBase, db: AsyncSession = Depends(get_db)):
    existing_user = await AuthService.get_user_by_username(db, user_data.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь существует"
        )
    new_user = await AuthService.create_user(db, user_data)
    return UserRespones(username=new_user.username)

@router.post("/auth", tags=["Авторизация"])
async def auth(user_data: UserBase, db: AsyncSession = Depends(get_db)):
    existing_user = await AuthService.get_user_by_username(db, user_data.username)
    
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный логин"
        )
    if existing_user.password != user_data.password:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detaile = "Неверный логин или пароль"
        )
    
    access_token = create_access_token(data={"sub": existing_user.username})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": existing_user.username
    }