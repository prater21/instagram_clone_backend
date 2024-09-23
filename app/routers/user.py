from fastapi import APIRouter, Depends, status, HTTPException, Body

from app.utils import hash_pw

from ..schemas import CreateUser, Message

from ..models import User
from ..database import db_dependency

router = APIRouter()


# api list
# 로그인
# 회원가입
# 유저네임 체크
# (이메일 인증)
# 로그아웃


@router.post("/register")
async def register(db: db_dependency, user_info: CreateUser):
    user = (
        db.query(User)
        .filter((User.email == user_info.email) | (User.username == user_info.username))
        .first()
    )
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="invalid user info"
        )

    user_info.password = hash_pw(user_info.password)

    new_user = User(**user_info.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return Message(message="register success")


# @router.post("/logout")
# async def logout():
#     return {}
