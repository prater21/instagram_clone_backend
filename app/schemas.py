from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime


# user model --------------------------------------------------------
class UserBase(BaseModel):
    email: EmailStr = Field(max_length=255)
    username: str = Field(max_length=30, min_length=1)
    password: str = Field(max_length=255)
    description: str | None = Field(default=None, max_length=255)
    profile_img: str | None = Field(default=None, max_length=255)


class CreateUser(UserBase):
    pass


class UsernameBase(BaseModel):
    username: str = Field(unique=True, max_length=30, min_length=1)


class EmailBase(BaseModel):
    email: EmailStr = Field(max_length=255)


class ResetPasswordBase(BaseModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(max_length=255)


class UserInfoBase(BaseModel):
    flag: bool | None
    id: int
    username: str = Field(unique=True, max_length=30, min_length=1)
    profile_img: str | None = Field(default=None, max_length=255)


class UserCommentBase(UserInfoBase):
    content: str = Field(max_length=2000, min_length=1)


class UserResponseBase(BaseModel):
    email: EmailStr = Field(max_length=255)
    username: str = Field(max_length=30, min_length=1)
    description: str | None = Field(default=None, max_length=255)
    profile_img: str | None = Field(default=None, max_length=255)
    is_follow: bool | None
    post: List[dict]
    follower: List[UserInfoBase]
    following: List[UserInfoBase]


class ChangeProfileImg(BaseModel):
    flag: bool = Field(default=False)
    url: Optional[str] = Field(default=None, max_length=255)


class CreatePost(BaseModel):
    content: str


class FollowBase(BaseModel):
    flag: bool
    follow_id: int


class UserInfoEditBase(BaseModel):
    username: str = Field(max_length=30, min_length=1)
    description: str | None = Field(default=None, max_length=255)


class ChangePasswordBase(BaseModel):
    password: str
    new_password: str


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


class LoginResponse(BaseModel):
    access_token: str
    username: str
    user_id: int


# post model --------------------------------------------------------
class ImageResponse(BaseModel):
    img_src: str


class CreatePost(BaseModel):
    content: str


# comment model
class CreateComment(BaseModel):
    post_id: int
    content: str = Field(default=None, max_length=255)
