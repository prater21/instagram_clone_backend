from fastapi import APIRouter, Depends, status, HTTPException, Body

from ..schemas import CreateUser, Message, Username

from ..models import User
from ..database import db_dependency

router = APIRouter()


# api list
# 로그인
# 회원가입
# 유저네임 체크
# (이메일 인증)
# 로그아웃


@router.post("/login")
async def login():
    return {}


# @router.post("/check/username", status_code=status.HTTP_200_OK)
# async def check_username(db: db_dependency, username: UsernameBase = Body()):
#     # print(username.username)
#     user = (
#         db.query(models.User).filter(models.User.username == username.username).first()
#     )
#     if user is None:
#         return {"result": "Y", "message": ""}

#     return {}


@router.post("/check/username")
async def check_username(db: db_dependency, username: Username):
    duplicate = db.query(User).filter(User.username == username.username).first()

    if duplicate:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="invalid username"
        )

    return Message(message="valid usernaeme")


@router.post("/auth/email")
async def auth_email():
    return {}


@router.post("/auth/email/confrim")
async def auth_email_confirm():
    return {}
