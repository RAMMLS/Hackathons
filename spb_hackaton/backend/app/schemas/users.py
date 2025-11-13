from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str
    password: str

class UserRespones(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    pass