from typing import Optional
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr = Field(unique=True, max_length=255)
    username: str = Field(unique=True, max_length=30, min_length=1)
    password: str = Field(max_length=255)
    description: str | None = Field(default=None, max_length=255)
    # reg_date: datetime = Field(default_factory=datetime.now())


class CreateUser(UserBase):
    pass


class Message(BaseModel):
    message: str


class Username(BaseModel):
    username: str = Field(unique=True, max_length=30, min_length=1)
