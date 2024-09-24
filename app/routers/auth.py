import datetime
from fastapi import APIRouter, BackgroundTasks, Depends, status, HTTPException, Body
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from app.utils.common import get_cur_datetime

from ..oauth2 import create_access_token
from ..utils.authUtils import get_auth_number, send_mail, verify_pw
from ..schemas import (
    AuthMailConfirm,
    AuthMailResponse,
    Message,
    TokenBase,
    Username,
    EmailSchema,
)
from ..models import AuthEmail, User
from ..database import db_dependency

router = APIRouter()


# api list
# 로그인
# 유저네임 체크
# 이메일 인증
# 로그아웃


@router.post("/login")
async def login(db: db_dependency, user_info: OAuth2PasswordRequestForm = Depends()):
    user = db.query(User).filter(User.email == user_info.username).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials"
        )

    if not verify_pw(user_info.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials"
        )

    access_token = create_access_token(data={"user_id": user.id})
    return TokenBase(access_token=access_token)


@router.post("/check/username")
async def check_username(db: db_dependency, username: Username):
    duplicate = db.query(User).filter(User.username == username.username).first()

    if duplicate:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="invalid username"
        )

    return Message(message="valid usernaeme")


@router.post("/auth/email", response_model=AuthMailResponse)
async def auth_email(
    db: db_dependency, email: EmailSchema, background_tasks: BackgroundTasks
):

    auth_code = get_auth_number()
    expire_date = get_cur_datetime() + datetime.timedelta(minutes=5)
    cur_date = get_cur_datetime(type="date")
    ret_info = {"auth_id": 0, "auth_code": auth_code}

    auth_info = (
        db.query(AuthEmail)
        .filter((AuthEmail.email == email.email) & (AuthEmail.auth_date == cur_date))
        .first()
    )

    if auth_info is None:
        new_auth = AuthEmail(
            email=email.email,
            auth_code=auth_code,
            auth_date=cur_date,
            expire_date=expire_date,
        )
        db.add(new_auth)
        db.commit()
        db.refresh(new_auth)
        ret_info["auth_id"] = new_auth.id

    else:
        if auth_info.auth_count >= 10:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="The maximum number of authentications per day has been exceeded.",
            )

        auth_info.auth_count += 1
        auth_info.status = "ready"
        auth_info.expire_date = expire_date
        auth_info.auth_code = auth_code

        db.add(auth_info)
        db.commit()
        db.refresh(auth_info)
        ret_info["auth_id"] = auth_info.id

    background_tasks.add_task(send_mail, email=email.email, auth_code=auth_code)

    return ret_info


@router.post("/auth/email/confirm")
async def auth_email_confirm(
    db: db_dependency,
    auth_info: AuthMailConfirm,
):

    cur_datetime = get_cur_datetime()

    auth_confirm = (
        db.query(AuthEmail)
        .filter(
            (AuthEmail.id == auth_info.auth_id)
            & (AuthEmail.auth_code == auth_info.auth_code)
            & (AuthEmail.expire_date > cur_datetime)
            & (AuthEmail.status == "ready")
        )
        .first()
    )

    if auth_confirm is None:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Invalid Auth Number Info",
        )

    auth_confirm.status = "ok"
    auth_confirm.auth_count = 0
    db.add(auth_confirm)
    db.commit()
    db.refresh(auth_confirm)

    return Message(message="success")
