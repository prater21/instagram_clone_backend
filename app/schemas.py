from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime


# user model --------------------------------------------------------
class UserBase(BaseModel):
    email: EmailStr = Field(max_length=255)
    username: str = Field(max_length=30, min_length=1)
    password: str = Field(max_length=255)
    description: str | None = Field(default=None, max_length=255)


class CreateUser(UserBase):
    pass


class UsernameBase(BaseModel):
    username: str = Field(unique=True, max_length=30, min_length=1)


class EmailBase(BaseModel):
    email: EmailStr = Field(max_length=255)


class ResetPasswordBase(BaseModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(max_length=255)


# token model --------------------------------------------------------
class TokenBase(BaseModel):
    access_token: str
    token_type: str = Field(default="bearer")


class TokenData(BaseModel):
    id: Optional[int] = None


# email model --------------------------------------------------------
class EmailSchema(BaseModel):
    email: EmailStr


# auth mail --------------------------------------------------------
class AuthMailResponse(BaseModel):
    auth_id: int


class AuthMailConfirm(BaseModel):
    auth_id: int
    auth_code: str


# response model --------------------------------------------------------
class Message(BaseModel):
    message: str
