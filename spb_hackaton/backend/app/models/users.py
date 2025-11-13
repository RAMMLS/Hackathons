from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from database import Base
from sqlalchemy.orm import mapped_column, Mapped


class User(Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(50), primary_key = True, unique=True)
    password: Mapped[str] = mapped_column(String)
    