import datetime
from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    status,
    Request,
)
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from app.utils.common import get_cur_datetime, raise_error
from app.models import AuthEmail, User
from app.database import db_dependency
from app.oauth2 import create_access_token
from app.utils.authUtils import get_auth_number, send_mail, verify_pw, hash_pw
from app.schemas import (
    AuthMailConfirm,
    AuthMailResponse,
    LoginResponse,
    Message,
    TokenBase,
    UsernameBase,
    EmailSchema,
    EmailBase,
    CreateUser,
)
from app.utils.logger import log_error, log_request


router = APIRouter()


# api list
# signup
# login
# username check
# email check, send authcode, confirm autocode


@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=Message)
async def sign_up(db: db_dependency, request: Request, user_info: CreateUser):
    """
    Sign Up
    """
    log_request(request.url.path, request.method, user_info)

    user = (
        db.query(User)
        .filter((User.email == user_info.email) | (User.username == user_info.username))
        .first()
    )
    if user:
        raise_error(request.url.path, request.method, 409, "Invalid user info")

    user_info.password = hash_pw(user_info.password)

    new_user = User(**user_info.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return Message(message="Signed up successfully")


@router.post("/login", status_code=status.HTTP_200_OK, response_model=LoginResponse)
async def login(
    db: db_dependency,
    request: Request,
    user_info: OAuth2PasswordRequestForm = Depends(),
):
    """
    Login
    """
    log_request(request.url.path, request.method, user_info)
    user = db.query(User).filter(User.email == user_info.username).first()
    if user is None:
        raise_error(request.url.path, request.method, 403, "Invalid Credentials")

    if not verify_pw(user_info.password, user.password):
        raise_error(request.url.path, request.method, 403, "Invalid Credentials")

    access_token = create_access_token(data={"user_id": user.id})

    return LoginResponse(
        access_token=access_token, username=user.username, user_id=user.id
    )


@router.post("/username/check", status_code=status.HTTP_200_OK, response_model=Message)
async def username_check(db: db_dependency, request: Request, username: UsernameBase):
    """
    check username validation
    """
    log_request(request.url.path, request.method, username)

    duplicate = db.query(User).filter(User.username == username.username).first()

    if duplicate:
        raise_error(request.url.path, request.method, 409, "Invalid username")

    return Message(message="Valid username")


@router.post("/email/check", status_code=status.HTTP_200_OK, response_model=Message)
async def email_check(db: db_dependency, request: Request, email: EmailBase):
    """
    check email validation
    """

    log_request(request.url.path, request.method, email)
    duplicate = db.query(User).filter(User.email == email.email).first()

    if duplicate:
        raise_error(request.url.path, request.method, 409, "Invalid email")

    return Message(message="Valid email")


@router.post(
    "/email/authcode/send",
    status_code=status.HTTP_200_OK,
    response_model=AuthMailResponse,
)
async def email_authcode_send(
    db: db_dependency,
    request: Request,
    email: EmailSchema,
    background_tasks: BackgroundTasks,
):
    """
    send email verification code
    """
    log_request(request.url.path, request.method, email)

    auth_code = get_auth_number()
    expire_date = get_cur_datetime() + datetime.timedelta(minutes=5)
    cur_date = get_cur_datetime(type="date")

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
        auth_id = new_auth.id

    else:
        if auth_info.auth_count >= 10:
            raise_error(
                request.url.path,
                request.method,
                429,
                "Maximum number of email authentication attempts exceeded for the day",
            )

        auth_info.auth_count += 1
        auth_info.status = "ready"
        auth_info.expire_date = expire_date
        auth_info.auth_code = auth_code

        db.add(auth_info)
        db.commit()
        db.refresh(auth_info)
        auth_id = auth_info.id

    background_tasks.add_task(send_mail, email=email.email, auth_code=auth_code)

    return AuthMailResponse(auth_id=auth_id)


@router.post(
    "/email/authcode/confirm", status_code=status.HTTP_200_OK, response_model=Message
)
async def email_authcode_confirm(
    db: db_dependency,
    request: Request,
    auth_info: AuthMailConfirm,
):
    """
    confirm email verification code
    """
    log_request(request.url.path, request.method, auth_info)

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
        raise_error(request.url.path, request.method, 406, "Invalid authcode info")

    auth_confirm.status = "ok"
    auth_confirm.auth_count = 0
    db.add(auth_confirm)
    db.commit()
    db.refresh(auth_confirm)

    return Message(message="Email authentication successful.")
