from fastapi import APIRouter, Depends, status, HTTPException, Body, Request

from app.utils.authUtils import hash_pw
from app.schemas import CreateUser, Message
from app.models import User
from app.database import db_dependency

router = APIRouter()


# 회원가입
@router.post("/signup")
async def register(db: db_dependency, request: Request, user_info: CreateUser):
    url = request.url.path
    try:
        user = (
            db.query(User)
            .filter(
                (User.email == user_info.email) | (User.username == user_info.username)
            )
            .first()
        )
        if user:
            return getError(url, 1009)
            # raise HTTPException(
            #     status_code=status.HTTP_409_CONFLICT, detail="invalid user info"
            # )

        user_info.password = hash_pw(user_info.password)

        new_user = User(**user_info.model_dump())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

    except Exception as e:
        return getError(url, 5000, e)

    ret_info = {"result": "Y", "code": 0, "message": ""}
    return ret_info


# @router.post("/logout")
# async def logout():
#     return {}
