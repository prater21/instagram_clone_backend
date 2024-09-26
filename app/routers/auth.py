import datetime
from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    status,
    HTTPException,
    Body,
    Request,
)
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from app.utils.common import get_cur_datetime, getError, printError
from app.utils.authUtils import hash_pw

from ..oauth2 import create_access_token
from ..utils.authUtils import get_auth_number, send_mail, verify_pw
from ..schemas import (
    AuthMailConfirm,
    AuthMailResponse,
    Message,
    TokenBase,
    UsernameBase,
    EmailSchema,
    SuccessResponse,
    ResetPasswordBase,
    EmailBase,
)
from ..models import AuthEmail, User
from ..database import db_dependency

router = APIRouter(tags=["Auth"])


# api list
# 로그인
# 유저네임 체크
# 이메일 인증
# 로그아웃


# 1002
@router.post("/login")
async def login(
    db: db_dependency,
    request: Request,
    user_info: OAuth2PasswordRequestForm = Depends(),
):
    url = request.url.path
    try:
        user = db.query(User).filter(User.email == user_info.username).first()
        if user is None:
            return getError(url, 2001)
            # raise HTTPException(
            #     status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials"
            # )

        if not verify_pw(user_info.password, user.password):
            return getError(url, 2003)
            # raise HTTPException(
            #     status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials"
            # )

    except Exception as e:
        return getError(url, 5000, e)

    ret_info = {"result": "Y", "code": 0, "message": ""}
    ret_info["access_token"] = create_access_token(data={"user_id": user.id})
    return ret_info


@router.post("/check/username")
async def check_username(db: db_dependency, request: Request, username: UsernameBase):
    url = request.url.path
    try:
        duplicate = db.query(User).filter(User.username == username.username).first()
        if duplicate:
            return getError(url, 3001)
            # raise HTTPException(
            #     status_code=status.HTTP_409_CONFLICT, detail="invalid username"
            # )

    except Exception as e:
        return getError(url, 5000, e)

    ret_info = {"result": "Y", "code": 0, "message": ""}
    return ret_info


@router.post("/check/email")
async def check_email(db: db_dependency, request: Request, email: EmailBase):
    url = request.url.path
    try:
        duplicate = db.query(User).filter(User.email == email.email).first()
        if duplicate:
            return getError(url, 3006)
            # raise HTTPException(
            #     status_code=status.HTTP_409_CONFLICT, detail="invalid username"
            # )

    except Exception as e:
        return getError(url, 5000, e)

    ret_info = {"result": "Y", "code": 0, "message": ""}
    return ret_info


@router.post("/auth/email")
async def auth_email(
    db: db_dependency,
    email: EmailSchema,
    background_tasks: BackgroundTasks,
    request: Request,
):

    auth_code = get_auth_number()
    expire_date = get_cur_datetime() + datetime.timedelta(minutes=5)
    cur_date = get_cur_datetime(type="date")
    ret_info = {"result": "Y", "code": 0, "message": ""}
    url = request.url.path

    try:
        auth_info = (
            db.query(AuthEmail)
            .filter(
                (AuthEmail.email == email.email) & (AuthEmail.auth_date == cur_date)
            )
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
                return getError(url, 3000)
                # raise HTTPException(
                #     status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                #     detail="The maximum number of authentications per day has been exceeded.",
                # )

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

    except Exception as e:
        return getError(url, 5000, e)


@router.post("/auth/email/confirm")
async def auth_email_confirm(
    db: db_dependency,
    request: Request,
    auth_info: AuthMailConfirm,
):
    url = request.url.path
    try:
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
            return getError(url, 4003)
            # raise HTTPException(
            #     status_code=status.HTTP_406_NOT_ACCEPTABLE,
            #     detail="Invalid Auth Number Info",
            # )

        auth_confirm.status = "ok"
        auth_confirm.auth_count = 0
        db.add(auth_confirm)
        db.commit()
        db.refresh(auth_confirm)

    except Exception as e:
        return getError(url, 5000, e)

    ret_info = {"result": "Y", "code": 0, "message": ""}
    return ret_info


@router.post("/reset/password")
async def reset_password(
    db: db_dependency,
    request: Request,
    user_info: ResetPasswordBase,
):
    url = request.url.path
    try:
        user = db.query(User).filter(User.email == user_info.email).first()

        if user is None:
            return getError(url, 2001)

        user.password = hash_pw(user_info.password)
        db.add(user)
        db.commit()
        db.refresh(user)

    except Exception as e:
        return getError(url, 5000, e)

    ret_info = {"result": "Y", "code": 0, "message": ""}
    return ret_info
