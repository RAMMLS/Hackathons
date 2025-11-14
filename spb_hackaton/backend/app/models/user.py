from pydantic import BaseModel, validator
from typing import Optional

class User(BaseModel):
    username: str
    hashed_password: str
    disabled: Optional[bool] = False

class UserInDB(User):
    id: str

class UserCreate(BaseModel):
    username: str
    password: str
    
    @validator('username')
    def validate_username(cls, v):
        if len(v) < 3:
            raise ValueError('Username must be at least 3 characters')
        if len(v) > 50:
            raise ValueError('Username must be less than 50 characters')
        return v
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 3:
            raise ValueError('Password must be at least 3 characters')
        return v

class UserResponse(BaseModel):
    id: str
    username: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None