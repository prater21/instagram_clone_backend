from fastapi import APIRouter, Depends, status, HTTPException, Body

from app.utils.authUtils import hash_pw
from app.schemas import CreateUser, Message
from app.models import User
from app.database import db_dependency

router = APIRouter()


# 회원가입
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
