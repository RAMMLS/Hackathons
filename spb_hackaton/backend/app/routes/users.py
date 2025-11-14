from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.models.user import UserResponse
from app.services.user_service import UserService
from app.auth.auth_bearer import JWTBearer

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=UserResponse)
async def get_current_user(username: str = Depends(JWTBearer())):
    """Get current user profile"""
    user = UserService.get_user(username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return UserResponse(**user.dict())

@router.get("/", response_model=List[UserResponse])
async def get_all_users(_: str = Depends(JWTBearer())):
    """Get all users (requires authentication)"""
    users = UserService.get_all_users()
    return [UserResponse(**user.dict()) for user in users]